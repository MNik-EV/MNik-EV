"""Capture the actual Three.js scene as lightweight animated WebP covers.

Requires Playwright, Chromium, ffmpeg and a local server at --url.
"""
from pathlib import Path
import argparse,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.path.insert(0,str(ROOT.parent/'.profile-preview-tools'))
    from playwright.sync_api import sync_playwright
parser=argparse.ArgumentParser()
parser.add_argument('--url',default='http://127.0.0.1:8766/docs/')
parser.add_argument('--browser',default=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
args=parser.parse_args()
with sync_playwright() as p:
    opts={'headless':True,'args':['--enable-unsafe-swiftshader']}
    if Path(args.browser).is_file():opts['executable_path']=args.browser
    browser=p.chromium.launch(**opts)
    for mobile in (False,True):
        name='hero-mobile' if mobile else 'hero'
        frames=ROOT/'.preview'/f'frames-{name}';frames.mkdir(parents=True,exist_ok=True)
        w,h=(720,900) if mobile else (1440,640)
        page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
        page.goto(args.url+'hero.html?export'+('&mobile' if mobile else ''),wait_until='networkidle')
        page.wait_for_function('window.heroReady === true')
        for i in range(80):
            page.evaluate('(t)=>renderFrame(t)',i/10)
            page.screenshot(path=str(frames/f'{i:03}.png'))
            if i%20==0:print(f'{name}: frame {i}/80',flush=True)
        page.close()
        target=660 if mobile else 1100
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','10','-i',str(frames/'%03d.png'),'-vf',f'scale={target}:-2:flags=lanczos','-c:v','libwebp_anim','-quality','78','-compression_level','6','-loop','0',str(ROOT/'assets'/f'{name}-motion.webp')],check=True)
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(frames/'000.png'),'-vf',f'scale={target}:-2:flags=lanczos','-quality','88',str(ROOT/'assets'/f'{name}.webp')],check=True)
        print(f'Encoded {name} covers.',flush=True)
    browser.close()
