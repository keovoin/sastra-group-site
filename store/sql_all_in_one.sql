-- Sastra Store — schema for khinvite Supabase project (vdhiiatsnbbizxsmhrxf)
-- Run in Lovable SQL editor (Everlasting Invites > Cloud > SQL editor). ASCII only.

create table if not exists public.store_products (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  title text not null,
  description text,
  price_usd numeric(10,2) not null check (price_usd > 0),
  cover_url text,
  file_path text not null,
  file_name text not null,
  description_km text,
  active boolean not null default true,
  sort integer not null default 0,
  created_at timestamptz not null default now()
);

create table if not exists public.store_orders (
  id uuid primary key default gen_random_uuid(),
  product_id uuid not null references public.store_products(id),
  buyer_email text,
  amount numeric(10,2) not null,
  status text not null default 'pending'
    check (status in ('pending','paid','delivered','expired','failed')),
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table public.store_products enable row level security;
alter table public.store_orders enable row level security;

-- anyone may browse active products
drop policy if exists store_products_public_read on public.store_products;
create policy store_products_public_read on public.store_products
  for select to anon, authenticated using (active = true);
-- orders: service-role only (edge function); no client policies

-- private storage bucket for paid files
insert into storage.buckets (id, name, public)
values ('store-files', 'store-files', false)
on conflict (id) do nothing;

-- seed: the budget proposal deck
insert into public.store_products (slug, title, description, price_usd, cover_url, file_path, file_name, sort)
values (
  'ppt-budget-proposal',
  'PPT_Budget Proposal',
  'Customizable budget-planning deck - quarterly and monthly tables, budget summaries, budget vs actual, breakdowns, Sankey financial chart and more.',
  4.99,
  '/assets/th-ppt-cover.webp',
  'store/ppt-budget-proposal/KEOVOIN_Budget_Planner.pptx',
  'Budget-Proposal-Templates.pptx',
  1
)
on conflict (slug) do update set
  title = excluded.title, description = excluded.description,
  price_usd = excluded.price_usd, cover_url = excluded.cover_url,
  file_path = excluded.file_path, file_name = excluded.file_name;

select id, slug, price_usd from public.store_products;

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
