# ux_audit.py — programmatic UX/UI checks on landing + store (both themes, desktop+mobile)
from playwright.sync_api import sync_playwright
import json

def luminance(rgb):
    r, g, b = [x/255 for x in rgb]
    def f(c): return c/12.92 if c <= .03928 else ((c+.055)/1.055)**2.4
    return .2126*f(r)+.7152*f(g)+.0722*f(b)

REPORT = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for page, name in [("http://127.0.0.1:8790/", "landing"), ("http://127.0.0.1:8790/store.html", "store"), ("http://127.0.0.1:8790/admin.html", "admin")]:
        res = {"issues": []}
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.goto(page, wait_until="domcontentloaded", timeout=30000)
        try:
            pg.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        pg.wait_for_timeout(1200)
        # 1 overflow / horizontal scroll
        res["h_overflow"] = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        # 2 images broken
        res["broken_imgs"] = pg.evaluate("[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.getAttribute('src'))")
        # 3 tap targets < 40px (desktop: ignore; measured on mobile pass below)
        # 4 contrast of key text
        res["contrast"] = pg.evaluate("""() => {
            function lum(rgb){const [r,g,b]=rgb.match(/\\d+/g).map(Number).map(v=>v/255);const f=c=>c<=.03928?c/12.92:((c+.055)/1.055)**2.4;return .2126*f(r)+.7152*f(g)+.0722*f(b);}
            function cmp(el){let c=el; while(c){const bg=getComputedStyle(c).backgroundColor; if(bg&&!bg.includes('rgba(0, 0, 0, 0)')&&!bg.startsWith('rgba(0,0,0,0)')) return bg; c=c.parentElement;} return 'rgb(19,18,17)';}
            const out=[];
            for(const sel of ['.prose','.hero-sub','h2.big','.tag','.d','p.d','.badge','.hint','.status','body','label','footer']){
                const el=document.querySelector(sel); if(!el) continue;
                const fg=getComputedStyle(el).color, bg=cmp(el);
                try{const ratio=(Math.max(lum(fg),lum(bg))+.05)/(Math.min(lum(fg),lum(bg))+.05); if(ratio<3.5) out.push([sel, +ratio.toFixed(2)]);}catch(e){}
            }
            return out;
        }""")
        # 5 inputs without labels/aria
        res["inputs"] = pg.evaluate("""() => [...document.querySelectorAll('input,button')].map(el=>({
            tag: el.tagName, id: el.id||null,
            labeled: !!(el.id && document.querySelector('label[for="'+el.id+'"]')) || !!el.getAttribute('aria-label') || !!el.textContent.trim() || !!el.placeholder
        })).filter(x=>!x.labeled)""")
        # 6 anchors with empty href
        res["dead_links"] = pg.evaluate("[...document.querySelectorAll('a')].filter(a=>!a.getAttribute('href')||a.getAttribute('href')==='#').map(a=>a.textContent.trim().slice(0,30))")
        # 7 mobile: small controls + overflow
        m = b.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
        m.goto(page, wait_until="domcontentloaded", timeout=30000)
        try:
            m.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        m.wait_for_timeout(1000)
        res["mobile_h_overflow"] = m.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        res["small_controls"] = m.evaluate("""() => [...document.querySelectorAll('button,a.btn,.btn,a.cta,.tag')].filter(el=>{const r=el.getBoundingClientRect(); return r.width>0 && (r.height<36 || r.width<36) && el.offsetParent !== null;}).map(el=>(el.id||el.className.toString().slice(0,20))+' '+Math.round(el.getBoundingClientRect().width)+'x'+Math.round(el.getBoundingClientRect().height))""")
        res["mobile_errors"] = []
        m.on("pageerror", lambda e: res["mobile_errors"].append(str(e)[:80]))
        # 8 tab order sanity: focus visible?
        res["focus_visible"] = pg.evaluate("""() => {const el=document.querySelector('.field input, input'); if(!el) return 'n/a'; el.focus(); const cs=getComputedStyle(el); return (cs.boxShadow!=='none'||cs.outlineStyle!=='none')?'yes':'no';}""")
        pg.close(); m.close()
        REPORT[name] = res
        print("====", name)
        print(json.dumps(res, indent=1)[:1400])
    b.close()
json.dump(REPORT, open("ux_report.json", "w", encoding="utf-8"), indent=1)
