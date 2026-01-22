import requests
import datetime
from datetime import timedelta

# CONFIGURARE
USERNAME = "andzcr"

def get_data():
    # 1. Luam repo-urile
    try:
        url = f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&direction=desc"
        r = requests.get(url)
        if r.status_code != 200 or not r.json(): return None, None
        repo = r.json()[0]
    except: return None, None

    # 2. Luam ultimul commit pentru detalii
    try:
        c_url = f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits"
        c = requests.get(c_url)
        commit = c.json()[0] if c.status_code == 200 and c.json() else None
    except: commit = None
    
    return repo, commit

def create_ios_card(repo, commit):
    if not repo: return

    # --- DATA PROCESSING ---
    name = repo['name']
    language = repo['language'] if repo['language'] else "Unknown"
    
    if commit:
        msg = commit['commit']['message'].split('\n')[0]
        if len(msg) > 45: msg = msg[:42] + "..."
    else:
        msg = "No details available"

    # Time Logic (Romania UTC+2)
    last_push_utc = datetime.datetime.strptime(repo['pushed_at'], "%Y-%m-%dT%H:%M:%SZ")
    last_push_ro = last_push_utc + timedelta(hours=2)
    
    now_utc = datetime.datetime.utcnow()
    now_ro = now_utc + timedelta(hours=2)
    
    # Calculam diferenta
    diff = now_ro - last_push_ro
    minutes_diff = diff.total_seconds() / 60
    
    # STATUS LOGIC
    if minutes_diff < 45: # Consideram activ daca a dat push in ultimele 45 min
        is_online = True
        status_text = "Active Now"
        status_color = "#30d158" # Apple Green
        status_sub = "Coding..."
    else:
        is_online = False
        time_str = last_push_ro.strftime("%H:%M")
        status_text = "Offline"
        status_color = "#8e8e93" # Apple Grey
        status_sub = f"Since {time_str}"

    last_update_str = last_push_ro.strftime("%d %b")

    # --- SVG DESIGN (Apple Glassmorphism) ---
    svg = f"""
    <svg width="450" height="240" viewBox="0 0 450 240" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <style>
            .sf-font {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
            .glass {{ fill: rgba(22, 22, 23, 0.9); stroke: rgba(255, 255, 255, 0.15); stroke-width: 1; }}
            
            /* Status Pulse Animation (Doar daca e online) */
            @keyframes pulse {{
                0% {{ box-shadow: 0 0 0 0 rgba(48, 209, 88, 0.7); opacity: 1; }}
                100% {{ box-shadow: 0 0 0 10px rgba(48, 209, 88, 0); opacity: 0.5; }}
            }}
            .pulse-circle {{ animation: {'pulse 2s infinite' if is_online else 'none'}; }}
            
            /* Text Colors */
            .text-white {{ fill: #ffffff; }}
            .text-grey {{ fill: #86868b; }}
            .text-accent {{ fill: #0a84ff; }} /* Apple Blue */
        </style>
        
        <linearGradient id="bg-grad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style="stop-color:#1c1c1e;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
        </linearGradient>
      </defs>

      <rect x="2" y="2" width="446" height="236" rx="26" fill="url(#bg-grad)" stroke="#3a3a3c" stroke-width="1" />
      
      <circle cx="35" cy="35" r="5" fill="{status_color}" class="pulse-circle" />
      <text x="50" y="39" class="sf-font text-white" font-size="14" font-weight="600">{status_text}</text>
      <text x="415" y="39" class="sf-font text-grey" font-size="12" text-anchor="end">{status_sub}</text>
      
      <line x1="25" y1="60" x2="425" y2="60" stroke="#3a3a3c" stroke-width="1" />

      <text x="35" y="90" class="sf-font text-grey" font-size="11" font-weight="500" letter-spacing="0.5">LATEST WORKSPACE</text>
      
      <text x="35" y="120" class="sf-font text-white" font-size="24" font-weight="700">{name}</text>
      
      <g transform="translate(35, 145)">
         <rect x="0" y="0" width="380" height="30" rx="8" fill="#2c2c2e" />
         <text x="10" y="20" class="sf-font" fill="#d1d1d6" font-size="13" font-family="monospace">git commit -m "{msg}"</text>
      </g>
      
      <rect x="35" y="190" width="100" height="24" rx="12" fill="rgba(10, 132, 255, 0.2)" stroke="rgba(10, 132, 255, 0.5)" />
      <text x="85" y="206" class="sf-font" fill="#0a84ff" font-size="12" font-weight="600" text-anchor="middle">{language}</text>
      
      <text x="415" y="206" class="sf-font text-grey" font-size="12" text-anchor="end">Updated on {last_update_str}</text>
      
    </svg>
    """
    
    with open("ios_card.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    r, c = get_data()
    create_ios_card(r, c)
