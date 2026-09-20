import json, urllib.request, os
k = open(os.path.expanduser("~/sastra-group-site/store/khi_anon.txt")).read().strip()
r = urllib.request.Request("https://vdhiiatsnbbizxsmhrxf.supabase.co/rest/v1/gateway_settings?select=*", headers={"apikey": k, "Authorization": "***" + k})
try:
    print(urllib.request.urlopen(r, timeout=20).read().decode()[:200])
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:150])
# columns via rpc? simpler: check the migration file khinvite used
m = open(os.path.expanduser("~/khinvite-bf9ea5b9/supabase/migrations/20260916_gateway_settings.sql"), encoding="utf-8", errors="ignore").read()
import re
i = m.find("create table")
print(m[i:i+400])
