# scripts/generate_assets.py
import requests, os
from jinja2 import Template

USER = "proAhmedUcv"
API = f"https://api.github.com/users/{USER}"

def fetch(url):
    r = requests.get(url, headers={"Accept":"application/vnd.github.v3+json"})
    r.raise_for_status()
    return r.json()

def main():
    # جلب بيانات المستخدم
    u = fetch(API)
    stats = {
      "name": u.get("name") or USER,
      "public_repos": u.get("public_repos"),
      "followers": u.get("followers"),
      "following": u.get("following"),
      "avatar": u.get("avatar_url")
    }

    # قالب SVG
    svg_tpl = """
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="120">
  <defs>
    <linearGradient id="g" x1="0" x2="1">
      <stop offset="0" stop-color="#36BCF7"/>
      <stop offset="1" stop-color="#7F5AF0"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" rx="12" fill="#071029"/>
  <text x="140" y="38" fill="#E6EEF8" font-size="20" font-family="Verdana">{{ name }}</text>
  <text x="140" y="66" fill="#9fb2d6" font-size="14" font-family="Verdana">
    Repos: {{ public_repos }} • Followers: {{ followers }} • Following: {{ following }}
  </text>
  <image x="14" y="14" width="92" height="92" href="{{ avatar }}"/>
  <rect x="0" y="118" width="100%" height="2" fill="url(#g)"/>
</svg>
"""
    svg = Template(svg_tpl).render(**stats)

    # حفظ الملف داخل assets
    os.makedirs("assets", exist_ok=True)
    with open("assets/dynamic_card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Generated assets/dynamic_card.svg")

if __name__ == "__main__":
    main()
