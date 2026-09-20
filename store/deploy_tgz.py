import os, json, io, tarfile, gzip, urllib.request, urllib.error

HOME = os.path.expanduser("~")
TOKEN = open(os.path.join(HOME, ".supa_sastra_token.txt"), "rb").read().strip().decode()
REF = "swxpjxdzkwdilgkbbrnz"
CR = chr(13) + chr(10)


def tar_gz(slug, fn):
    code = open(os.path.join(HOME, "sastra-group-site/store", fn), "rb").read()
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        info = tarfile.TarInfo("index.ts")
        info.size = len(code)
        tf.addfile(info, io.BytesIO(code))
    return buf.getvalue()


def deploy(slug, fn):
    blob = tar_gz(slug, fn)
    bd = "----tgz" + slug
    body = (
        ("--" + bd + CR).encode()
        + ('Content-Disposition: form-data; name="bundled"; filename="%s.tar.gz"' % slug + CR).encode()
        + ("Content-Type: application/gzip" + CR + CR).encode()
        + blob
        + (CR + "--" + bd + "--" + CR).encode()
    )
    url = ("https://api.supabase.com/v1/projects/%s/functions/deploy?slug=%s&name=%s"
           "&entrypoint_path=index.ts&verify_jwt=false&import_map=false" % (REF, slug, slug))
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Content-Type", "multipart/form-data; boundary=" + bd)
    try:
        r = urllib.request.urlopen(req, timeout=180)
        return r.status, r.read().decode()[:150]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:250]


print("payment:", *deploy("store-payment", "store-payment-index.ts"))
print("admin:  ", *deploy("store-admin", "store-admin-compact.ts"))

req = urllib.request.Request("https://api.supabase.com/v1/projects/%s/functions" % REF)
req.add_header("Authorization", "Bearer " + TOKEN)
for f in json.loads(urllib.request.urlopen(req, timeout=60).read().decode()):
    print(f.get("slug"), "verify_jwt=", f.get("verify_jwt"), "v", f.get("version"), f.get("status"))
