import os, json, subprocess, urllib.request, urllib.error, time, shutil

HOME = os.path.expanduser("~")
G = os.path.join(HOME, "sastra-group-site", "store")
D = os.path.join(HOME, "sbstore")

# rebuild function dir from TRUE local files + config with verify_jwt=false
shutil.rmtree(D, ignore_errors=True)
for f in ["store-payment", "store-admin"]:
    os.makedirs(os.path.join(D, "supabase", "functions", f), exist_ok=True)
shutil.copy(os.path.join(G, "store-payment-index.ts"), os.path.join(D, "supabase", "functions", "store-payment", "index.ts"))
shutil.copy(os.path.join(G, "store-admin-compact.ts"), os.path.join(D, "supabase", "functions", "store-admin", "index.ts"))
open(os.path.join(D, "supabase", "config.toml"), "w").write(
    'project_id = "swxpjxdzkwdilgkbbrnz"\n\n[functions.store-payment]\nverify_jwt = false\n\n[functions.store-admin]\nverify_jwt = false\n')

env = dict(os.environ)
env["SUPABASE_ACCESS_TOKEN"] = open(os.path.join(HOME, ".supa_sastra_token.txt"), "rb").read().strip().decode()
env["PATH"] = "C:\\tools\\node-v24.11.1-win-x64;" + env.get("PATH", "")
r = subprocess.run(["supabase.CMD", "functions", "deploy", "store-payment", "store-admin",
                    "--project-ref", "swxpjxdzkwdilgkbbrnz", "--no-verify-jwt"],
                   cwd=D, env=env, capture_output=True, text=True, timeout=300)
print("deploy exit:", r.returncode)
print("out:", (r.stdout or "")[-300:])
print("err:", (r.stderr or "")[-200:])

K = open(os.path.join(G, "khi_anon.txt")).read().strip()


def call(fn, body, auth):
    req = urllib.request.Request("https://swxpjxdzkwdilgkbbrnz.supabase.co/functions/v1/" + fn,
                                 data=json.dumps(body).encode(), method="POST")
    req.add_header("apikey", K)
    req.add_header("Content-Type", "application/json")
    if auth:
        req.add_header("Authorization", "Bearer " + K)
    try:
        x = urllib.request.urlopen(req, timeout=60)
        return x.status, x.read().decode()[:150]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:150]


for i in range(4):
    s, t = call("store-payment", {"action": "create", "product_slug": "ppt-budget-proposal", "email": "noauth@test.io"}, False)
    print("no-auth create:", s, t)
    if s == 200:
        break
    time.sleep(20)
