import os, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
TOKEN = open(os.path.join(HOME, ".supa_sastra_token.txt"), "rb").read().strip().decode()
REF = "swxpjxdzkwdilgkbbrnz"
CR = chr(13) + chr(10)


def raw(path, method="GET", data=None, ct=None):
    req = urllib.request.Request("https://api.supabase.com/v1" + path, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    if ct:
        req.add_header("Content-Type", ct)
    if data is not None:
        req.data = data
    try:
        r = urllib.request.urlopen(req, timeout=120)
        return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:250]


def build_body(code, slug):
    bd = "----h" + slug
    return ((CR + "--" + bd + CR).encode()
            + ('Content-Disposition: form-data; name="index.ts"; filename="index.ts"' + CR).encode()
            + ("Content-Type: text/plain" + CR + CR).encode()
            + code
            + (CR + "--" + bd + CR).encode()
            + ('Content-Disposition: form-data; name="metadata"' + CR).encode()
            + ("Content-Type: application/json" + CR + CR).encode()
            + json.dumps({"entrypoint_path": "index.ts", "verify_jwt": False, "name": slug}).encode()
            + (CR + "--" + bd + "--" + CR).encode()), "multipart/form-data; boundary=" + bd


for slug, fn in [("store-payment", "store-payment-index.ts"),
                 ("store-admin", "store-admin-compact.ts")]:
    code = open(os.path.join(HOME, "sastra-group-site/store", fn), "rb").read()
    body, ct = build_body(code, slug)
    tried = []
    for path, method in [
        ("/projects/%s/functions/deploy?slug=%s" % (REF, slug), "PATCH"),
        ("/projects/%s/functions/deploy?slug=%s" % (REF, slug), "PUT"),
        ("/projects/%s/functions/deploy" % REF, "PUT"),
        ("/projects/%s/functions/%s" % (REF, slug), "PATCH"),
    ]:
        s, t = raw(path, method, body, ct)
        tried.append((method, path.split("/v1")[-1] if "/v1" in path else path[-30:], s, t[:80]))
        if s in (200, 201):
            break
    for m, p, s, t in tried:
        print(m, p, "->", s, t)
