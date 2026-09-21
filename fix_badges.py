f = "index.html"
s = open(f, encoding="utf-8").read()

# nav-mark img sizing CSS (after the .nav-mark rule line)
anchor = '.nav-mark .kh{font-family:var(--font-khmer);font-size:15px;color:var(--gold);letter-spacing:.06em}'
add = '.nav-mark img{height:26px;width:auto;display:block}'
assert anchor in s and add not in s
s = s.replace(anchor, anchor + "\n" + add, 1)

# Sastra Biz logo-badge: wide lockup doesn't fit 64px square -> use temple mark
old = '<div class="logo-badge"><img src="assets/sastra-lockup.png" alt="Sastra logo"></div>'
new = '<div class="logo-badge"><img src="assets/sastra-mark.png" alt="Sastra temple mark"></div>'
assert s.count(old) == 1
s = s.replace(old, new)

open(f, "w", encoding="utf-8").write(s)
print("nav img css + biz badge = mark")
