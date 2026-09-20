import os, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
TOKEN = open(os.path.join(HOME, ".supa_sastra_token.txt"), "rb").read().strip().decode()
REF = "swxpjxdzkwdilgkbbrnz"

def man(path):
    req = urllib.request.Request("https://api.supabase.com/v1" + path)
    req.add_header("Authorization", "Bearer " + TOKEN)
    try:
        r = urllib.request.urlopen(req, timeout=60)
        return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:150]

for p in [
    "/projects/%s/api-keys" % REF,
    "/projects/%s/service-keys" % REF,
    "/projects/%s/keys" % REF,
]:
    s, j = man(p)
    print(p.split("/")[-1], "->", s)
    if s == 200:
        items = j if isinstance(j, list) else j.get("keys", [])
        for it in items:
            nm = str(it.get("name", it.get("type", "?")))
            val = it.get("value") or it.get("api_key") or it.get("secret") or ""
            print("   ", nm, "type=", it.get("type"), "len=", len(val))
            if val and ("service" in nm.lower() or it.get("type") == "service_role"):
                open(os.path.join(HOME, "sastra-group-site/store/SVC.txt"), "w").write(val)
                print("   saved service key")
        break
