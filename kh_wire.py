import json, os

G = os.path.expanduser("~/sastra-group-site")
K = json.load(open(os.path.join(G, "km_brand.json"), encoding="utf-8"))

BRAND = K["Sastra Digital Innovation"]                      # សាស្ត្រា នវានុវត្តន៍ឌីជីថល
COPY = K["© Sastra Digital Innovation. Phnom Penh, Cambodia."]
FOOT = K["Sastra Store — by Sastra Digital Innovation, Phnom Penh"]

OLD_STAND = "សាស្ត្រា សូលូសិន"      # សាស្ត្រា សូលូសិន (part of ក្រុមហ៊ុន សា...)
OLD_GRING = "ក្រុមហ៊ុន សាស្ត្រា សូលូសិន"


def replace_all(fname, pairs):
    p = os.path.join(G, fname)
    s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s)
    left = s.count("សូលូសិន")
    print(fname, "left:", left)


replace_all("index.html", [
    (OLD_GRING, BRAND),                      # group form collapses to brand form
    ("ក្រុមហ៊ុន " + BRAND, BRAND),          # safety: any reformed group prefix
    (OLD_STAND, BRAND),
    # hero kick + footer brand .kh now equal BRAND already
    # i18n kick was "... — កម្ពុជា" (em-dash + Cambodia): rebrand handled by generic replace
])

# verify the specific spots
s = open(os.path.join(G, "index.html"), encoding="utf-8").read()
import re
for k in ("kick", "f_copy", "f_brand"):
    m = re.search('"' + k + '":"([^"]{0,120})"', s)
    if m: print(k, "=", m.group(1)[:100])
m = re.search(r'<div class="f-brand">([^<]*)(<span class="kh">[^<]*</span>)?', s)
print("f-brand:", m.group(0)[:140] if m else "?")
m = re.search(r'"alternateName":"([^"]*)"', s)
print("altName:", m.group(1) if m else "?")

replace_all("store.html", [
    (OLD_GRING, FOOT),
    (OLD_STAND, BRAND),
])
s2 = open(os.path.join(G, "store.html"), encoding="utf-8").read()
m = re.search('"s_foot1":"([^"]{0,140})"', s2)
print("s_foot1 =", m.group(1) if m else "?")
