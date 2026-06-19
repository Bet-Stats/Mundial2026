# -*- coding: utf-8 -*-
import json, os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.join(BASE_DIR, "src")
OUT_DIR  = os.path.join(BASE_DIR, "docs")
PART_DIR = os.path.join(OUT_DIR, "partidos")

sys.path.insert(0, SRC_DIR)
from teams_data import TEAMS, RANK, HIST, QUAL, RECENT_NOTE, PLAYERS, STYLE
from model import simulate_match
from extra_data import VENUE_WEATHER, REAL_SCORES as _STATIC_SCORES, H2H_WC

os.makedirs(PART_DIR, exist_ok=True)

# ── Fusionar marcadores estáticos + marcadores live (API) ────────────────────
REAL_SCORES = dict(_STATIC_SCORES)

_live_path = os.path.join(SRC_DIR, "scores_live.json")
if os.path.exists(_live_path):
    with open(_live_path, encoding="utf-8") as _f:
        _live = json.load(_f)
    for _key, _val in _live.get("scores", {}).items():
        _h, _a = _key.split("-")
        REAL_SCORES[(_h, _a)] = tuple(_val)
    print(f"  scores_live.json cargado — {len(_live.get('scores', {}))} resultados de la API")
# ────────────────────────────────────────────────────────────────────────────

with open(os.path.join(SRC_DIR, "matches.json"), encoding="utf-8") as f:
    MATCHES = json.load(f)

STADIUMS = {
"Mexico City": "Estadio Azteca (Ciudad de México)",
"Guadalajara": "Estadio Akron (Guadalajara)",
"Monterrey": "Estadio BBVA (Monterrey)",
"Toronto": "BMO Field (Toronto)",
"Vancouver": "BC Place (Vancouver)",
"San Francisco": "Levi's Stadium (Santa Clara, Bahía de SF)",
"Los Angeles": "SoFi Stadium (Inglewood, LA)",
"Seattle": "Lumen Field (Seattle)",
"New York/NJ": "MetLife Stadium (East Rutherford, NJ)",
"Boston": "Gillette Stadium (Foxborough, MA)",
"Philadelphia": "Lincoln Financial Field (Filadelfia)",
"Miami": "Hard Rock Stadium (Miami Gardens)",
"Atlanta": "Mercedes-Benz Stadium (Atlanta)",
"Houston": "NRG Stadium (Houston)",
"Dallas": "AT&T Stadium (Arlington, Dallas)",
"Kansas City": "Arrowhead Stadium (Kansas City)",
}

WEEKDAY_ES = {"Monday":"Lun","Tuesday":"Mar","Wednesday":"Mié","Thursday":"Jue",
              "Friday":"Vie","Saturday":"Sáb","Sunday":"Dom"}
MONTH_ES = {"01":"Ene","02":"Feb","03":"Mar","04":"Abr","05":"May","06":"Jun",
            "07":"Jul","08":"Ago","09":"Sep","10":"Oct","11":"Nov","12":"Dic"}

NAME_TO_CODE = {
"Mexico":"MEX","South Africa":"RSA","South Korea":"KOR","Czechia":"CZE",
"Canada":"CAN","Bosnia and Herzegovina":"BIH","Qatar":"QAT","Switzerland":"SUI",
"Brazil":"BRA","Morocco":"MAR","Haiti":"HAI","Scotland":"SCO",
"United States":"USA","Paraguay":"PAR","Australia":"AUS","Turkiye":"TUR",
"Germany":"GER","Curacao":"CUW","Ivory Coast":"CIV","Ecuador":"ECU",
"Netherlands":"NED","Japan":"JPN","Sweden":"SWE","Tunisia":"TUN",
"Belgium":"BEL","Egypt":"EGY","Iran":"IRN","New Zealand":"NZL",
"Spain":"ESP","Cape Verde":"CPV","Saudi Arabia":"KSA","Uruguay":"URU",
"France":"FRA","Senegal":"SEN","Iraq":"IRQ","Norway":"NOR",
"Argentina":"ARG","Algeria":"ALG","Austria":"AUT","Jordan":"JOR",
"Portugal":"POR","DR Congo":"COD","Uzbekistan":"UZB","Colombia":"COL",
"England":"ENG","Croatia":"CRO","Ghana":"GHA","Panama":"PAN",
}

HOST_CODES = {"MEX", "USA", "CAN"}

GROUPS_ORDER = sorted({m["group"] for m in MATCHES})
GROUP_CODES = {}
GROUP_MATCHES = {}
for _m in MATCHES:
    g = _m["group"]
    GROUP_MATCHES.setdefault(g, []).append(_m)
    for _nm in (_m["home"], _m["away"]):
        _c = NAME_TO_CODE[_nm]
        GROUP_CODES.setdefault(g, [])
        if _c not in GROUP_CODES[g]:
            GROUP_CODES[g].append(_c)
for g in GROUP_MATCHES:
    GROUP_MATCHES[g].sort(key=lambda x: x["num"])


def fmt_date_es(date_iso, weekday_co):
    y, m, d = date_iso.split("-")
    return f"{WEEKDAY_ES[weekday_co]} {int(d)} {MONTH_ES[m]} {y}"


def bar_class(p):
    if p >= 65: return ""
    if p >= 45: return "mid"
    if p >= 25: return "warn"
    return "danger"


def txt_class(p):
    if p >= 45: return "high"
    if p >= 15: return "mid"
    return "low"


def implied_odd(p):
    p = max(p, 1.0)
    return f"{100/p:.2f}"


def mrow(name, pct, extra_right=""):
    cls = bar_class(pct)
    barcls = f" {cls}" if cls else ""
    return f'''<div class="mrow">
        <div class="mrow-header">
          <span class="mrow-name">{name}</span>
          <div class="mrow-right">{extra_right}<span class="mrow-pct">{pct:.0f}%</span></div>
        </div>
        <div class="bar-track"><div class="bar-fill{barcls}" style="width:{pct:.0f}%"></div></div>
      </div>'''


def dc_row(label, pct):
    cls = txt_class(pct)
    barcls = bar_class(pct)
    barcls = f" {barcls}" if barcls else ""
    return f'''<div class="dc-row">
        <div class="dc-label">{label}</div>
        <div class="dc-bar"><div class="bar-track"><div class="bar-fill{barcls}" style="width:{pct:.0f}%"></div></div></div>
        <div class="dc-pct {cls}">{pct:.0f}%</div>
      </div>'''


