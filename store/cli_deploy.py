import os, subprocess, shutil, io

HOME = os.path.expanduser("~")
G = os.path.join(HOME, "sastra-group-site", "store")
token = open(os.path.join(HOME, ".supa_sastra_token.txt"), "rb").read().strip().decode()
PROJ = "swxpjxdzkwdilgkbbrnz"

D = os.path.join(HOME, "sbstore")
shutil.rmtree(D, ignore_errors=True)
for f in ["store-payment", "store-admin"]:
    os.makedirs(os.path.join(D, "supabase", "functions", f), exist_ok=True)
shutil.copy(os.path.join(G, "store-payment-index.ts"), os.path.join(D, "supabase", "functions", "store-payment", "index.ts"))
shutil.copy(os.path.join(G, "store-admin-compact.ts"), os.path.join(D, "supabase", "functions", "store-admin", "index.ts"))
cfg = 'project_id = "%s"\n\n[functions.store-payment]\nverify_jwt = false\n\n[functions.store-admin]\nverify_jwt = false\n' % PROJ
open(os.path.join(D, "supabase", "config.toml"), "w").write(cfg)

env = dict(os.environ)
env["SUPABASE_ACCESS_TOKEN"] = token
env["PATH"] = "C:\\tools\\node-v24.11.1-win-x64;" + env.get("PATH", "")

r = subprocess.run(
    ["supabase.CMD", "functions", "deploy", "store-payment", "store-admin", "--project-ref", PROJ, "--no-verify-jwt"],
    cwd=D, env=env, capture_output=True, text=True, shell=False, timeout=240)
print("exit:", r.returncode)
print((r.stdout or "")[-600:])
print((r.stderr or "")[-300:])
