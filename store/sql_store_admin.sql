-- Sastra Store CMS migration (run AFTER sql_store_schema.sql)
-- adds: admin pass row + public media bucket for cover images

-- 1) admin passcode (CHANGE 'sastra-admin-2026' to your own secret before running,
--    or use the admin panel's "Change passcode" after first login)
insert into public.gateway_settings (key, value)
values ('store_admin_pass', 'sastra-admin-2026')
on conflict (key) do nothing;

-- 2) public bucket for product cover images
insert into storage.buckets (id, name, public)
values ('store-media', 'store-media', true)
on conflict (id) do nothing;

-- 3) Khmer description + cover column safety (idempotent)
alter table public.store_products add column if not exists description_km text;

select key from public.gateway_settings where key='store_admin_pass';
