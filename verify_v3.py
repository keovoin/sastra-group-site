# verify_v3.py — landing (hero, store section, more-cards, km) + store.html states
from playwright.sync_api import sync_playwright
import os

OUT = r"C:\Users\KEOVOIN-DESKTOP\sastra-group-site\shots"
with sync_playwright() as p:
    b = p.chromium.launch()
    errs = []
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    pg.on("pageerror", lambda e: errs.append("landing:" + str(e)[:100]))

    # --- landing ---
    pg.goto("http://127.0.0.1:8790/", wait_until="networkidle")
    pg.wait_for_timeout(1400)
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(400)
    pg.screenshot(path=os.path.join(OUT, "w1-hero-new.png"))
    ov = pg.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
    # store section
    pg.evaluate("document.querySelector('#store').scrollIntoView({block:'center'})"); pg.wait_for_timeout(1400)
    pg.screenshot(path=os.path.join(OUT, "w2-store-sec.png"))
    # more cards
    pg.evaluate("document.querySelector('#more').scrollIntoView({block:'start'})"); pg.wait_for_timeout(1600)
    cards = pg.evaluate("() => ({rows: document.querySelectorAll('.more-card').length, imgs: [...document.querySelectorAll('.more-thumb img')].map(i=>i.complete&&i.naturalWidth>0), soon: document.querySelectorAll('.more-soon span').length})")
    pg.screenshot(path=os.path.join(OUT, "w3-more-cards.png"))
    print("landing overflow:", ov, "| cards:", cards)

    # --- store page ---
    sp = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    sp.on("pageerror", lambda e: errs.append("store:" + str(e)[:100]))
    sp.goto("http://127.0.0.1:8790/store.html", wait_until="networkidle")
    sp.wait_for_timeout(1500)
    st = sp.evaluate("""() => ({
        title: document.getElementById('p-title').textContent,
        price: document.getElementById('p-price').textContent,
        cover: (()=>{const i=document.getElementById('cover');return i.complete&&i.naturalWidth>0})(),
    })""")
    print("store state:", st)
    # email validation error path
    sp.click("#go"); sp.wait_for_timeout(500)
    e1 = sp.evaluate("document.getElementById('e1').textContent")
    print("bad-email error:", repr(e1))
    sp.screenshot(path=os.path.join(OUT, "w4-store-en.png"))
    # km + light on store
    sp.click("#b-km"); sp.wait_for_timeout(400); sp.click("#b-theme"); sp.wait_for_timeout(400)
    sp.screenshot(path=os.path.join(OUT, "w5-store-light-km.png"))
    # landing km cards
    pg.click("#btn-km"); pg.wait_for_timeout(800)
    pg.evaluate("document.querySelector('#more').scrollIntoView({block:'start'})"); pg.wait_for_timeout(900)
    pg.screenshot(path=os.path.join(OUT, "w6-more-km.png"))
    print("ERRORS:", errs if errs else "none")
    b.close()
