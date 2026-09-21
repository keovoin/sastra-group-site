"""Build real-brand assets from user's logo images into the site."""
import os
from collections import deque
from PIL import Image, ImageDraw

CACHE = r"C:\Users\KEOVOIN-DESKTOP\AppData\Local\hermes\profiles\video-extractor-agent\cache\images"
LOCKUP = os.path.join(CACHE, "img_46457213372c.jpg")   # SASTRA + mark
MARK = os.path.join(CACHE, "img_45d88470435f.jpg")     # temple mark only
QUIZ = os.path.join(CACHE, "img_d8055b14c52c.jpg")     # Sastra Quiz full
QUIZQ = os.path.join(CACHE, "img_0c6f6d024f7c.jpg")    # pink Q mark
A = r"C:\Users\KEOVOIN-DESKTOP\sastra-group-site\assets"


def cut_bg(im, tol=38):
    """Flood-fill near-background from edges -> transparent. Keeps interior whites."""
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    bg = px[2, 2][:3]
    seen = [[False] * w for _ in range(h)]
    q = deque()

    def push(x, y):
        if 0 <= x < w and 0 <= y < h and not seen[y][x]:
            seen[y][x] = True
            q.append((x, y))

    for x in range(w):
        push(x, 0); push(x, h - 1)
    for y in range(h):
        push(0, y); push(w - 1, y)
    while q:
        x, y = q.popleft()
        r, g, b = px[y and x or x, y][:3] if False else px[x, y][:3]
        if abs(r - bg[0]) <= tol and abs(g - bg[1]) <= tol and abs(b - bg[2]) <= tol:
            px[x, y] = (r, g, b, 0)
            push(x + 1, y); push(x - 1, y); push(x, y + 1); push(x, y - 1)
    return im


def trim(im, pad=12):
    b = im.getbbox()
    im = im.crop(b)
    return im


# --- 1) mark (temple) transparent, square ---
mk = trim(cut_bg(Image.open(MARK).resize((700, 700), Image.LANCZOS)))
side = max(mk.size)
sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
sq.paste(mk, ((side - mk.width) // 2, (side - mk.height) // 2), mk)
sq.save(os.path.join(A, "sastra-mark.png"))

# --- 2) lockup transparent (keep as wide) ---
lk = trim(cut_bg(Image.open(LOCKUP)))
lk.save(os.path.join(A, "sastra-lockup.png"))

# --- 3) favicons from mark ---
def icon(size, name):
    im = sq.copy()
    padim = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    r = im.resize((int(size * 0.9), int(size * 0.9)), Image.LANCZOS)
    padim.paste(r, ((size - r.width) // 2, (size - r.height) // 2), r)
    padim.save(os.path.join(A, name))
    return name

icon(32, "favicon.png")
icon(180, "apple-touch-icon.png")
icon(512, "icon-512.png")
# ico (32)
Image.open(os.path.join(A, "favicon.png")).save(os.path.join(A, "favicon.ico"), sizes=[(32, 32)])

# --- 4) maskable: mark on canvas-dark square (centered 60%) ---
mask = Image.new("RGBA", (512, 512), (19, 18, 17, 255))
r = sq.resize((300, 300), Image.LANCZOS)
mask.paste(r, (106, 106), r)
mask.save(os.path.join(A, "icon-512-maskable.png"))

# --- 5) quiz thumbnails (16:9 800x450) ---
for src, out in ((QUIZ, "th-quiz.webp"), (QUIZQ, "th-quizq.webp")):
    im = Image.open(src).convert("RGB")
    cv = Image.new("RGB", (800, 450), (247, 242, 233))
    tg = Image.open(src).convert("RGB")
    t = cut_bg(tg.resize((min(560, tg.width), int(tg.height * min(560, tg.width) / tg.width)), Image.LANCZOS))
    t = trim(t)
    fit = min(640 / t.width, 380 / t.height, 1.0)
    t = t.resize((int(t.width * fit), int(t.height * fit)), Image.LANCZOS)
    cv.paste(t, ((800 - t.width) // 2, (450 - t.height) // 2), t)
    cv.save(os.path.join(A, out), quality=88)

for f in ["sastra-mark.png", "sastra-lockup.png", "favicon.png", "apple-touch-icon.png",
          "icon-512.png", "icon-512-maskable.png", "th-quiz.webp", "th-quizq.webp"]:
    print(f, Image.open(os.path.join(A, f)).size)
