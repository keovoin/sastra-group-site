import os, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
TOKEN = open(os.path.join(HOME, ".supa_sastra_token.txt"), "rb").read().strip().decode()
REF = "swxpjxdzkwdilgkbbrnz"

def man(path, method="GET", data=None, ct=None):
    req = urllib.request.Request("https://api.supabase.com/v1" + path, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    if ct:
        req.add_header("Content-Type", ct)
    if data is not None:
        req.data = data
    try:
        r = urllib.request.urlopen(req, timeout=120)
        return r.status, r.read().decode()[:200]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:250]

# try POST /functions/{slug} update shape with verify_jwt (docs: POST functions/{functionSlug})
for slug in ["store-payment", "store-admin"]:
    body = json.dumps({"verify_jwt": False}).encode()
    s, t = man("/projects/%s/functions/%s" % (REF, slug), "POST", body, "application/json")
    print("update", slug, "->", s, t[:120])
