import re
star = chr(42) * 3
q = chr(34)
raw = open("admin.html", encoding="utf-8").read()
lines = raw.split("\n")
for i, l in enumerate(lines):
    if l.startswith("function lock()"):
        # rebuild entirely: lock = clear session pass, show login, hide dash
        lines[i] = ("function lock(){sessionStorage.removeItem(" + chr(39) + "sgadm" + chr(39) + ");PASS=" + q + q + ";"
                    + "document.getElementById(" + chr(39) + "dash" + chr(39) + ").classList.add(" + chr(39) + "hide" + chr(39) + ");"
                    + "document.getElementById(" + chr(39) + "login" + chr(39) + ").classList.remove(" + chr(39) + "hide" + chr(39) + ");}")
        print("replaced line", i)
raw = "\n".join(lines)
open("admin.html", "w", encoding="utf-8").write(raw)
print("stars left:", raw.count(star))
ms = re.findall(r"<script>(.+?)</script>", raw, re.S)
open("C:/Users/KEOVOIN-DESKTOP/AppData/Local/Temp/admin_check.js", "w", encoding="utf-8").write(ms[-1])
