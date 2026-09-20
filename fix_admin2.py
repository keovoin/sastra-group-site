import re
raw = open("admin.html", "rb").read().decode("utf-8")
star = chr(42) * 3
n = raw.count(star)
print("file contains triple-star:", n)
if n:
    # statement 1: let PASS=***  ->  let PASS=sess...()||""
    raw = re.sub(r"let PASS=.*?;", 'let PASS=' + "sessionStorage.getItem('sgadm')" + "||" + chr(34)*2 + ";", raw, count=1)
    # statement 2 in lock(): PASS=*** -> PASS=''
    raw = re.sub(r"PASS=.*?(?=document)", "PASS=" + chr(34)*2 + ";", raw, count=1)
    open("admin.html", "w", encoding="utf-8").write(raw)
    print("after fix, triple-star:", raw.count(star))
# extract inline script, sanity-parse braces
m = re.search(r"<script>\n(.*?)\n</script>", raw, re.S)
js = m.group(1)
print("js len:", len(js))
bal = 0
for ch in js:
    if ch == "{": bal += 1
    elif ch == "}": bal -= 1
print("brace balance:", bal)
open("C:/Users/KEOVOIN-DESKTOP/AppData/Local/Temp/admin_check.js", "w", encoding="utf-8").write(js)
