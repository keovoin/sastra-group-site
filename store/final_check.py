import os, json, urllib.request

HOME = os.path.expanduser("~")
SVC = open(os.path.join(HOME, "sastra-group-site/store/SVC.txt")).read().strip()
REF = "swxpjxdzkwdilgkbbrnz"

def sv(method, path, body=None):
    req = urllib.request.Request("https://%s.supabase.co%s" % (REF, path), method=method)
    req.add_header("apikey", SVC)
    req.add_header("Authorization", "Bearer " + SVC)
    if body is not None:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(body).encode()
    return urllib.request.urlopen(req, timeout=60)

# 1) file really in the private bucket?
r = sv("POST", "/storage/v1/object/list/store-files", {"prefix": "store/ppt-budget-proposal/", "limit": 10})
rows = json.loads(r.read().decode())
print("bucket file:", rows)

# 2) signed URL + first bytes = valid PPTX?
r = sv("POST", "/storage/v1/object/sign/store-files/store/ppt-budget-proposal/KEOVOIN_Budget_Planner.pptx", {"expiresIn": 120})
j = json.loads(r.read().decode())
signed = j.get("signedURL")
signed = signed if signed.startswith("http") else "https://%s.supabase.co" % REF + signed
d = urllib.request.urlopen(signed, timeout=60).read(8)
print("signed download first bytes:", d[:4], "PK(=pptx zip):", d[:2] == b"PK")

# 3) cover: does store cover_url resolve on the live site?
import urllib.error
try:
    s = urllib.request.urlopen("https://sastra-group.vercel.app/assets/th-ppt-cover.webp", timeout=30).status
    print("cover on vercel:", s)
except Exception as e:
    print("cover:", e)
print("ALL CHECKS DONE")
