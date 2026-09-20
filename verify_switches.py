# verify_switches.py — EN/KM + dark/light interactive QA + screenshots
from playwright.sync_api import sync_playwright
import os

OUT = r"C:\Users\KEOVOIN-DESKTOP\sastra-group-site\shots"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("http://127.0.0.1:8790/", wait_until="networkidle", timeout=30000)
    pg.wait_for_timeout(1500)
    pg.screenshot(path=os.path.join(OUT, "v1-dark-en.png"))

    # switch to Khmer
    pg.click("#btn-km"); pg.wait_for_timeout(700)
    km_ok = pg.evaluate("""() => {
        const h1 = document.querySelector('.hero h1').innerText;
        const nav = document.getElementById('nav').innerText;
        return {h1: h1.slice(0,40), navHasKm: /[\\u1780-\\u17FF]/.test(nav+h1)};
    }""")
    pg.screenshot(path=os.path.join(OUT, "v2-dark-km.png"))

    # light mode
    pg.click("#btn-theme"); pg.wait_for_timeout(700)
    bg = pg.evaluate("getComputedStyle(document.body).backgroundColor")
    pg.screenshot(path=os.path.join(OUT, "v3-light-km.png"))

    # back to EN, check restore
    pg.click("#btn-en"); pg.wait_for_timeout(500)
    en_restored = pg.evaluate("() => document.querySelector('.hero h1').innerText")
    pg.screenshot(path=os.path.join(OUT, "v4-light-en.png"))

    # more-products section visible, scroll reveal
    pg.evaluate("document.querySelector('#more').scrollIntoView({block:'start'})")
    pg.wait_for_timeout(1300)
    rows = pg.evaluate("document.querySelectorAll('.more-row').length")
    pg.screenshot(path=os.path.join(OUT, "v5-more-rows.png"))

    # persistence after reload
    pg.reload(wait_until="networkidle"); pg.wait_for_timeout(900)
    persist = pg.evaluate("() => ({lang: document.documentElement.lang, light: document.documentElement.classList.contains('light')})")
    print("km switch:", km_ok)
    print("light bg:", bg)
    print("en restored:", en_restored[:40].replace("\n", "/"))
    print("more rows:", rows)
    print("persist after reload:", persist)
    print("PAGE ERRORS:", errs if errs else "none")

    # mobile km
    m = b.new_page(viewport={"width": 390, "height": 844})
    m.goto("http://127.0.0.1:8790/")
    m.wait_for_timeout(800)
    m.evaluate("() => {document.getElementById('btn-km').click();document.getElementById('btn-theme').click();}")
    m.wait_for_timeout(600)
    m.screenshot(path=os.path.join(OUT, "v6-mobile-light-km.png"))
    ov = m.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
    print("mobile overflow px:", ov)
    b.close()
