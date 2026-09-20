import urllib.request, ssl, json

URLS = [
    ("KHChess", "https://kh-chess-app.vercel.app"),
    ("EliteQuiz", "https://elitequiz.onrender.com"),
    ("GodsEyeView", "https://godeye-60ce.onrender.com"),
    ("HowToLiveBetter", "https://keovoin.github.io/Sastra-HowToLiveBetter/"),
    ("card-design", "https://sastra-card-design.vercel.app"),
    ("sastratech", "https://www.sastratech.live"),
    ("sastraquiz", "https://sastraquiz.vercel.app"),
    ("urplant", "https://urplant.com"),
    ("khcv-alt", "https://tvercv.com"),
    ("dramabox", "https://urdrama.app"),
]
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
for name, u in URLS:
    try:
        r = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(r, timeout=12, context=ctx)
        title = ""
        raw = resp.read(4000).decode("utf-8", "ignore")
        i = raw.find("<title>")
        if i >= 0:
            title = raw[i + 7:raw.find("</title>", i)][:70]
        print("OK ", name, resp.status, u, "|", title)
    except Exception as e:
        print("ERR", name, str(e)[:80], u)
