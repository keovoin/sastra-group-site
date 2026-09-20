import os, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
K = open(os.path.join(HOME, "sastra-group-site/store/khi_anon.txt")).read().strip()
TOKEN = open(os.path.join(HOME, ".supa_sastra_token.txt"), "rb").read().strip().decode()
REF = "swxpjxdzkwdilgkbbrnz"

req = urllib.request.Request("https://api.supabase.com/v1/projects/%s/functions/store-payment" % REF)
req.add_header("Authorization", "Bearer " + TOKEN)
j = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())
print("resp keys:", list(j.keys())[:14])
src = ""
for k in ["source", "definition"]:
    v = j.get(k)
    if isinstance(v, str):
        src = v
    elif isinstance(v, dict):
        src = v.get("source", "") or src
    if src:
        break
if not src and isinstance(j.get("metadata"), dict):
    src = j["metadata"].get("source", "")
print("source len:", len(src))
print("has Missing bearer:", "Missing bearer" in src)
print("head:", src[:180].replace("\n", " "))
import re
m = re.search(r"Missing bearer.{0,60}", src)
if m:
    print("CTX:", src[max(0, m.start()-120):m.end()].replace("\n", " "))
