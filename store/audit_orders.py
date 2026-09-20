import os, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
SVC = open(HOME + "/sastra-group-site/store/SVC.txt").read().strip()
REF = "swxpjxdzkwdilgkbbrnz"


def sv(method, path, body=None):
    req = urllib.request.Request("https://%s.supabase.co%s" % (REF, path), method=method)
    req.add_header("apikey", SVC)
    req.add_header("Authorization", "Bearer " + SVC)
    if body is not None:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(body).encode()
    try:
        return urllib.request.urlopen(req, timeout=40).read().decode()
    except urllib.error.HTTPError as e:
        return "HTTP%d %s" % (e.code, e.read().decode()[:100])


rows = json.loads(sv("GET", "/rest/v1/store_orders?select=id,buyer_email,status,amount,created_at&order=created_at.desc"))
for r in rows:
    print(r["status"], r["buyer_email"], r["amount"], r["created_at"][:16])
# delete test pendings (hermestest/verify/x.io/noauth/test.io/demo@sastra.store)
for r in rows:
    em = r["buyer_email"] or ""
    if r["status"] == "pending" and any(t in em for t in ["hermestest", "test.io", "x.io", "noauth", "demo@sastra", "@x.", "auth@test", "no@auth", "verify"]):
        print("del:", sv("DELETE", "/rest/v1/store_orders?id=eq." + r["id"]) or "ok")
