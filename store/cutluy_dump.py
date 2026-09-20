import json, urllib.request, os

key = open(os.path.expanduser("~/cutluy_key.txt")).read().strip()
req = urllib.request.Request("https://cutluy.com/v1/payments?limit=60")
req.add_header("Authorization", "Bearer " + key)
req.add_header("User-Agent", "sastra-check/1.0")
js = json.loads(urllib.request.urlopen(req, timeout=40).read().decode())
print("type:", type(js).__name__)
if isinstance(js, dict):
    print("keys:", list(js.keys()))
    for k, v in js.items():
        if isinstance(v, list):
            print("LIST under", k, "len", len(v))
            for it in v:
                print("  ", it.get("id"), it.get("status"), it.get("amount"), it.get("reference_id"), str(it.get("created_at"))[:16])
else:
    for it in js[:25]:
        print(it.get("id"), it.get("status"), it.get("amount"), str(it.get("created_at"))[:16])
