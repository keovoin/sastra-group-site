from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    m = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True)
    m.goto("https://sastra-group.vercel.app/", wait_until="networkidle", timeout=45000)
    m.wait_for_timeout(2500)
    m.screenshot(path="shots/mv1-hero.png")
    m.evaluate("document.querySelector('#khinvite').scrollIntoView({block:'start'})")
    m.wait_for_timeout(1500)
    m.screenshot(path="shots/mv2-prod.png")
    m.evaluate("document.querySelector('#more').scrollIntoView({block:'start'})")
    m.wait_for_timeout(1500)
    m.screenshot(path="shots/mv3-more.png")
    # numeric checks
    r = m.evaluate("""() => {
        const h1=document.querySelector('.hero h1');
        const de=document.documentElement;
        return {
            vw: window.innerWidth, scrollW: de.scrollWidth,
            h1size: getComputedStyle(h1).fontSize,
            sectionPad: getComputedStyle(document.querySelector('section')).paddingLeft,
            splitCols: getComputedStyle(document.querySelector('.split')).gridTemplateColumns,
            moreCols: getComputedStyle(document.querySelector('.more-list')).gridTemplateColumns,
        };
    }""")
    print(r)
    b.close()
