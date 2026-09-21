"""Sweep: 'Sastra Solution Group' -> 'Sastra Digital Innovation' everywhere.
EN: plain replace. KH: find any Khmer string that embeds the new EN name and
re-translate it as a whole via the 27B engine."""
import os, json, re, urllib.request

HOME = os.path.expanduser("~")
G = os.path.join(HOME, "sastra-group-site")
KEY = open(os.path.join(HOME, "g1-all-in-one-biz-tool/tools/qwen_key.txt")).read().strip()
BASE = "https://http--vllm-router-27b-128k--5knphghcvbd8.code.run/v1/chat/completions"
NEW_EN = "Sastra Digital Innovation"


def km_map(pairs):
    body = {
        "model": "Qwen3.6-27B",
        "messages": [
            {"role": "system", "content": "Translate English strings for a Cambodian tech company into Khmer as used on Cambodian business Facebook pages (transliterate brand names as loanwords: Sastra=សាស្ត្រា, Digital=ឌីជីថល, Innovation=ីណូវ៉េសិន or ការបង្កើតថ្មី; keep ©, Phnom Penh=ភ្នំពេញ). Answer ONLY with compact JSON mapping input->Khmer."},
            {"role": "user", "content": json.dumps(pairs, ensure_ascii=False)},
        ],
        "temperature": 0.2, "max_tokens": 700,
    }
    req = urllib.request.Request(BASE, data=json.dumps(body).encode(), method="POST")
    req.add_header("Authorization", "***" + KEY)
    req.add_header("Content-Type", "application/json")
    txt = json.loads(urllib.request.urlopen(req, timeout=180).read().decode())["choices"][0]["message"]["content"]
    return json.loads(re.search(r"\{.*\}", txt, re.S).group(0))

# ---------- step 1: EN sweep, remember which Khmer lines contained the EN name ----------
targets = ("index.html", "store.html", "admin.html", "manifest.webmanifest")
texts = {}
for f in targets:
    s = open(os.path.join(G, f), encoding="utf-8").read()
    texts[f] = s.replace("Sastra Solution Group", NEW_EN).replace("Sastra Solution", NEW_EN)
    open(os.path.join(G, f), "w", encoding="utf-8").write(texts[f])

# Khmer fragments that still embed the old Khmer name of the group
OLD_KH_NAME = "សាស្ត្រា សូលូសិន"
kh_need = set()
for f in targets:
    for m in re.finditer(r"[\"\u0027>]([^\"\u0027<]*)(" + OLD_KH_NAME + r")([^\"\u0027<]*)", texts[f]):
        kh_need.add(m.group(0).strip("\"'>"))
print("Khmer fragments to fix:", list(kh_need)[:6])

# ---------- step 2: re-translate each fragment (replace old KH name with new EN first) ----------
inputs = {frag.replace(OLD_KH_NAME, NEW_EN): "" for frag in kh_need}
# also the canonical brand alone for the JSON-LD alternateName
inputs[NEW_EN] = ""
try:
    K = km_map(inputs)
except Exception as e:
    print("translate FAIL:", e)
    K = {}

for f in targets:
    s = texts[f]
    for orig in kh_need:
        en_equiv = orig.replace(OLD_KH_NAME, NEW_EN)
        new_kh = K.get(en_equiv)
        if new_kh and orig != new_kh:
            s = s.replace(orig, new_kh)
    texts[f] = s

# canonical brand standalone (JSON-LD alternateName, footer brand .kh, og)
canon = K.get(NEW_EN)
if canon:
    for f in targets:
        texts[f] = texts[f].replace("សាស្ត្រា សូលូសិន", canon)

for f in targets:
    open(os.path.join(G, f), "w", encoding="utf-8").write(texts[f])

# ---------- step 3: report residues ----------
for f in targets:
    s = texts[f]
    print(f, "| Sastra Solution:", s.count("Sastra Solution"),
          "| សូលូសិន:", s.count("សូលូសិន"),
          "| new name:", s.count(NEW_EN))
print(json.dumps(K, ensure_ascii=False, indent=1))
