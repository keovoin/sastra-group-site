from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    info = []
    pg.on("response", lambda r: info.append((r.status, r.url[:110])) if "store-payment" in r.url else None)
    pg.goto("https://sastra-group.vercel.app/store.html", wait_until="networkidle")
    pg.wait_for_timeout(2500)
    pg.click(".buy")
    pg.fill("#email", "demo@sastra.store")
    pg.click("#go")
    pg.wait_for_timeout(12000)
    print("net:", info)
    print("e1:", pg.evaluate("document.getElementById('e1').textContent"))
    print("e2:", pg.evaluate("document.getElementById('e2').textContent"))
    q = pg.evaluate("document.getElementById('qr-img').getAttribute('src')")
    print("qr src:", (q or "")[:80])
    b.close()
