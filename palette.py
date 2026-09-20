# extract dominant colors from each product screenshot
from PIL import Image
import os
D = r"C:\Users\KEOVOIN-DESKTOP\sastra-group-site\assets"
for f in ['khinvite.png', 'tvercv.png', 'urdrama.png', 'khfinder.png', 'biztool.png']:
    im = Image.open(os.path.join(D, f)).convert('RGB').resize((60, 40))
    cols = im.getcolors(2400)
    cols.sort(reverse=True)
    top = ['#%02x%02x%02x' % (r, g, b) for cnt, (r, g, b) in cols[:6]]
    print(f, top)
