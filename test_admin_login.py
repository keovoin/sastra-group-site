from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:80]))
    pg.goto("https://sastra-group.vercel.app/admin.html", wait_until="networkidle", timeout=40000)
    pg.wait_for_timeout(1500)
    # wrong pass
    pg.fill("#pass", "wrongpass")
    pg.click("#lgo")
    pg.wait_for_timeout(2500)
    print("wrong-pass msg:", pg.evaluate("document.getElementById('lmsg').textContent"))
    # right pass (Juniper@123)
    pg.fill("#pass", "Juniper@123")
    pg.click("#lgo")
    pg.wait_for_timeout(4000)
    shown = pg.evaluate("() => ({dash:!document.getElementById('dash').classList.contains('hide'), stats:document.getElementById('stats').innerText.replace(/\\n+/g,' | ')})")
    print("after correct pass:", shown)
    print("errors:", errs or "none")
    pg.screenshot(path="shots/ad-unlocked.png")
    b.close()
