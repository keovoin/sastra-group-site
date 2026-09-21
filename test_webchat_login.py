import http.cookiejar, urllib.request, urllib.parse, os

PW = open(os.path.expanduser("~/.webchat_pw.txt")).read().strip()
BASE = "https://trades-forms-expect-mysimon.trycloudflare.com"
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [("User-Agent", "Mozilla/5.0")]

# find the login form action by trying the documented POST endpoint
data = urllib.parse.urlencode({"username": "keovoin", "password": PW}).encode()
try:
    r = op.open(BASE + "/login", data, timeout=40)
    body = r.read().decode("utf-8", "replace")
    print("POST /login ->", r.status, "| final url:", r.geturl())
    print("cookies:", [c.name for c in cj])
except urllib.error.HTTPError as e:
    print("POST /login ->", e.code, e.read(300)[:200])

# now hit an authenticated page
for path in ("/", "/api/sessions", "/chat"):
    try:
        r = op.open(BASE + path, timeout=40)
        print(path, "->", r.status, "|", r.geturl().replace(BASE, ""), "| len", len(r.read()))
    except urllib.error.HTTPError as e:
        print(path, "->", e.code)
