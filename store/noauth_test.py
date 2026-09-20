import os, json, urllib.request, urllib.error, time, subprocess

HOME = os.path.expanduser("~")
K = open(os.path.join(HOME, "sastra-group-site/store/khi_anon.txt")).read().strip()
R = "https://swxpjxdzkwdilgkbbrnz.supabase.co/functions/v1"


def call(fn, body, auth):
    req = urllib.request.Request(R + "/" + fn, data=json.dumps(body).encode(), method="POST")
    req.add_header("apikey", K)
    req.add_header("Content-Type", "application/json")
    if auth:
        req.add_header("Authorization", "Bearer " + K)
    try:
        r = urllib.request.urlopen(req, timeout=40)
        return r.status, r.read().decode()[:120]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:120]


print("no-auth payment create:", call("store-payment", {"action": "create", "product_slug": "ppt-budget-proposal", "email": "z@z.io"}, False))
print("no-auth admin login  :", call("store-admin", {"action": "login", "pass": "sastra-admin-2026"}, False))
print("auth   payment bad-mail:", call("store-payment", {"action": "create", "product_slug": "ppt-budget-proposal", "email": "bad"}, True))
