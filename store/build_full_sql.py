import os

HOME = os.path.expanduser("~")
key = open(os.path.join(HOME, "cutluy_key.txt")).read().strip()
assert key.startswith("ck_"), "unexpected key format: " + key[:6]

sql = open(os.path.join(HOME, "sastra-group-site", "store", "sql_store_schema.sql"), encoding="utf-8").read()

head = """-- Sastra Store FULL standalone setup — run ONCE in Supabase SQL editor.
-- Safe to re-run (idempotent).

create table if not exists public.gateway_settings (
  id uuid primary key default gen_random_uuid(),
  key text unique not null,
  value text not null,
  updated_at timestamptz not null default now()
);
alter table public.gateway_settings enable row level security;

"""

tail = """

-- CutLuy gateway key + store admin passcode
-- (log into admin.html and press Change passcode IMMEDIATELY — the default is public knowledge)
insert into public.gateway_settings (key, value) values
  ('cutluy_api_key', '""" + key + """'),
  ('store_admin_pass', 'sastra-admin-2026')
on conflict (key) do nothing;

-- public bucket for cover images
insert into storage.buckets (id, name, public)
values ('store-media', 'store-media', true)
on conflict (id) do nothing;

select key, left(value, 8) as prefix from public.gateway_settings;
"""

out = os.path.join(HOME, "sastra-group-site", "store", "sql_sastra_store_full.sql")
open(out, "w", encoding="utf-8").write(head + sql + tail)
print("written", out, len(head + sql + tail), "chars")
