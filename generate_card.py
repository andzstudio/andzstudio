import requests
import datetime
from datetime import timedelta
import html

# --- CONFIGURARE ---
USERNAME = "andzcr"

def get_data():
    try:
        # 1. Repo info
        url = f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&direction=desc"
        r = requests.get(url, timeout=10)
        if r.status_code != 200 or not r.json(): return None, None
        repo = r.json()[0]
        
        # 2. Commit info
        c_url = f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits"
        c = requests.get(c_url, timeout=10)
        commit = c.json()[0] if c.status_code == 200 and c.json() else None
        return repo, commit
    except:
        return None, None

def create_apple_dashboard(repo, commit):
    if not repo: return

    # --- DATE ---
    name = html.escape(repo['name'])
    desc = html.escape(repo['description']) if repo['description'] else "No description provided."
    if len(desc) > 60: desc = desc[:57] + "..."
    
    language = html.escape(repo['language']) if repo['language'] else "Plain Text"
    
    if commit:
        msg = commit['commit']['message'].split('\n')[0]
        if len(msg) > 50: msg = msg[:48] + "..."
        msg = html.escape(msg)
    else:
        msg = "Initial commit"

    # Time & Status Logic
    last_push_utc = datetime.datetime.strptime(repo['pushed_at'], "%Y-%m-%dT%H:%M:%SZ")
    last_push_ro = last_push_utc + timedelta(hours=2)
    now_ro = datetime.datetime.utcnow() + timedelta(hours=2)
    
    diff_minutes = (now_ro - last_push_ro).total_seconds() / 60
    
    # STATUS APPLE STYLE
    if diff_minutes < 45: # Active in last 45 mins
        status_text = "Active Now"
        status_color = "#30D158" # Apple Green
        sub_text = "Writing code..."
        opacity_pulse = "1"
    else:
        status_text = "Offline"
        status_color = "#8E8E93" # Apple Gray
        sub_text = f"Seen {last_push_ro.strftime('%H:%M')}"
        opacity_pulse = "0.5"

    current_time = now_ro.strftime("%H:%M")
    date_str = now_ro.strftime("%A, %d %B")

    # --- SVG DESIGN: iOS DASHBOARD ---
    svg = f"""
    <svg width="800" height="250" viewBox="0 0 800 250" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <style>
            /* System Fonts mimicking Apple San Francisco */
            .sf-pro {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
            .bold {{ font-weight: 700; }}
            .medium {{ font-weight: 500; }}
            .regular {{ font-weight: 400; }}
            
            /* Colors */
            .bg-card {{ fill: #1C1C1E; }} /* iOS Dark Surface */
            .border {{ stroke: rgba(255,255,255,0.1); stroke-width: 1; }}
            .text-primary {{ fill: #FFFFFF; }}
            .text-secondary {{ fill: #98989D; }}
            .text-accent {{ fill: #0A84FF; }} /* Apple Blue */
            
            /* Status Animation */
            @keyframes pulse {{
                0% {{ opacity: 1; r: 4; }}
                50% {{ opacity: 0.6; r: 5; }}
                100% {{ opacity: 1; r: 4; }}
            }}
            .dot-anim {{ animation: pulse 3s infinite ease-in-out; }}
        </style>
        
        <rect id="widget-shape" width="240" height="220" rx="22" />
        <rect id="wide-widget-shape" width="500" height="220" rx="22" />
      </defs>

      <g transform="translate(10, 15)">
          <rect width="240" height="220" rx="22" class="bg-card border" />
          
          <circle cx="30" cy="30" r="4" fill="{status_color}" class="{ 'dot-anim' if diff_minutes < 45 else '' }" />
          <text x="45" y="34" class="sf-pro medium text-secondary" font-size="12">{status_text}</text>
          
          <text x="120" y="110" class="sf-pro bold text-primary" font-size="48" text-anchor="middle" letter-spacing="-1">{current_time}</text>
          <text x="120" y="135" class="sf-pro medium text-accent" font-size="14" text-anchor="middle">{date_str}</text>
          
          <rect x="20" y="170" width="200" height="1" fill="#38383A" />
          <text x="120" y="195" class="sf-pro regular text-secondary" font-size="12" text-anchor="middle">{sub_text}</text>
      </g>

      <g transform="translate(270, 15)">
          <rect width="500" height="220" rx="22" class="bg-card border" />
          
          <text x="30" y="35" class="sf-pro medium text-secondary" font-size="11" letter-spacing="1">LATEST ACTIVITY</text>
          <g transform="translate(460, 30)">
             <path d="M5 0C2.2 0 0 2.2 0 5c0 2.2 1.4 4.1 3.4 4.8.2 0 .3-.1.3-.2v-.9c-1.4.3-1.7-.6-1.7-.6-.2-.6-.5-.8-.5-.8-.4-.3 0-.3 0-.3.5 0 .8.5.8.5.5.8 1.3.6 1.6.4.1-.4.2-.6.4-.8-1.1-.1-2.3-.6-2.3-2.5 0-.6.2-1 .5-1.4 0-.1-.2-.6.1-1.3 0 0 .4-.1 1.4.6.4-.1.9-.2 1.3-.2.4 0 .9.1 1.3.2 1-.7 1.4-.6 1.4-.6.3.7.1 1.2 0 1.3.3.4.5.8.5 1.4 0 1.9-1.2 2.4-2.3 2.5.2.2.4.6.4 1.2v1.8c0 .1.1.3.4.2C8.6 9.1 10 7.2 10 5c0-2.8-2.2-5-5-5z" fill="#38383A" transform="scale(2)"/>
          </g>
          
          <text x="30" y="80" class="sf-pro bold text-primary" font-size="28">{name}</text>
          
          <rect x="30" y="100" width="{len(language)*8 + 20}" height="24" rx="12" fill="rgba(10, 132, 255, 0.15)" />
          <text x="{30 + (len(language)*8 + 20)/2}" y="116" class="sf-pro medium text-accent" font-size="12" text-anchor="middle">{language}</text>
          
          <text x="30" y="150" class="sf-pro regular text-secondary" font-size="14" width="440">{desc}</text>
          
          <g transform="translate(30, 185)">
              <rect width="440" height="1" fill="#38383A" />
              <text y="20" class="sf-pro regular text-secondary" font-size="12" font-family="monospace">git commit: <tspan class="text-primary">"{msg}"</tspan></text>
          </g>
      </g>
      
    </svg>
    """
    
    with open("ios_dashboard.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    r, c = get_data()
    create_apple_dashboard(r, c)
