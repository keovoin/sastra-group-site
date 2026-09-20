# compress screenshots for web (webp q78, max 1400w)
from PIL import Image
import os
D = r"C:\Users\KEOVOIN-DESKTOP\sastra-group-site\assets"
for f in ['khinvite.png', 'tvercv.png', 'urdrama.png', 'khfinder.png', 'biztool.png']:
    im = Image.open(os.path.join(D, f)).convert('RGB')
    if im.width > 1400:
        im = im.resize((1400, int(im.height * 1400 / im.width)), Image.LANCZOS)
    out = os.path.join(D, f.replace('.png', '.webp'))
    im.save(out, 'WEBP', quality=80)
    print(out, round(os.path.getsize(out) / 1024), 'KB')
