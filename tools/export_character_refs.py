"""Export clean character reference PNGs (512x640) from the game's own drawing code, for AI video tools.

Run: CHROMIUM_PATH=/path/to/chromium python tools/export_character_refs.py OUT_DIR
"""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright
html = (pathlib.Path(__file__).resolve().parents[1] / 'index.html').read_text(encoding='utf-8')
INJ = r"""
window.__ref=(who)=>{const c=document.createElement('canvas');c.width=512;c.height=640;const g=c.getContext('2d');
 const bg=g.createLinearGradient(0,0,0,640);bg.addColorStop(0,'#fbf6ff');bg.addColorStop(1,'#efe6fa');g.fillStyle=bg;g.fillRect(0,0,512,640);
 g.imageSmoothingEnabled=false;
 if(who==='penny'){drawPenny(g,256,430,7,0,true,{pile:false});}
 else if(who==='muffin'){const t=document.createElement('canvas');t.width=512;t.height=640;const tg=t.getContext('2d');drawMuffin(tg,256,470,'sit',1,0,'',1);
   const d=tg.getImageData(0,0,512,640).data;let x0=512,y0=640,x1=0,y1=0;for(let y=0;y<640;y++)for(let x=0;x<512;x++)if(d[(y*512+x)*4+3]>8){x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);}
   const w=x1-x0+1,h=y1-y0+1,k=Math.floor(400/Math.max(w,h));g.drawImage(t,x0,y0,w,h,256-w*k/2,500-h*k,w*k,h*k);}
 else if(who==='Mrs. Emiko Tanaka'){drawPerson(g,256,480,{name:who,cast:who},0,'down',false,9);drawPerson(g,256,480,{name:who,cast:who},0,'down',false,9);}
 else{drawPerson(g,256,480,{name:who,cast:who},0,'down',false,9);}
 return c.toDataURL('image/png');};
"""
idx = html.rfind('\n})();\n</script>')
html = html[:idx] + '\n' + INJ + html[idx:]
cast = {'delores':'delores','player-raccoon':'player','dr-merriweather':'Dr. Evangeline Merriweather',
 'hiroshi-tanaka':'Mr. Hiroshi Tanaka','emiko-tanaka':'Mrs. Emiko Tanaka','mr-finch':'Mr. Finch','m-nine':'M. Nine',
 'cece-wrenwood':'Celestine "Cece" Wrenwood','penny':'penny','muffin':'muffin'}
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=__import__('os').getenv('CHROMIUM_PATH','/usr/bin/chromium'), args=['--no-sandbox'])
    pg = b.new_page()
    pg.route('**/*', lambda r: r.abort() if not r.request.url.startswith(('data:','about:','file:')) else r.continue_())
    pg.set_content(html, wait_until='load'); pg.wait_for_timeout(800)
    for f, who in cast.items():
        d = pg.evaluate('w=>window.__ref(w)', who)
        (out / f'{f}.png').write_bytes(base64.b64decode(d.split(',')[1]))
        print(f)
    b.close()
