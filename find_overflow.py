from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto("http://127.0.0.1:8790/")
    pg.wait_for_timeout(800)
    offenders = pg.evaluate("""() => {
        const dw = document.documentElement.clientWidth;
        const out = [];
        for (const el of document.querySelectorAll('*')) {
            const r = el.getBoundingClientRect();
            if (r.width === 0) continue;
            const right = r.right + scrollX, left = r.left + scrollX;
            if (right > document.documentElement.scrollWidth - 2 && r.width > 30) {
                const cs = getComputedStyle(el);
                if (cs.position === 'fixed' || el.closest('.ticker')) continue;
                out.push(el.tagName + '.' + (el.className.toString().slice(0,40)) + ' right=' + Math.round(right));
            }
        }
        return {docW: document.documentElement.scrollWidth, clientW: dw, out: out.slice(0,12)};
    }""")
    print(offenders)
    b.close()
