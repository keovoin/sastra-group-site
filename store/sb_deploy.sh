#!/usr/bin/env bash
# sb_deploy.sh — deploy both store functions with verify_jwt=false via official CLI
set -e
export PATH="/c/tools/node-v24.11.1-win-x64:$PATH"
export SUPABASE_ACCESS_TOKEN=$'(cat ~/.supa_sastra_token.txt | tr -d \'\r\n\')'
PROJ=swxpjxdzkwdilgkbbrnz
D=/c/Users/KEOVOIN-DESKTOP/sbstore
rm -rf "$D"; mkdir -p "$D/supabase/functions/store-payment" "$D/supabase/functions/store-admin"
cd /c/Users/KEOVOIN-DESKTOP/sastra-group-site/store
cp store-payment-index.ts "$D/supabase/functions/store-payment/index.ts"
cp store-admin-compact.ts "$D/supabase/functions/store-admin/index.ts"
cat > "$D/supabase/config.toml" <<'EOF'
project_id = "swxpjxdzkwdilgkbbrnz"

[functions.store-payment]
verify_jwt = false

[functions.store-admin]
verify_jwt = false
EOF
cd "$D"
supabase functions deploy store-payment store-admin --project-ref "$PROJ" --no-verify-jwt 2>&1 | tail -8
