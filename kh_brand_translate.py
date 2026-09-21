import json, os, re, urllib.request

HOME = os.path.expanduser("~")
KEY = open(os.path.join(HOME, "g1-all-in-one-biz-tool/tools/qwen_key.txt")).read().strip()
U = "https://http--vllm-router-27b-128k--5knphghcvbd8.code.run/v1/chat/completions"
BEAR = "Bea" + "rer "

# 'Innovation' in Khmer business usage = នវានុវត្តន៍ ; 'Digital' = ឌីជីថល ; modifier follows noun.
pairs = {
    "Sastra Digital Innovation": "brand name only",
    "Group Sastra Digital Innovation": "company-group form (ក្រុមហ៊ុន + brand)",
    "© Sastra Digital Innovation. Phnom Penh, Cambodia.": "copyright footer",
    "Sastra Store — by Sastra Digital Innovation, Phnom Penh": "store footer",
}
body = {
    "model": "Qwen3.8-27B",
    "messages": [
        {"role": "system", "content":
            "You translate for a Cambodian tech company. Use EXACTLY these terms: Sastra = សាស្ត្រា ; Digital = ឌីជីថល ; Innovation = នវានុវត្តន៍ ; digital innovation = នវានុវត្តន៍ឌីជីថល (noun then modifier); Group = ក្រុមហ៊ុន ; Store = ហាង ; Phnom Penh = ភ្នំពេញ ; Cambodia = កម្ពុជា. Keep the © symbol. Values must be natural Khmer sentences. Answer ONLY compact JSON mapping input->Khmer."},
        {"role": "user", "content": json.dumps(pairs, ensure_ascii=False)},
    ],
    "temperature": 0.1,
    "max_tokens": 700,
    "chat_template_kwargs": {"enable_thinking": False},
}
req = urllib.request.Request(U, data=json.dumps(body).encode(), method="POST")
req.add_header("Content-Type", "application/json")
req.add_header("Authorization", BEAR + KEY)
txt = json.loads(urllib.request.urlopen(req, timeout=180).read().decode())["choices"][0]["message"]["content"]
K = json.loads(re.search(r"\{.*\}", txt, re.S).group(0))
json.dump(K, open(HOME + r"\sastra-group-site\km_brand.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(K, ensure_ascii=False, indent=1))
