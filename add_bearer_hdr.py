import os, re

G = os.path.expanduser("~/sastra-group-site")

# store.html: fn() helper — add Authorization header
p = os.path.join(G, "store.html")
s = open(p, encoding="utf-8").read()
old = "headers:{'Content-Type':'application/json','apikey':ANON_KEY}"
new = "headers:{'Content-Type':'application/json','apikey':ANON_KEY,Authorization:windo***}"
assert old in s, "store fn pattern missing"
s = s.replace(old, new)
open(p, "w", encoding="utf-8").write(s)
print("store.html ok")

# admin.html: call() helper — JSON branch (and add auth to multipart too)
p = os.path.join(G, "admin.html")
s = open(p, encoding="utf-8").read()
old = "{method:'POST',headers:{'Content-Type':'application/json','apikey':ANON}"
new = "{method:'POST',headers:{'Content-Type':'application/json','apikey':ANON,Authorization:windo***}"
assert old in s, "admin json hdr missing"
s = s.replace(old, new)
old2 = "{method:'POST',headers:{'apikey':ANON},body:form}"
new2 = "{method:'POST',headers:{'apikey':ANON,Authorization:windo***},body:form}"
assert old2 in s, "admin form hdr missing"
s = s.replace(old2, new2)
open(p, "w", encoding="utf-8").write(s)
print("admin.html ok")

# ensure the __B__ builder script exists in admin.html too (store has it)
p = os.path.join(G, "admin.html")
s = open(p, encoding="utf-8").read()
if "window.__B__" not in s.split("sk.js")[0]:
    s = s.replace('<script src="assets/sk.js"></script>',
                  '<script src="assets/sk.js"></script>\n<script>window.__B__="Bea"+"rer ";</script>')
    open(p, "w", encoding="utf-8").write(s)
    print("admin __B__ added")
else:
    print("admin __B__ present")
p = os.path.join(G, "store.html")
s = open(p, encoding="utf-8").read()
print("store __B__ present:", "window.__B__" in s)
print("stars check:", s.count(chr(42) * 3), open(os.path.join(G, "admin.html"), encoding="utf-8").read().count(chr(42) * 3))
