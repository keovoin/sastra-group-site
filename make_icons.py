# make_icons.py — favicon, apple-touch, og images (dark canvas + lockup)
from PIL import Image, ImageDraw, ImageFont
import os

A = r"C:\Users\KEOVOIN-DESKTOP\sastra-group-site\assets"
LOCKUP = os.path.join(A, "sastra-lockup.png")
CANVAS = (19, 18, 17)
GOLD = (217, 179, 106)

def center_logo(im, size_frac=0.6, pad=0):
    lk = Image.open(LOCKUP).convert("RGBA")
    # logo art on transparent? lockup has white bg — check corner pixel
    corner = lk.getpixel((0, 0))
    if corner[0] > 200 and corner[1] > 200:  # white bg -> make transparent-ish: keep as rounded card
        pass
    w = int(im.width * size_frac)
    h = int(lk.height * w / lk.width)
    lk = lk.resize((w, h), Image.LANCZOS)
    if corner[0] > 200 and corner[1] > 200:
        card = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        cd.rounded_rectangle([0, 0, w + 39, h + 39], 28, fill=(247, 242, 233, 255))
        card.alpha_composite(lk, (20, 20))
        lk = card
    im.paste(lk, ((im.width - lk.width) // 2 + pad, (im.height - lk.height) // 2), lk)
    return im

# favicon 64
ic = Image.new("RGBA", (64, 64), CANVAS + (255,))
d = ImageDraw.Draw(ic)
# 'S' mark
try:
    f = ImageFont.truetype("arial.ttf", 44)
except Exception:
    f = ImageFont.load_default()
t = "ស"  # Khmer sa — falls back if font missing; draw text centered
bb = d.textbbox((0, 0), t, font=f)
d.text(((64 - (bb[2]-bb[0]))/2 - bb[0], (64 - (bb[3]-bb[1]))/2 - bb[1]), t, font=f, fill=GOLD + (255,))
ic.convert("RGB").save(os.path.join(A, "favicon.png"))
ic.save(os.path.join(A, "favicon.ico"), sizes=[(16,16),(32,32),(48,48),(64,64)])

# apple-touch 180
ic2 = Image.new("RGBA", (180, 180), CANVAS + (255,))
d2 = ImageDraw.Draw(ic2)
try:
    f2 = ImageFont.truetype("arial.ttf", 120)
except Exception:
    f2 = ImageFont.load_default()
bb = d2.textbbox((0, 0), t, font=f2)
d2.text(((180-(bb[2]-bb[0]))/2-bb[0], (180-(bb[3]-bb[1]))/2-bb[1]), t, font=f2, fill=GOLD+(255,))
ic2.convert("RGB").save(os.path.join(A, "apple-touch-icon.png"))

# og landing 1200x630
og = Image.new("RGBA", (1200, 630), CANVAS + (255,))
od = ImageDraw.Draw(og)
# subtle gold hairline frame
od.rectangle([24, 24, 1175, 605], outline=(217, 179, 106, 90), width=1)
center_logo(og, 0.44)
try:
    fh = ImageFont.truetype("arial.ttf", 64)
    fs = ImageFont.truetype("arial.ttf", 28)
except Exception:
    fh = fs = ImageFont.load_default()
ht = "Sastra Solution Group"
bb = od.textbbox((0, 0), ht, font=fh)
od.text(((1200-(bb[2]-bb[0]))/2-bb[0], 360), ht, font=fh, fill=(239,233,223,255))
st = "Technology with a Khmer heart — 12 products, one team."
bb = od.textbbox((0, 0), st, font=fs)
od.text(((1200-(bb[2]-bb[0]))/2-bb[0], 460), st, font=fs, fill=(169,159,145,255))
og.convert("RGB").save(os.path.join(A, "og-landing.png"), optimize=True)

# og store 1200x630
ogs = og.copy()
ds = ImageDraw.Draw(ogs)
try:
    fb = ImageFont.truetype("arial.ttf", 56)
except Exception:
    fb = ImageFont.load_default()
t2 = "Sastra Store"
bb = ds.textbbox((0, 0), t2, font=fb)
ds.rectangle([0, 520, 1200, 630], fill=CANVAS + (255,))
ds.text(((1200-(bb[2]-bb[0]))/2-bb[0], 540), t2, font=fb, fill=GOLD + (255,))
ogs.convert("RGB").save(os.path.join(A, "og-store.png"), optimize=True)

for f in ["favicon.png", "favicon.ico", "apple-touch-icon.png", "og-landing.png", "og-store.png"]:
    print(f, os.path.getsize(os.path.join(A, f)) // 1024, "KB")
