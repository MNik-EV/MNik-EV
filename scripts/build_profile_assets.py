"""Build the small original SVG layouts around the Three.js and snk assets."""
from pathlib import Path
from html import escape
from datetime import date
import json,textwrap
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'
BG='#0e1218'; LINE='#2b323b'; WHITE='#efede8'; AMBER='#ffbb63'; MUTED='#9aa5b1'
def text(x,y,value,size=18,color=WHITE,weight=400,extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{weight}" {extra}>{escape(value)}</text>'
def doc(w,h,title,body,css=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><style>{css}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="{BG}" stroke="{LINE}"/>{body}</svg>\n'
def save(name,value):(OUT/name).write_text(value,encoding='utf-8',newline='\n')
def terminal(mobile=False):
    w,h=(660,320) if mobile else (1100,242)
    body=''.join(f'<circle cx="{30+i*19}" cy="28" r="5" fill="{c}"/>' for i,c in enumerate(['#f0887b','#e3b66f','#79b8a7']))
    body+=text(w-24,34,'mnik@lab ~',13,MUTED,extra='text-anchor="end"')
    body+=f'<path d="M1 52H{w-1}" stroke="{LINE}"/>'
    lines=[('> whoami',AMBER),('Embedded systems. Motor drives. Energy.',WHITE),('> previous --team',AMBER),('Electrical & Computer Lead / Persian Gazelle',WHITE)]
    if mobile:lines=[('> whoami',AMBER),('Embedded systems. Motor drives. Energy.',WHITE),('> previous --team',AMBER),('Electrical & Computer Lead',WHITE),('Persian Gazelle / Solar Car',MUTED)]
    for i,(v,c) in enumerate(lines):body+=text(27,87+i*31,v,26 if mobile else 20,c,extra='font-variant-ligatures="none"')
    y=281 if mobile else 216
    body+=text(27,y,'> ',26 if mobile else 19,AMBER)
    for i,value in enumerate(['make firmware','measure. debug. repeat.','keep the magic smoke inside.']):
        body+=f'<g class="line{i}">'+text(58 if mobile else 50,y,value,26 if mobile else 19,AMBER)+'</g>'
    css='.line0{animation:a 15s infinite}.line1{opacity:0;animation:b 15s infinite}.line2{opacity:0;animation:c 15s infinite}@keyframes a{0%,30%,100%{opacity:1}33%,97%{opacity:0}}@keyframes b{0%,32%,66%,100%{opacity:0}34%,63%{opacity:1}}@keyframes c{0%,65%,100%{opacity:0}67%,97%{opacity:1}}'
    return doc(w,h,'MNik-EV: embedded systems, motor drives, energy; former Electrical and Computer Lead, Persian Gazelle',body,css)
save('terminal.svg',terminal());save('terminal-mobile.svg',terminal(True))
projects=[
    ('foc','01','MOTOR CONTROL','Single-shunt FOC','STM32F446 firmware, current sensing & motor control.','C / STM32 / MCSDK','cpu'),
    ('copilot','02','ENGINEERING TOOLS','Engineering Copilot','Deterministic calculations. Source-aware design review.','PYTHON / PYQT6 / ELECTRONICS','terminal'),
    ('shield','03','OPEN HARDWARE','Robot Shield','ATmega328P, power protection & battery monitoring.','PCB / ATMEGA328P / ROBOTICS','circuit-board'),
    ('fusion','04','SENSOR FUSION','LiDAR × Camera','LD19–IMX219 ranging, Pi relay & laptop processing.','PYTHON / OPENCV / PERCEPTION','scan')
]
for slug,n,category,title,desc,tags,icon in projects:
    for mobile in (False,True):
        w,h=(660,245) if mobile else (1100,176)
        body=f'<path d="M1 30V{h-30}" stroke="{AMBER}" stroke-width="3"/>'
        x=25 if mobile else 32
        body+=text(x,32,n+' / '+category,18 if mobile else 13,AMBER,extra='letter-spacing="1.5"')
        body+=text(x,82,title,35,WHITE,600)
        for line_no,part in enumerate(textwrap.wrap(desc,42) if mobile else [desc]):
            body+=text(x,120+line_no*31,part,24 if mobile else 19,MUTED)
        body+=text(x,215 if mobile else 151,tags,18 if mobile else 12,MUTED,extra='letter-spacing="1"')
        body+=text(w-38,195 if mobile else 100,'↗',34,AMBER,extra='text-anchor="end"')
        if not mobile:
            raw=(ROOT/'docs/vendor/lucide'/f'{icon}.svg').read_text(encoding='utf-8')
            inner=raw[raw.index('>',raw.index('<svg'))+1:raw.rindex('</svg>')]
            body+=f'<g transform="translate(884 49) scale(2.5)" fill="none" stroke="{AMBER}" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" opacity=".75">{inner}</g>'
        save(f'project-{slug}{"-mobile" if mobile else ""}.svg',doc(w,h,title+' — '+desc,body))
body=text(34,40,'SOLAR ROOTS / ELECTRIC FUTURE',13,AMBER,extra='letter-spacing="2"')+text(33,100,'Persian Gazelle',44,WHITE,600)+text(35,144,'Former Electrical & Computer Team Lead',23,MUTED)
body+=text(1066,106,'غزال ایرانی',40,AMBER,extra='text-anchor="end"')
body+=f'<path d="M34 174H1066" stroke="{LINE}"/>'+text(34,207,'Solar car engineering · Embedded control · Energy systems',18,MUTED)
save('gazelle.svg',doc(1100,236,'Persian Gazelle — Former Electrical and Computer Team Lead',body))
body=text(27,32,'SOLAR ROOTS / ELECTRIC FUTURE',13,AMBER,extra='letter-spacing="1"')+text(26,87,'Persian Gazelle',39,WHITE,600)+text(27,122,'Former Electrical & Computer Team Lead',20,MUTED)+text(27,181,'غزال ایرانی',30,AMBER)
save('gazelle-mobile.svg',doc(660,215,'Persian Gazelle — Former Electrical and Computer Team Lead',body))
body=text(34,41,'THE LIVE LAB',13,AMBER,extra='letter-spacing="2"')+text(34,98,'Go on. Touch the controls.',38,WHITE,600)+text(35,140,'Spin the motor. Balance the pack. Pull the plug.',21,MUTED)+text(35,190,'THREE.JS / WEBGL / THREE INTERACTIVE EXPERIMENTS',12,AMBER,extra='letter-spacing="1"')
body+=f'<circle cx="989" cy="112" r="51" fill="#ffbb63"/>'+text(988,127,'↗',43,'#18140f',extra='text-anchor="middle"')
save('launch.svg',doc(1100,222,'Open the live lab: motor, battery balancing, and DC UPS',body))
body=text(27,35,'THE LIVE LAB',13,AMBER,extra='letter-spacing="2"')+text(27,91,'Touch the controls.',36,WHITE,600)+text(27,134,'Motor. Battery. DC UPS.',22,MUTED)+text(27,185,'THREE.JS / WEBGL',14,AMBER)+text(610,188,'↗',38,AMBER,extra='text-anchor="end"')
save('launch-mobile.svg',doc(660,216,'Open the live lab',body))
print('Built terminal, project cards, Gazelle identity and launch graphics.')
