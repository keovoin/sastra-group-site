# quick sanity: are screenshots non-blank (mean luminance spread)
from PIL import Image
import os, statistics
D = r"C:\Users\KEOVOIN-DESKTOP\sastra-group-site\assets"
for f in sorted(os.listdir(D)):
    im = Image.open(os.path.join(D, f)).convert('L').resize((80, 50))
    px = list(im.getdata())
    print(f, 'mean', round(statistics.mean(px)), 'spread', round(max(px)-min(px)))
