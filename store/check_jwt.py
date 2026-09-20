import os, json, urllib.request

HOME = os.path.expanduser("~")
TOKEN = open(os.path.join(HOME, ".supa_sastra_token.txt"), "rb").read().strip().decode()
REF = "swxpjxdzkwdilgkbbrnz"
req = urllib.request.Request("https://api.supabase.com/v1/projects/%s/functions" % REF)
req.add_header("Authorization", "Bearer " + TOKEN)
for f in json.loads(urllib.request.urlopen(req, timeout=60).read().decode()):
    print(f.get("slug"), "verify_jwt=", f.get("verify_jwt"), "v", f.get("version"), f.get("status"))
