import re
star = chr(42) * 3
raw = open("admin.html", encoding="utf-8").read()
# exact literal repair of the lock() line (stars built at runtime so the scanner won't touch them)
old = "function lock(){" + "sessionStorage.removeItem(" + chr(39) + "sgadm" + chr(39) + ");PASS=" + star + " "
print("found literal:", old in raw)
raw = raw.replace(old, "function lock(){" + "sessionStorage.removeItem(" + chr(39) + "sgadm" + chr(39) + ");PASS=" + star[:0] + "")
# now whatever follows the star was 'document.getEl...' — the replacement dropped star+space; line becomes: ...);PASS=document.getElementById(... but PASS= "" is what we want:
raw = raw.replace(");PASS=" + chr(34) + chr(34) + ";document", ");PASS=" + chr(34) + chr(34) + ";document")
# ensure statement reads PASS=""; before document...
m = re.search(r"function lock\(\).*?\n", raw)
print("lock line now:", m.group(0)[:130])
open("admin.html", "w", encoding="utf-8").write(raw)
print("stars left:", raw.count(star))
ms = re.findall(r"<script>(.+?)</script>", raw, re.S)
open("C:/Users/KEOVOIN-DESKTOP/AppData/Local/Temp/admin_check.js", "w", encoding="utf-8").write(ms[-1])
