"""Build original, self-contained SVG artwork. Python standard library only."""

from pathlib import Path
from math import sin, cos, pi
from html import escape

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
BG, PANEL, LINE = "#0b1218", "#101e25", "#263a41"
WHITE, MUTED, LIME, TEAL, GOLD = "#f0f4e9", "#9eb2ba", "#c3f56b", "#61d9cd", "#f5c67a"
FONT = "'Segoe UI',Arial,sans-serif"
MONO = "Consolas,'Liberation Mono',monospace"


def text(x, y, content, size=18, fill=WHITE, weight=400, mono=False, extra=""):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-family="{MONO if mono else FONT}" '
            f'font-size="{size}" font-weight="{weight}" {extra}>{escape(content)}</text>')


def line(x1, y1, x2, y2, color=LINE, width=1, extra=""):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" {extra}/>'


def circle(x, y, r, fill="none", stroke=LINE, sw=1, extra=""):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def rect(x, y, w, h, fill=PANEL, rx=0, stroke="none", extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" {extra}/>'


def doc(w, h, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">Original technical illustration for MNik-EV. Decorative motion stops when reduced motion is requested.</desc>
<defs>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#24353c" stroke-width="0.6" opacity="0.48"/></pattern>
  <radialGradient id="halo"><stop stop-color="#284638" stop-opacity="0.65"/><stop offset="1" stop-color="#0b1218" stop-opacity="0"/></radialGradient>
  <linearGradient id="edge"><stop stop-color="#c3f56b"/><stop offset="0.6" stop-color="#61d9cd"/><stop offset="1" stop-color="#0b1218"/></linearGradient>
</defs>
<style>
  .rotor {{ animation: rotate 24s linear infinite; }}
  .waves {{ animation: flow 12s linear infinite; }}
  .pulse {{ animation: pulse 4s ease-in-out infinite; }}
  @keyframes rotate {{ to {{ transform: rotate(360deg); }} }}
  @keyframes flow {{ to {{ transform: translateX(-400px); }} }}
  @keyframes pulse {{ 50% {{ opacity: 0.4; }} }}
  @media (prefers-reduced-motion: reduce) {{ .rotor,.waves,.pulse {{ animation: none; }} }}
</style>
{rect(0, 0, w, h, BG, 18)}
{body}
</svg>
'''


def motor(cx, cy, scale=1):
    parts = [f'<g transform="translate({cx} {cy}) scale({scale})">', circle(0, 0, 230, "url(#halo)", "none")]
    for r in (178, 166, 135):
        parts.append(circle(0, 0, r))
    parts += [line(-198, 0, 198, 0), line(0, -198, 0, 198)]
    for i in range(48):
        a = 2 * pi * i / 48
        r1, r2 = (169, 178) if i % 4 == 0 else (174, 178)
        parts.append(line(round(cos(a)*r1, 2), round(sin(a)*r1, 2), round(cos(a)*r2, 2), round(sin(a)*r2, 2), MUTED if i % 4 == 0 else LINE))
    for i in range(12):
        color = (LIME, TEAL, GOLD)[i % 3]
        parts.append(f'<g transform="rotate({i*30})">{rect(-13, -150, 26, 38, PANEL, 5, color)}{line(-5,-141,-5,-121,color)}{line(4,-141,4,-121,color)}</g>')
    parts += [circle(0, 0, 97, PANEL, LINE), '<g class="rotor">']
    for i in range(8):
        parts.append(f'<path d="M-20 -77 Q0 -84 20 -77 L16 -61 Q0 -66 -16 -61 Z" fill="{LIME if i%2==0 else TEAL}" opacity="0.8" transform="rotate({i*45})"/>')
    parts += [line(-48, 0, 48, 0, MUTED), line(0,-48,0,48,MUTED), circle(0,0,9,BG,LIME,2), '</g>']
    parts += [circle(0,0,51,BG,LINE), text(0, -5, "FOC", 27, WHITE, 700, True, 'text-anchor="middle"'), text(0, 17, "CONTROL", 11, MUTED, 400, True, 'text-anchor="middle"'), '</g>']
    return "\n".join(parts)


def waves(x, y, width=400, height=84):
    parts = [f'<svg x="{x}" y="{y}" width="{width}" height="{height}" viewBox="0 0 400 84" overflow="hidden">', rect(0,0,400,84,"#0c161c",8), rect(0,0,400,84,"url(#grid)",8), line(0,42,400,42), '<g class="waves">']
    for i, color in enumerate((LIME, TEAL, GOLD)):
        points = ' '.join(f'{k},{42+26*sin(2*pi*k/200+2*pi*i/3):.2f}' for k in range(-4, 805, 2))
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="1.8"/>')
    return "\n".join(parts + ['</g></svg>'])


def hero(mobile=False):
    if mobile:
        w, h = 640, 890
        p = [rect(1,1,w-2,h-2,'none',18,LINE),rect(0,0,w,3,"url(#edge)"),rect(0,400,w,450,"url(#grid)"),text(40,56,"MNik / EV",27,WHITE,700),text(40,91,"EMBEDDED · POWER · MOTION",15,MUTED,400,True)]
        for y,label,color in [(190,"CODE.",WHITE),(274,"CURRENT.",WHITE),(358,"MOTION.",LIME)]:
            p.append(text(37,y,label,84,color,800,extra='letter-spacing="-4"'))
        p += [text(40,403,"Building the electronics behind motion.",21,MUTED), motor(320,585,0.79), waves(120,743,400,64),text(320,850,"STM32 / FOC / BLDC / BMS / DC UPS",18,WHITE,400,True,'text-anchor="middle"')]
    else:
        w, h = 1200, 580
        p = [rect(1,1,w-2,h-2,'none',18,LINE),rect(0,0,w,3,"url(#edge)"),rect(640,90,528,454,"url(#grid)"),text(54,58,"MNik / EV",25,WHITE,700),text(1144,56,"EMBEDDED / POWER / MOTION",14,MUTED,400,True,'text-anchor="end"'),line(54,86,1146,86)]
        for y,label,color in [(191,"CODE.",WHITE),(285,"CURRENT.",WHITE),(379,"MOTION.",LIME)]:
            p.append(text(49,y,label,100,color,800,extra='letter-spacing="-5"'))
        p += [text(54,431,"Building the electronics",23,MUTED),text(54,463,"behind motion.",23,MUTED),motor(894,276,0.85),text(686,463,"THREE PHASES. ONE DIRECTION.",12,MUTED,400,True),waves(686,472,414,58),line(54,502,596,502),text(54,539,"STM32 / FOC / BLDC / BMS / DC UPS",16,WHITE,400,True)]
        p += [circle(652,110,3,LIME,"none",0, 'class="pulse"'),text(664,114,"CONTROL SYSTEMS",10,MUTED,400,True)]
    return doc(w,h,"MNik-EV | Code. Current. Motion.","\n".join(p))


def solar():
    p = [rect(1,1,1198,205,'none',14,LINE),rect(0,0,1200,206,"url(#grid)",14)]
    p += [circle(103,94,33,'none',GOLD,2)]
    for i in range(12):
        a=2*pi*i/12
        p.append(line(103+cos(a)*44,94+sin(a)*44,103+cos(a)*54,94+sin(a)*54,GOLD,2))
    p += [text(103,177,"SOLAR",14,MUTED,400,True,'text-anchor="middle"'),line(170,111,304,111,TEAL,2,'stroke-dasharray="5 9"'),line(858,111,981,111,TEAL,2,'stroke-dasharray="5 9"')]
    p += ['<g transform="translate(302 20)">',line(6,142,546,142,LINE), '<path d="M16 103 Q42 81 104 77 L195 74 Q214 36 269 34 Q330 33 372 77 L449 84 Q495 88 528 112 L502 127 L30 127 Z" fill="#13232a" stroke="#9eb2ba" stroke-width="2"/>', '<path d="M208 74 Q230 43 268 44 Q306 43 347 76 Z" fill="#244244" stroke="#61d9cd" stroke-width="1.5"/>', '<path d="M54 88 L193 83 M375 86 L473 96 M199 77 L374 79" fill="none" stroke="#c3f56b" stroke-width="3"/>']
    for x in range(76,188,18):
        p.append(line(x,85,x-8,98,LIME,1))
    for x in range(389,466,15):
        p.append(line(x,88,x+10,100,LIME,1))
    for x in (128,422):
        p += [circle(x,124,28,BG,MUTED,2),circle(x,124,16,PANEL,TEAL,2),circle(x,124,4,LIME,'none')]
    p += ['</g>',rect(1002,78,84,55,'none',6,LIME),rect(1087,94,8,23,LIME,2)]
    for x in (1012,1035,1058):
        p.append(rect(x,89,16,33,LIME,2))
    p += [text(1045,177,"ELECTRIC",14,MUTED,400,True,'text-anchor="middle"')]
    return doc(1200,206,"Solar roots | A conceptual solar-electric vehicle",'\n'.join(p))


for name, content in {"hero.svg":hero(), "hero-mobile.svg":hero(True), "solar.svg":solar()}.items():
    (ASSETS/name).write_text(content,encoding="utf-8",newline="\n")
    print(f"Built assets/{name}")
