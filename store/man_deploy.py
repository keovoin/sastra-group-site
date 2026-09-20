import json, os, urllib.request, urllib.error

HOME = os.path.expanduser("~")
TOKEN = open(os.path.join(HOME, os.path.expanduser("~/.supa_sastra_token.txt"))).read().strip().strip(chr(13))
REF = "swxpjxdzkwdilgkbbrnz"
M = "https://api.supabase.com/v1"

def man(path, method="GET", data=None, headers=None):
    req = urllib.request.Request(M + path, data=data, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        r = urllib.request.urlopen(req, timeout=90)
        body = r.read().decode()
        try:
            return r.status, json.loads(body)
        except Exception:
            return r.status, body[:300]
    except urllib.error.HTTPError as e:
        try:
            return e.code, e.read().decode()[:400]
        except Exception:
            return e.code, "?"

# ---- 1) deploy store-admin ----
code = open(os.path.join(HOME, "sastra-group-site/store/store-admin-compact.ts"), "rb").read()
bd = "----hermes"
parts = []
parts.append(("--" + bd + "\r\n").encode())
parts.append(b'Content-Disposition: form-data; name="index.ts"; filename="index.ts"\r\nContent-Type: text/plain\r\n\r\n')
parts.append(code)
parts.append(b"\r\n")
parts.append(("--" + bd + "\r\n").encode())
parts.append(b'Content-Disposition: form-data; name="metadata"\r\nContent-Type: application/json\r\n\r\n')
parts.append(json.dumps({"entrypoint_path": "index.ts", "verify_jwt": False}).encode())
parts.append(b"\r\n")
parts.append(("--" + bd + "--\r\n").encode())
body = b"".join(parts)
s, j = man(f"/projects/{REF}/deploy/functions?slug=store-admin", "POST", body,
           {"Content-Type": "multipart/form-data; boundary=" + bd})
print("deploy store-admin:", s, (j.get("id") if isinstance(j, dict) else str(j)[:200]))

# ---- 2) confirm both functions exist ----
s, j = man(f"/projects/{REF}/functions")
if isinstance(j, list):
    print("functions:", [(f.get("slug") or f.get("name"), f.get("status")) for f in j])
else:
    print("list:", s, str(j)[:200])
