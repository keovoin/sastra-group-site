import os, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
TOKEN = open(os.path.join(HOME, ".supa_sastra_token.txt"), "rb").read().strip().decode()
REF = "swxpjxdzkwdilgkbbrnz"

# service-role key via management API
req = urllib.request.Request("https://api.supabase.com/v1/projects/%s/api-keys?latest=true" % REF)
req.add_header("Authorization", "Bearer " + TOKEN)
try:
    r = urllib.request.urlopen(req, timeout=60)
    keys = json.loads(r.read().decode())
    svc = None
    for it in keys:
        name = (it.get("name") or "") + (it.get("service") or "")
        if "service" in name.lower():
            svc = it.get("value") or it.get("api_key")
    print("found service key:", bool(svc))
except urllib.error.HTTPError as e:
    print("api-keys HTTP", e.code, e.read().decode()[:200]); svc = None

if svc:
    # list with service role
    req = urllib.request.Request("https://%s.supabase.co/storage/v1/object/list/store-files" % REF,
                                 data=json.dumps({"prefix": "store/ppt-budget-proposal/", "limit": 10}).encode(), method="POST")
    req.add_header("apikey", svc)
    req.add_header("Authorization", "Bearer " + svc)
    req.add_header("Content-Type", "application/json")
    print("list:", urllib.request.urlopen(req, timeout=30).read().decode()[:300])
    # create signed url directly = same call store-payment makes after paid
    req = urllib.request.Request("https://%s.supabase.co/storage/v1/object/sign/store-files/store/ppt-budget-proposal/KEOVOIN_Budget_Planner.pptx" % REF,
                                 data=json.dumps({"expiresIn": 60}).encode(), method="POST")
    req.add_header("apikey", svc)
    req.add_header("Authorization", "Bearer " + svc)
    req.add_header("Content-Type", "application/json")
    j = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
    signed = j.get("signedURL")
    signed = signed if signed.startswith("http") else "https://%s.supabase.co" % REF + signed
    print("signed url ok:", "token=" in signed)
    # actually download first bytes
    d = urllib.request.urlopen(signed, timeout=40).read(4)
    print("magic bytes:", d[:2], "= PPTX zip PK:", d[:2] == b"PK")
    open(os.path.join(HOME, "sastra-group-site/store/SVC.txt"), "w").write(svc)
