import urllib.request, re

r = urllib.request.urlopen("https://trades-forms-expect-mysimon.trycloudflare.com/login", timeout=40)
h = r.read().decode("utf-8", "replace")
print("form action:", re.findall(r'<form[^>]*action="([^"]+)"', h)[:3])
print("inputs:", re.findall(r'name="([a-zA-Z_]+)"', h)[:8])
print("api paths:", sorted(set(re.findall(r"/api/[a-zA-Z_/]+", h)))[:10])
print("script src:", re.findall(r'src="([^"]+)"', h)[:5])
# inline JS endpoints
print("fetch/POST hints:", re.findall(r'fetch\(`?"?([^"`?)]+)', h)[:6])
