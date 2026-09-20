import re

f = "index.html"
s = open(f, encoding="utf-8").read()

# fix hero counter: '12' followed by '(space or newline + <' per original file
s = s.replace('data-count="12"', 'data-count="13"', 1)

# add KnowItAll card BEFORE the book card (make book=14th card? no—book keeps 13, know gets its own 12/13 chain):
# current cards nums: chess08 card09 quiz10 god11 plant12 book13 -> we want book13, add know as 12? no plant is 12.
# Simplest correct: products are: 5 flagship + store + chess + card-design + quiz + godeye + urplant + knowitall + book = 13
# Family strip shows 08..13 for 6 items (chess,card,quiz,god,plant,book) -> insert know between plant and book,
# renumber: plant 11? keep order simple: chess08, card09, quiz10, god11, plant12, know13, book14. Strip nums can
# exceed the "13 products" (book included in the 13) -> then count="14"? Count = 7 flagship-ish? 
# FINAL: hero data-count = 13 (products incl. store & book & knowitall). Family card nums: chess 08 .. book 14 is fine
# (they're just list numbers, not "product N of 13" semantics).
i = s.index("How To Live Better")
i0 = s.rindex('<a class="more-card"', 0, i)
KNOW = '''    <a class="more-card" style="--more-c:#e879a0" href="https://knowitall-kh.com" target="_blank" rel="noopener">
      <div class="more-thumb"><img src="assets/th-know.webp" alt="Sastra KH-HELPER" loading="lazy"></div>
      <div class="more-body">
        <span class="name">Sastra KH-HELPER</span>
        <span class="desc" data-i18n="r_know">All-in-one Cambodia helper — tax calculators, loan comparison, government guides and community Q&amp;A.</span>
        <div class="more-foot"><span class="num">13</span>
          <span class="go"><svg width="13" height="13" viewBox="0 0 16 16" fill="none"><path d="M3 13L13 3M13 3H6M13 3v7" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg></span></div>
      </div>
    </a>
'''
s = s[:i0] + KNOW + s[i0:]
# book 13 -> 14
j = s.index("How To Live Better")
j1 = s.index('<span class="num">13</span>', j)
s = s[:j1] + '<span class="num">14</span>' + s[j1 + len('<span class="num">13</span>'):]

# store CTA on mobile: add a store highlight band right under hero-kicker? Instead add gold pill in nav (done via style)
# ticker first item = store
s = s.replace("const items=[['khinvite','#d9b36a']", "const items=[['Sastra Store','#10b981'],['khinvite','#d9b36a']")
s = s.replace("['Sastra Biz','#6e49e8'],['Sastra Store','#10b981']", "['Sastra Biz','#6e49e8']")
# knowitall in ticker
s = s.replace("['UrPlant','#65a30d']]", "['UrPlant','#65a30d'],['KH-HELPER','#e879a0']]")

open(f, "w", encoding="utf-8").write(s)
print("know card added; counter:", s.count("more-card"), "refs;", "data-count=\"13\"" in s)