CSS = """
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap');

  :root {
    --bg:       #0b0f14;
    --surface:  #131920;
    --card:     #19222d;
    --border:   #1f2d3d;
    --accent:   #00e5a0;
    --warn:     #f0b429;
    --danger:   #f05252;
    --text:     #e8edf3;
    --muted:    #6b7f96;
    --home:     #3fb6e0;
    --away:     #f0b429;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    line-height: 1.6;
    min-height: 100vh;
  }

  nav {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 12px 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    position: sticky;
    top: 0;
    z-index: 100;
  }
  .logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 18px;
    color: var(--accent);
    letter-spacing: -0.5px;
    margin-right: auto;
    text-decoration: none;
  }
  nav a { color: var(--muted); text-decoration: none; font-size: 13px; font-weight: 500; transition: color .2s; }
  nav a:hover { color: var(--text); }

  .hero {
    background: linear-gradient(160deg, #0f1922 0%, #0b1420 60%, #091018 100%);
    border-bottom: 1px solid var(--border);
    padding: 40px 24px 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 60% 50% at 50% 100%, rgba(0,229,160,.06) 0%, transparent 70%);
    pointer-events: none;
  }
  .competition-tag {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; font-weight: 500;
    color: var(--accent);
    background: rgba(0,229,160,.1);
    border: 1px solid rgba(0,229,160,.25);
    border-radius: 4px; padding: 3px 10px; margin-bottom: 20px;
    letter-spacing: .5px; text-transform: uppercase;
  }
  .matchup { display: flex; align-items: center; justify-content: center; gap: 24px; margin-bottom: 12px; }
  .team { display: flex; flex-direction: column; align-items: center; gap: 6px; }
  .team-flag { font-size: 52px; line-height: 1; }
  .team-name { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 22px; letter-spacing: -0.5px; }
  .team-name.home { color: var(--home); }
  .team-name.away { color: var(--away); }
  .vs { font-family: 'IBM Plex Mono', monospace; font-size: 13px; color: var(--muted); padding: 0 8px; }
  .match-meta { font-size: 13px; color: var(--muted); margin-top: 8px; }
  .match-meta span { color: var(--text); }

  .disclaimer {
    background: rgba(240,180,41,.07);
    border: 1px solid rgba(240,180,41,.2);
    border-radius: 8px; margin: 16px 24px; padding: 10px 16px;
    font-size: 12px; color: #c9a23a; display: flex; gap: 10px; align-items: flex-start;
  }
  .disclaimer-icon { flex-shrink: 0; margin-top: 1px; }

  .content { max-width: 820px; margin: 0 auto; padding: 24px 16px 60px; display: flex; flex-direction: column; gap: 20px; }

  .section-label {
    font-family: 'IBM Plex Mono', monospace; font-size: 10px; font-weight: 500;
    letter-spacing: 1.5px; text-transform: uppercase; color: var(--muted);
    margin-bottom: 12px; display: flex; align-items: center; gap: 10px;
  }
  .section-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }

  .card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 18px 20px; }
  .card-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 15px; margin-bottom: 14px; display: flex; align-items: center; gap: 8px; }
  .card-title .icon { font-size: 16px; }

  .result-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }
  .result-cell { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 14px 10px; text-align: center; }
  .result-cell.highlight { border-color: var(--accent); background: rgba(0,229,160,.06); }
  .result-label { font-size: 11px; color: var(--muted); margin-bottom: 4px; font-weight: 500; }
  .result-pct { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 26px; }
  .result-pct.high { color: var(--accent); }
  .result-pct.mid  { color: var(--warn); }
  .result-pct.low  { color: var(--muted); }
  .result-odd { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: var(--muted); margin-top: 3px; }

  .market-row { display: flex; flex-direction: column; gap: 10px; }
  .mrow { display: flex; flex-direction: column; gap: 4px; }
  .mrow-header { display: flex; justify-content: space-between; align-items: center; font-size: 13px; }
  .mrow-name { font-weight: 500; }
  .mrow-right { display: flex; align-items: center; gap: 10px; font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: var(--muted); }
  .mrow-pct { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 15px; color: var(--text); min-width: 40px; text-align: right; }
  .bar-track { height: 6px; background: var(--border); border-radius: 99px; overflow: hidden; }
  .bar-fill { height: 100%; border-radius: 99px; background: var(--accent); transition: width .8s cubic-bezier(.4,0,.2,1); }
  .bar-fill.warn { background: var(--warn); }
  .bar-fill.danger { background: var(--danger); }
  .bar-fill.mid { background: #5b8af0; }

  .corners-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 16px; }
  .corner-cell { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 14px 14px; display: flex; flex-direction: column; gap: 2px; }
  .corner-cell.hot { border-color: var(--accent); }
  .corner-label { font-size: 11px; color: var(--muted); }
  .corner-value { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 22px; }
  .corner-value.accent { color: var(--accent); }
  .corner-value.warn   { color: var(--warn); }
  .corner-sub { font-size: 11px; color: var(--muted); }

  .pill-list { display: flex; flex-wrap: wrap; gap: 8px; }
  .pill { display: flex; align-items: center; gap: 6px; background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 7px 12px; font-size: 13px; }

  .cards-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 16px; }

  .temporal-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px; margin-bottom: 8px; }
  .temp-cell { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 8px 4px 6px; text-align: center; position: relative; overflow: hidden; }
  .temp-fill { position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,229,160,.12); }
  .temp-label { font-family: 'IBM Plex Mono', monospace; font-size: 9px; color: var(--muted); margin-bottom: 4px; position: relative; z-index: 1; }
  .temp-pct { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 13px; color: var(--accent); position: relative; z-index: 1; }

  .scores-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
  .score-cell { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 12px 10px; text-align: center; }
  .score-cell.top { border-color: var(--accent); }
  .score-result { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 18px; margin-bottom: 3px; }
  .score-pct { font-size: 12px; color: var(--accent); font-family: 'IBM Plex Mono', monospace; }

  .confidence-wrap { display: flex; flex-direction: column; gap: 6px; }
  .confidence-bar-track { height: 10px; background: var(--border); border-radius: 99px; overflow: hidden; }
  .confidence-bar-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #00e5a0, #5b8af0); }
  .confidence-labels { display: flex; justify-content: space-between; font-size: 11px; color: var(--muted); font-family: 'IBM Plex Mono', monospace; }

  .cs-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .cs-cell { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 14px; text-align: center; }
  .cs-flag { font-size: 28px; margin-bottom: 4px; }
  .cs-team { font-size: 11px; color: var(--muted); margin-bottom: 6px; }
  .cs-pct { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 24px; }

  .dc-list { display: flex; flex-direction: column; gap: 10px; }
  .dc-row { display: flex; align-items: center; gap: 12px; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px; }
  .dc-label { flex: 1; font-size: 13px; font-weight: 500; }
  .dc-pct { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 16px; min-width: 44px; text-align: right; }
  .dc-pct.high { color: var(--accent); }
  .dc-pct.mid  { color: var(--warn); }
  .dc-pct.low  { color: var(--muted); }
  .dc-bar { width: 80px; }

  .profile-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .profile-cell { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 14px; }
  .profile-head { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
  .profile-flag { font-size: 26px; }
  .profile-name { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 15px; }
  .profile-rank { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: var(--muted); margin-left: auto; }
  .profile-row { font-size: 12px; color: var(--muted); margin-bottom: 6px; line-height: 1.5; }
  .profile-row b { color: var(--text); font-weight: 600; }
  .profile-recent { font-size: 12px; color: var(--text); background: rgba(255,255,255,.03); border-radius: 6px; padding: 8px 10px; margin-top: 8px; }

  .sim-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 14px; }
  .sim-cell { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 14px; text-align: center; }
  .sim-label { font-size: 11px; color: var(--muted); margin-bottom: 4px; }
  .sim-value { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 20px; color: var(--accent); }

  /* ── Resultado real (partidos ya jugados) ── */
  .real-result-banner {
    background: linear-gradient(135deg, rgba(0,229,160,.10) 0%, rgba(91,138,240,.08) 100%);
    border: 1px solid rgba(0,229,160,.35); border-radius: 10px;
    padding: 16px 20px; text-align: center;
  }
  .real-result-tag {
    font-family: 'IBM Plex Mono', monospace; font-size: 10px; letter-spacing: 1.5px;
    text-transform: uppercase; color: var(--accent); margin-bottom: 8px;
  }
  .real-result-score {
    font-family: 'Syne', sans-serif; font-weight: 800; font-size: 42px;
    color: var(--text); line-height: 1; margin-bottom: 4px;
  }
  .real-result-sub { font-size: 12px; color: var(--muted); }

  /* ── Clima ── */
  .weather-row {
    display: flex; align-items: center; gap: 14px;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 12px 16px;
  }
  .weather-icon { font-size: 28px; flex-shrink: 0; }
  .weather-main { flex: 1; }
  .weather-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 14px; margin-bottom: 2px; }
  .weather-note { font-size: 12px; color: var(--muted); }
  .weather-pill {
    font-family: 'IBM Plex Mono', monospace; font-size: 11px; font-weight: 600;
    padding: 4px 10px; border-radius: 20px; flex-shrink: 0;
  }
  .weather-pill.hot { background: rgba(240,82,82,.15); color: #f05252; border: 1px solid rgba(240,82,82,.3); }
  .weather-pill.warm { background: rgba(240,180,41,.12); color: var(--warn); border: 1px solid rgba(240,180,41,.3); }
  .weather-pill.cool { background: rgba(0,229,160,.10); color: var(--accent); border: 1px solid rgba(0,229,160,.3); }

  /* ── H2H ── */
  .h2h-box {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 14px 16px;
  }
  .h2h-label { font-size: 11px; color: var(--muted); margin-bottom: 6px; font-family: 'IBM Plex Mono', monospace; text-transform: uppercase; letter-spacing: 1px; }
  .h2h-text { font-size: 13px; color: var(--text); line-height: 1.6; }

  footer { background: var(--surface); border-top: 1px solid var(--border); text-align: center; padding: 16px; font-size: 11px; color: var(--muted); }

  /* ── NAV: volver + menus desplegables ── */
  nav { flex-wrap: wrap; row-gap: 8px; }
  .back-btn { display: flex; align-items: center; gap: 4px; color: var(--muted); text-decoration: none; font-size: 13px; font-weight: 500; }
  .back-btn:hover { color: var(--text); }
  .nav-dd { position: relative; }
  .nav-dd summary {
    list-style: none; cursor: pointer; color: var(--muted);
    font-size: 13px; font-weight: 500; padding: 4px 2px; user-select: none;
  }
  .nav-dd summary::-webkit-details-marker { display: none; }
  .nav-dd summary::after { content: ' ▾'; font-size: 9px; }
  .nav-dd[open] summary, .nav-dd summary:hover { color: var(--text); }
  .nav-dd-panel {
    position: absolute; top: 26px; left: 0;
    background: var(--card); border: 1px solid var(--border); border-radius: 10px;
    padding: 10px; min-width: 250px; max-height: 380px; overflow-y: auto;
    box-shadow: 0 12px 30px rgba(0,0,0,.5); z-index: 300;
  }
  .nav-dd-panel.wide { min-width: 280px; }
  .nav-group-item { display: flex; flex-direction: column; padding: 6px 8px; border-radius: 6px; text-decoration: none; }
  .nav-group-item:hover { background: var(--surface); }
  .nav-group-item .g-name { color: var(--text); font-family: 'Syne', sans-serif; font-weight: 700; font-size: 13px; }
  .nav-group-item .g-countries { font-size: 11px; color: var(--muted); margin-top: 2px; line-height: 1.5; }
  .nav-match-header {
    font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: var(--accent);
    text-transform: uppercase; letter-spacing: 1px; margin: 10px 4px 4px;
  }
  .nav-match-header:first-child { margin-top: 2px; }
  .nav-match-item { display: block; padding: 5px 8px; border-radius: 6px; color: var(--text); text-decoration: none; font-size: 12px; }
  .nav-match-item:hover { background: var(--surface); }
  .nav-match-item .d { color: var(--muted); font-family: 'IBM Plex Mono', monospace; font-size: 10px; margin-right: 6px; }

  @media (max-width: 480px) {
    .result-grid { grid-template-columns: 1fr; }
    .corners-grid { grid-template-columns: 1fr; }
    .cards-row { grid-template-columns: 1fr; }
    .scores-grid { grid-template-columns: repeat(2,1fr); }
    .temporal-grid { grid-template-columns: repeat(3,1fr); }
    .cs-grid { grid-template-columns: 1fr 1fr; }
    .profile-grid { grid-template-columns: 1fr; }
    .sim-grid { grid-template-columns: 1fr 1fr; }
    .team-flag { font-size: 36px; }
    .team-name { font-size: 18px; }
    .nav-dd-panel { min-width: 200px; max-width: 86vw; }
  }
"""

