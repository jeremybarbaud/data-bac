"""
Design System : The Editorial Scholar
Injection CSS complète pour l'app Streamlit.

Palette :
  Primary   (Royal Blue) : #001360
  Secondary (Gold)       : #775a19
  Tertiary  (Red)        : #470003
  Surface   (Parchment)  : #faf9f5
"""

import streamlit as st

# ── Tokens ────────────────────────────────────────────────────────────────────
PRIMARY           = "#001360"
SECONDARY         = "#775a19"
TERTIARY          = "#470003"
SURFACE           = "#faf9f5"
SURFACE_LOW       = "#f4f4f0"
SURFACE_CONTAINER = "#efeeea"
SURFACE_HIGH      = "#e9e8e4"
SURFACE_HIGHEST   = "#e3e2df"
ON_SURFACE        = "#1b1c1a"
ON_SURFACE_VAR    = "#444653"
OUTLINE_VAR       = "rgba(197,197,213,0.3)"
SEC_CONTAINER     = "#fed488"

FONT_HEADLINE = "'Newsreader', Georgia, serif"
FONT_BODY     = "'Inter', system-ui, sans-serif"

_CSS = f"""
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..900;1,6..72,300..900&family=Inter:wght@300..800&display=swap" rel="stylesheet">
<style>

/* ══════════════════════════════════════════════════════════════════════
   1. RESET STREAMLIT CHROME
   ══════════════════════════════════════════════════════════════════════ */
#MainMenu, footer, header {{ visibility: hidden !important; height: 0 !important; }}
[data-testid="stHeader"]      {{ display: none !important; }}
[data-testid="stToolbar"]     {{ display: none !important; }}
[data-testid="stDecoration"]  {{ display: none !important; }}
.stDeployButton               {{ display: none !important; }}
[data-testid="stStatusWidget"]{{ display: none !important; }}


/* ══════════════════════════════════════════════════════════════════════
   2. FOND & TYPOGRAPHIE GLOBALE
   ══════════════════════════════════════════════════════════════════════ */
html, body, .stApp, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main, section[data-testid="stMain"] {{
    background-color: {SURFACE} !important;
    font-family: {FONT_BODY} !important;
    color: {ON_SURFACE} !important;
}}

.block-container {{
    padding-top: 2.5rem !important;
    padding-bottom: 5rem !important;
    max-width: 860px !important;
}}

h1, h2, h3, h4, h5, h6 {{
    font-family: {FONT_HEADLINE} !important;
    color: {PRIMARY} !important;
}}

p {{ font-family: {FONT_BODY}; }}


/* ══════════════════════════════════════════════════════════════════════
   3. NAVIGATION PAR ONGLETS
   ══════════════════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {{
    background: transparent !important;
    border-bottom: 1px solid rgba(0,19,96,0.12) !important;
    gap: 0 !important;
    padding: 0 !important;
}}
.stTabs [data-baseweb="tab"] {{
    font-family: {FONT_BODY} !important;
    font-size: 0.85rem !important;
    font-style: normal !important;
    font-weight: 500 !important;
    color: #666 !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.6rem 1.4rem !important;
    margin: 0 !important;
    letter-spacing: normal !important;
    transition: color 0.2s !important;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color: {PRIMARY} !important;
    background: transparent !important;
}}
.stTabs [aria-selected="true"] {{
    color: {PRIMARY} !important;
    font-weight: 700 !important;
    border-bottom: 2px solid {PRIMARY} !important;
    background: transparent !important;
}}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {{
    display: none !important;
}}
.stTabs [data-baseweb="tab-panel"] {{
    padding: 2rem 0 0 !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   4. CHAMPS TEXTE — SIGNATURE LINE
   ══════════════════════════════════════════════════════════════════════ */
.stTextInput > label,
.stTextInput label p {{
    font-family: {FONT_BODY} !important;
    font-size: 0.6rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.14em !important;
    color: {SECONDARY} !important;
}}
.stTextInput [data-baseweb="input"] {{
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid rgba(0,19,96,0.15) !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    padding: 0 !important;
    transition: border-color 0.25s !important;
}}
.stTextInput [data-baseweb="input"]:focus-within {{
    border-bottom: 1px solid {PRIMARY} !important;
    box-shadow: none !important;
}}
.stTextInput input {{
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0.9rem 0 !important;
    font-family: {FONT_HEADLINE} !important;
    font-size: 1.75rem !important;
    font-style: italic !important;
    color: {PRIMARY} !important;
    box-shadow: none !important;
}}
.stTextInput input:focus {{
    box-shadow: none !important;
    outline: none !important;
}}
.stTextInput input::placeholder {{
    color: rgba(68,70,83,0.35) !important;
    font-style: italic !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   5. RADIO BUTTONS
   ══════════════════════════════════════════════════════════════════════ */
.stRadio > label,
.stRadio label p {{
    font-family: {FONT_BODY} !important;
    font-size: 0.6rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    color: {ON_SURFACE_VAR} !important;
}}
.stRadio [data-testid="stMarkdownContainer"] p {{
    font-family: {FONT_BODY} !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: {ON_SURFACE} !important;
}}
[data-baseweb="radio"] [role="radio"] {{
    border-color: rgba(0,19,96,0.3) !important;
    background: transparent !important;
}}
[data-baseweb="radio"] [role="radio"][aria-checked="true"] {{
    background: {PRIMARY} !important;
    border-color: {PRIMARY} !important;
}}
[data-baseweb="radio"] [role="radio"][aria-checked="true"]::after {{
    background: white !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   6. SLIDER
   ══════════════════════════════════════════════════════════════════════ */
.stSlider > label,
.stSlider label p {{
    font-family: {FONT_BODY} !important;
    font-size: 0.6rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    color: {ON_SURFACE_VAR} !important;
}}
[data-testid="stSlider"] [role="slider"] {{
    background: {PRIMARY} !important;
    border-color: {PRIMARY} !important;
    width: 14px !important;
    height: 14px !important;
    box-shadow: 0 2px 6px rgba(0,19,96,0.25) !important;
}}
[data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child > div:nth-child(2) {{
    background: {PRIMARY} !important;
}}
[data-testid="stSlider"] [data-testid="stThumbValue"] {{
    color: {PRIMARY} !important;
    font-family: {FONT_BODY} !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   7. MÉTRIQUES
   ══════════════════════════════════════════════════════════════════════ */
[data-testid="metric-container"] {{
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}}
[data-testid="stMetricLabel"] > div {{
    font-family: {FONT_BODY} !important;
    font-size: 0.55rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.13em !important;
    color: #666 !important;
    overflow: visible !important;
}}
[data-testid="stMetricValue"] > div {{
    font-family: {FONT_HEADLINE} !important;
    font-size: 2.8rem !important;
    font-weight: 900 !important;
    color: {PRIMARY} !important;
    letter-spacing: -0.03em !important;
    line-height: 1 !important;
}}
[data-testid="stMetricDelta"] svg {{ display: none !important; }}


/* ══════════════════════════════════════════════════════════════════════
   8. BOUTONS
   ══════════════════════════════════════════════════════════════════════ */
.stButton > button {{
    background-color: {PRIMARY} !important;
    color: white !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: {FONT_BODY} !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    padding: 0.7rem 2rem !important;
    transition: opacity 0.2s !important;
}}
.stButton > button:hover {{
    opacity: 0.88 !important;
    background-color: {PRIMARY} !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   9. ALERTES & MESSAGES
   ══════════════════════════════════════════════════════════════════════ */
[data-testid="stAlert"] {{
    border-radius: 0 !important;
    border: none !important;
    border-left: 3px solid {PRIMARY} !important;
    background: #f4f4f0 !important;
    padding: 1.25rem 1.5rem 1.25rem 1.75rem !important;
}}
[data-testid="stAlert"] p,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {{
    font-family: {FONT_HEADLINE} !important;
    font-style: italic !important;
    color: {PRIMARY} !important;
    font-size: 1rem !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   10. DIVIDERS
   ══════════════════════════════════════════════════════════════════════ */
hr {{ border-color: rgba(0,19,96,0.1) !important; margin: 2.5rem 0 !important; }}


/* ══════════════════════════════════════════════════════════════════════
   11. SELECTBOX
   ══════════════════════════════════════════════════════════════════════ */
.stSelectbox > label,
.stSelectbox label p {{
    font-family: {FONT_BODY} !important;
    font-size: 0.6rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    color: {ON_SURFACE_VAR} !important;
}}
.stSelectbox [data-baseweb="select"] {{
    background: transparent !important;
    border-bottom: 1px solid rgba(0,19,96,0.15) !important;
    border-top: none !important;
    border-left: none !important;
    border-right: none !important;
    border-radius: 0 !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   12. DATAFRAMES
   ══════════════════════════════════════════════════════════════════════ */
.stDataFrame {{
    font-family: {FONT_BODY} !important;
    font-size: 0.85rem !important;
    border: none !important;
}}
.stDataFrame thead th {{
    font-family: {FONT_BODY} !important;
    font-size: 0.55rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: #666 !important;
    background: #f4f4f0 !important;
    border: none !important;
}}
.stDataFrame tbody td {{
    font-family: {FONT_BODY} !important;
    font-size: 0.85rem !important;
    border: none !important;
    color: {ON_SURFACE} !important;
}}
.stDataFrame tbody tr:nth-child(even) {{
    background: #f8f8f8 !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   13. SPINNER
   ══════════════════════════════════════════════════════════════════════ */
[data-testid="stSpinner"] p {{
    font-family: {FONT_BODY} !important;
    font-size: 0.75rem !important;
    font-style: italic !important;
    color: {ON_SURFACE_VAR} !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   14. COMPOSANTS CUSTOM (.es-*)
   ══════════════════════════════════════════════════════════════════════ */

/* Input hero wrapper */
.es-input-hero {{
    padding: 2.5rem 0 1rem;
    border-bottom: 1px solid rgba(0,19,96,0.08);
    margin-bottom: 2rem;
}}

/* Result container */
.es-result {{
    padding: 0;
    margin-bottom: 0;
}}

/* Name */
.es-name {{
    font-family: {FONT_HEADLINE};
    font-size: clamp(3rem, 8vw, 6rem);
    font-weight: 900;
    color: {PRIMARY};
    letter-spacing: -0.04em;
    line-height: 0.95;
    margin: 0 0 0.25rem;
}}

/* Gender pill */
.es-gender-pill {{
    font-family: {FONT_BODY};
    font-size: 0.55rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    border: 1px solid rgba(119,90,25,0.3);
    padding: 0.2rem 0.6rem;
    color: {SECONDARY};
    display: inline-block;
    margin-bottom: 1.5rem;
}}

/* Score row */
.es-score-row {{
    display: flex;
    align-items: baseline;
    gap: 0.6rem;
    margin: 0.5rem 0 0.25rem;
}}

.es-score-num {{
    font-family: {FONT_HEADLINE};
    font-size: clamp(3rem, 7vw, 5rem);
    font-weight: 900;
    color: {PRIMARY};
    letter-spacing: -0.04em;
    line-height: 1;
}}

.es-score-unit {{
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-size: 1.4rem;
    color: {SECONDARY};
}}

.es-score-caption {{
    font-family: {FONT_BODY};
    font-size: 0.5rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #888;
    display: block;
    margin-top: 0.2rem;
}}

/* Percentile bar */
.es-pct-bar-wrap {{
    margin: 1.25rem 0 0.5rem;
    max-width: 420px;
}}

.es-pct-bar-track {{
    height: 4px;
    background: #e8e8e4;
    border-radius: 2px;
    position: relative;
    margin-bottom: 0.4rem;
}}

.es-pct-bar-fill {{
    height: 100%;
    background: {PRIMARY};
    border-radius: 2px;
    transition: width 0.6s ease;
}}

.es-pct-label {{
    font-family: {FONT_BODY};
    font-size: 0.6rem;
    font-weight: 600;
    color: #666;
}}

/* Stats row */
.es-stats-row {{
    display: flex;
    gap: 2rem;
    margin-top: 1.25rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(0,19,96,0.08);
}}

.es-stat-item {{
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}}

.es-stat-label {{
    font-family: {FONT_BODY};
    font-size: 0.5rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #999;
}}

.es-stat-val {{
    font-family: {FONT_BODY};
    font-size: 0.9rem;
    font-weight: 700;
    color: {PRIMARY};
}}

/* Verdict */
.es-verdict {{
    margin-top: 1.5rem;
    padding: 1.75rem 2rem;
    background: {PRIMARY};
    color: white;
}}

.es-verdict-eyebrow {{
    font-family: {FONT_BODY};
    font-size: 0.5rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: rgba(186,195,255,0.7);
    display: block;
    margin-bottom: 0.75rem;
}}

.es-verdict-stars {{
    color: #fed488;
    font-size: 1rem;
    float: right;
}}

.es-verdict-text {{
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-size: 1.05rem;
    color: rgba(255,255,255,0.9);
    line-height: 1.8;
    margin: 0;
}}

/* Absent */
.es-absent {{
    border-left: 3px solid {SECONDARY};
    background: #f4f4f0;
    padding: 1.25rem 1.75rem;
    margin-bottom: 1rem;
}}

.es-absent-text {{
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-size: 1rem;
    color: {ON_SURFACE};
    margin: 0 0 0.5rem;
}}

.es-absent-pills {{
    margin-top: 0.5rem;
}}

.es-pill {{
    font-family: {FONT_BODY};
    font-size: 0.7rem;
    font-weight: 600;
    background: #e8e8e4;
    padding: 0.2rem 0.65rem;
    display: inline-block;
    margin: 0.2rem 0.15rem 0 0;
    color: {PRIMARY};
    cursor: pointer;
}}

/* Duel */
.es-duel-wrap {{
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 0.5rem;
    align-items: stretch;
    margin-bottom: 1.5rem;
}}

.es-duel-card {{
    padding: 1.75rem 2rem;
    background: #f4f4f0;
}}

.es-duel-card.winner {{
    background: {PRIMARY};
    color: white;
}}

.es-duel-name {{
    font-family: {FONT_HEADLINE};
    font-size: clamp(1.75rem, 4vw, 2.75rem);
    font-weight: 900;
    letter-spacing: -0.03em;
    margin: 0 0 0.25rem;
}}

.es-duel-score {{
    font-family: {FONT_HEADLINE};
    font-size: 2.25rem;
    font-weight: 900;
    letter-spacing: -0.03em;
    margin: 0.75rem 0 0.25rem;
}}

.es-duel-bar {{
    height: 3px;
    background: rgba(0,19,96,0.15);
    margin: 0.5rem 0 0.75rem;
}}

.es-duel-caption {{
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-size: 0.8rem;
    color: #666;
    line-height: 1.6;
    margin-top: 0.75rem;
}}

.es-duel-card.winner .es-duel-caption {{
    color: rgba(255,255,255,0.75);
}}

.es-vs {{
    width: 3rem;
    height: 3rem;
    background: {PRIMARY};
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-weight: 900;
    font-size: 1.1rem;
    align-self: center;
    flex-shrink: 0;
}}

.es-duel-result {{
    padding: 1rem 1.75rem;
    background: {PRIMARY};
    color: white;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: baseline;
    gap: 1rem;
}}

/* Section */
.es-section {{
    margin-bottom: 1.75rem;
}}

.es-eyebrow {{
    font-family: {FONT_BODY};
    font-size: 0.55rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: {SECONDARY};
    display: block;
    margin-bottom: 0.6rem;
}}

.es-h1 {{
    font-family: {FONT_HEADLINE};
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 900;
    color: {PRIMARY};
    letter-spacing: -0.03em;
    margin: 0 0 0.4rem;
    line-height: 1.05;
}}

.es-lead {{
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-size: 1rem;
    color: #666;
    margin: 0 0 1.5rem;
}}

/* Generation cards */
.es-gen-card {{
    padding: 1.75rem 2rem;
    background: {PRIMARY};
    color: white;
}}

.es-gen-vibe {{
    font-size: 2rem;
    display: block;
    margin-bottom: 0.5rem;
}}

.es-gen-label {{
    font-family: {FONT_HEADLINE};
    font-size: 1.75rem;
    font-weight: 900;
    color: white;
    margin: 0 0 0.2rem;
}}

.es-gen-peak {{
    font-family: {FONT_BODY};
    font-size: 0.55rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    color: rgba(186,195,255,0.7);
    margin: 0;
}}

/* Rank card */
.es-rank-card {{
    padding: 1.75rem 2rem;
    background: #f4f4f0;
}}

.es-rank-num {{
    font-family: {FONT_HEADLINE};
    font-size: 2.25rem;
    font-weight: 900;
    color: {PRIMARY};
    letter-spacing: -0.03em;
}}

.es-rank-caption {{
    font-family: {FONT_BODY};
    font-size: 0.7rem;
    color: #666;
    margin-top: 0.35rem;
}}

/* Hero */
.es-hero {{
    padding: 3rem 0 2rem;
}}

.es-hero-title {{
    font-family: {FONT_HEADLINE};
    font-size: clamp(3rem, 8vw, 5.5rem);
    font-weight: 900;
    color: {PRIMARY};
    letter-spacing: -0.04em;
    line-height: 1;
    margin: 0 0 1rem;
}}

.es-hero-lead {{
    font-family: {FONT_BODY};
    font-size: 0.95rem;
    color: #444;
    max-width: 500px;
    line-height: 1.85;
    margin: 0 0 2rem;
}}

.es-hero-stats {{
    display: flex;
    gap: 2.5rem;
    border-top: 1px solid rgba(0,19,96,0.08);
    padding-top: 1.25rem;
}}

.es-hero-stat-n {{
    font-family: {FONT_HEADLINE};
    font-size: 1.75rem;
    font-weight: 900;
    color: {PRIMARY};
    letter-spacing: -0.03em;
}}

.es-hero-stat-l {{
    font-family: {FONT_BODY};
    font-size: 0.5rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #888;
    display: block;
    margin-bottom: 0.2rem;
}}

/* Rule */
.es-rule {{
    border: none;
    border-top: 1px solid rgba(0,19,96,0.1);
    margin: 2.5rem 0;
}}

</style>
"""


def inject_css() -> None:
    """Injecte l'intégralité du design system dans l'app Streamlit."""
    st.html(_CSS)
