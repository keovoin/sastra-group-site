import os, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
K = open(os.path.join(HOME, "sastra-group-site/store/khi_anon.txt")).read().strip()
URL = "https://swxpjxdzkwdilgkbbrnz.supabase.co/functions/v1/store-admin"

def call(body):
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("apikey", K)
    req.add_header("Authorization", "Bearer " + K)
    try:
        r = urllib.request.urlopen(req, timeout=40)
        return r.status, r.read().decode()[:400]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
    except Exception as e:
        return "ERR", str(e)[:120]

print("login wrong pass:", call({"action": "login", "pass": "wrong"}))
print("login right pass:", call({"action": "login", "pass": "sastra-admin-2026"}))
print("list:", call({"action": "list", "pass": "sastra-admin-2026"})[:1] if False else call({"action": "list", "pass": "sastra-admin-2026"}))
