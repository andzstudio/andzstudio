import requests
import datetime
from datetime import timedelta

# CONFIGURARE
USERNAME = "andzcr"

def get_last_updated_repo():
    try:
        # Luam repo-urile sortate dupa push
        url = f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&direction=desc"
        response = requests.get(url)
        if response.status_code == 200:
            repos = response.json()
            if repos:
                return repos[0]
    except Exception as e:
        print(f"Error fetching repo: {e}")
    return None

def create_svg(repo):
    if not repo:
        return
    
    # Date extrase
    name = repo['name']
    desc = repo['description'] if repo['description'] else "No description provided."
    if len(desc) > 60:
        desc = desc[:57] + "..."
        
    language = repo['language'] if repo['language'] else "N/A"
    stars = repo['stargazers_count']
    forks = repo['forks_count']
    
    # Timezone fix: GitHub da ora in UTC, noi adaugam 2 ore pentru Romania
    last_push_utc = datetime.datetime.strptime(repo['pushed_at'], "%Y-%m-%dT%H:%M:%SZ")
    last_push_ro = last_push_utc + timedelta(hours=2)
    time_str = last_push_ro.strftime("%d %b %Y, %H:%M") # Format curat

    # SVG Design - Modern Dark Theme cu Animatie CSS
    svg_content = f"""
    <svg width="450" height="220" viewBox="0 0 450 220" xmlns="http://www.w3.org/2000/svg">
      <style>
        .container {{ font-family: 'Segoe UI', Ubuntu, Sans-Serif; fill: #E6EDF3; }}
        .card-bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; rx: 15px; }}
        
        /* Gradient Animat pentru Header */
        .header-bg {{ fill: url(#grad1); }}
        @keyframes gradient-anim {{
            0% {{ stop-color: #2f80ed; }}
            50% {{ stop-color: #a044ff; }}
            100% {{ stop-color: #2f80ed; }}
        }}
        #stop1 {{ animation: gradient-anim 4s infinite; }}
        
        /* Texte */
        .title {{ font-size: 20px; font-weight: 700; fill: #ffffff; }}
        .desc {{ font-size: 14px; fill: #8b949e; }}
        .label {{ font-size: 12px; font-weight: 600; fill: #8b949e; }}
        .value {{ font-size: 12px; font-weight: 600; fill: #E6EDF3; }}
        
        /* Icon placeholders (simple circles/paths for clean look) */
        .icon {{ fill: #8b949e; }}
      </style>
      
      <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color:#2f80ed;stop-opacity:1" id="stop1" />
          <stop offset="100%" style="stop-color:#00c6ff;stop-opacity:1" />
        </linearGradient>
        <clipPath id="clip-header">
            <path d="M1 1 L449 1 L449 60 L1 60 Z" />
        </clipPath>
      </defs>

      <rect x="0.5" y="0.5" width="449" height="219" class="card-bg" />
      
      <rect x="1" y="1" width="448" height="8" rx="14" fill="url(#grad1)" clip-path="url(#clip-header)" />
      
      <text x="25" y="50" class="title">{name}</text>
      
      <text x="25" y="80" class="desc">{desc}</text>
      
      <line x1="25" y1="100" x2="425" y2="100" stroke="#30363d" stroke-width="1" />
      
      <text x="25" y="130" class="label">MAIN LANGUAGE</text>
      <text x="25" y="150" class="value" style="fill:#58a6ff;">● {language}</text>
      
      <text x="220" y="130" class="label">LAST UPDATE (RO)</text>
      <text x="220" y="150" class="value">{time_str}</text>
      
      <text x="25" y="185" class="label">STARS</text>
      <text x="25" y="205" class="value">★ {stars}</text>
      
      <text x="100" y="185" class="label">FORKS</text>
      <text x="100" y="205" class="value">⑂ {forks}</text>
      
      <text x="360" y="205" font-size="10" fill="#30363d">andzcr bot</text>
      
    </svg>
    """
    
    with open("last_project.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)

if __name__ == "__main__":
    repo = get_last_updated_repo()
    create_svg(repo)
