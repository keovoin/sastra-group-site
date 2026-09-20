#!/usr/bin/env bash
# curl_jwt_off.sh — flip verify_jwt=false on both store functions
T=$(tr -d '\r\n' < ~/.supa_sastra_token.txt)
REF=swxpjxdzkwdilgkbbrnz
for slug in store-payment store-admin; do
  echo "== $slug"
  curl -s -X PATCH "https://api.supabase.com/v1/projects/$REF/functions/$slug" \
    -H "Authorization: Bearer $T" -H "Content-Type: application/json" \
    -d '{"verify_jwt": false}' | head -c 300
  echo
done
echo "== final state"
curl -s "https://api.supabase.com/v1/projects/$REF/functions" -H "Authorization: Bearer $T" | python -c "import sys,json; [print(f['slug'],f.get('verify_jwt'),f.get('status')) for f in json.load(sys.stdin)]"
