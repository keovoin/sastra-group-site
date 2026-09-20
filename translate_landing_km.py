# translate_landing_km.py — proper Khmer translation for the landing page strings
# engine: Qwen3.8-27B via code.run router (same as tools/ui_km.py), batched+numbered.
import json, re, time, urllib.request, os

HOME = os.path.expanduser("~")
KEY = open(os.path.join(HOME, "g1-all-in-one-biz-tool/tools/qwen_key.txt")).read().strip()
BASE = "https://http--vllm-router-27b-128k--5knphghcvbd8.code.run/v1/chat/completions"
OUT = os.path.join(HOME, "sastra-group-site", "km_translations.json")

# key + English text to translate (value = what a Khmer reader should see)
PAIRS = {
 "kick": "Sastra Solution Group — Cambodia",
 "h1a": "Software that",
 "h1b": "moves a country",
 "h1c": "forward.",
 "hsub": "We build and operate digital products — from Khmer event invitations to enterprise management — designed here, used everywhere.",
 "m1": "Products",
 "m2": "Languages (EN / Khmer)",
 "m3": "Built in Cambodia",
 "nav_more": "More",
 "p1_e": "Celebrations, digitized",
 "p1_b": "Elegant digital invitations for every Khmer occasion — weddings, engagements, birthdays, shop openings, memorial services and more. Nine event types, each with its own art, animation and atmosphere. Guests RSVP, pay by ABA KHQR, and gift money lands on a live kiosk total at the venue.",
 "p1_t1": "9 event types",
 "p1_t2": "KHQR payments",
 "p1_t3": "Live gift kiosk",
 "p1_t4": "EN + Khmer",
 "visit": "Visit",
 "p2_e": "Careers, decoded",
 "p2_b": "Job seekers upload a CV and get an ATS analysis instantly — what recruiters see, what is missing, what to fix. AI rewrites, bilingual templates, and a live board of jobs and freelance gigs across Cambodia.",
 "p2_t1": "ATS scoring",
 "p2_t2": "AI resume rewrite",
 "p2_t3": "Jobs & gigs board",
 "p2_t4": "KHQR checkout",
 "p3_e": "Stories that binge",
 "p3_b": "A streaming home for short drama and reels — vertical episodes, auto-continuing playback, subscriptions with promo codes, and watch statistics. Built on Firebase and Cloud Run, delivered fast across the region.",
 "p3_t1": "Short-form streaming",
 "p3_t2": "Subscriptions",
 "p3_t3": "Promo engine",
 "p3_t4": "Analytics",
 "p4_e": "Discover Cambodia",
 "p4_b": "A living map of places worth going to — restaurants, cafes, temples, attractions, EV charging. Community listings with photos and reviews, province-by-province attraction guides, and near-me discovery.",
 "p4_t1": "Interactive map",
 "p4_t2": "Community reviews",
 "p4_t3": "25 provinces",
 "p4_t4": "Offline-friendly PWA",
 "p5_e": "Run the whole company",
 "p5_b": "Our enterprise platform for the team: time tracking, tasks, projects, invoices, HR, CRM and reports in one workspace — fully Khmer-localised, with an in-app AI assistant that acts on your own company data, always behind an approval click.",
 "p5_t1": "ERP · CRM · HRM · ATS",
 "p5_t2": "AI assistant + tools",
 "p5_t3": "5,800+ Khmer UI strings",
 "p5_t4": "Self-hosted",
 "open": "Open",
 "more_e": "Also shipping from the group",
 "more_h": "And the rest of the family.",
 "r_chess": "Play chess against a live engine or friends — leaderboards, instant matches, bilingual board UI.",
 "r_card": "Design Khmer greeting cards — birthdays, holidays, thank-you cards — in seconds, in the browser.",
 "r_quiz": "Mobile quiz competition with an admin panel for questions, categories and prize rounds.",
 "r_god": "A live 3D globe tracking planes, satellites and ships in real time.",
 "r_plant": "Plant-care companion app — watering reminders, plant library and growth journal on Android.",
 "r_book": "An open knowledge book on trading money and time for health and freedom — Chinese / English / Khmer.",
 "grp_e": "The group",
 "grp_lead": "Eleven products, one team. We start with a problem we can see from our own desk — an invitation sent by messenger, a CV lost in an inbox, a place with no pin on the map — and we ship it, run it, and keep it fast.",
 "pr1_h": "Khmer first",
 "pr1_p": "Full Khmer language support, KHQR payments, and designs that respect local ceremony and habit.",
 "pr2_h": "AI with a seatbelt",
 "pr2_p": "Assistants that act on real company data — but every mutating move waits for a human approve.",
 "pr3_h": "Lean and live",
 "pr3_p": "Small team, modern stack, deployments measured in minutes. Every product here is running in production today.",
 "f_prod": "Products",
 "f_comp": "Company",
 "f_all": "All products",
 "f_about": "About the group",
 "f_top": "Back to top",
 "f_copy": "© Sastra Solution Group. Phnom Penh, Cambodia.",
}

def call(prompt):
    body = json.dumps({
        "model": "Qwen3.8-27B",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3, "max_tokens": 4000,
        "chat_template_kwargs": {"enable_thinking": False},
    }).encode()
    req = urllib.request.Request(BASE, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", "Bea" + "rer " + KEY)
    with urllib.request.urlopen(req, timeout=180) as r:
        j = json.loads(r.read().decode())
    return j["choices"][0]["message"]["content"]

keys = list(PAIRS.keys())
BATCH = 8
out = {}
if os.path.exists(OUT):
    out = json.load(open(OUT, encoding="utf-8"))
todo = [k for k in keys if k not in out]
for i in range(0, len(todo), BATCH):
    chunk = todo[i:i+BATCH]
    numbered = "\n".join(f"{n+1}. {PAIRS[k]}" for n, k in enumerate(chunk))
    prompt = (
        "Translate each numbered line to natural, professional KHMER (Cambodian). "
        "Rules: keep brand names exactly (Sastra, khinvite, tvercv, UrDrama, KHFinder, KHChess, "
        "Aba KHQR/KHQR keep as KHQR, Firebase, Cloud Run, Android, PWA, ATS, ERP, CRM, HRM, AI, UI, CV, "
        "EN); marketing tone, no word-for-word machine feel; output ONLY lines 'N. translation' in the same order; "
        "no explanations.\n\n" + numbered)
    for attempt in range(3):
        try:
            resp = call(prompt)
            got = dict((int(m[0]), m[1].strip()) for m in re.findall(r"^(\d+)\.\s*(.+)$", resp, re.M))
            if all(n in got for n in range(1, len(chunk)+1)):
                for n, k in enumerate(chunk, 1):
                    out[k] = got[n]
                print("batch", i // BATCH + 1, "ok")
                break
        except Exception as e:
            print("retry", e); time.sleep(20)
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    time.sleep(8)

print("translated:", len(out), "/", len(PAIRS))
missing = [k for k in keys if k not in out]
print("missing:", missing)
