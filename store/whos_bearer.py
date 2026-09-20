# who returns "Missing bearer token"? grep our own code + try to find in deno/supabase stacks
import os, re
HOME = os.path.expanduser("~")
G = os.path.join(HOME, "sastra-group-site")

for root, dirs, files in os.walk(G):
    dirs[:] = [d for d in dirs if d not in (".vercel", ".git", "shots")]
    for fn in files:
        if fn.endswith((".html", ".ts", ".js", ".py", ".txt")):
            p = os.path.join(root, fn)
            try:
                s = open(p, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            if "Missing bearer" in s:
                print("FOUND in:", p)
                m = re.search(r".{0,120}Missing bearer.{0,80}", s)
                print("   ", m.group(0).replace("\n", " ")[:200])
print("scan done")
