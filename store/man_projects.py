import os, urllib.request, urllib.error

HOME = os.path.expanduser("~")
TOKEN = open(os.path.join(HOME, os.path.expanduser("~/.supa_sastra_token.txt"))).read().strip().strip(chr(13))
M = "https://api.supabase.com/v1"

req = urllib.request.Request(M + "/projects", headers={"Authorization": "***" + TOKEN})
try:
    r = urllib.request.urlopen(req, timeout=60)
    js = __import__("json").loads(r.read().decode())
    for p in js:
        print(p.get("ref"), "|", p.get("name"), "|", p.get("status"), "|", p.get("region"))
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:300])