def build_nav(context):
    """context: 'index' (estamos en index.html) o 'match' (estamos en partidos/x.html)"""
    if context == "index":
        logo_href = "index.html"
        anchor_prefix = ""              # -> "#grupo-A"
        match_prefix = "partidos/"      # -> "partidos/mex-vs-rsa.html"
        back_html = ""
    else:
        logo_href = "../index.html"
        anchor_prefix = "../index.html"  # -> "../index.html#grupo-A"
        match_prefix = ""                # archivos hermanos dentro de partidos/
        back_html = ('<a class="back-btn" href="../index.html" '
                     'onclick="if(window.history.length>1){history.back();return false;}">'
                     '&larr; Volver</a>')

    # --- Panel "Fase de grupos" ---
    group_items = ""
    for g in GROUPS_ORDER:
        countries = ", ".join(TEAMS[c]["name"] for c in GROUP_CODES[g])
        group_items += (f'<a class="nav-group-item" href="{anchor_prefix}#grupo-{g}">'
                         f'<span class="g-name">Grupo {g}</span>'
                         f'<span class="g-countries">{countries}</span></a>')
    groups_dd = f'''<details class="nav-dd">
    <summary>Fase de grupos</summary>
    <div class="nav-dd-panel">{group_items}</div>
  </details>'''

    # --- Panel "Partidos" (los 72) ---
    match_items = ""
    for g in GROUPS_ORDER:
        match_items += f'<div class="nav-match-header">Grupo {g}</div>'
        for m in GROUP_MATCHES[g]:
            hc, ac = NAME_TO_CODE[m["home"]], NAME_TO_CODE[m["away"]]
            d = m["date_co"][8:10] + "/" + m["date_co"][5:7]
            fn = filename_for(m)
            match_items += (f'<a class="nav-match-item" href="{match_prefix}{fn}">'
                             f'<span class="d">{d}</span>{hc} vs {ac}</a>')
    matches_dd = f'''<details class="nav-dd">
    <summary>Partidos</summary>
    <div class="nav-dd-panel wide">{match_items}</div>
  </details>'''

    return f'''<nav>
  <a class="logo" href="{logo_href}">⚽ BetStats</a>
  {back_html}
  {groups_dd}
  {matches_dd}
</nav>'''


