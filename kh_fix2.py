import json, os

G = os.path.expanduser("~/sastra-group-site")
K = json.load(open(os.path.join(G, "km_brand.json"), encoding="utf-8"))
B = K["Sastra Digital Innovation"]
C = K["© Sastra Digital Innovation. Phnom Penh, Cambodia."]
F = K["Sastra Store — by Sastra Digital Innovation, Phnom Penh"]
KICK = B + " — កម្ពុជា"

# store: repair the doubled s_foot1
p = os.path.join(G, "store.html")
s = open(p, encoding="utf-8").read()
import re
s = re.sub(r'"s_foot1":"[^"]*"', '"s_foot1":"' + F + '"', s)
open(p, "w", encoding="utf-8").write(s)

# index: kick full-KH + f_copy full-KH
p = os.path.join(G, "index.html")
s = open(p, encoding="utf-8").read()
s = re.sub(r'"kick":"[^"]*"', '"kick":"' + KICK + '"', s, count=1)
s = re.sub(r'"f_copy":"[^"]*"', '"f_copy":"' + C + '។"', s, count=1)
open(p, "w", encoding="utf-8").write(s)

# report
for f, pat in (("store.html", "s_foot1"), ("index.html", "kick"), ("index.html", "f_copy")):
    m = re.search('"' + pat + '":"([^"]*)"', open(os.path.join(G, f), encoding="utf-8").read())
    print(f, pat, "=", m.group(1))
