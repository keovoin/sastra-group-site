import os, json, mimetypes, urllib.request, urllib.error

HOME = os.path.expanduser("~")
K = open(os.path.join(HOME, "sastra-group-site/store/khi_anon.txt")).read().strip()
URL = "https://swxpjxdzkwdilgkbbrnz.supabase.co/functions/v1/store-admin"
FILE = os.path.join(HOME, "Downloads", "KEOVOIN_Budget_Planner.pptx")
PASS = "sastra-admin-2026"

data = open(FILE, "rb").read()
print("deck size:", len(data) // 1024, "KB")
bd = "----up"
def part(name, value):
    return ("--" + bd + "\r\nContent-Disposition: form-data; name=\"" + name + "\"\r\n\r\n" + value + "\r\n").encode()
fields = part("pass", PASS) + part("kind", "file") + part("slug", "ppt-budget-proposal")
filehdr = ("--" + bd + "\r\nContent-Disposition: form-data; name=\"file\"; filename=\"" + os.path.basename(FILE) + "\"\r\nContent-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation\r\n\r\n").encode()
body = fields + filehdr + data + ("\r\n--" + bd + "--\r\n").encode()

req = urllib.request.Request(URL, data=body, method="POST")
req.add_header("Content-Type", "multipart/form-data; boundary=" + bd)
req.add_header("apikey", K)
req.add_header("Authorization", "Bearer " + K)
try:
    r = urllib.request.urlopen(req, timeout=180)
    print("upload:", r.status, r.read().decode()[:300])
except urllib.error.HTTPError as e:
    print("upload HTTP", e.code, e.read().decode()[:300])
