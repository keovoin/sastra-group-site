# merge_km.py — replace STR.km object in index.html with engine translations
import json, re

src = json.load(open("km_translations.json", encoding="utf-8"))
html = open("index.html", encoding="utf-8").read()

# build JS object body (keys as-is, JSON.stringify escapes quotes safely)
lines = []
for k in src:
    lines.append("  " + json.dumps(k) + ":" + json.dumps(src[k], ensure_ascii=False) + ",")
new_block = "km:{\n" + "\n".join(lines) + "\n }"

# replace the km:{...} block inside const STR={ en:{}, km:{...} };
pat = re.compile(r"km:\{.*?\n \}", re.S)
m = pat.search(html)
assert m, "km block not found"
html = html[:m.start()] + new_block + html[m.end():]
open("index.html", "w", encoding="utf-8").write(html)

# sanity: count entries in new block, check for stray <em> handling
n = len(re.findall(r'"[a-z0-9_]+":', new_block))
print("merged", n, "km strings; grp_lead has em:", "<em>" in src.get("grp_lead", ""))
print("sample:", src["h1a"], src["h1b"], src["h1c"])
