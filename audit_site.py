# layout audit: overflow, image load, contrast spot checks
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    for vw, name in [(1440, 'desktop'), (768, 'tablet'), (390, 'mobile')]:
        pg = b.new_page(viewport={"width": vw, "height": 900})
        pg.goto("http://127.0.0.1:8790/", wait_until="networkidle")
        pg.wait_for_timeout(1000)
        r = pg.evaluate("""() => {
            const de = document.documentElement;
            const imgs = [...document.images];
            const broken = imgs.filter(i => !i.complete || i.naturalWidth === 0).map(i => i.getAttribute('src'));
            const badges = [...document.querySelectorAll('.logo-badge')].map(e => {
                const s = getComputedStyle(e); const r = e.getBoundingClientRect();
                return {vis: r.width > 0 && r.height > 0, shadow: s.boxShadow !== 'none'};
            });
            return {
                hscroll: de.scrollWidth > de.clientWidth ? de.scrollWidth : 0,
                imgs: imgs.length, broken,
                sections: document.querySelectorAll('section').length,
                ctaBg: getComputedStyle(document.querySelector('.cta')).backgroundColor,
                badgesShown: badges.filter(x => x.vis).length,
            };
        }""")
        print(name, vw, r)
        pg.close()
    b.close()
