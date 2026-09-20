import re

f = "index.html"
s = open(f, encoding="utf-8").read()

# 1) extract the store section (marker to marker)
m = re.search(r"<!-- store -->\n<section class=\"section prod\" id=\"store\".*?</section>\n\n<div class=\"rule\"></div>\n\n", s, re.S)
assert m, "store block not found"
store = m.group(0)
s = s[:m.start()] + s[m.end():]

# 2) re-insert store FIRST (before khinvite)
anchor = "<!-- khinvite -->"
assert anchor in s
s = s.replace(anchor, store + anchor, 1)

# 3) renumber eyebrows: store=01, khinvite=02, tvercv=03, urdrama=04, khfinder=05, biz=06, more=07
def sect_idx(slug, num):
    global s
    pat = '(id="%s" .*?data-i18n=)' % slug
    m = re.search(r'(<span class="idx">)\d+(</span>.*?id="%s")' % slug, s, re.S)
    # easier: find the idx within this section block
    i0 = s.index('id="%s"' % slug)
    i1 = s.index("</section>", i0)
    block = s[i0:i1]
    block = re.sub(r"<span class=\"idx\">\d+</span>", '<span class="idx">%s</span>' % num, block, count=1)
    s = s[:i0] + block + s[i1:]

for slug, num in [("store", "01"), ("khinvite", "02"), ("tvercv", "03"), ("urdrama", "04"), ("khfinder", "05"), ("biz", "06")]:
    sect_idx(slug, num)
# more section idx
i = s.index('id="more"')
blk = s[i:s.index("</section>", i)]
blk = re.sub(r"<span class=\"idx\">\d+</span>", '<span class="idx">07</span>', blk, count=1)
s = s[:i] + blk + s[s.index("</section>", i):]

# 4) card numbers in more section +3 -> now 08..13; currently 08..13 already? they were 08-13. keep. Add KnowItAll card numbered 14 -> but cards show product count 12 -> bump hero counter to 13
s = s.replace('data-count="12"', 'data-count="13"', 1)

# 5) add KnowItAll card (insert after KHFinder/UrPlant card; before HowToLiveBetter) and its strings
know = '''    <a class="more-card" style="--more-c:#e879a0" href="https://knowitall-kh.com" target="_blank" rel="noopener">
      <div class="more-thumb"><img src="assets/th-know.webp" alt="Sastra KH-HELPER" loading="lazy"></div>
      <div class="more-body">
        <span class="name">Sastra KH-HELPER</span>
        <span class="desc" data-i18n="r_know">All-in-one Cambodia helper — tax calculators, loan comparison, government guides and community Q&amp;A.</span>
        <div class="more-foot"><span class="num">13</span>
          <span class="go"><svg width="13" height="13" viewBox="0 0 16 16" fill="none"><path d="M3 13L13 3M13 3H6M13 3v7" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg></span></div>
      </div>
    </a>
    '''
# book card currently numbered 13 -> move it to 14 and put know at 13 position before it
i = s.index('How To Live Better')
i0 = s.rindex("<a class=\"more-card\"", 0, i)
s = s[:i0] + know + s[i0:]
# renumber the book's card foot from 13 to 14
j = s.index("How To Live Better")
j1 = s.index('<span class="num">13</span>', j)
s = s[:j1] + '<span class="num">14</span>' + s[j1 + len('<span class="num">13</span>'):]

# 6) nav: store first in links, add KH-HELPER? keep nav as is but ensure Store link exists (already) and move it up: store after biz currently; order: khinvite,tvercv,urdrama,khfinder,biz,store,more,group? Reorder: Store, khinvite, tvercv, urdrama, khfinder, Biz, more
nav_old = s[s.index('<div class="nav-links">'):s.index('</div>', s.index('<div class="nav-links">'))]
nav_new = '''<div class="nav-links">
    <a href="#store" data-i18n="nav_store" style="color:var(--gold);font-weight:700">Store</a>
    <a href="#khinvite">khinvite</a>
    <a href="#tvercv">TVERCV</a>
    <a href="#urdrama">UrDrama</a>
    <a href="#khfinder">KHFinder</a>
    <a href="#biz">Sastra Biz</a>
    <a href="#more" data-i18n="nav_more">More</a>
    '''
s = s.replace(nav_old + "</div>", nav_new + "</div>", 1)

# 7) r_know km string handled by merge script later; also add soon removal done earlier

open(f, "w", encoding="utf-8").write(s)
print("reordered. store first. know added. count:", s.count("more-card"), "cards;", "r_know" in s)
