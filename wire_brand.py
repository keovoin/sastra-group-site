import re

f = "index.html"
s = open(f, encoding="utf-8").read()

# 1) nav: text lockup -> real logo image
old = '<a class="nav-mark" href="#top">Sastra Solution <span class="kh">សាស្ត្រា</span></a>'
new = '<a class="nav-mark" href="#top" aria-label="Sastra"><img src="assets/sastra-lockup.png" alt="Sastra logo"></a>'
assert old in s
s = s.replace(old, new)

# 2) hero: insert mark above kicker + CSS
old = '<header class="hero" id="top">\n  <div class="hero-ghost" aria-hidden="true">សាស្ត្រា</div>\n  <div class="hero-kicker">'
new = '<header class="hero" id="top">\n  <div class="hero-ghost" aria-hidden="true">សាស្ត្រា</div>\n  <img class="hero-mark" src="assets/sastra-mark.png" alt="Sastra temple mark">\n  <div class="hero-kicker">'
assert old in s
s = s.replace(old, new)

css_anchor = ".hero-ghost{"
css = (".hero-mark{width:clamp(88px,11vw,128px);height:auto;opacity:.92;filter:drop-shadow(0 10px 30px rgba(217,179,106,.18));margin-bottom:18px;animation:rise .9s var(--ease) both .15s}\n"
       "@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:.92;transform:none}}\n"
       "[data-theme=light] .hero-mark{filter:none;opacity:1}\n")
assert css_anchor in s
s = s.replace(css_anchor, css + css_anchor, 1)

# 3) quiz card: cleaner pink-Q emblem thumbnail
s = s.replace('src="assets/th-quiz.webp"', 'src="assets/th-quizq.webp"')

# 4) light-theme nav mark contrast is fine (gold on cream) — no change.
open(f, "w", encoding="utf-8").write(s)
print("hero mark + nav lockup + quiz thumb wired")
