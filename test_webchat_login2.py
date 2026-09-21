import http.cookiejar, urllib.request, urllib.parse, json, os

PW = open(os.path.expanduser("~/.webchat_pw.txt")).read().strip()
BASE = "https://trades-forms-expect-mysimon.trycloudflare.com"
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [("User-Agent", "Mozilla/5.0")]

body = json.dumps({"username": "keovoin", "password": PW}).encode()
req = urllib.request.Request(BASE + "/auth/password-login", data=body, method="POST")
req.add_header("Content-Type", "application/json")
try:
    r = op.open(req, timeout=40)
    print("login ->", r.status, r.read(200)[:150])
except urllib.error.HTTPError as e:
    print("login ->", e.code, e.read(200))
print("cookies:", [c.name for c in cj])

for path in ("/", "/chat"):
    try:
        r = op.open(BASE + path, timeout=40)
        print(path, "->", r.status, "| url:", r.geturl().replace(BASE, ""))
    except urllib.error.HTTPError as e:
        print(path, "->", e.code)
