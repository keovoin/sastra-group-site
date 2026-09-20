import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const C = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-store-pass" };
const J = (b, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { ...C, "Content-Type": "application/json" } });

async function ok(a, req, body) {
  const g = (body && body.pass) || req.headers.get("x-store-pass") || "";
  const { data } = await a.from("gateway_settings").select("value").eq("key", "store_admin_pass").maybeSingle();
  return !!data && g === data.value;
}

serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: C });
  try {
    const a = createClient(Deno.env.get("SUPABASE_URL"), Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"));
    const ct = req.headers.get("content-type") || "";
    if (ct.includes("multipart/form-data")) {
      const f = await req.formData();
      if (!(await ok(a, req, { pass: String(f.get("pass") || "") }))) return J({ error: "Unauthorized." }, 401);
      const kind = String(f.get("kind") || "file");
      const slug = String(f.get("slug") || "misc").replace(/[^a-z0-9-]/g, "-");
      const fl = f.get("file");
      if (!(fl instanceof File) || fl.size === 0) return J({ error: "No file received." }, 400);
      if (fl.size > 80 * 1048576) return J({ error: "File too large (80MB)." }, 400);
      const buf = await fl.arrayBuffer();
      const ext = (fl.name.match(/\.[a-z0-9]+$/i) || [".bin"])[0].toLowerCase();
      const nm = fl.name.replace(/[^A-Za-z0-9._-]+/g, "_").slice(-80);
      if (kind === "cover") {
        const p = "covers/" + slug + ext;
        const { error } = await a.storage.from("store-media").upload(p, buf, { contentType: fl.type, upsert: true });
        if (error) return J({ error: error.message }, 400);
        return J({ ok: true, url: a.storage.from("store-media").getPublicUrl(p).data.publicUrl });
      }
      const p = "store/" + slug + "/" + nm;
      const { error } = await a.storage.from("store-files").upload(p, buf, { contentType: fl.type, upsert: true });
      if (error) return J({ error: error.message }, 400);
      return J({ ok: true, file_path: p, file_name: nm });
    }
    const b = await req.json().catch(() => ({}));
    const act = b.action;
    if (act === "login") return J({ ok: await ok(a, req, b) });
    if (act === "change-pass") {
      if (!(await ok(a, req, b))) return J({ error: "Wrong passcode." }, 401);
      const np = String(b.new_pass || "");
      if (np.length < 6) return J({ error: "New passcode too short." }, 400);
      const ex = await a.from("gateway_settings").select("key").eq("key", "store_admin_pass").maybeSingle();
      if (ex.data) await a.from("gateway_settings").update({ value: np }).eq("key", "store_admin_pass");
      else await a.from("gateway_settings").insert({ key: "store_admin_pass", value: np });
      return J({ ok: true });
    }
    if (!(await ok(a, req, b))) return J({ error: "Unauthorized." }, 401);
    if (act === "list") {
      const pr = await a.from("store_products").select("*").order("sort").order("created_at", { ascending: false });
      const or = await a.from("store_orders").select("status, amount, created_at, product_id");
      return J({ products: pr.data || [], orders: or.data || [] });
    }
    if (act === "save") {
      const p = b.product || {};
      const c = {
        slug: String(p.slug || "").trim().toLowerCase().replace(/[^a-z0-9-]+/g, "-").replace(/^-+|-+$/g, ""),
        title: String(p.title || "").trim(),
        description: String(p.description || "").trim(),
        description_km: String(p.description_km || "").trim() || null,
        price_usd: Number(p.price_usd),
        cover_url: String(p.cover_url || "").trim() || null,
        file_path: String(p.file_path || "").trim(),
        file_name: String(p.file_name || "").trim(),
        active: p.active !== false,
        sort: Number(p.sort || 0),
      };
      if (!c.slug || !c.title) return J({ error: "Slug and title are required." }, 400);
      if (!(c.price_usd > 0)) return J({ error: "Price must be > 0." }, 400);
      if (!c.file_path) return J({ error: "Upload the product file first." }, 400);
      const r = p.id ? await a.from("store_products").update(c).eq("id", p.id).select().single() : await a.from("store_products").insert(c).select().single();
      if (r.error) return J({ error: r.error.message }, 400);
      return J({ product: r.data });
    }
    if (act === "toggle") {
      const r = await a.from("store_products").update({ active: !b.active }).eq("id", b.id).select().single();
      if (r.error) return J({ error: r.error.message }, 400);
      return J({ product: r.data });
    }
    if (act === "delete") {
      const r = await a.from("store_products").delete().eq("id", b.id);
      if (r.error) return J({ error: r.error.message }, 400);
      return J({ ok: true });
    }
    return J({ error: "Unsupported action." }, 400);
  } catch (e) { return J({ error: e && e.message ? e.message : "Admin request failed." }, 400); }
});
