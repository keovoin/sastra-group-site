import os, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
TOKEN = open(os.path.join(HOME, ".supa_sastra_token.txt"), "rb").read().strip().decode()
REF = "swxpjxdzkwdilgkbbrnz"


def man(path):
    req = urllib.request.Request("https://api.supabase.com/v1" + path)
    req.add_header("Authorization", "Bearer " + TOKEN)
    return json.loads(urllib.request.urlopen(req, timeout=60).read().decode())


for f in man("/projects/%s/functions" % REF):
    print(f.get("slug"), "v", f.get("version"), "verify_jwt=", f.get("verify_jwt"), "ezbr=", str(f.get("ezbr_sha256"))[:16])

# what does the platform return when calling payment fn with an obviously invalid bearer (not our key)?
K = open(os.path.join(HOME, "sastra-group-site/store/khi_anon.txt")).read().strip()


def probe(authval, body):
    req = urllib.request.Request("https://swxpjxdzkwdilgkbbrnz.supabase.co/functions/v1/store-payment",
                                 data=json.dumps(body).encode(), method="POST")
    req.add_header("apikey", K)
    req.add_header("Content-Type", "application/json")
    if authval is not None:
        req.add_header("Authorization", authval)
    try:
        x = urllib.request.urlopen(req, timeout=40)
        return x.status, x.read().decode()[:100]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:100]


print("no-auth:", probe(None, {"action": "nope"}))
print("garbage-auth:", probe("Bearer garbage.token.here", {"action": "nope"}))
print("anon-auth:", probe("Bearer " + K, {"action": "nope"}))
