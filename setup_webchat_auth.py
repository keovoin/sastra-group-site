import secrets, string, subprocess, os, sys

sys.path.insert(0, r"C:\Users\KEOVOIN-DESKTOP\AppData\Local\hermes\hermes-agent")
from plugins.dashboard_auth.basic import hash_password

a = string.ascii_letters + string.digits
pw = "kh" + secrets.choice(string.ascii_uppercase) + "".join(secrets.choice(a) for _ in range(9))
home = os.path.expanduser("~")
open(home + "/.webchat_pw.txt", "w").write(pw)
h = hash_password(pw)
print("pw saved to ~/.webchat_pw.txt (len %d)" % len(pw))

HERMES = r"C:\Users\KEOVOIN-DESKTOP\AppData\Local\hermes\bin\hermes.exe"
for kv in [("dashboard.basic_auth.username", "keovoin"), ("dashboard.basic_auth.password_hash", h)]:
    r = subprocess.run([HERMES, "config", "set", *kv], capture_output=True, text=True, timeout=60)
    print(kv[0], "->", (r.stdout or r.stderr).strip().splitlines()[-1][:70] if (r.stdout or r.stderr) else r.returncode)
