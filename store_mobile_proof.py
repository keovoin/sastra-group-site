from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    m = b.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True,
                   user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")
    m.goto("https://sastra-group.vercel.app/store.html", wait_until="networkidle")
    m.wait_for_timeout(3000)
    cards = m.locator(".product-card").count()
    print("product cards on mobile:", cards)
    if cards:
        print("first card text:", m.locator(".product-card").first.inner_text().replace("\n", " | ")[:90])
        print("buy btn:", m.locator(".product-card .buy, .product-card button, .product-card a").first.is_visible())
    m.screenshot(path="shots/fin_store_mobile.png")
    b.close()
