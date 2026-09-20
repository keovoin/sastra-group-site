import os, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
SVC = open(HOME + "/sastra-group-site/store/SVC.txt").read().strip()
REF = "swxpjxdzkwdilgkbbrnz"

# 1) get the CutLuy key from gateway_settings (service role)
rows = json.loads(urllib.request.urlopen(urllib.request.Request(
    "https://%s.supabase.co/rest/v1/gateway_settings?key=eq.cutluy_api_key&select=value" % REF,
    headers={"apikey": SVC, "Authorization": "***" + SVC}), timeout=30).read().decode())
key = rows[0]["value"]
print("key len:", len(key))

# 2) list payments from CutLuy, find paid ones today
req = urllib.request.Request("https://cutluy.com/v1/payments?limit=50")
req.add_header("Authorization", "Bearer " + key)
req.add_header("User-Agent", "sastra-check/1.0")
try:
    js = json.loads(urllib.request.urlopen(req, timeout=40).read().decode())
except urllib.error.HTTPError as e:
    print("cutluy list:", e.code, e.read().decode()[:200]); raise SystemExit
items = js.get("items") or js.get("data") or js if isinstance(js, list) else js.get("items", [])
print("payments:", len(items))
for it in items:
    st = it.get("status")
    if st == "paid":
        print("PAID:", it.get("id"), it.get("amount"), it.get("reference_id"), (it.get("created_at") or "")[:16], it.get("checkout_url"))
