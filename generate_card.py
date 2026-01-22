import requests
import datetime
from datetime import timedelta
from collections import defaultdict

# CONFIGURARE
USERNAME = "andzcr"
TOKEN = "" # Lasa gol daca nu ai token, dar API-ul are limite (60 requests/ora). 
# Daca ai erori de limita, iti arat cum sa pui un token.

def get_data():
    headers = {}
    if TOKEN:
        headers['Authorization'] = f"token {TOKEN}"
        
    # Luam repo-urile (pana la 100 pt statistica)
    url = f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&direction=desc&per_page=100"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return None, None
        
    repos = response.json()
    if not repos:
        return None, None
        
    # 1. Date pentru Ultimul Proiect (Primul din lista)
    last_repo = repos[0]
    
    # 2. Calculam Top Limbaje din toate repo-urile
    langs = defaultdict(int)
    total_size = 0
    
    for repo in repos:
        if repo['language']:
            # Folosim marimea repo-ului ca aproximare pentru cat cod e scris
            langs[repo['language']] += repo['size']
            total_size += repo['size']
            
    # Sortam si luam top 4
    top_langs = sorted(langs.items(), key=lambda x: x[1], reverse=True)[:4]
    
    # Convertim in procente
    stats = []
    if total_size > 0:
        for l, size in top_langs:
            percent = (size / total_size) * 100
            stats.append((l, percent))
            
    return last_repo, stats

def create_left_card(repo):
    # CARD 1: LAST PROJECT (FOCUS)
    if not repo: return

    name = repo['name']
    desc = repo['description'] if repo['description'] else "Top secret project."
    if len(desc) > 50: desc = desc[:47] + "..."
    
    last_push_utc = datetime.datetime.strptime(repo['pushed_at'], "%Y-%m-%dT%H:%M:%SZ")
    last_push_ro = last_push_utc + timedelta(hours=2)
    time_str = last_push_ro.strftime("%H:%M")
    date_str = last_push_ro.strftime("%d %b")

    svg = f"""
    <svg width="400" height="200" viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
      <style>
        .bg {{ fill: #0d1117; stroke: #2f80ed; stroke-width: 2px; rx: 10px; }}
        .text {{ font-family: 'Courier New', monospace; fill: #fff; }}
        .label {{ font-size: 10px; fill: #8b949e; }}
        .title {{ font-size: 18px; font-weight: bold; fill: #58a6ff; }}
        .desc {{ font-size: 12px; fill: #c9d1d9; }}
        
        /* Animatie Puls */
        @keyframes pulse {{
            0% {{ opacity: 0.5; r: 3; }}
            50% {{ opacity: 1; r: 5; }}
            100% {{ opacity: 0.5; r: 3; }}
        }}
        .status-dot {{ fill: #3fb950; animation: pulse 2s infinite; }}
        
        /* Animatie Linie */
        @keyframes scan {{
            0% {{ width: 0; }}
            100% {{ width: 100px; }}
        }}
        .loading-line {{ stroke: #58a6ff; stroke-width: 2; stroke-dasharray: 100; stroke-dashoffset: 100; animation: scan 1.5s forwards; }}
      </style>
      
      <rect width="398" height="198" x="1" y="1" class="bg" />
      
      <circle cx="20" cy="25" r="4" class="status-dot" />
      <text x="35" y="28" class="text" font-size="12" fill="#3fb950">ACTIVE SESSION</text>
      <text x="320" y="28" class="text" font-size="12" fill="#8b949e">{time_str}</text>
      
      <text x="20" y="70" class="label">CURRENT MISSION</text>
      <text x="20" y="95" class="text title">{name}</text>
      <text x="20" y="115" class="text desc">{desc}</text>
      
      <line x1="20" y1="140" x2="380" y2="140" stroke="#30363d" />
      
      <text x="20" y="165" class="label">LAST COMMIT</text>
      <text x="20" y="180" class="text" font-size="12">{date_str} @ {time_str}</text>
      
      <text x="250" y="165" class="label">STATUS</text>
      <text x="250" y="180" class="text" font-size="12" fill="#3fb950">IN PROGRESS...</text>
    </svg>
    """
    with open("card_left.svg", "w", encoding="utf-8") as f: f.write(svg)

def create_right_card(stats):
    # CARD 2: ARSENAL (STATS)
    if not stats: return

    # Generam barele de progres dinamic
    bars_svg = ""
    y_pos = 60
    colors = ["#f1e05a", "#3178c6", "#e34c26", "#563d7c"] # Galben, Albastru, Rosu, Mov
    
    for i, (lang, pct) in enumerate(stats):
        color = colors[i % len(colors)]
        width = int((pct / 100) * 200) # Max width 200px
        
        bars_svg += f"""
        <text x="20" y="{y_pos}" class="text" font-size="12">{lang}</text>
        <text x="330" y="{y_pos}" class="text" font-size="12" text-anchor="end">{int(pct)}%</text>
        
        <rect x="20" y="{y_pos + 5}" width="200" height="6" rx="3" fill="#30363d" />
        <rect x="20" y="{y_pos + 5}" width="0" height="6" rx="3" fill="{color}">
            <animate attributeName="width" from="0" to="{width}" dur="1s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1" />
        </rect>
        """
        y_pos += 35

    svg = f"""
    <svg width="400" height="200" viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
      <style>
        .bg {{ fill: #0d1117; stroke: #a371f7; stroke-width: 2px; rx: 10px; }} 
        /* Stroke mov pentru contrast cu celalalt card */
        .text {{ font-family: 'Courier New', monospace; fill: #fff; }}
        .header {{ font-size: 14px; font-weight: bold; fill: #a371f7; }}
      </style>
      
      <rect width="398" height="198" x="1" y="1" class="bg" />
      
      <text x="20" y="30" class="header">/// SKILL_ARSENAL_ANALYSIS</text>
      <line x1="20" y1="40" x2="380" y2="40" stroke="#30363d" />
      
      {bars_svg}
      
    </svg>
    """
    with open("card_right.svg", "w", encoding="utf-8") as f: f.write(svg)

if __name__ == "__main__":
    repo, stats = get_data()
    create_left_card(repo)
    create_right_card(stats)
