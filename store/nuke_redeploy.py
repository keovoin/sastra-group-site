import os, json, subprocess, urllib.request, urllib.error, time

HOME = os.path.expanduser("~")
K = open(os.path.join(HOME, "sastra-group-site/store/khi_anon.txt")).read().strip()
env = dict(os.environ)
env["SUPABASE_ACCESS_TOKEN"] = open(os.path.join(HOME, ".supa_sastra_token.txt"), "rb").read().strip().decode()
env["PATH"] = "C:\\tools\\node-v24.11.1-win-x64;" + env.get("PATH", "")
D = os.path.join(HOME, "sbstore")

# 1) hard-delete both via management API (PUT works, DELETE earlier untested with clean header)
for slug in ["store-payment", "store-admin"]:
    r = subprocess.run(["supabase.CMD", "functions", "delete", slug,
                        "--project-ref", "swxpjxdzkwdilgkbbrnz", "--yes"],
                       cwd=D, env=env, capture_output=True, text=True, timeout=120)
    print("del", slug, r.returncode, (r.stdout or r.stderr or "")[-120:].replace("\n", " "))

# confirm gone
import urllib.request as u
req = u.Request("https://api.supabase.com/v1/projects/swxpjxdzkwdilgkbbrnz/functions")
req.add_header("Authorization", "Bearer " + env["SUPABASE_ACCESS_TOKEN"])
print("remaining:", [f.get("slug") for f in json.loads(u.urlopen(req, timeout=60).read().decode())])

# 2) redeploy fresh
r = subprocess.run(["supabase.CMD", "functions", "deploy", "store-payment", "store-admin",
                    "--project-ref", "swxpjxdzkwdilgkbbrnz", "--no-verify-jwt"],
                   cwd=D, env=env, capture_output=True, text=True, timeout=300)
print("deploy exit:", r.returncode, (r.stdout or "")[-160:].replace("\n", " "), (r.stderr or "")[-120:].replace("\n", " "))


def call(fn, body, auth):
    req = urllib.request.Request("https://swxpjxdzkwdilgkbbrnz.supabase.co/functions/v1/" + fn,
                                 data=json.dumps(body).encode(), method="POST")
    req.add_header("apikey", K)
    req.add_header("Content-Type", "application/json")
    if auth:
        req.add_header("Authorization", "Bearer " + K)
    try:
        x = urllib.request.urlopen(req, timeout=60)
        return x.status, x.read().decode()[:130]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:130]


for i in range(5):
    s, t = call("store-payment", {"action": "create", "product_slug": "ppt-budget-proposal", "email": "noauth@x.io"}, False)
    print("no-auth:", s, t)
    if s == 200:
        break
    time.sleep(20)
