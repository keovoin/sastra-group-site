import re
raw = open("admin.html", encoding="utf-8").read()
lines = raw.split("\n")
q = chr(34)
idx = None
for i, l in enumerate(lines):
    if l.startswith("function lock()"):
        idx = i
        break
# the correct one-liner (already replaced) + leftover duplicated body lines until the one ending with '}'
# Rebuild span: lock line + the orphan continuation line(s) that follow, until a line whose rstrip ends with '}'
# Our replaced line already ends with '}' — so any following line containing dash/login again is the orphan to drop
j = idx + 1
while j < len(lines) and "document.getElementById(" in lines[j]:
    if lines[j].strip().startswith("async function"): break
    print("dropping orphan:", lines[j][:80])
    del lines[j]
    break
# lock line itself: ensure it is exactly complete
lines[idx] = ("function lock(){sessionStorage.removeItem(" + chr(39) + "sgadm" + chr(39) + ");PASS=" + q + q + ";"
              + "document.getElementById(" + chr(39) + "dash" + chr(39) + ").classList.add(" + chr(39) + "hide" + chr(39) + ");"
              + "document.getElementById(" + chr(39) + "login" + chr(39) + ").classList.remove(" + chr(39) + "hide" + chr(39) + ");}")
open("admin.html", "w", encoding="utf-8").write("\n".join(lines))
raw2 = "\n".join(lines)
print("stars:", raw2.count(chr(42) * 3))
ms = re.findall(r"<script>(.+?)</script>", raw2, re.S)
open("C:/Users/KEOVOIN-DESKTOP/AppData/Local/Temp/admin_check.js", "w", encoding="utf-8").write(ms[-1])
