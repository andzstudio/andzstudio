import requests
import datetime
from datetime import timedelta
import html

# CONFIGURARE
USERNAME = "andzcr"
# Nu mai avem nevoie de link extern pentru logo, folosim vectori interni.

def get_data():
    try:
        # Timeout redus pentru rapiditate
        url = f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&direction=desc"
        r = requests.get(url, timeout=5)
        if r.status_code != 200 or not r.json(): return None, None
        repo = r.json()[0]
        
        c_url = f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits"
        c = requests.get(c_url, timeout=5)
        commit = c.json()[0] if c.status_code == 200 and c.json() else None
        return repo, commit
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def create_nebula_card(repo, commit):
    if not repo: return

    # --- DATA PROCESSING ---
    name = html.escape(repo['name'])
    language = html.escape(repo['language']) if repo['language'] else "N/A"
    
    if commit:
        msg = commit['commit']['message'].split('\n')[0]
        if len(msg) > 45: msg = msg[:42] + "..."
        msg = html.escape(msg)
        sha = commit['sha'][:6]
    else:
        msg = "System initialized."
        sha = "INIT"

    # Time Logic (UTC+2)
    last_push_utc = datetime.datetime.strptime(repo['pushed_at'], "%Y-%m-%dT%H:%M:%SZ")
    last_push_ro = last_push_utc + timedelta(hours=2)
    now_ro = datetime.datetime.utcnow() + timedelta(hours=2)
    minutes_diff = (now_ro - last_push_ro).total_seconds() / 60
    
    # --- DYNAMIC THEME LOGIC ---
    # 45 minute window pentru "Online"
    if minutes_diff < 45:
        is_online = True
        theme_color = "#00f2ff" # Neon Cyan (Online)
        secondary_color = "#0066ff"
        status_text = "NEBULA CORE: ONLINE"
        status_sub = "Uplink active. Systems optimal."
        # Animatie rapida si stralucitoare
        bg_anim_dur = "15s"
        pulse_anim = """<animate attributeName="r" values="3;5;3" dur="1.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0.7;1" dur="1.5s" repeatCount="indefinite"/>"""
        glow_filter = "url(#cyan-glow)"
    else:
        is_online = False
        theme_color = "#bd00ff" # Deep Violet (Offline)
        secondary_color = "#6a00ff"
        time_str = last_push_ro.strftime("%H:%M")
        status_text = "NEBULA CORE: IDLE"
        status_sub = f"Last transmission at {time_str}"
        # Animatie lenta si calma
        bg_anim_dur = "30s"
        pulse_anim = """<animate attributeName="opacity" values="0.6;0.3;0.6" dur="4s" repeatCount="indefinite"/>"""
        glow_filter = "none"

    last_date_nice = last_push_ro.strftime("%d %b %Y")

    # --- THE ULTIMATE SVG ---
    svg = f"""
    <svg width="550" height="280" viewBox="0 0 550 280" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <style>
            .sf {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
            .mono {{ font-family: 'SF Mono', 'Fira Code', Consolas, monospace; }}
            .t-accent {{ fill: {theme_color}; }}
            .t-white {{ fill: #ffffff; }}
            .t-dim {{ fill: rgba(255,255,255,0.6); }}
            
            /* ANIMATII CSS */
            /* 1. Background Lichid */
            @keyframes moveTheme {{ 
                0% {{ stop-color: {theme_color}; }} 50% {{ stop-color: {secondary_color}; }} 100% {{ stop-color: {theme_color}; }} 
            }}
            .anim-stop {{ animation: moveTheme {bg_anim_dur} infinite linear; }}
            
            /* 2. Levitatie Card */
            @keyframes float {{ 0% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-6px); }} 100% {{ transform: translateY(0px); }} }}
            .floating {{ animation: float 6s ease-in-out infinite; }}
        </style>
        
        <linearGradient id="nebula-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0a0a0a" />
            <stop offset="50%" class="anim-stop" stop-opacity="0.3" />
            <stop offset="100%" stop-color="#0a0a0a" />
        </linearGradient>
        
        <filter id="cyan-glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
            <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>

        <path id="git-icon" d="M10 0a10 10 0 0 0-3.16 19.49c.5.1.68-.22.68-.48l-.01-1.7c-2.78.6-3.37-1.34-3.37-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.89 1.52 2.34 1.08 2.91.83.1-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.94 0-1.1.39-1.99 1.03-2.69a3.6 3.6 0 0 1 .1-2.64s.84-.27 2.75 1.02a9.58 9.58 0 0 1 5 0c1.91-1.29 2.75-1.02 2.75-1.02.55 1.37.2 2.3.1 2.64.64.7 1.03 1.6 1.03 2.69 0 3.84-2.33 4.68-4.56 4.93.36.31.68.92.68 1.85l-.01 2.75c0 .26.18.58.69.48A10 10 0 0 0 10 0z"/>
      </defs>

      <rect width="550" height="280" rx="30" fill="#050508" />
      <rect width="550" height="280" rx="30" fill="url(#nebula-bg)" opacity="0.6" />
      
      <g class="floating">
          <rect x="2" y="2" width="546" height="276" rx="28" fill="none" stroke="{theme_color}" stroke-width="1.5" stroke-opacity="0.3" />
          
          <g transform="translate(30, 30)">
              <circle cx="20" cy="20" r="20" fill="rgba(255,255,255,0.1)" stroke="{theme_color}" stroke-width="2"/>
              <text x="20" y="27" text-anchor="middle" class="sf t-accent" font-weight="bold" font-size="18">A</text>
              <circle cx="35" cy="35" r="5" fill="{theme_color}" filter="{glow_filter}">{pulse_anim}</circle>
          </g>
          
          <g transform="translate(85, 45)">
              <text class="sf t-accent" font-size="12" font-weight="bold" letter-spacing="1">{status_text}</text>
              <text y="18" class="sf t-dim" font-size="11">{status_sub}</text>
          </g>
          
          <text x="520" y="45" text-anchor="end" class="mono t-dim" font-size="10" letter-spacing="2">/// ANDZ.OS_NEBULA_BUILD_v4</text>
          
          <g transform="translate(30, 120)">
              <text class="sf t-dim" font-size="10" font-weight="600" letter-spacing="1">ACTIVE NEURAL PATHWAY</text>
              <text y="35" class="sf t-white" font-size="32" font-weight="800" letter-spacing="-0.5" filter="{glow_filter}">{name}</text>
              
              <g transform="translate(0, 55)">
                 <rect width="490" height="40" rx="12" fill="rgba(0,0,0,0.3)" stroke="rgba(255,255,255,0.05)"/>
                 <g transform="translate(15, 25) scale(0.8)">
                    <use href="#git-icon" fill="{theme_color}"/>
                 </g>
                 <text x="45" y="24" class="mono t-dim" font-size="12">
                    <tspan fill="{theme_color}">[{sha}]</tspan> {msg}
                 </text>
              </g>
          </g>
          
          <g transform="translate(30, 245)">
              <circle cx="5" cy="-4" r="5" fill="{theme_color}" opacity="0.8"/>
              <text x="15" y="0" class="sf t-white" font-size="12" font-weight="600">{language}</text>
              
              <line x1="100" y1="-4" x2="130" y2="-4" stroke="rgba(255,255,255,0.1)"/>
              
              <text x="145" y="0" class="sf t-dim" font-size="12">Updated: {last_date_nice}</text>
          </g>
      </g></svg>
    """
    
    with open("nebula_card.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    r, c = get_data()
    create_nebula_card(r, c)
