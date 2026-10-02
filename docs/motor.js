import * as THREE from './vendor/three.module.min.js';
import { OrbitControls } from './vendor/OrbitControls.js';
import { RoomEnvironment } from './vendor/RoomEnvironment.js';

// A procedural, illustrative 12-slot / 8-pole inner-rotor machine.
export function createMotor(host) {
  const renderer = new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio,2));
  renderer.setClearColor(0x0b0d10,0);
  renderer.toneMapping=THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure=1.05;
  host.appendChild(renderer.domElement);
  const scene=new THREE.Scene();
  const pmrem=new THREE.PMREMGenerator(renderer);
  const environment=new RoomEnvironment();
  const envTarget=pmrem.fromScene(environment,.04);
  scene.environment=envTarget.texture;
  environment.dispose();pmrem.dispose();
  const camera=new THREE.PerspectiveCamera(34,1,.1,100);
  camera.position.set(6,7,8); camera.lookAt(0,.25,0);
  const controls=new OrbitControls(camera,renderer.domElement);
  controls.enablePan=false;controls.enableDamping=true;controls.minDistance=7;controls.maxDistance=15;
  controls.minPolarAngle=.28;controls.maxPolarAngle=1.4;controls.target.set(0,.25,0);
  const hemi=new THREE.HemisphereLight(0xcbdcec,0x383329,.85);scene.add(hemi);
  for (const [color,intensity,pos] of [[0xffffff,20,[4,7,3]],[0xffb85b,14,[-5,3,-2]],[0xa2c5eb,22,[1,2,-6]]]) {
    const l=new THREE.PointLight(color,intensity,40,1.5);l.position.set(...pos);scene.add(l);
  }
  const assembly=new THREE.Group();scene.add(assembly);
  const metal=(color,roughness=.3,metalness=.8)=>new THREE.MeshStandardMaterial({color,roughness,metalness});
  const graphite=metal(0x262c32,.31,.72), steel=metal(0x85949e,.24,.88), copper=metal(0xc77637,.25,.83);
  const amber=metal(0xe2a849,.26,.75), black=metal(0x10151a,.44,.45);
  function mesh(geo,mat,parent=assembly,x=0,y=0,z=0){const m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);parent.add(m);return m;}
  function ring(outer,inner,height,mat,parent=assembly,y=0){
    const shape=new THREE.Shape();shape.absarc(0,0,outer,0,Math.PI*2,false);
    const hole=new THREE.Path();hole.absarc(0,0,inner,0,Math.PI*2,true);shape.holes.push(hole);
    const g=new THREE.ExtrudeGeometry(shape,{depth:height,bevelEnabled:true,bevelSize:.025,bevelThickness:.025,bevelSegments:2,steps:1,curveSegments:96});g.rotateX(-Math.PI/2);
    return mesh(g,mat,parent,0,y,0);
  }
  const base=new THREE.Group();assembly.add(base);
  ring(2.42,.26,.16,graphite,base,-.82);
  ring(2.34,2.13,.8,graphite,base,-.66);
  for(let i=0;i<24;i++){
    const a=i*Math.PI/12;
    const fin=mesh(new THREE.BoxGeometry(.055,.71,.23),steel,base,Math.cos(a)*2.35,-.28,Math.sin(a)*2.35);fin.rotation.y=-a;
  }
  for(let i=0;i<8;i++){
    const a=i*Math.PI/4;
    mesh(new THREE.CylinderGeometry(.07,.07,.09,6),steel,base,Math.cos(a)*2.21,-.59,Math.sin(a)*2.21);
  }
  const stator=new THREE.Group();assembly.add(stator);
  // Thin stacked laminations, teeth and visible copper turns.
  for(let i=0;i<17;i++)ring(2.08,1.75,.017,i%2?steel:graphite,stator,-.4+i*.029);
  const coils=[];
  for(let i=0;i<12;i++){
    const a=i*Math.PI/6, tooth=new THREE.Group();tooth.rotation.y=a;stator.add(tooth);
    mesh(new THREE.BoxGeometry(.42,.55,.85),steel,tooth,0,-.12,1.52);
    const winding=new THREE.Group();tooth.add(winding);
    const mat=copper.clone();coils.push(mat);
    for(let j=0;j<12;j++){
      const loop=mesh(new THREE.TorusGeometry(.29,.032,7,24),mat,winding,0,-.11,1.18+j*.059);
      loop.scale.set(.91,1.14,1);
    }
    mesh(new THREE.BoxGeometry(.64,.57,.17),steel,tooth,0,-.11,1.04);
  }
  const rotor=new THREE.Group();assembly.add(rotor);
  mesh(new THREE.CylinderGeometry(.77,.77,.67,80),graphite,rotor,0,-.1,0);
  for(let i=0;i<8;i++){
    const a=i*Math.PI/4;
    const m=mesh(new THREE.CylinderGeometry(.9,.9,.6,16,1,false,a,.63),i%2?steel:amber,rotor,0,-.1,0);
    m.material=m.material.clone();
  }
  ring(.59,.22,.07,steel,rotor,.25);
  mesh(new THREE.CylinderGeometry(.21,.21,2.15,48),steel,rotor,0,.38,0);
  mesh(new THREE.BoxGeometry(.055,.31,.11),graphite,rotor,0,1.21,.18);
  const lid=new THREE.Group();assembly.add(lid);
  ring(2.38,2.09,.11,graphite,lid,.35);
  ring(2.4,2.35,.05,steel,lid,.47);
  for(let i=0;i<8;i++){
    const a=i*Math.PI/4;
    mesh(new THREE.CylinderGeometry(.075,.075,.07,6),steel,lid,Math.cos(a)*2.22,.5,Math.sin(a)*2.22);
  }
  // Three insulated phase terminals.
  for(let i=0;i<3;i++){
    const terminal=new THREE.Group();terminal.position.set((i-1)*.22,-.2,-2.25);assembly.add(terminal);
    mesh(new THREE.CylinderGeometry(.055,.055,.55,16),[amber,copper,steel][i],terminal,0,.4,0);
    mesh(new THREE.CylinderGeometry(.082,.082,.24,16),black,terminal,0,.14,0);
  }
  let size={w:1,h:1},angle=.35,view=.7,explode=0;
  function resize(){size={w:host.clientWidth||640,h:host.clientHeight||520};renderer.setSize(size.w,size.h);camera.aspect=size.w/size.h;camera.updateProjectionMatrix();}
  new ResizeObserver(resize).observe(host);resize();
  return {
    render({theta=0,exploded=false,phase=0,power=.4,azimuth=null}={}){
      explode+=(Number(exploded)-explode)*.13;
      rotor.position.y=explode*1.85; lid.position.y=explode*2.4; stator.position.y=explode*.3;
      rotor.rotation.y=theta;
      coils.forEach((m,i)=>{m.emissive.setHex(0xf17b22);m.emissiveIntensity=power*(.07+.12*(Math.sin(phase+i*Math.PI*2/3)+1));});
      if(azimuth!==null){view=azimuth;camera.position.set(Math.sin(view)*9,7.1,Math.cos(view)*9);}
      controls.target.y=.25+explode*.65;controls.update();
      assembly.rotation.y=angle;
      renderer.render(scene,camera);
    },
    rotate(delta){angle+=delta;},
    dispose(){controls.dispose();envTarget.dispose();renderer.dispose();}
  };
}
