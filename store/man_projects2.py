import os, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
TOKEN = open(os.path.join(HOME, ".supa_sastra_token.txt"), "rb").read().strip().decode()
print("token len:", len(TOKEN), "| repr head:", repr(TOKEN[:8]), "| repr tail:", repr(TOKEN[-4:]))
req = urllib.request.Request("https://api.supabase.com/v1/projects")
req.add_header("Authorization", "Bearer " + TOKEN)
try:
    r = urllib.request.urlopen(req, timeout=60)
    js = json.loads(r.read().decode())
    print("OK projects:", len(js))
    for p in js:
        print(p.get("ref"), "|", p.get("name"))
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:200])
