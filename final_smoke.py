# final_smoke.py — all 3 pages, no page errors, key wiring correct
from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    b = p.chromium.launch()
    allerr = []
    for page in ["/", "/store.html", "/admin.html"]:
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:100]))
        pg.goto("http://127.0.0.1:8790" + page, wait_until="networkidle", timeout=30000)
        pg.wait_for_timeout(1500)
        ov = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        sk = pg.evaluate("() => (window.__SK__||'').length")
        print(page, "| errors:", errs or "none", "| overflow:", ov, "| key len:", sk)
        allerr += errs
        if page == "/store.html":
            pg.screenshot(path="shots/y1-store-grid.png")
        if page == "/admin.html":
            pg.screenshot(path="shots/y2-admin.png")
        pg.close()
    print("TOTAL ERRORS:", sum(len(a) for a in allerr) if allerr else "NONE")
    b.close()