FOOTER = '''<footer>
  Análisis estadístico de entretenimiento · BetStats no es una casa de apuestas ni presta asesoría financiera · Juega con responsabilidad
</footer>'''


def team_profile_cell(code, side_class, matchday):
    t = TEAMS[code]
    apps, last, best = HIST[code]
    host_tag = " · Anfitrión" if t.get("host") else ""
    if matchday == 1:
        ctx_label = "Clasificación"
        ctx_val = QUAL[code]
    else:
        ctx_label = "Resultado más reciente"
        ctx_val = RECENT_NOTE[code]
    return f'''<div class="profile-cell">
        <div class="profile-head">
          <span class="profile-flag">{t['flag']}</span>
          <span class="profile-name">{t['name']}</span>
          <span class="profile-rank">FIFA #{t['rank']}{host_tag}</span>
        </div>
        <div class="profile-row"><b>{ctx_label}:</b> {ctx_val}</div>
        <div class="profile-row"><b>Historial mundialista:</b> {apps} aparición, última en {last}</div>
        <div class="profile-row"><b>Mejor resultado:</b> {best}</div>
        <div class="profile-row"><b>Jugador clave:</b> {PLAYERS[code]}</div>
      </div>'''


def render_real_result(home_code, away_code, th, ta):
    """Bloque de resultado real si el partido ya se jugó."""
    score = REAL_SCORES.get((home_code, away_code)) or REAL_SCORES.get((away_code, home_code))
    if score is None:
        return ""
    # Si la clave estaba invertida, invertimos el marcador para mostrarlo correctamente
    if (away_code, home_code) in REAL_SCORES and (home_code, away_code) not in REAL_SCORES:
        score = (score[1], score[0])
    gh, ga = score
    if gh > ga:
        winner = f"{th['name']} venció"
        color = "var(--home)"
    elif ga > gh:
        winner = f"{ta['name']} venció"
        color = "var(--away)"
    else:
        winner = "Empate"
        color = "var(--muted)"
    return f'''<div class="section-label">Resultado real</div>
  <div class="card">
    <div class="real-result-banner">
      <div class="real-result-tag">✅ Partido ya disputado · Resultado oficial</div>
      <div class="real-result-score">{gh} – {ga}</div>
      <div class="real-result-sub" style="color:{color};font-weight:600">{winner}</div>
      <div class="real-result-sub" style="margin-top:6px">{th['flag']} {th['name']} {gh} – {ga} {ta['name']} {ta['flag']}</div>
    </div>
  </div>'''


