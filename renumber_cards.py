import re

f = "index.html"
s = open(f, encoding="utf-8").read()

# remove the duplicated store card from family strip (store already has flagship section 01)
m = re.search(r'    <a class="more-card" style="--more-c:#10b981" href="store.html">.*?</a>\n', s, re.S)
if m:
    s = s[:m.start()] + s[m.end():]
    print("dup store card removed")

# family heading: dash instead of 07 (cards carry 07-13)
s = s.replace('<span class="idx">07</span> <span data-i18n="more_e">', '<span class="idx">—</span> <span data-i18n="more_e">')

# renumber card feet sequentially from 07 in document order
def renum(mo):
    return mo  # placeholder
nums = re.findall(r'<span class="num">(\d+)</span>', s)
print("feet before:", nums)
i = 7
out = s
for old in nums:
    out = out.replace('<span class="num">%s</span>' % old, '<span class="num">%02d</span>' % i, 1)
    i += 1
s = out
nums = re.findall(r'<span class="num">(\d+)</span>', s)
print("feet after:", nums)

open(f, "w", encoding="utf-8").write(s)
print("more-card count:", s.count('<a class="more-card"'))
