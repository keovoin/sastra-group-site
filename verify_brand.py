from playwright.sync_api import sync_playwright

H = "https://sastra-group.vercel.app"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:80]))
    pg.goto(H, wait_until="networkidle")
    pg.wait_for_timeout(2200)
    # hero mark rendered?
    print("hero mark:", pg.evaluate("()=>{const i=document.querySelector('.hero-mark');return i&&i.complete&&i.naturalWidth>0;}"))
    print("nav logo:", pg.evaluate("()=>{const i=document.querySelector('.nav-mark img');return i&&i.complete&&i.naturalWidth>0;}"))
    pg.screenshot(path="shots/brand_hero.png")
    # quiz card thumb
    pg.evaluate("document.querySelector('#more')&&document.getElementById('more').scrollIntoView()")
    pg.wait_for_timeout(1500)
    pg.screenshot(path="shots/brand_more.png")
    print("quiz thumb loaded:", pg.evaluate("()=>{const i=document.querySelector('img[src*=th-quizq]');return i&&i.complete&&i.naturalWidth>0;}"))
    # store page header logo
    pg.goto(H + "/store.html", wait_until="networkidle")
    pg.wait_for_timeout(2500)
    print("store logo:", pg.evaluate("()=>{const i=document.querySelector('img[alt=Sastra]');return i&&i.complete&&i.naturalWidth>0;}"))
    pg.screenshot(path="shots/brand_store.png")
    print("errors:", errs)
    b.close()