def render_weather(city):
    """Sección de condiciones climáticas del estadio."""
    w = VENUE_WEATHER.get(city, {})
    if not w:
        return ""
    temp = w["temp_c"]
    roof = w["roof"]
    note = w["note_es"]
    if roof:
        icon = "🏟️"
        pill_cls = "cool"
        pill_txt = "Clima controlado"
    elif temp >= 33:
        icon = "🌡️"
        pill_cls = "hot"
        pill_txt = f"{temp} °C · Calor extremo"
    elif temp >= 27:
        icon = "☀️"
        pill_cls = "warm"
        pill_txt = f"{temp} °C · Calor"
    else:
        icon = "🌤️"
        pill_cls = "cool"
        pill_txt = f"{temp} °C · Condiciones cómodas"

    xg_note = ""
    if not roof and temp >= 33:
        xg_note = '<div style="font-size:11px;color:var(--muted);margin-top:8px">⚠️ El calor extremo al aire libre puede reducir el ritmo del partido y afectar los valores de xG esperados.</div>'
    return f'''<div class="section-label">Condiciones del estadio</div>
  <div class="card">
    <div class="card-title"><span class="icon">🌍</span> Clima y sede</div>
    <div class="weather-row">
      <div class="weather-icon">{icon}</div>
      <div class="weather-main">
        <div class="weather-title">{STADIUMS.get(city, city)}</div>
        <div class="weather-note">{note}</div>
      </div>
      <div class="weather-pill {pill_cls}">{pill_txt}</div>
    </div>{xg_note}
  </div>'''


def render_h2h(home_code, away_code, th, ta):
    """Sección de historial directo entre los dos equipos en Mundiales."""
    h2h = H2H_WC.get((home_code, away_code)) or H2H_WC.get((away_code, home_code), "Sin historial directo registrado en Mundiales.")
    return f'''<div class="section-label">Historial directo · Mundiales</div>
  <div class="card">
    <div class="card-title"><span class="icon">📜</span> {th['flag']} {th['name']} vs {ta['flag']} {ta['name']}</div>
    <div class="h2h-box">
      <div class="h2h-label">Antecedentes en Copa del Mundo</div>
      <div class="h2h-text">{h2h}</div>
    </div>
  </div>'''


