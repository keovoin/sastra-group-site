# capture_thumbs.py — thumbnails for the 6 "rest of family" products
from playwright.sync_api import sync_playwright
from PIL import Image
import os

OUT = r"C:\Users\KEOVOIN-DESKTOP\sastra-group-site\assets"
JOBS = [
    ("th-chess", "https://kh-chess-app.vercel.app", 6000),
    ("th-card", "https://sastra-card-design.vercel.app", 7000),
    ("th-quiz", "https://elitequiz.onrender.com", 6000),
    ("th-god", "https://godeye-60ce.onrender.com", 15000),
    ("th-plant", "https://urplant-app.web.app", 6000),
    ("th-book", "https://keovoin.github.io/Sastra-HowToLiveBetter/", 5000),
]

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, url, settle in JOBS:
        ok = False
        for attempt in (1, 2):
            try:
                pg = b.new_page(viewport={"width": 1280, "height": 720})
                pg.goto(url, wait_until="domcontentloaded", timeout=70000)
                pg.wait_for_timeout(settle)
                # scroll a bit to wake lazy content, back up
                pg.evaluate("window.scrollTo(0,300)"); pg.wait_for_timeout(700)
                pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(500)
                png = os.path.join(OUT, name + ".png")
                pg.screenshot(path=png)
                im = Image.open(png).convert('RGB')
                im.save(os.path.join(OUT, name + ".webp"), 'WEBP', quality=80)
                os.remove(png)
                print("OK ", name, im.size)
                ok = True
                break
            except Exception as e:
                print("TRY", attempt, name, str(e)[:90])
        if not ok:
            print("FAIL", name)
    b.close()
