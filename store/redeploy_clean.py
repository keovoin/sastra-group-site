import os, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
TOKEN = open(os.path.join(HOME, ".supa_sastra_token.txt"), "rb").read().strip().decode()
REF = "swxpjxdzkwdilgkbbrnz"
CR = chr(13) + chr(10)


def raw(url, method="GET", data=None, ct=None):
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    if ct:
        req.add_header("Content-Type", ct)
    if data is not None:
        req.data = data
    try:
        r = urllib.request.urlopen(req, timeout=180)
        return r.status, r.read().decode()[:220]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:220]


# try: delete + POST create with ONLY the source file part and ALL config in query string
for slug, fn in [("store-payment", "store-payment-index.ts"), ("store-admin", "store-admin-compact.ts")]:
    code = open(os.path.join(HOME, "sastra-group-site/store", fn), "rb").read()
    s1, t1 = raw("https://api.supabase.com/v1/projects/%s/functions/%s" % (REF, slug), "DELETE")
    print("delete", slug, s1, t1[:80])
    bd = "----onlysrc"
    body = (
        ("--" + bd + CR).encode()
        + ('Content-Disposition: form-data; name="%s"; filename="index.ts"' % slug + CR).encode()
        + ("application/octet-stream" + CR + CR).encode()
        + code
        + (CR + "--" + bd + "--" + CR).encode()
    )
    url = ("https://api.supabase.com/v1/projects/%s/functions/deploy?slug=%s&name=%s"
           "&entrypoint_path=index.ts&verify_jwt=false" % (REF, slug, slug))
    s2, t2 = raw(url, "POST", body, "multipart/form-data; boundary=" + bd)
    print("redeploy", slug, s2, t2[:160])

s, t = raw("https://api.supabase.com/v1/projects/%s/functions" % REF)
print(t[:400])
