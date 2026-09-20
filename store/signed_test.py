import os, json, urllib.request

HOME = os.path.expanduser("~")
SVC = open(os.path.join(HOME, "sastra-group-site/store/SVC.txt")).read().strip()
REF = "swxpjxdzkwdilgkbbrnz"

req = urllib.request.Request("https://%s.supabase.co/storage/v1/object/sign/store-files/store/ppt-budget-proposal/KEOVOIN_Budget_Planner.pptx" % REF, method="POST")
req.add_header("apikey", SVC)
req.add_header("Authorization", "Bearer " + SVC)
req.add_header("Content-Type", "application/json")
req.data = json.dumps({"expiresIn": 120}).encode()
j = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())
print("raw:", json.dumps(j)[:160])
signed = j.get("signedURL") or j.get("url") or ""
if not signed.startswith("http"):
    signed = "https://%s.supabase.co" % REF + signed
signed += ("&" if "?" in signed else "?") + "apikey=" + SVC
d = urllib.request.urlopen(signed, timeout=90).read(16)
print("download first bytes:", d[:4], "PK:", d[:2] == b"PK")
