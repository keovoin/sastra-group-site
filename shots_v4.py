# shots_v4.py — visual check: store grid, modal step1, admin login+dash layout
from playwright.sync_api import sync_playwright
import os
OUT = r"C:\Users\KEOVOIN-DESKTOP\sastra-group-site\shots"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:90]))
    pg.goto("http://127.0.0.1:8790/store.html", wait_until="networkidle")
    pg.wait_for_timeout(1500)
    pg.screenshot(path=os.path.join(OUT, "x1-store-grid.png"))
    km = pg.evaluate("() => {document.getElementById('b-km').click(); return document.querySelector('.head h1').textContent.slice(0,30);}")
    print("km head:", km)
    pg.click("#b-en")
    a = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    a.on("pageerror", lambda e: errs.append("admin:" + str(e)[:90]))
    a.goto("http://127.0.0.1:8790/admin.html", wait_until="networkidle")
    a.wait_for_timeout(1200)
    a.screenshot(path=os.path.join(OUT, "x2-admin-login.png"))
    # fake-unlock to see dash layout? (no backend yet) — just fill+save view via direct DOM
    print("admin grid hidden ok:", a.evaluate("document.getElementById('dash').classList.contains('hide')"))
    # landing nav now has Store link
    l = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    l.goto("http://127.0.0.1:8790/", wait_until="networkidle"); l.wait_for_timeout(1200)
    print("store link in nav:", l.evaluate("!!document.querySelector('.nav-links a[href=\"#store\"]')"))
    print("ERRORS:", errs if errs else "none")
    b.close()
