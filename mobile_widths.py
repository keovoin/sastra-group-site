from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (320, 360, 412):
        m = b.new_page(viewport={"width": w, "height": 800}, is_mobile=True)
        m.goto("https://sastra-group.vercel.app/", wait_until="domcontentloaded", timeout=45000)
        m.wait_for_timeout(1500)
        r = m.evaluate("""() => {
            const de = document.documentElement;
            // find elements wider than viewport
            const wide = [];
            for (const el of document.querySelectorAll('body *')) {
                const rc = el.getBoundingClientRect();
                if (rc.right > de.clientWidth + 2 && rc.width > 40 && getComputedStyle(el).position !== 'fixed') {
                    const cn = (el.className || '').toString().slice(0, 30);
                    wide.push(el.tagName + '.' + cn + ' r=' + Math.round(rc.right) + ' w=' + Math.round(rc.width));
                }
            }
            return {vw: de.clientWidth, scrollW: de.scrollWidth, wide: wide.slice(0, 8)};
        }""")
        print(w, "→ overflow:", r["scrollW"] - r["vw"], "| offenders:", r["wide"])
        m.close()
    b.close()
