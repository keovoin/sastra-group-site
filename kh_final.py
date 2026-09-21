"""Apply Khmer brand to the SA visible default text + verify all spots."""
import json, os, re

G = os.path.expanduser("~/sastra-group-site")
K = json.load(open(os.path.join(G, "km_brand.json"), encoding="utf-8"))
B = K["Sastra Digital Innovation"]
COPY = K["© Sastra Digital Innovation. Phnom Penh, Cambodia."]

p = os.path.join(G, "index.html")
s = open(p, encoding="utf-8").read()
s = s.replace('© Sastra Digital Innovation. Phnom Penh, Cambodia.</span>', COPY + '។</span>')
open(p, "w", encoding="utf-8").write(s)

# full audit
pats = {
    "title": r"<title>([^<]*)</title>",
    "og:site_name": r'og:site_name" content="([^"]*)"',
    "desc": r'name="description" content="([^"]{0,70})',
    "ld_name": r'"Organization","name":"([^"]*)"',
    "altName": r'"alternateName":"([^"]*)"',
    "kick_default": r'data-i18n="kick">([^<]*)<',
    "kick_i18n": r'"kick":"([^"]*)"',
    "fbrand_visible": r'<div class="f-brand">([^<]*)<',
    "fbrand_kh": r'<div class="f-brand">[^<]*<span class="kh">([^<]*)</span>',
    "fcopy_visible": r'data-i18n="f_copy">([^<]*)<',
    "fcopy_i18n": r'"f_copy":"([^"]*)"',
}
ok = True
for name, pat in pats.items():
    m = re.search(pat, s)
    v = m.group(1) if m else "?"
    bad = ("Solution" in v) or ("សូលូសិន" in v)
    ok = ok and not bad
    print(("✗" if bad else "✓"), name, "=", v[:80])
print("brand:", B)
print("ALL CLEAN" if ok else "RESIDUE LEFT")
