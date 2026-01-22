import requests
import datetime
from datetime import timedelta

USERNAME = "andzcr"

def get_latest_activity():
    # 1. Luam ultimul repo editat
    repos_url = f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&direction=desc"
    try:
        r = requests.get(repos_url)
        if r.status_code != 200 or not r.json(): return None
        repo = r.json()[0]
    except: return None

    # 2. Luam ultimul COMMIT din acel repo (pentru mesaj si autor)
    commits_url = f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits"
    try:
        c = requests.get(commits_url)
        latest_commit = c.json()[0] if c.status_code == 200 and c.json() else None
    except: latest_commit = None

    return repo, latest_commit

def get_time_context(hour):
    if 5 <= hour < 12: return "MORNING RUN"
    elif 12 <= hour < 18: return "DAY SESSION"
    elif 18 <= hour < 22: return "EVENING GRIND"
    else: return "NIGHT OPS ☾" # Pentru coding noaptea

def create_hud(repo, commit):
    if not repo: return

    # Date de baza
    repo_name = repo['name'].upper()
    language = repo['language'] if repo['language'] else "RAW DATA"
    
    # Date Commit
    if commit:
        message = commit['commit']['message'].split('\n')[0] # Luam doar prima linie
        # Curatam mesajul sa nu fie prea lung
        if len(message) > 40: message = message[:37] + "..."
        sha = commit['sha'][:7] # Scurtul hash (ex: a1b2c3d)
    else:
        message = "No commit details"
        sha = "UNKNOWN"

    # Timp
    last_push_utc = datetime.datetime.strptime(repo['pushed_at'], "%Y-%m-%dT%H:%M:%SZ")
    last_push_ro = last_push_utc + timedelta(hours=2)
    time_str = last_push_ro.strftime("%H:%M")
    date_str = last_push_ro.strftime("%d.%m.%Y")
    session_type = get_time_context(last_push_ro.hour)

    # Culoare dinamica in functie de limbaj (poti adauga altele)
    colors = {
        "Python": "#3572A5", "JavaScript": "#f1e05a", "HTML": "#e34c26", 
        "CSS": "#563d7c", "Java": "#b07219", "C++": "#f34b7d"
    }
    accent = colors.get(language, "#00f0ff") # Cyan default

    svg = f"""
    <svg width="800" height="300" viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&amp;display=swap');
            .txt {{ font-family: 'Share Tech Mono', monospace; fill: {accent}; text-transform: uppercase; }}
            .dim {{ fill: rgba(255,255,255,0.4); }}
            .white {{ fill: #fff; }}
            
            /* ANIMATII LIVE */
            
            /* 1. Cercul care se invarte (Reactor) */
            @keyframes spin {{ 
                from {{ transform: rotate(0deg); transform-origin: 150px 150px; }} 
                to {{ transform: rotate(360deg); transform-origin: 150px 150px; }} 
            }}
            .reactor {{ animation: spin 10s linear infinite; }}
            
            /* 2. Cercul opus */
            @keyframes spin-back {{ 
                from {{ transform: rotate(360deg); transform-origin: 150px 150px; }} 
                to {{ transform: rotate(0deg); transform-origin: 150px 150px; }} 
            }}
            .reactor-outer {{ animation: spin-back 15s linear infinite; opacity: 0.5; }}

            /* 3. Blink Effect pentru cursor */
            @keyframes blink {{ 50% {{ opacity: 0; }} }}
            .cursor {{ animation: blink 1s step-end infinite; fill: {accent}; }}
            
            /* 4. Slide in pentru text */
            @keyframes slide {{ from {{ x: 350; opacity: 0; }} to {{ x: 320; opacity: 1; }} }}
            .slide-text {{ animation: slide 1s ease-out forwards; }}
            
            /* Background Grid */
            .grid {{ stroke: rgba(255,255,255,0.05); stroke-width: 1; }}
        </style>
        
        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:rgba(10,10,20,1);stop-opacity:1" />
            <stop offset="100%" style="stop-color:rgba(20,20,40,1);stop-opacity:1" />
        </linearGradient>
      </defs>

      <rect width="800" height="300" rx="15" fill="url(#grad)" stroke="{accent}" stroke-width="2" stroke-opacity="0.3"/>
      
      <line x1="0" y1="50" x2="800" y2="50" class="grid" />
      <line x1="0" y1="150" x2="800" y2="150" class="grid" />
      <line x1="0" y1="250" x2="800" y2="250" class="grid" />
      
      <circle cx="150" cy="150" r="40" stroke="{accent}" stroke-width="2" fill="none" stroke-dasharray="10 5" class="reactor" />
      <circle cx="150" cy="150" r="70" stroke="{accent}" stroke-width="1" fill="none" stroke-dasharray="40 10" class="reactor-outer" />
      <text x="150" y="155" text-anchor="middle" class="txt white" font-size="14" font-weight="bold">LIVE</text>
      
      <text x="320" y="60" class="txt dim" font-size="12">ACTIVE PROJECT // {session_type}</text>
      <text x="320" y="90" class="txt white slide-text" font-size="32" filter="url(#glow)">{repo_name}</text>
      
      <text x="320" y="140" class="txt dim" font-size="12">LAST TRANSMISSION (COMMIT {sha})</text>
      <text x="320" y="165" class="txt" font-size="18">
         > {message}<tspan class="cursor">_</tspan>
      </text>
      
      <line x1="320" y1="200" x2="750" y2="200" stroke="{accent}" stroke-width="1" stroke-opacity="0.3" />
      
      <text x="320" y="230" class="txt dim" font-size="12">LANGUAGE</text>
      <text x="320" y="250" class="txt white" font-size="16">{language}</text>
      
      <text x="450" y="230" class="txt dim" font-size="12">TIMESTAMP (RO)</text>
      <text x="450" y="250" class="txt white" font-size="16">{date_str} {time_str}</text>
      
      <text x="600" y="230" class="txt dim" font-size="12">SYSTEM</text>
      <text x="600" y="250" class="txt" font-size="16" fill="#0f0">ONLINE</text>
      
    </svg>
    """
    
    with open("hud_card.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    r, c = get_latest_activity()
    create_hud(r, c)
