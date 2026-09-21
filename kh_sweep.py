import json, os, re, urllib.request

HOME = os.path.expanduser("~")
G = os.path.join(HOME, "sastra-group-site")
KEY = open(os.path.join(HOME, "g1-all-in-one-biz-tool/tools/qwen_key.txt")).read().strip()
U = "https://http--vllm-router-27b-128k--5knphghcvbd8.code.run/v1/chat/completions"

pairs = {
    "Sastra Digital Innovation": "",
    "Group Sastra Digital Innovation": "",
    "© Sastra Digital Innovation. Phnom Penh, Cambodia.": "",
    "Sastra Store — by Sastra Digital Innovation, Phnom Penh": "",
}
body = {
    "model": "Qwen3.8-27B",
    "messages": [
        {"role": "system", "content": "Translate these English strings into Khmer as a Cambodian tech company would write them on its official Facebook page. Transliterate 'Sastra' as សាស្ត្រា. Decide natural Khmer for 'Digital Innovation' (loanword transliteration is common for brand names; so is ឌីជីថល + នវានុវត្តន៍). Keep © symbol, Phnom Penh = ភ្នំពេញ, Cambodia = កម្ពុជា. Answer ONLY with compact JSON object mapping each input string to its Khmer translation."},
        {"role": "user", "content": json.dumps(pairs, ensure_ascii=False)},
    ],
    "temperature": 0.15,
    "max_tokens": 600,
}
req = urllib.request.Request(U, data=json.dumps(body).encode(), method="POST")
req.add_header("Authorization", "***" + KEY)
req.add_header("Content-Type", "application/json")
txt = json.loads(urllib.request.urlopen(req, timeout=180).read().decode())["choices"][0]["message"]["content"]
K = json.loads(re.search(r"\{.*\}", txt, re.S).group(0))
print(json.dumps(K, ensure_ascii=False, indent=1))

BRAND_KH = K["Sastra Digital Innovation"]
GRP_KH = K["Sastra Digital Innovation"]
COPY_KH = K["© Sastra Digital Innovation. Phnom Penh, Cambodia."]
FOOT_KH = K["Sastra Store — by Sastra Digital Innovation, Phnom Penh"]

OLD = "សាស្ត្រា សូលូសិន"  # សាស្ត្រា សូលូសិន

def fix(fname):
    p = os.path.join(G, fname)
    s = open(p, encoding="utf-8").read()
    n = s.count(OLD)
    s = s.replace("ក្រុមហ៊ុន " + OLD, GRP_KH)
    s = s.replace(OLD, BRAND_KH)
    open(p, "w", encoding="utf-8").write(s)
    print(fname, "replaced", n, "left", s.count(OLD))

fix("index.html")
fix("store.html")

# exact Khmer i18n replacements if model returned full strings
idx = os.path.join(G, "index.html")
s = open(idx, encoding="utf-8").read()
if COPY_KH:
    s = s.replace("© " + BRAND_KH + ". ភ្នំពេញ កម្ពុជា។", COPY_KH)
    open(idx, "w", encoding="utf-8").write(s)
st = os.path.join(G, "store.html")
s2 = open(st, encoding="utf-8").read()
if FOOT_KH:
    # current store foot kh = សាស្ត្រា ហាង — ដោយ <brand> ភ្នំពេញ pattern; just verify no old brand left
    pass
print("store_old_left:", s2.count(OLD), "index_old_left:", open(idx, encoding='utf-8').read().count(OLD))
