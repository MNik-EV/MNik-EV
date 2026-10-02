import { createMotor } from './motor.js';

const $=id=>document.getElementById(id);
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
let mode='motor',paused=reduced.matches,stopped=false,reverse=false,exploded=false;
let rpm=1200,theta=0,phase=0,last=0,accumulator=0,motor=null,audio=null,sound=false;
let cells=[4.06,4.11,4.08,3.91,4.04,4.09],balancing=false,inputOn=true,soc=100;
try{motor=createMotor($('motor-view'));}catch(error){$('fallback').hidden=false;console.info('Using the 2D motor fallback:',error.message);}
const scope=$('scope').getContext('2d');
function beep(hz=660){if(!sound)return;audio??=new AudioContext();audio.resume();const o=audio.createOscillator(),g=audio.createGain();o.connect(g);g.connect(audio.destination);o.frequency.value=hz;g.gain.setValueAtTime(.035,audio.currentTime);g.gain.exponentialRampToValueAtTime(.001,audio.currentTime+.09);o.start();o.stop(audio.currentTime+.1);}
function syncPause(){ $('pause').textContent=paused?'▶ Resume motion':'Ⅱ Pause motion';$('pause').setAttribute('aria-pressed',String(paused)); }
syncPause();
reduced.addEventListener('change',event=>{if(event.matches){paused=true;syncPause();}});
document.querySelectorAll('[data-mode]').forEach((button,index,buttons)=>{
  button.addEventListener('click',()=>{mode=button.dataset.mode;buttons.forEach(b=>{const selected=b===button;b.setAttribute('aria-selected',String(selected));b.tabIndex=selected?0:-1;$(`panel-${b.dataset.mode}`).hidden=!selected;});beep();});
  button.addEventListener('keydown',event=>{let i=index;if(event.key==='ArrowRight')i=(index+1)%3;else if(event.key==='ArrowLeft')i=(index+2)%3;else if(event.key==='Home')i=0;else if(event.key==='End')i=2;else return;event.preventDefault();buttons[i].focus();buttons[i].click();});
});
$('speed').addEventListener('input',()=>{$('speed-label').textContent=Number($('speed').value).toLocaleString()+' rpm';});
$('direction').addEventListener('click',()=>{reverse=!reverse;$('direction').setAttribute('aria-pressed',String(reverse));$('direction').textContent=reverse?'↺ Reverse':'↻ Forward';beep(440);});
$('pause').addEventListener('click',()=>{paused=!paused;syncPause();beep();});
$('explode').addEventListener('click',()=>{exploded=!exploded;$('explode').setAttribute('aria-pressed',String(exploded));$('explode').textContent=exploded?'Reassemble ↙':'Explode assembly ↗';beep(880);});
$('estop').addEventListener('click',()=>{stopped=!stopped;if(stopped)rpm=0;$('speed').disabled=stopped;$('direction').disabled=stopped;$('estop').textContent=stopped?'↻ RESET DRIVE':'■ EMERGENCY STOP';$('motor-status').innerHTML=stopped?'■ DRIVE DISABLED':'<i class="led"></i> DRIVE ENABLED';$('motor-hint').textContent=stopped?'Drive disabled. Reset to resume the experiment.':'All the fun. None of the magic smoke.';beep(stopped?180:880);});
$('sound').addEventListener('click',()=>{sound=!sound;$('sound').textContent=sound?'Sound on ♪':'Sound off ♪';$('sound').setAttribute('aria-pressed',String(sound));beep();});
function drawScope(){const w=620,h=190;scope.clearRect(0,0,w,h);scope.fillStyle='#0d1117';scope.fillRect(0,0,w,h);scope.strokeStyle='#20262e';scope.lineWidth=1;scope.beginPath();for(let x=0;x<w;x+=31){scope.moveTo(x,0);scope.lineTo(x,h);}for(let y=0;y<h;y+=38){scope.moveTo(0,y);scope.lineTo(w,y);}scope.stroke();['#ffbb63','#76c9dc','#bc9ae9'].forEach((color,i)=>{scope.strokeStyle=color;scope.lineWidth=2.2;scope.beginPath();for(let x=0;x<=w;x+=2){const y=h/2+(stopped?0:57)*Math.sin(x/w*Math.PI*4+phase+i*Math.PI*2/3);if(!x)scope.moveTo(x,y);else scope.lineTo(x,y);}scope.stroke();});}
function drawPack(){const min=Math.min(...cells),max=Math.max(...cells),spread=Math.round((max-min)*1000);$('pack').innerHTML=cells.map((v,i)=>`<div class="cell ${v<max-.1?'low':''} ${balancing&&v>min+.005?'balancing':''}"><div class="cell-body"><span>LI-ION</span></div><strong class="cell-voltage">${v.toFixed(3)} V</strong><span class="cell-no">CELL ${String(i+1).padStart(2,'0')}</span></div>`).join('');$('pack-voltage').value=cells.reduce((a,b)=>a+b,0).toFixed(2);$('spread').textContent=spread+' mV';$('balance-status').textContent=balancing?'Balancing':spread<=5?'Balanced':'Idle';$('balance').textContent=balancing?'Pause balancing':spread<=5?'Pack balanced':'Start balancing';$('balance').disabled=spread<=5;}
$('balance').addEventListener('click',()=>{balancing=!balancing;drawPack();beep();});
$('weak-cell').addEventListener('click',()=>{cells[3]=Math.max(3.2,cells[3]-.18);drawPack();$('battery-hint').textContent='Cell 04 is lower. Passive balancing dissipates energy from the higher cells.';beep(220);});
$('reset-pack').addEventListener('click',()=>{cells=[4.06,4.11,4.08,3.91,4.04,4.09];balancing=false;drawPack();$('battery-hint').textContent='The weakest cell sets the limit.';});
function drawUPS(){const online=inputOn||soc>0;$('soc').textContent=Math.max(0,soc).toFixed(0)+'%';$('output-voltage').value=online?'24.0':'0.0';$('input-node').classList.toggle('offline',!inputOn);$('input-node').classList.toggle('active',inputOn);$('input-state').textContent=inputOn?'CONNECTED':'DISCONNECTED';$('input-flow').classList.toggle('off',!inputOn);$('battery-flow').classList.toggle('off',!online);$('load-state').textContent=online?'ONLINE':'OFFLINE';$('supply').textContent=inputOn?'DC input':soc>0?'Battery':'None';$('unplug').textContent=inputOn?'Disconnect input':'Reconnect input';$('ups-caption').textContent=inputOn?'GO ON. PULL THE PLUG.':soc>0?'INPUT LOST. OUTPUT STILL HERE.':'BATTERY EMPTY. RECONNECT THE INPUT.';}
$('unplug').addEventListener('click',()=>{inputOn=!inputOn;drawUPS();beep(inputOn?660:220);});
$('reset-ups').addEventListener('click',()=>{soc=100;drawUPS();});
$('load').addEventListener('input',()=>{$('load-label').textContent=$('load').value+' W';});
$('easter-egg').addEventListener('click',()=>{$('secret').showModal();beep(1100);});
drawPack();drawUPS();
function frame(now){const dt=Math.min((now-last)/1000||0,.05);last=now;accumulator+=dt;
  const target=stopped?0:Number($('speed').value)*(reverse?-1:1);rpm+=(target-rpm)*Math.min(dt*6,1);if(Math.abs(rpm)<.1)rpm=0;
  if(!paused&&mode==='motor'){theta+=rpm/60*Math.PI*2*dt/60;phase=theta*4;}
  if(mode==='motor'){motor?.render({theta,phase,power:stopped?0:.55,exploded});drawScope();if(!motor)$('fallback').querySelector('svg').style.transform=`rotate(${theta}rad)`;}
  if(balancing&&mode==='battery'){const min=Math.min(...cells);cells=cells.map(v=>Math.max(min,v-dt*.013));if(Math.max(...cells)-min<=.003)balancing=false;}
  if(mode==='ups'&&!inputOn)soc=Math.max(0,soc-(Number($('load').value)/.9)/(24*8)*100*dt/3600*600);
  if(accumulator>.1){$('rpm').value=Math.round(Math.abs(rpm)).toLocaleString();if(mode==='battery')drawPack();if(mode==='ups')drawUPS();accumulator=0;}
  requestAnimationFrame(frame);
}
document.addEventListener('visibilitychange',()=>{last=performance.now();});requestAnimationFrame(frame);
window.labState=()=>({mode,paused,stopped,rpm,exploded,cells:[...cells],balancing,inputOn,soc,webgl:!!motor});
