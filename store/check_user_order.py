import os, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
K = open(HOME + "/sastra-group-site/store/khi_anon.txt").read().strip()
SVC = open(HOME + "/sastra-group-site/store/SVC.txt").read().strip()
REF = "swxpjxdzkwdilgkbbrnz"

# 1) verify the USER's pending order against CutLuy (might really be paid, modal was closed early)
rows = json.loads(urllib.request.urlopen(
    urllib.request.Request("https://%s.supabase.co/rest/v1/store_orders?select=id,buyer_email,status&buyer_email=eq.keovoin@gmail.com"
                            % REF,
                           headers={"apikey": SVC, "Authorization": "***" + SVC}), timeout=30).read().decode())
for o in rows:
    req = urllib.request.Request("https://%s.supabase.co/functions/v1/store-payment" % REF,
                                 data=json.dumps({"action": "status", "order_id": o["id"], "email": o["buyer_email"]}).encode(), method="POST")
    req.add_header("apikey", K)
    req.add_header("Authorization", "Bearer " + K)
    req.add_header("Content-Type", "application/json")
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=40).read().decode())
    except urllib.error.HTTPError as e:
        r = json.loads(e.read().decode())
    print("user order", o["id"][:8], "->", r.get("status"), ("HAS DOWNLOAD" if r.get("download_url") else ""))

# 2) delete my simulated paid test order (qa.e2e) so revenue is honest
req = urllib.request.Request("https://%s.supabase.co/rest/v1/store_orders?buyer_email=eq.qa.e2e@hermestest.dev" % REF, method="DELETE")
req.add_header("apikey", SVC)
req.add_header("Authorization", "Bearer " + SVC)
print("deleted my e2e paid test:", urllib.request.urlopen(req, timeout=30).status)
