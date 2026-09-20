import re
raw = open("admin.html", encoding="utf-8").read()
star = chr(42) * 3
# show all remaining triple-star lines
bad = [l for l in raw.split("\n") if star in l]
print("triple-star lines:", len(bad))
for l in bad: print("  ", l[:100])
# extract the last inline script block regardless of newlines
ms = re.findall(r"<script>(.+?)</script>", raw, re.S)
print("inline script blocks:", len(ms))
js = ms[-1] if ms else ""
open("C:/Users/KEOVOIN-DESKTOP/AppData/Local/Temp/admin_check.js", "w", encoding="utf-8").write(js)
print("js len:", len(js))
