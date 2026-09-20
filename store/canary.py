import os, json, urllib.request, urllib.error, subprocess, shutil

HOME = os.path.expanduser("~")

os.makedirs(HOME + "/sbstore/supabase/functions/canary", exist_ok=True)
open(HOME + "/sbstore/supabase/functions/canary/index.ts", "w").write(
    "Deno.serve(() => new Response(JSON.stringify({ canary: 'HERMES-CANARY-9' }), { headers: { 'Content-Type': 'application/json' } }));\n")
cfg = 'project_id = "swxpjxdzkwdilgkbbrnz"\n\n[functions.canary]\nverify_jwt = false\n'
open(HOME + "/sbstore/supabase/config.toml", "w").write(cfg)

env = dict(os.environ)
env["SUPABASE_ACCESS_TOKEN"] = open(HOME + "/.supa_sastra_token.txt", "rb").read().strip().decode()
env["PATH"] = "C:\\tools\\node-v24.11.1-win-x64;" + env.get("PATH", "")
r = subprocess.run(["supabase.CMD", "functions", "deploy", "canary", "--project-ref", "swxpjxdzkwdilgkbbrnz", "--no-verify-jwt"],
                   cwd=HOME + "/sbstore", env=env, capture_output=True, text=True, timeout=180)
print("deploy exit:", r.returncode, (r.stdout or "")[-160:])

K = open(HOME + "/sastra-group-site/store/khi_anon.txt").read().strip()
req = urllib.request.Request("https://swxpjxdzkwdilgkbbrnz.supabase.co/functions/v1/canary")
req.add_header("apikey", K)
try:
    print("canary call:", urllib.request.urlopen(req, timeout=30).read().decode()[:80])
except urllib.error.HTTPError as e:
    print("canary HTTP", e.code, e.read().decode()[:120])

# cleanup canary
r2 = subprocess.run(["supabase.CMD", "functions", "delete", "canary", "--project-ref", "swxpjxdzkwdilgkbbrnz", "--yes"],
                    cwd=HOME + "/sbstore", env=env, capture_output=True, text=True, timeout=120)
print("canary delete:", r2.returncode, (r2.stdout or r2.stderr or "")[-100:])
