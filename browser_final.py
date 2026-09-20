from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:80]))
    pg.goto("https://sastra-group.vercel.app/store.html", wait_until="networkidle", timeout=45000)
    pg.wait_for_timeout(4000)
    cards = pg.evaluate('() => document.querySelectorAll(".card").length')
    cover = pg.evaluate('() => {const i=document.querySelector(".card .thumb img"); return i?(i.complete&&i.naturalWidth>0):false;}')
    title = pg.evaluate('() => {const h=document.querySelector(".card h3"); return h?h.textContent:null;}')
    pg.click(".buy")
    pg.wait_for_timeout(600)
    pg.fill("#email", "demo@sastra.store")
    pg.click("#go")
    pg.wait_for_timeout(9000)
    qr = pg.evaluate('() => {const q=document.getElementById("qr-img"); return q&&q.naturalWidth>0;}')
    amt = pg.evaluate('() => document.getElementById("qr-amt").textContent')
    pg.screenshot(path="shots/z1-LIVE-STORE-WORKING.png")
    print("cards:", cards, "| title:", title, "| cover:", cover, "| real QR painted:", qr, "| amount:", amt, "| errors:", errs or "none")
    b.close()
