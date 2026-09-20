import re
star = chr(42) * 3
raw = open("admin.html", encoding="utf-8").read()
print("triple-star occurrences:", raw.count(star))
for ln, l in enumerate(raw.split("\n"), 1):
    if star in l:
        print("L%d:" % ln, l.strip()[:140])
ms = re.findall(r"<script>(.+?)</script>", raw, re.S)
open("C:/Users/KEOVOIN-DESKTOP/AppData/Local/Temp/admin_check.js", "w", encoding="utf-8").write(ms[-1])
bal = 0
for ch in ms[-1]:
    if ch == "{": bal += 1
    elif ch == "}": bal -= 1
print("brace balance:", bal)
