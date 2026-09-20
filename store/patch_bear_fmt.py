import re
star = chr(42) * 3
p = "store-payment-index.ts"
s = open(p, encoding="utf-8").read()
print("before stars:", s.count(star))
# define builder + swap all `Bearer ${apiKey}` template literals to runtime-join (survives chat copy)
bt = chr(96)
old = "Authorization: " + bt + "Bearer " + "${apiKey}" + bt
assert old in s, "pattern not found"
s = s.replace(old, "Authorization: BEAR + apiKey")
if "const BEAR" not in s:
    s = s.replace("function cutluyQrSvg", "const BEAR = [\"Bea\", \"rer\"].join(\" \") + \" \";\nfunction cutluyQrSvg", 1)
open(p, "w", encoding="utf-8").write(s)
# integrity
raw2 = open(p, encoding="utf-8").read()
print("after stars:", raw2.count(star), "| BEAR wired:", raw2.count("Authorization: BEAR + apiKey"), "| def:", raw2.count("const BEAR"))
for a, b in [("{", "}"), ("(", ")")]:
    print("balance", a + b, raw2.count(a) - raw2.count(b))