def render_match_page(m):
    home_code = NAME_TO_CODE[m["home"]]
    away_code = NAME_TO_CODE[m["away"]]
    th, ta = TEAMS[home_code], TEAMS[away_code]
    host_home = th.get("host", False)
    host_away = ta.get("host", False)

    r = simulate_match(RANK[home_code], RANK[away_code], host_home, host_away,
                       seed_offset=m["num"],
                       style_home=STYLE[home_code], style_away=STYLE[away_code])

    date_str = fmt_date_es(m["date_co"], m["weekday_co"])
    stadium = STADIUMS.get(m["city"], m["city"])
    title = f"{home_code} vs {away_code} · Análisis de Apuestas · Mundial 2026"

    # --- HERO ---
    hero = f'''<div class="hero">
  <div class="competition-tag">Mundial 2026 · Grupo {m['group']} · Jornada {m['matchday']}</div>
  <div class="matchup">
    <div class="team">
      <div class="team-flag">{th['flag']}</div>
      <div class="team-name home">{home_code}</div>
    </div>
    <div class="vs">vs</div>
    <div class="team">
      <div class="team-flag">{ta['flag']}</div>
      <div class="team-name away">{away_code}</div>
    </div>
  </div>
  <div class="match-meta">{date_str} · <span>{m['time_co']}</span> hora Colombia · <span>{stadium}</span></div>
  <div class="match-meta" style="margin-top:4px">Modelo: Elo (ranking FIFA 11-jun-2026) + Poisson bivariado + Monte Carlo (50.000 sims)</div>
</div>'''

    disclaimer = '''<div class="disclaimer" style="max-width:820px;margin:16px auto;">
  <span class="disclaimer-icon">⚠️</span>
  <span>Análisis estadístico de entretenimiento generado por un modelo propio. No es asesoría financiera ni de apuestas. Las probabilidades son estimaciones y no garantizan resultado. Juega con responsabilidad.</span>
</div>'''

    # --- CONTEXTO Y DATOS REALES ---
    contexto = f'''<div class="section-label">Contexto y datos reales</div>
  <div class="card">
    <div class="card-title"><span class="icon">📋</span> Perfil de los equipos</div>
    <div class="profile-grid">
      {team_profile_cell(home_code, 'home', m['matchday'])}
      {team_profile_cell(away_code, 'away', m['matchday'])}
    </div>
  </div>'''

    # --- 1X2 ---
    x1 = f'''<div class="section-label">Resultado 1×2</div>
  <div class="card">
    <div class="card-title"><span class="icon">🏆</span> Ganador del partido</div>
    <div class="result-grid">
      <div class="result-cell highlight">
        <div class="result-label">{th['flag']} {home_code} gana</div>
        <div class="result-pct {txt_class(r['p_home'])}">{r['p_home']:.0f}%</div>
        <div class="result-odd">Cuota referencial: {implied_odd(r['p_home'])}</div>
      </div>
      <div class="result-cell">
        <div class="result-label">Empate</div>
        <div class="result-pct {txt_class(r['p_draw'])}">{r['p_draw']:.0f}%</div>
        <div class="result-odd">Cuota referencial: {implied_odd(r['p_draw'])}</div>
      </div>
      <div class="result-cell">
        <div class="result-label">{ta['flag']} {away_code} gana</div>
        <div class="result-pct {txt_class(r['p_away'])}">{r['p_away']:.0f}%</div>
        <div class="result-odd">Cuota referencial: {implied_odd(r['p_away'])}</div>
      </div>
    </div>
  </div>

  <div class="card">
    <div class="card-title"><span class="icon">🔄</span> Doble oportunidad</div>
    <div class="dc-list">
      {dc_row(f"{th['flag']} {home_code} o Empate (1X)", r['p_1x'])}
      {dc_row(f"{home_code} o {away_code} gana (12)", r['p_12'])}
      {dc_row(f"{ta['flag']} {away_code} o Empate (X2)", r['p_x2'])}
    </div>
  </div>'''

    # --- GOLES O/U ---
    goles = f'''<div class="section-label">Goles · Over / Under</div>
  <div class="card">
    <div class="card-title"><span class="icon">⚽</span> Líneas de goles</div>
    <div class="market-row">
      <div class="mrow">
        <div class="mrow-header">
          <span class="mrow-name">xG esperados totales</span>
          <div class="mrow-right"><span style="color:var(--accent);font-family:'Syne',sans-serif;font-weight:700;font-size:15px">{r['xg_total']:.2f}</span></div>
        </div>
      </div>
      {mrow("Over 1.5 goles", r['over_1.5'])}
      {mrow("Over 2.5 goles", r['over_2.5'])}
      {mrow("Under 2.5 goles", r['under_2.5'])}
      {mrow("Over 3.5 goles", r['over_3.5'])}
      {mrow("Over 4.5 goles", r['over_4.5'])}
    </div>
  </div>'''

    # --- CORNERS ---
    lo_c = max(0, round(r['corners_total'] - 1.5))
    hi_c = round(r['corners_total'] + 1.5)
    corners = f'''<div class="section-label">Corners</div>
  <div class="card">
    <div class="card-title"><span class="icon">📐</span> Corners · Over / Under</div>
    <div class="corners-grid">
      <div class="corner-cell hot">
        <div class="corner-label">Corners esperados</div>
        <div class="corner-value accent">{r['corners_total']:.1f}</div>
        <div class="corner-sub">promedio del modelo</div>
      </div>
      <div class="corner-cell hot">
        <div class="corner-label">Corners {home_code} esperados</div>
        <div class="corner-value accent">{r['corners_home']:.1f}</div>
        <div class="corner-sub">según dominio esperado</div>
      </div>
      <div class="corner-cell">
        <div class="corner-label">Corners {away_code} esperados</div>
        <div class="corner-value warn">{r['corners_away']:.1f}</div>
        <div class="corner-sub">según dominio esperado</div>
      </div>
      <div class="corner-cell">
        <div class="corner-label">Intervalo más probable</div>
        <div class="corner-value warn">{lo_c}–{hi_c}</div>
        <div class="corner-sub">rango central</div>
      </div>
    </div>
    <div class="market-row">
      {mrow("Over 5.5 corners", r['over_corners_5.5'])}
      {mrow("Over 7.5 corners", r['over_corners_7.5'])}
      {mrow("Over 9.5 corners", r['over_corners_9.5'])}
      {mrow("Under 9.5 corners", r['under_corners_9.5'])}
      {mrow("Over 11.5 corners", r['over_corners_11.5'])}
      {mrow(f"{home_code} más corners (Hándicap −1.5)", r['hcap_corners_home_-1.5'])}
    </div>
  </div>'''

    # --- TARJETAS ---
    cards = f'''<div class="section-label">Tarjetas</div>
  <div class="card">
    <div class="card-title"><span class="icon">🟨</span> Tarjetas · Over / Under</div>
    <div class="cards-row">
      <div class="corner-cell">
        <div class="corner-label">Tarjetas amarillas esperadas</div>
        <div class="corner-value warn">{r['cards_total']:.1f}</div>
        <div class="corner-sub">promedio del modelo</div>
      </div>
      <div class="corner-cell">
        <div class="corner-label">Prob. tarjeta roja</div>
        <div class="corner-value" style="color:var(--danger)">{r['red_prob']:.0f}%</div>
        <div class="corner-sub">en el partido</div>
      </div>
    </div>
    <div class="market-row">
      {mrow("Over 2.5 tarjetas", r['over_cards_2.5'])}
      {mrow("Over 3.5 tarjetas", r['over_cards_3.5'])}
      {mrow("Over 4.5 tarjetas", r['over_cards_4.5'])}
      {mrow("Al menos 1 tarjeta roja", r['red_prob'])}
    </div>
  </div>'''

    # --- FALTAS ---
    faltas = f'''<div class="section-label">Faltas</div>
  <div class="card">
    <div class="card-title"><span class="icon">🦵</span> Faltas totales</div>
    <div class="corner-cell" style="margin-bottom:12px">
      <div class="corner-label">Faltas esperadas totales</div>
      <div class="corner-value warn">{r['fouls_total']:.1f}</div>
      <div class="corner-sub">promedio del modelo</div>
    </div>
    <div class="market-row">
      {mrow("Over 19.5 faltas", r['over_fouls_19.5'])}
      {mrow("Over 21.5 faltas", r['over_fouls_21.5'])}
      {mrow("Over 25.5 faltas", r['over_fouls_25.5'])}
    </div>
  </div>'''

    # --- BTTS ---
    btts = f'''<div class="section-label">BTTS · Ambos marcan</div>
  <div class="card">
    <div class="card-title"><span class="icon">🎯</span> Ambos equipos anotan</div>
    <div class="market-row">
      {mrow("BTTS Sí (partido completo)", r['btts_yes'])}
      {mrow("BTTS No", r['btts_no'])}
      {mrow("BTTS Sí · 2da mitad", r['btts_2h'])}
      {mrow(f"{home_code} marca en 1ra mitad", r['home_scores_1h'])}
    </div>
  </div>'''

    # --- HANDICAP ---
    handicap = f'''<div class="section-label">Hándicap asiático</div>
  <div class="card">
    <div class="card-title"><span class="icon">⚖️</span> Hándicap ± goles</div>
    <div class="dc-list">
      {dc_row(f"{home_code} −1.5 (gana por 2+)", r['hcap_home_-1.5'])}
      {dc_row(f"{away_code} +1.5 (pierde por 1 o menos)", r['hcap_away_+1.5'])}
      {dc_row(f"{home_code} −2.5 (gana por 3+)", r['hcap_home_-2.5'])}
      {dc_row(f"{away_code} +2.5 (pierde por 2 o menos)", r['hcap_away_+2.5'])}
    </div>
  </div>'''

    # --- CLEAN SHEET ---
    cs = f'''<div class="section-label">Portería a cero · Clean Sheet</div>
  <div class="card">
    <div class="card-title"><span class="icon">🧤</span> Clean Sheet</div>
    <div class="cs-grid">
      <div class="cs-cell">
        <div class="cs-flag">{th['flag']}</div>
        <div class="cs-team">{home_code} no recibe</div>
        <div class="cs-pct" style="color:var(--accent)">{r['cs_home']:.0f}%</div>
      </div>
      <div class="cs-cell">
        <div class="cs-flag">{ta['flag']}</div>
        <div class="cs-team">{away_code} no recibe</div>
        <div class="cs-pct" style="color:var(--muted)">{r['cs_away']:.0f}%</div>
      </div>
    </div>
  </div>'''

    # --- TEMPORAL ---
    labels = ["1'–15'", "16'–30'", "31'–45'", "46'–60'", "61'–75'", "76'–90'"]
    cells = "".join(f'''<div class="temp-cell">
        <div class="temp-fill" style="height:{v:.0f}%"></div>
        <div class="temp-label">{lab}</div>
        <div class="temp-pct">{v:.0f}%</div>
      </div>''' for lab, v in zip(labels, r["temporal"]))
    temporal = f'''<div class="section-label">Distribución temporal de goles</div>
  <div class="card">
    <div class="card-title"><span class="icon">⏱️</span> Prob. de gol por intervalo de 15 min</div>
    <div class="temporal-grid">{cells}</div>
    <div style="font-size:11px;color:var(--muted)">Probabilidad de que caiga al menos un gol en ese intervalo, calibrada al xG del partido. Segunda mitad históricamente más prolífica en Mundiales.</div>
  </div>'''

    # --- MARCADORES EXACTOS ---
    score_cells = ""
    for i, (score, pct) in enumerate(r["top_scores"]):
        top_cls = " top" if i < 2 else ""
        score_cells += f'''<div class="score-cell{top_cls}">
        <div class="score-result">{score}</div>
        <div class="score-pct">{pct:.1f}%</div>
      </div>'''
    marcadores = f'''<div class="section-label">Marcadores exactos más probables</div>
  <div class="card">
    <div class="card-title"><span class="icon">📊</span> Top 6 resultados exactos (Monte Carlo)</div>
    <div class="scores-grid">{score_cells}</div>
  </div>'''

    # --- SIMULACIÓN MONTE CARLO (sección nueva, distinta de 1X2/marcadores) ---
    simulacion = f'''<div class="section-label">Simulación Monte Carlo</div>
  <div class="card">
    <div class="card-title"><span class="icon">🎲</span> Resultado de 50.000 partidos simulados</div>
    <div class="sim-grid">
      <div class="sim-cell">
        <div class="sim-label">Marcador promedio simulado</div>
        <div class="sim-value">{r['avg_home_goals']:.2f} – {r['avg_away_goals']:.2f}</div>
      </div>
      <div class="sim-cell">
        <div class="sim-label">Resultado más repetido</div>
        <div class="sim-value">{r['mode_score']}</div>
      </div>
    </div>
    <div class="dc-list">
      {dc_row(f"{home_code} va ganando al descanso", r['ht_home'])}
      {dc_row("Empate al descanso", r['ht_draw'])}
      {dc_row(f"{away_code} va ganando al descanso", r['ht_away'])}
      {dc_row("Giro de resultado tras el descanso", r['giro_resultado'])}
      {dc_row(f"Goleada de {home_code} (margen 3+)", r['goleada_home'])}
      {dc_row(f"Goleada de {away_code} (margen 3+)", r['goleada_away'])}
    </div>
    <div style="margin-top:12px;font-size:11px;color:var(--muted);line-height:1.6">
      Metodología: rating tipo Elo derivado del ranking FIFA real (11-jun-2026), con ventaja de localía para los anfitriones (México, Estados Unidos, Canadá). Goles repartidos en una distribución de Poisson bivariada (45% primera mitad / 55% segunda mitad, según la tendencia histórica real de los Mundiales) y simulados 50.000 veces con números aleatorios independientes por mitad.
    </div>
  </div>'''

    # --- CONFIANZA ---
    rank_gap = abs(th['rank'] - ta['rank'])
    fav_code = home_code if r['p_home'] >= r['p_away'] else away_code
    fav_name = th['name'] if fav_code == home_code else ta['name']
    host_factor = f"{fav_name} juega como anfitrión, " if (fav_code == home_code and host_home) or (fav_code == away_code and host_away) else ""
    confianza = f'''<div class="section-label">Confianza del modelo</div>
  <div class="card">
    <div class="card-title"><span class="icon">🤖</span> Nivel de certeza estadística</div>
    <div class="confidence-wrap">
      <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px">
        <span style="font-size:13px;color:var(--muted)">Confianza general</span>
        <span style="font-family:'Syne',sans-serif;font-weight:800;font-size:20px;color:var(--accent)">{r['confidence']:.0f}%</span>
      </div>
      <div class="confidence-bar-track"><div class="confidence-bar-fill" style="width:{r['confidence']:.0f}%"></div></div>
      <div class="confidence-labels"><span>0%</span><span>Mayor brecha FIFA → mayor confianza</span><span>100%</span></div>
    </div>
    <div style="margin-top:14px;font-size:12px;color:var(--muted);line-height:1.7">
      <strong style="color:var(--text)">Factores que aumentan la confianza:</strong> diferencia de {rank_gap} posiciones en el ranking FIFA entre {th['name']} (#{th['rank']}) y {ta['name']} (#{ta['rank']}), {host_factor}vía de clasificación real de cada equipo.<br><br>
      <strong style="color:var(--text)">Factores de riesgo:</strong> variabilidad propia de un solo partido eliminatorio de grupo, posibles rotaciones, y el factor sorpresa característico de los Mundiales con 48 equipos.
    </div>
  </div>'''

    # --- MERCADOS ESPECIALES / FIGURAS ---
    mercados = f'''<div class="section-label">Mercados especiales</div>
  <div class="card">
    <div class="card-title"><span class="icon">🎲</span> Props adicionales</div>
    <div class="market-row">
      {mrow(f"{home_code} gana ambas mitades", r['win_both_halves_home'])}
      {mrow("Más de 0.5 goles en la 1ra mitad", r['over_0.5_1h'])}
      {mrow(f"{home_code} gana la 1ra mitad", r['win_1h_home'])}
    </div>
    <div style="margin-top:14px">
      <div class="card-title" style="font-size:13px;margin-bottom:8px"><span class="icon">⭐</span> Figuras a seguir</div>
      <div class="pill-list">
        <div class="pill">{th['flag']} {PLAYERS[home_code]}</div>
        <div class="pill">{ta['flag']} {PLAYERS[away_code]}</div>
      </div>
    </div>
  </div>'''

    # --- SECCIONES NUEVAS ---
    real_result = render_real_result(home_code, away_code, th, ta)
    weather     = render_weather(m["city"])
    h2h         = render_h2h(home_code, away_code, th, ta)

    # Orden de secciones:
    # hero → disclaimer → (resultado real si ya jugó) → contenido analítico
    # Dentro del contenido: clima · H2H · perfil equipos · mercados estadísticos
    sections = [hero, disclaimer, '<div class="content">']
    if real_result:
        sections.append(real_result)
    sections += [
        weather, h2h, contexto,
        x1, goles, corners, cards, faltas, btts, handicap, cs,
        temporal, marcadores, simulacion, confianza, mercados,
        "</div>", FOOTER
    ]
    body = "\n\n".join(sections)

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
{build_nav("match")}
{body}
</body>
</html>
'''


def filename_for(m):
    h = NAME_TO_CODE[m["home"]].lower()
    a = NAME_TO_CODE[m["away"]].lower()
    return f"{h}-vs-{a}.html"


def main():
    for m in MATCHES:
        html = render_match_page(m)
        fn = filename_for(m)
        with open(os.path.join(PART_DIR, fn), "w", encoding="utf-8") as f:
            f.write(html)
        m["_file"] = fn
    print(f"Generadas {len(MATCHES)} páginas de partidos en {PART_DIR}")
    with open(os.path.join(SRC_DIR, "matches_with_files.json"), "w", encoding="utf-8") as f:
        json.dump(MATCHES, f, ensure_ascii=False, indent=2)


def build_index():
    groups = {}
    for m in MATCHES:
        groups.setdefault(m["group"], []).append(m)

    group_team_codes = {}
    for g, ms in groups.items():
        codes = []
        for m in ms:
            for nm in (m["home"], m["away"]):
                c = NAME_TO_CODE[nm]
                if c not in codes:
                    codes.append(c)
        group_team_codes[g] = codes

    nav_links = " ".join(f'<a href="#grupo-{g}">{g}</a>' for g in sorted(groups))

    group_sections = ""
    for g in sorted(groups):
        codes = group_team_codes[g]
        team_chips = "".join(
            f'<div class="pill">{TEAMS[c]["flag"]} {TEAMS[c]["name"]} <span style="color:var(--muted);font-family:\'IBM Plex Mono\',monospace;font-size:11px">#{TEAMS[c]["rank"]}</span></div>'
            for c in codes
        )
        rows = ""
        for m in sorted(groups[g], key=lambda x: x["num"]):
            hc, ac = NAME_TO_CODE[m["home"]], NAME_TO_CODE[m["away"]]
            th_, ta_ = TEAMS[hc], TEAMS[ac]
            date_str = fmt_date_es(m["date_co"], m["weekday_co"])
            fn = filename_for(m)
            rows += f'''<a class="match-row" href="partidos/{fn}">
        <div class="match-row-date">{date_str.split()[0]} {date_str.split()[1]} {date_str.split()[2]}<br>{m['time_co']}</div>
        <div class="match-row-teams">{th_['flag']} {hc} <span class="vs">vs</span> {ac} {ta_['flag']}</div>
        <div class="match-row-jor">J{m['matchday']}</div>
      </a>'''
        group_sections += f'''<div class="card" id="grupo-{g}" style="margin-bottom:18px">
      <div class="card-title"><span class="icon">🏟️</span> Grupo {g}</div>
      <div class="pill-list" style="margin-bottom:14px">{team_chips}</div>
      <div class="match-list">{rows}</div>
    </div>'''

    extra_css = '''
  .match-list { display: flex; flex-direction: column; gap: 6px; }
  .match-row {
    display: flex; align-items: center; gap: 10px;
    background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
    padding: 10px 12px; text-decoration: none; color: var(--text); font-size: 13px;
    transition: border-color .15s;
  }
  .match-row:hover { border-color: var(--accent); }
  .match-row-date { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: var(--muted); min-width: 64px; line-height: 1.4; }
  .match-row-teams { flex: 1; font-weight: 600; font-family: 'Syne', sans-serif; font-size: 14px; }
  .match-row-teams .vs { color: var(--muted); font-family: 'IBM Plex Mono', monospace; font-weight: 400; font-size: 11px; }
  .match-row-jor { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: var(--muted); background: rgba(255,255,255,.04); border-radius: 4px; padding: 2px 6px; }
  .index-hero-stats { display: flex; justify-content: center; margin: 18px auto 0; max-width: 420px; }
  .index-stat { text-align: center; margin: 0 14px; }
  .index-stat-num { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 22px; color: var(--accent); }
  .index-stat-label { font-size: 11px; color: var(--muted); }
  .group-nav { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; margin: 16px auto; max-width: 820px; padding: 0 16px; }
  .group-nav a {
    font-family: 'IBM Plex Mono', monospace; font-size: 12px; font-weight: 600; color: var(--text);
    background: var(--card); border: 1px solid var(--border); border-radius: 6px; padding: 5px 11px; text-decoration: none;
  }
  .group-nav a:hover { border-color: var(--accent); color: var(--accent); }
