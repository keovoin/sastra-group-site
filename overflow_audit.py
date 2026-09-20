from playwright.sync_api import sync_playwright

JS = """
(vw) => {
  const out=[];
  document.querySelectorAll('*').forEach(el=>{
    const r=el.getBoundingClientRect();
    if(r.width>0 && r.right > vw+2){
      out.push((el.tagName+'.'+(el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)).slice(0,42)+' right='+Math.round(r.right));
    }
  });
  return out.slice(0,12);
}
"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for vw in (320, 360):
        pg = b.new_page(viewport={"width": vw, "height": 760})
        for url in ("https://sastra-group.vercel.app", "https://sastra-group.vercel.app/store.html"):
            pg.goto(url, wait_until="networkidle")
            pg.wait_for_timeout(2000)
            bad = pg.evaluate(JS, vw)
            print(f"--- {vw}px {url.split('/')[-1] or 'index'}: {len(bad)} overflowing")
            for x in bad[:8]: print("   ", x)
        pg.close()
    b.close()
