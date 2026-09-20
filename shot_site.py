# screenshot the landing page: desktop hero + each product section + mobile
from playwright.sync_api import sync_playwright
import time

URL = "http://127.0.0.1:8790/"
OUT = r"C:\Users\KEOVOIN-DESKTOP\sastra-group-site\shots"
import os; os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    errs = []
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL, wait_until="networkidle", timeout=30000)
    pg.wait_for_timeout(1600)
    pg.screenshot(path=os.path.join(OUT, "01-hero.png"))
    for anchor in ["#khinvite", "#tvercv", "#urdrama", "#khfinder", "#biz", "#group"]:
        pg.evaluate(f"document.querySelector('{anchor}').scrollIntoView({{behavior:'instant',block:'center'}})")
        pg.wait_for_timeout(1300)
        pg.screenshot(path=os.path.join(OUT, "sec-" + anchor.strip("#") + ".png"))
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    pg.wait_for_timeout(1200)
    pg.screenshot(path=os.path.join(OUT, "09-footer.png"))
    # mobile
    m = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True)
    m.goto(URL, wait_until="networkidle", timeout=30000)
    m.wait_for_timeout(1200)
    m.screenshot(path=os.path.join(OUT, "m1-hero.png"))
    m.evaluate("document.querySelector('#khinvite').scrollIntoView({behavior:'instant',block:'start'})")
    m.wait_for_timeout(1200)
    m.screenshot(path=os.path.join(OUT, "m2-prod.png"))
    print("ERRORS:", errs if errs else "none")
    b.close()
