import os, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
TOKEN = open(HOME + "/.supa_sastra_token.txt", "rb").read().strip().decode()
REF = "swxpjxdzkwdilgkbbrnz"

req = urllib.request.Request("https://api.supabase.com/v1/projects/%s/api-keys" % REF)
req.add_header("Authorization", "Bearer " + TOKEN)
keys = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())
SVC = None
for it in keys:
    if it.get("type") == "service_role":
        SVC = it["value"]
        break
assert SVC
open(HOME + "/sastra-group-site/store/SVC.txt", "w").write(SVC)
print("fresh service key saved")

def sv(method, path, body=None):
    r = urllib.request.Request("https://%s.supabase.co%s" % (REF, path), method=method)
    r.add_header("apikey", SVC)
    r.add_header("Authorization", "Bearer " + SVC)
    if body is not None:
        r.add_header("Content-Type", "application/json")
        r.data = json.dumps(body).encode()
    try:
        x = urllib.request.urlopen(r, timeout=40)
        return x.status, x.read().decode()[:120]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:120]


print("gateway rows:", sv("GET", "/rest/v1/gateway_settings?select=key")[1])
print("clean stale orders:", sv("DELETE", "/rest/v1/store_orders?status=in.(pending,expired)"))
print("orders left:", sv("GET", "/rest/v1/store_orders?select=status"))
