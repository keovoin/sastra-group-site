import os, json, urllib.request, urllib.error, time

HOME = os.path.expanduser("~")
SVC = open(os.path.join(HOME, "sastra-group-site/store/SVC.txt")).read().strip()
K = open(os.path.join(HOME, "sastra-group-site/store/khi_anon.txt")).read().strip()
REF = "swxpjxdzkwdilgkbbrnz"
FN = "https://%s.supabase.co/functions/v1/store-payment" % REF

def req(url, key, method="GET", body=None, auth=None):
    r = urllib.request.Request(url, method=method)
    r.add_header("apikey", key)
    r.add_header("Authorization", "Bearer " + (auth or key))
    if body is not None:
        r.add_header("Content-Type", "application/json")
        r.data = json.dumps(body).encode()
    return r

def call(url, key, method="GET", body=None, auth=None):
    try:
        r = urllib.request.urlopen(req(url, key, method, body, auth), timeout=60)
        t=r.read().decode();
        return r.status, (json.loads(t) if t else {})
    except urllib.error.HTTPError as e:
        t = e.read().decode()
        try:
            return e.code, json.loads(t)
        except Exception:
            return e.code, t[:200]

EMAIL = "qa.e2e@hermestest.dev"

# 1) real create
s, j = call(FN, K, "POST", {"action": "create", "product_slug": "ppt-budget-proposal", "email": EMAIL})
print("create:", s, "order", j.get("order_id"), "checkout", j.get("checkout_url"))
oid = j["order_id"]
cid = j["cutluy_id"]

# 2) simulate payment: set order paid (same mutation the polling fn does)
s, j2 = call("https://%s.supabase.co/rest/v1/store_orders?id=eq.%s" % (REF, oid), SVC, "PATCH",
             {"status": "paid"})
print("mark paid:", s)

# 3) buyer polls status -> download url
s, j3 = call(FN, K, "POST", {"action": "status", "order_id": oid, "email": EMAIL})
print("status:", s, j3.get("status"))
dl = j3.get("download_url")
if dl:
    r = urllib.request.urlopen(dl, timeout=120)
    first = r.read(8)
    print("download:", r.status, "PK-zip:", first[:2] == b"PK", "| size head ok")
else:
    print("NO DOWNLOAD URL:", j3)

# 4) cleanup test order
s, _ = call("https://%s.supabase.co/rest/v1/store_orders?id=eq.%s" % (REF, oid), SVC, "DELETE", None)
print("cleanup test order:", s)

# 5) fix cover to absolute URL + set Khmer description
KM_DESC = "សំណុំស្លាយថវិកាសម្រាប់អាជីវកម្ម — តារាងត្រីមាស និងខែ, សង្ខេបថវិកា, ថវិកាប្រៀបធៀបការចាយពិត, ការបំបែកថវិកា, គ្រាហ្វ Sankey ហិរញ្ញវត្ថុ និងច្រើនទៀត។"
pid = "edb20f1a-8a06-4a1d-b7f2-b42168d4eb3a"
s, _ = call("https://%s.supabase.co/rest/v1/store_products?id=eq.%s" % (REF, pid), SVC, "PATCH",
            {"cover_url": "https://sastra-group.vercel.app/assets/th-ppt-cover.webp", "description_km": KM_DESC})
print("product cover/km updated:", s)
