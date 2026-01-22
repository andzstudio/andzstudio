import requests
import datetime

# CONFIGURARE
USERNAME = "andzcr"
GIF_URL = "https://github.com/andzcr/andzcr/assets/banner.gif"

def get_last_updated_repo():
    url = f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&direction=desc"
    response = requests.get(url)
    if response.status_code == 200:
        repos = response.json()
        if repos:
            return repos[0] # Primul repo este cel mai recent editat
    return None

def create_svg(repo):
    if not repo:
        return
    
    name = repo['name']
    desc = repo['description'] if repo['description'] else "No description available."
    # Tăiem descrierea dacă e prea lungă
    if len(desc) > 55:
        desc = desc[:52] + "..."
        
    language = repo['language'] if repo['language'] else "Unknown"
    last_push = datetime.datetime.strptime(repo['pushed_at'], "%Y-%m-%dT%H:%M:%SZ")
    time_str = last_push.strftime("%d %b %Y, %H:%M")
    
    # SVG Template
    svg_content = f"""
    <svg width="800" height="200" viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
      <style>
        .title {{ font-family: 'Segoe UI', Ubuntu, Sans-Serif; font-size: 24px; font-weight: bold; fill: #ffffff; }}
        .desc {{ font-family: 'Segoe UI', Ubuntu, Sans-Serif; font-size: 16px; fill: #cccccc; }}
        .stat {{ font-family: 'Segoe UI', Ubuntu, Sans-Serif; font-size: 14px; fill: #00ff00; font-weight: bold; }}
        .bg-overlay {{ fill: rgba(0, 0, 0, 0.7); }}
        .border {{ fill: none; stroke: #30363d; stroke-width: 2px; rx: 10px; }}
      </style>
      
      <defs>
        <clipPath id="clip">
          <rect width="800" height="200" rx="10" />
        </clipPath>
      </defs>
      <image href="{GIF_URL}" width="800" height="200" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip)" />
      
      <rect x="0" y="0" width="800" height="200" class="bg-overlay" clip-path="url(#clip)" />
      
      <text x="30" y="50" class="title">Last Project: {name}</text>
      <text x="30" y="85" class="desc">{desc}</text>
      
      <text x="30" y="140" class="stat">⚡ Last Update: {time_str}</text>
      <text x="30" y="165" class="stat">💻 Main Language: {language}</text>
      
      <rect x="1" y="1" width="798" height="198" class="border" rx="10" />
    </svg>
    """
    
    with open("last_project.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)

if __name__ == "__main__":
    repo = get_last_updated_repo()
    create_svg(repo)

