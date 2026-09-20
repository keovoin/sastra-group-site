import re

f = "index.html"
s = open(f, encoding="utf-8").read()

# 1) ticker: Store first, add KH-HELPER
s = s.replace("['Sastra Biz','#6e49e8'],['Sastra Store','#10b981']", "['Sastra Biz','#6e49e8']", 1)
if "const items=[['Sastra Store'" not in s:
    s = s.replace("const items=[['khinvite'", "const items=[['Sastra Store','#10b981'],['khinvite'", 1)
s = s.replace("['UrPlant','#65a30d']]", "['UrPlant','#65a30d'],['KH-HELPER','#e879a0']]", 1)

# 2) counter: 13 products total (6 flagship incl. store + 7 family incl. knowitall+book)
s = s.replace('data-count="14"', 'data-count="13"')
s = s.replace('data-count="12"', 'data-count="13"')

# 3) hero ghost narrower (was overflowing 320-360px viewports to the right)
s = s.replace("font-size:clamp(130px,26vw,420px);", "font-size:clamp(92px,24vw,420px);")

# 4) nav wraps on tiny screens
s = s.replace("display:flex;align-items:center;justify-content:space-between;\n  padding:18px clamp(20px,5vw,64px);",
              "display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;\n  padding:18px clamp(20px,5vw,64px);")
if "flex-wrap:wrap;align-items:center;justify-content:space-between" not in s:
    s = s.replace(".nav-tools{display:flex;align-items:center;gap:10px;margin-left:auto}",
                  ".nav-tools{display:flex;align-items:center;gap:10px;margin-left:auto;flex-wrap:wrap}")

# 5) family strip heading number: it's the 7th block
s = s.replace('<div class="eyebrow rv" style="--prod:var(--gold)"><span class="idx">07</span>',
              '<div class="eyebrow rv" style="--prod:var(--gold)"><span class="idx">07</span>')

# 6) mobile product sections: reduce dead space (shot min-width clamp) + hero meta wrap already flex
# 7) store section: add urgency pill + bigger CTA on mobile? just make cta full width on small screens
s = s.replace("</style>", "@media(max-width:600px){.cta{width:100%;justify-content:center;padding:17px 20px}.hero-meta{gap:18px 26px}.hero h1{font-size:clamp(34px,9.6vw,44px)}}\n</style>", 1)

open(f, "w", encoding="utf-8").write(s)
checks = {
 "ticker store first": "const items=[['Sastra Store'" in s,
 "KH-HELPER ticker": "KH-HELPER" in s.split("const items")[1][:600],
 "counter 13": 'data-count="13"' in s and 'data-count="12"' not in s and 'data-count="14"' not in s,
 "ghost 92px": "clamp(92px" in s,
 "nav wrap or tools wrap": ("flex-wrap:wrap;align-items:center;justify-content:space-between" in s) or ("margin-left:auto;flex-wrap:wrap" in s),
 "mobile cta rule": "@media(max-width:600px){.cta" in s,
}
print(checks)
