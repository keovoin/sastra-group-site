from playwright.sync_api import sync_playwright

H = "https://sastra-group.vercel.app"
with sync_playwright() as p:
    b = p.chromium.launch()

    # A) admin login with new password, real UI clicks
    pg = b.new_page(viewport={"width": 1280, "height": 860})
    pg.goto(H + "/admin.html", wait_until="networkidle")
    pg.fill("#pass", "Juniper@123")
    pg.click("#lgo")
    pg.wait_for_timeout(3000)
    print("A admin unlocked:", pg.locator("#dash").is_visible())
    print("A stats:", pg.locator("#stats").inner_text().replace("\n", " | ")[:110])
    pg.screenshot(path="shots/fin_admin.png")

    # B) landing mobile: store-first + knowitall
    m = b.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    m.goto(H, wait_until="networkidle")
    m.wait_for_timeout(1500)
    print("B order:", m.evaluate("()=>[...document.querySelectorAll('.prod')].map(s=>s.id).join(',')"))
    print("B store-first:", m.evaluate("()=>document.querySelectorAll('.prod')[0].id==='store'"))
    print("B kh-helper card:", m.evaluate("()=>[...document.querySelectorAll('.more-card')].some(a=>a.href.includes('knowitall'))"))
    print("B scrollW==vw:", m.evaluate("()=>document.documentElement.scrollWidth-window.innerWidth"))

    # C) store mobile render
    m.goto(H + "/store.html", wait_until="networkidle")
    m.wait_for_timeout(3500)
    n = m.locator(".card").count()
    print("C store cards(mobile):", n, "| buy visible:", m.locator(".buy, .card a, .card button").first.is_visible() if n else False)
    m.screenshot(path="shots/fin_store_mobile.png", full_page=False)
    b.close()
