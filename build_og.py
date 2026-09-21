"""Regenerate OG images with the real brand lockup + temple mark."""
import os
from PIL import Image, ImageDraw, ImageFont

A = r"C:\Users\KEOVOIN-DESKTOP\sastra-group-site\assets"
LOCK = os.path.join(A, "sastra-lockup.png")
MARK = os.path.join(A, "sastra-mark.png")
KHI = os.path.join(A, "khinvite-logo.png")


def canvas(bg):
    return Image.new("RGB", (1200, 630), bg)


def center_paste(base, im, y=None, scale=1.0):
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    x = (base.width - im.width) // 2
    if y is None:
        y = (base.height - im.height) // 2
    base.paste(im, (x, y), im if im.mode == "RGBA" else None)


# --- og-landing: dark #131211, gold accent line, lockup center ---
im = canvas((19, 18, 17))
d = ImageDraw.Draw(im)
d.rectangle([0, 0, 1200, 6], fill=(217, 179, 106))
center_paste(im, Image.open(MARK), y=150, scale=0.42)
center_paste(im, Image.open(LOCK), y=378, scale=0.95)
try:
    fp = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 30)
except OSError:
    fp = ImageFont.load_default()
d.text((600, 560), "Technology with a Khmer heart", font=fp, fill=(167, 160, 150), anchor="mm")
im.save(os.path.join(A, "og-landing.png"))

# --- og-store: dark with green accent + lockup + $4.99 product feel ---
im = canvas((19, 18, 17))
d = ImageDraw.Draw(im)
d.rectangle([0, 0, 1200, 6], fill=(16, 185, 129))
center_paste(im, Image.open(LOCK), y=200, scale=0.8)
try:
    fb = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 52)
    fs = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 30)
except OSError:
    fb = fs = ImageFont.load_default()
d.text((600, 350), "Sastra Store", font=fb, fill=(240, 236, 228), anchor="mm")
d.text((600, 420), "Digital products · KHQR · instant download", font=fs, fill=(150, 165, 158), anchor="mm")
d.rounded_rectangle([490, 480, 710, 545], radius=14, outline=(16, 185, 129), width=2)
d.text((600, 512), "from $4.99", font=fs, fill=(16, 185, 129), anchor="mm")
im.save(os.path.join(A, "og-store.png"))
print("og-landing", Image.open(os.path.join(A, "og-landing.png")).size)
print("og-store", Image.open(os.path.join(A, "og-store.png")).size)
