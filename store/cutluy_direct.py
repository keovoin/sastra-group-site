import json, urllib.request, urllib.error, os

key = open(os.path.expanduser("~/cutluy_key.txt")).read().strip()
req = urllib.request.Request("https://cutluy.com/v1/payments?limit=60")
req.add_header("Authorization", "Bearer " + key)
req.add_header("User-Agent", "sastra-check/1.0")
try:
    js = json.loads(urllib.request.urlopen(req, timeout=40).read().decode())
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:200])
    raise SystemExit
items = js.get("items") or js.get("data") or js or []
print("listed:", len(items))
for it in items:
    if it.get("status") == "paid":
        print("PAID:", it.get("id"), "amount", it.get("amount"), "ref", it.get("reference_id"), str(it.get("created_at"))[:16])
pend = [i for i in items if i.get("status") == "pending"]
print("pending:", len(pend))
for it in pend[:8]:
    print("  PEND:", it.get("reference_id"), str(it.get("created_at"))[:16])
