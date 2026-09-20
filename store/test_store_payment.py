import json, urllib.request, urllib.error, os, time

HOME = os.path.expanduser("~")
K = open(os.path.join(HOME, "sastra-group-site/store/khi_anon.txt")).read().strip()
URL = "https://swxpjxdzkwdilgkbbrnz.supabase.co/functions/v1/store-payment"

def call(body):
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("apikey", K)
    req.add_header("Authorization", "Bearer " + K)
    try:
        r = urllib.request.urlopen(req, timeout=40)
        return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {}
    except Exception as e:
        return "ERR", str(e)[:120]

# 1) invalid email -> 400
print("bad email:", call({"action": "create", "product_slug": "ppt-budget-proposal", "email": "nope"}))
# 2) bad slug -> 404
print("bad slug:", call({"action": "create", "product_slug": "does-not-exist", "email": "qa.store@hermestest.dev"}))
# 3) real create -> 200 + checkout_url
s, j = call({"action": "create", "product_slug": "ppt-budget-proposal", "email": "qa.store@hermestest.dev"})
print("create:", s, {k: j.get(k) for k in ("order_id", "checkout_url", "amount", "status", "error")} if isinstance(j, dict) else j)
if isinstance(j, dict) and j.get("order_id"):
    # 4) poll status with wrong email -> 404, right email -> pending
    print("status wrong-email:", call({"action": "status", "order_id": j["order_id"], "email": "attacker@evil.com"}))
    print("status right-email:", call({"action": "status", "order_id": j["order_id"], "email": "qa.store@hermestest.dev"}))
