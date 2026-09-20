import shutil, os, re, json, urllib.request, urllib.error

HOME = os.path.expanduser("~")
G = os.path.join(HOME, "sastra-group-site")
shutil.copy(os.path.join(G, "store", "key.js"), os.path.join(G, "assets", "sk.js"))

# also verify the copy now builds the NEW key
raw = open(os.path.join(G, "assets", "sk.js"), encoding="utf-8").read()
m = re.search(r'"([^"]*)" \+ "([^"]*)"', raw)
built = m.group(1) + m.group(2)
want = open(os.path.join(G, "store", "khi_anon.txt"), encoding="utf-8").read().strip()
print("sk.js matches new key:", built == want, "| ref:", json.loads(built.split(".")[1] + "==")["ref"] if False else built.split(".")[1])
# decode ref safely
import base64
p = built.split(".")[1]
p += "=" * (-len(p) % 4)
print("sk.js project ref:", json.loads(base64.urlsafe_b64decode(p))["ref"])
