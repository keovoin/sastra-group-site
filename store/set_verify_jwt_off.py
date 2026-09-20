import os, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
TOKEN = open(os.path.join(HOME, ".supa_sastra_token.txt"), "rb").read().strip().decode()
REF = "swxpjxdzkwdilgkbbrnz"

def man(path, method="GET", body=None):
    req = urllib.request.Request("https://api.supabase.com/v1" + path, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    if body is not None:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(body).encode()
    try:
        r = urllib.request.urlopen(req, timeout=60)
        return r.status, r.read().decode()[:250]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:250]

# discover current config
s, j = man(f"/projects/{REF}/functions")
print("GET:", s, j[:200])

for slug in ["store-payment", "store-admin"]:
    s, t = man(f"/projects/{REF}/functions/{slug}", "PUT", {"verify_jwt": False})
    print("PUT", slug, "->", s, t[:120])
