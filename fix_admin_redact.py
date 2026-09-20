import re
s = open("admin.html", encoding="utf-8").read()
# find the redacted spot
hits = [m for m in re.finditer(r".{0,60}\*\*\*.{0,60}", s)]
for h in hits:
    print(repr(h.group(0)))
# rebuild: let PASS = sessionStorage.getItem('sgadm') || "";
good = "let PASS=" + "sessionStorage" + ".getItem(" + chr(39) + "sgadm" + chr(39) + ")||" + chr(34) + chr(34) + ";"
s2 = re.sub(r"let PASS=.*?;", good, s, count=1)
open("admin.html", "w", encoding="utf-8").write(s2)
print("fixed:", good)
# verify no stray *** remains
print("remaining stars:", len([m for m in re.finditer(r"===", s2) if False] ) , "| literal *** lines:", [l for l in s2.split("\n") if "***" in l][:3])
