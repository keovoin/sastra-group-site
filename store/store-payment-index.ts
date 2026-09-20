import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// Sastra Store checkout — CutLuy KHQR, guest-friendly (email buyer, no login).
// Actions:
//   { action:'create', product_slug, email } -> { order_id, checkout_url, qr_image, qr, amount, expires_at }
//   { action:'status', order_id, email }     -> { status } and when paid: { download_url }
// Gateway key is read from gateway_settings (same row khinvite already uses).
const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...corsHeaders, "Content-Type": "application/json" } });

function cutluyQrSvg(qrString: string) {
  return `https://cutluy.com/api/render/khqr/${encodeURIComponent(qrString)}.svg`;
}
function validEmail(e: unknown): e is string {
  return typeof e === "string" && /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(e) && e.length < 200;
}

serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: corsHeaders });
  try {
    const url = Deno.env.get("SUPABASE_URL")!;
    const admin = createClient(url, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
    const body = await req.json().catch(() => ({}));
    const action = body?.action;

    const { data: keyRows } = await admin.from("gateway_settings").select("key, value").eq("key", "cutluy_api_key");
    const apiKey = (keyRows || [])[0]?.value;
    if (!apiKey) return json({ error: "CutLuy payments are not configured yet." }, 400);

    if (action === "create") {
      const slug = String(body?.product_slug || "");
      const email = String(body?.email || "").trim().toLowerCase();
      if (!validEmail(email)) return json({ error: "Please enter a valid email address." }, 400);
      const { data: product } = await admin.from("store_products").select("*").eq("slug", slug).eq("active", true).maybeSingle();
      if (!product) return json({ error: "Product not found." }, 404);

      const idem = crypto.randomUUID();
      const gwRes = await fetch("https://cutluy.com/v1/payments", {
        method: "POST",
        headers: { Authorization: `Bearer ${apiKey}`, "User-Agent": "sastra-store/1.0", "Content-Type": "application/json", "Idempotency-Key": idem },
        body: JSON.stringify({ amount: Number(product.price_usd), reference_id: idem }),
      });
      const payment: any = await gwRes.json().catch(() => null);
      if (!gwRes.ok || !payment?.id) return json({ error: payment?.error?.message || payment?.message || "CutLuy could not create a KHQR payment." }, 400);

      const { data: order, error: insErr } = await admin.from("store_orders").insert({
        product_id: product.id,
        buyer_email: email,
        amount: product.price_usd,
        status: "pending",
        metadata: { cutluy_payment_id: String(payment.id), checkout_url: payment.checkout_url || null },
      }).select().single();
      if (insErr) throw insErr;

      return json({
        order_id: order.id,
        cutluy_id: payment.id,
        status: "pending",
        amount: Number(product.price_usd),
        title: product.title,
        checkout_url: payment.checkout_url || null,
        qr_image: cutluyQrSvg(payment.qr_string),
        qr: payment.qr_string,
        expires_at: payment.expires_at,
      });
    }

    if (action === "status") {
      const { data: order } = await admin.from("store_orders").select("*, store_products(*)").eq("id", body?.order_id).maybeSingle();
      if (!order) return json({ error: "Order not found." }, 404);
      // email is the possession secret for the order — must match to read status/download
      const email = String(body?.email || "").trim().toLowerCase();
      if (!order.buyer_email || order.buyer_email !== email) return json({ error: "Order not found." }, 404);
      if (order.status === "paid" || order.status === "delivered") {
        const { data: signed } = await admin.storage.from("store-files").createSignedUrl(order.store_products.file_path, 60 * 60 * 24, { download: order.store_products.file_name });
        return json({ status: "paid", download_url: signed?.signedUrl || null, file_name: order.store_products.file_name, title: order.store_products.title });
      }
      const cutluyId = order.metadata?.cutluy_payment_id;
      if (!cutluyId) return json({ status: "pending" });
      const gwRes = await fetch(`https://cutluy.com/v1/payments/${encodeURIComponent(String(cutluyId))}`, { headers: { Authorization: `Bearer ${apiKey}`, "User-Agent": "sastra-store/1.0" } });
      const payment: any = await gwRes.json().catch(() => null);
      if (!gwRes.ok || !payment?.status) return json({ status: "pending" });
      if (payment.status === "paid") {
        await admin.from("store_orders").update({ status: "paid", metadata: { ...order.metadata, payment }, updated_at: new Date().toISOString() }).eq("id", order.id);
        const { data: signed } = await admin.storage.from("store-files").createSignedUrl(order.store_products.file_path, 60 * 60 * 24, { download: order.store_products.file_name });
        return json({ status: "paid", download_url: signed?.signedUrl || null, file_name: order.store_products.file_name, title: order.store_products.title });
      }
      if (payment.status === "expired") {
        await admin.from("store_orders").update({ status: "expired", updated_at: new Date().toISOString() }).eq("id", order.id);
        return json({ status: "expired" });
      }
      if (payment.status === "failed") return json({ status: "failed" });
      return json({ status: "pending" });
    }

    return json({ error: "Unsupported action." }, 400);
  } catch (error) {
    console.error("store-payment", error);
    return json({ error: error instanceof Error ? error.message : "Payment request failed." }, 400);
  }
});
