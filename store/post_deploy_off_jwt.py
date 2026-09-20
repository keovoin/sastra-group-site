import os, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
TOKEN = open(os.path.join(HOME, ".supa_sastra_token.txt"), "rb").read().strip().decode()
REF = "swxpjxdzkwdilgkbbrnz"
CR = chr(13) + chr(10)


def post_deploy(slug, fn):
    code = open(os.path.join(HOME, "sastra-group-site/store", fn), "rb").read()
    bd = "----sb" + slug
    body = (
        (CR+"--" + bd + CR).encode()
        + ('Content-Disposition: form-data; name="index.ts"; filename="index.ts"' + CR).encode()
        + ("Content-Type: text/plain" + CR + CR).encode()
        + code
        + (CR + "--" + bd + CR).encode()
        + ('Content-Disposition: form-data; name="metadata"' + CR).encode()
        + ("Content-Type: application/json" + CR + CR).encode()
        + json.dumps({"entrypoint_path": "index.ts", "verify_jwt": False, "name": slug}).encode()
        + (CR + "--" + bd + "--" + CR).encode()
    )
    url = "https://api.supabase.com/v1/projects/%s/functions/deploy?slug=%s" % (REF, slug)
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Content-Type", "multipart/form-data; boundary=" + bd)
    try:
        r = urllib.request.urlopen(req, timeout=180)
        return r.status, r.read().decode()[:200]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:250]


print("payment:", *post_deploy("store-payment", "store-payment-index.ts"))
print("admin:  ", *post_deploy("store-admin", "store-admin-compact.ts"))

# verify flag
req = urllib.request.Request("https://api.supabase.com/v1/projects/%s/functions" % REF)
req.add_header("Authorization", "Bearer " + TOKEN)
import json as J
for f in J.loads(urllib.request.urlopen(req, timeout=60).read().decode()):
    print(f.get("slug"), "verify_jwt=", f.get("verify_jwt"), "status=", f.get("status"))
