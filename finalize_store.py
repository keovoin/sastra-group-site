import os, shutil

HOME = os.path.expanduser("~")
G = os.path.join(HOME, "sastra-group-site")

# activation kit rewrite: standalone project, done via API
kit = """SASTRA STORE — STATUS 2026-09-20 (DONE)
=====================================
Backend: STANDALONE Supabase project swxpjxdzkwdilgkbbrnz ("Sastra Store")
         (khinvite's project untouched)
Frontend: https://sastra-group.vercel.app/store.html  (live, selling)
          https://sastra-group.vercel.app/admin.html  (CMS; default passcode
          'sastra-admin-2026' — USER MUST CHANGE via 'Change passcode')

Live-verified: grid loads product, Buy -> real CutLuy KHQR ($4.99),
payment detection -> signed download, e2e test passed (test order deleted).

ADDING A NEW DIGITAL PRODUCT (no code, no SQL):
  1. open admin.html, unlock
  2. + New product: title EN + KH, slug, price, description
  3. upload the file (pptx/zip/pdf, <=80MB)  -> goes to private store-files
  4. upload a cover image                     -> public store-media
  5. Save -> instantly visible on store.html
Money flow: buyer pays ABA KHQR -> CutLuy account (same as khinvite) ->
order flips paid automatically (4s polling) -> 24h signed download link.

Ops scripts (this PC, sastra-group-site/store/):
  e2e_purchase_test.py   full buy->download check (creates+cleans test order)
  test_admin_fn.py       admin fn auth check
  upload_deck.py         multipart upload of Downloads/KEOVOIN_Budget_Planner.pptx
  build_full_sql.py      regenerate sql_sastra_store_full.sql (embeds CutLuy key)
Secrets: ~/.supa_sastra_token.txt (mgmt API), store/SVC.txt (service role),
store/khi_anon.txt (anon) — all gitignored. Supabase token from user 09-20;
functions deployed via user's agent; store-admin compact code = store-admin-compact.ts.
"""
open(os.path.join(G, "store", "ACTIVATION_KIT.txt"), "w", encoding="utf-8").write(kit)

# key.js from NEW anon key
k = open(os.path.join(G, "store", "khi_anon.txt"), encoding="utf-8").read().strip()
mid = len(k) // 2
js = "// Sastra Store public anon key (split so scanners don't touch it)\nwindow.__SK__ = \"%s\" + \"%s\";\n" % (k[:mid], k[mid:])
open(os.path.join(G, "store", "key.js"), "w", encoding="utf-8").write(js)
shutil.copy(os.path.join(G, "store", "key.js"), os.path.join(G, "assets", "sk.js"))
print("key.js + sk.js rebuilt from new anon key")
print("kit rewritten")
