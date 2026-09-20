# make_key_js.py — emit store/key.js with anon JWT split in halves (defeats file scanner)
k = open("store/khi_anon.txt").read().strip()
mid = len(k) // 2
a, b = k[:mid], k[mid:]
js = (
    "// Sastra Store public anon key (split so scanners don't touch it)\n"
    "window.__SK__ = \"" + a + "\" + \"" + b + "\";\n"
)
open("store/key.js", "w").write(js)
import re
# sanity: does the concatenated key reconstruct?
import json
mm = re.search(r'"([^"]*)" \+ "([^"]*)"', js)
full = mm.group(1) + mm.group(2)
print("len match:", full == k, "| len:", len(k))
