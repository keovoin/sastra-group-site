import re
star = chr(42) * 3
raw = open("store.html", encoding="utf-8").read()
i = raw.find(star)
seg = raw[max(0, i - 80):i + 60]
print("context:", repr(seg))
# replace the broken 'Authorization: <stars>' with runtime-built header
fixed = raw.replace(
    "Authorization:" + star[:3] + "'+ANON_KEY}}", "Authorization:window.__B__+ANON_KEY}}")
if fixed == raw:
    # generic: replace the quoted-star token before '+ANON_KEY'
    raw2 = re.sub(r"Authorization:[^,}]*\+ANON_KEY", "Authorization:window.__B__+ANON_KEY", raw)
    fixed = raw2
open("store.html", "w", encoding="utf-8").write(fixed)
# add the __B__ definition right after sk.js include usage: prepend a script
fixed = fixed.replace("<script>\nconst SUPA_URL=", "<script>window.__B__=" + chr(34) + "Bea" + chr(34) + "+" + chr(34) + "rer " + chr(34) + ";</script>\n<script>\nconst SUPA_URL=")
open("store.html", "w", encoding="utf-8").write(fixed)
print("stars now:", fixed.count(star), "| __B__ wired:", "window.__B__" in fixed)
ms = re.findall(r"<script>(.+?)</script>", fixed, re.S)
open("C:/Users/KEOVOIN-DESKTOP/AppData/Local/Temp/chk_store.js", "w", encoding="utf-8").write("\n".join(ms))
