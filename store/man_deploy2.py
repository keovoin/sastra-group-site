import os, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
TOKEN = open(os.path.join(HOME, ".supa_sastra_token.txt"), "rb").read().strip().decode()
REF = "swxpjxdzkwdilgkbbrnz"
M = "https://api.supabase.com/v1"

def man(path, method="GET", data=None, headers=None):
    req = urllib.request.Request(M + path, data=data, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        r = urllib.request.urlopen(req, timeout=120)
        b = r.read().decode()
        try:
            return r.status, json.loads(b)
        except Exception:
            return r.status, b[:300]
    except urllib.error.HTTPError as e:
        try:
            return e.code, e.read().decode()[:400]
        except Exception:
            return e.code, "?"

# 1) current functions (is store-admin deployed already?)
s, j = man(f"/projects/{REF}/functions")
have = []
if isinstance(j, list):
    have = [f.get("slug") or f.get("name") for f in j]
print("existing functions:", have)

# 2) deploy store-admin
code = open(os.path.join(HOME, "sastra-group-site/store/store-admin-compact.ts"), "rb").read()
bd = "----hermesb"
parts = [
    ("--" + bd + "\r\n").encode(),
    b'Content-Disposition: form-data; name="index.ts"; filename="index.ts"\r\nContent-Type: text/plain\r\n\r\n',
    code, b"\r\n",
    ("--" + bd + "\r\n").encode(),
    b'Content-Disposition: form-data; name="metadata"\r\nContent-Type: application/json\r\n\r\n',
    json.dumps({"entrypoint_path": "index.ts", "verify_jwt": False}).encode(), b"\r\n",
    ("--" + bd + "--\r\n").encode(),
]
s, j = man(f"/projects/{REF}/deploy/functions?slug=store-admin", "POST", b"".join(parts),
           {"Content-Type": "multipart/form-data; boundary=" + bd})
print("deploy:", s, (j.get("id") or j.get("version") if isinstance(j, dict) else str(j)[:200]))

# 3) also re-deploy store-payment from our local file (guarantees exact code matches what frontend expects)
code2 = open(os.path.join(HOME, "sastra-group-site/store/store-payment-index.ts"), "rb").read()
parts2 = [
    ("--" + bd + "\r\n").encode(),
    b'Content-Disposition: form-data; name="index.ts"; filename="index.ts"\r\nContent-Type: text/plain\r\n\r\n',
    code2, b"\r\n",
    ("--" + bd + "\r\n").encode(),
    b'Content-Disposition: form-data; name="metadata"\r\nContent-Type: application/json\r\n\r\n',
    json.dumps({"entrypoint_path": "index.ts", "verify_jwt": False}).encode(), b"\r\n",
    ("--" + bd + "--\r\n").encode(),
]
s2, j2 = man(f"/projects/{REF}/deploy/functions?slug=store-payment", "POST", b"".join(parts2),
             {"Content-Type": "multipart/form-data; boundary=" + bd})
print("redeploy payment:", s2, (j2.get("id") if isinstance(j2, dict) else str(j2)[:150]))
