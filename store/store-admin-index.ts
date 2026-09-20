import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// Sastra Store CMS — passcode-guarded product manager (create/update/delete/toggle,
// file + cover upload, orders view). Passcode lives in gateway_settings.store_admin_pass.
// All mutating actions require { pass } in the JSON body (or X-Store-Pass header for uploads).
const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-store-pass",
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...corsHeaders, "Content-Type": "application/json" } });

async function checkPass(admin: any, req: Request, body: any): Promise<boolean> {
  const given = body?.pass || req.headers.get("x-store-pass") || "";
  const { data } = await admin.from("gateway_settings").select("value").eq("key", "store_admin_pass").maybeSingle();
  if (!data) return false;
  return typeof given === "string" && given === data.value;
}

serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: corsHeaders });
  try {
    const url = Deno.env.get("SUPABASE_URL")!;
    const admin = createClient(url, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
    const action = req.method === "GET" ? "list" : (await req.clone().json().catch(() => ({})))?.action;

    // login probe: cheap pass check the admin UI can call first
    if (action === "login") {
      const body = await req.json().catch(() => ({}));
      return json({ ok: await checkPass(admin, req, body) }, 200);
    }
    if (action === "change-pass") {
      const body = await req.json();
      if (!(await checkPass(admin, req, body))) return json({ error: "Wrong passcode." }, 401);
      const np = String(body.new_pass || "");
      if (np.length < 6) return json({ error: "New passcode too short." }, 400);
      const { data: ex } = await admin.from("gateway_settings").select("key").eq("key", "store_admin_pass").maybeSingle();
      if (ex) await admin.from("gateway_settings").update({ value: np }).eq("key", "store_admin_pass");
      else await admin.from("gateway_settings").insert({ key: "store_admin_pass", value: np });
      return json({ ok: true });
    }

    // ---- everything below is admin-only ----
    const ct = req.headers.get("content-type") || "";
    const body = ct.includes("application/json") ? await req.json().catch(() => ({})) : {};
    if (!(await checkPass(admin, req, body))) return json({ error: "Unauthorized." }, 401);

    if (action === "list") {
      const { data: products } = await admin.from("store_products").select("*").order("sort").order("created_at", { ascending: false });
      const { data: orders } = await admin.from("store_orders").select("status, amount, created_at, product_id");
      return json({ products: products || [], orders: orders || [] });
    }

    if (action === "save") {
      const p = body.product || {};
      const clean = {
        slug: String(p.slug || "").trim().toLowerCase().replace(/[^a-z0-9-]+/g, "-").replace(/^-+|-+$/g, ""),
        title: String(p.title || "").trim(),
        description: String(p.description || "").trim(),
        price_usd: Number(p.price_usd),
        description_km: String(p.description_km || "").trim() || null,
        cover_url: String(p.cover_url || "").trim() || null,
        file_path: String(p.file_path || "").trim(),
        file_name: String(p.file_name || "").trim(),
        active: p.active !== false,
        sort: Number(p.sort || 0),
      };
      if (!clean.slug || !clean.title) return json({ error: "Slug and title are required." }, 400);
      if (!(clean.price_usd > 0)) return json({ error: "Price must be > 0." }, 400);
      if (!clean.file_path) return json({ error: "Upload the product file first." }, 400);
      let data, error;
      if (p.id) {
        ({ data, error } = await admin.from("store_products").update(clean).eq("id", p.id).select().single());
      } else {
        ({ data, error } = await admin.from("store_products").insert(clean).select().single());
      }
      if (error) return json({ error: error.message }, 400);
      return json({ product: data });
    }

    if (action === "toggle") {
      const { data, error } = await admin.from("store_products").update({ active: !body.active }).eq("id", body.id).select().single();
      if (error) return json({ error: error.message }, 400);
      return json({ product: data });
    }

    if (action === "delete") {
      const { error } = await admin.from("store_products").delete().eq("id", body.id);
      if (error) return json({ error: error.message }, 400); // FK will block if orders exist -> tell user
      return json({ ok: true });
    }

    // binary upload (file or cover) — multipart with fields: pass, kind, slug; file part
    if (action === "upload" || ct.includes("multipart/form-data")) {
      const form = await req.formData();
      const pass = String(form.get("pass") || "");
      if (!(await checkPass(admin, req, { pass }))) return json({ error: "Unauthorized." }, 401);
      const kind = String(form.get("kind") || "file");         // 'file' | 'cover'
      const slug = String(form.get("slug") || "misc").replace(/[^a-z0-9-]/g, "-");
      const f = form.get("file");
      if (!(f instanceof File) || f.size === 0) return json({ error: "No file received." }, 400);
      if (f.size > 80 * 1024 * 1024) return json({ error: "File too large (80MB max)." }, 400);
      const buf = await f.arrayBuffer();
      const ext = (f.name.match(/\.[a-z0-9]+$/i) || [".bin"])[0].toLowerCase();
      const safeName = f.name.replace(/[^A-Za-z0-9._-]+/g, "_").slice(-80);
      if (kind === "cover") {
        const path = `covers/${slug}${ext}`;
        const { error } = await admin.storage.from("store-media").upload(path, buf, { contentType: f.type || "application/octet-stream", upsert: true });
        if (error) return json({ error: error.message }, 400);
        const { data: pub } = admin.storage.from("store-media").getPublicUrl(path);
        return json({ ok: true, url: pub.publicUrl });
      }
      const path = `store/${slug}/${safeName}`;
      const { error } = await admin.storage.from("store-files").upload(path, buf, { contentType: f.type || "application/octet-stream", upsert: true });
      if (error) return json({ error: error.message }, 400);
      return json({ ok: true, file_path: path, file_name: safeName });
    }

    return json({ error: "Unsupported action." }, 400);
  } catch (error) {
    console.error("store-admin", error);
    return json({ error: error instanceof Error ? error.message : "Admin request failed." }, 400);
  }
});