'''

    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Mundial 2026 · Fase de Grupos · Análisis de Apuestas</title>
<style>{CSS}{extra_css}</style>
</head>
<body>
{build_nav("index")}
<div class="hero">
  <div class="competition-tag">Mundial 2026 · Fase de Grupos</div>
  <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:26px">Calendario y análisis de los 72 partidos</div>
  <div class="match-meta" style="margin-top:8px">Modelo propio: Elo (ranking FIFA 11-jun-2026) + Poisson bivariado + Monte Carlo (50.000 simulaciones) para cada partido</div>
  <div class="index-hero-stats">
    <div class="index-stat"><div class="index-stat-num">48</div><div class="index-stat-label">equipos</div></div>
    <div class="index-stat"><div class="index-stat-num">12</div><div class="index-stat-label">grupos</div></div>
    <div class="index-stat"><div class="index-stat-num">72</div><div class="index-stat-label">partidos</div></div>
    <div class="index-stat"><div class="index-stat-num">3</div><div class="index-stat-label">países anfitriones</div></div>
  </div>
</div>
<div class="disclaimer" style="max-width:820px;margin:16px auto;">
  <span class="disclaimer-icon">⚠️</span>
  <span>Análisis estadístico de entretenimiento generado por un modelo propio a partir de datos reales (ranking FIFA, historial mundialista, vía de clasificación y resultados ya disputados). No es asesoría financiera ni de apuestas. Juega con responsabilidad.</span>
</div>
<div class="group-nav" id="grupos">{nav_links}</div>
<div class="content">
  {group_sections}
</div>
{FOOTER}
</body>
</html>
'''
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html generado")


if __name__ == "__main__":
    main()
    build_index()

