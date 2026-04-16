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
PRIMARY          = "#001360"
SECONDARY        = "#775a19"
TERTIARY         = "#470003"
SURFACE          = "#faf9f5"
SURFACE_LOW      = "#f4f4f0"
SURFACE_CONTAINER = "#efeeea"
SURFACE_HIGH     = "#e9e8e4"
SURFACE_HIGHEST  = "#e3e2df"
ON_SURFACE       = "#1b1c1a"
ON_SURFACE_VAR   = "#444653"
OUTLINE_VAR      = "rgba(197,197,213,0.3)"
SEC_CONTAINER    = "#fed488"

FONT_HEADLINE    = "'Newsreader', Georgia, serif"
FONT_BODY        = "'Inter', system-ui, sans-serif"

_CSS = f"""
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..900;1,6..72,300..900&family=Inter:wght@300..800&display=swap" rel="stylesheet">
<style>

/* ══════════════════════════════════════════════════════════════════════
   1. RESET STREAMLIT CHROME
   ══════════════════════════════════════════════════════════════════════ */
#MainMenu, footer, header {{ visibility: hidden !important; height: 0 !important; }}
[data-testid="stHeader"]    {{ display: none !important; }}
[data-testid="stToolbar"]   {{ display: none !important; }}
[data-testid="stDecoration"]{{ display: none !important; }}
.stDeployButton             {{ display: none !important; }}
[data-testid="stStatusWidget"] {{ display: none !important; }}


/* ══════════════════════════════════════════════════════════════════════
   2. FOND & TYPOGRAPHIE GLOBALE
   ══════════════════════════════════════════════════════════════════════ */
html, body, .stApp, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main, section[data-testid="stMain"] {{
    background-color: {SURFACE} !important;
    font-family: {FONT_BODY} !important;
    color: {ON_SURFACE} !important;
}}

/* Block container */
.block-container {{
    padding-top: 2.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 1100px !important;
}}

/* Headings → Newsreader */
h1, h2, h3, h4, h5, h6 {{
    font-family: {FONT_HEADLINE} !important;
    color: {PRIMARY} !important;
}}

/* Paragraphes */
p {{ font-family: {FONT_BODY}; }}


/* ══════════════════════════════════════════════════════════════════════
   3. NAVIGATION PAR ONGLETS
   ══════════════════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {{
    background: transparent !important;
    border-bottom: 1px solid {OUTLINE_VAR} !important;
    gap: 0.25rem !important;
    padding: 0 !important;
}}
.stTabs [data-baseweb="tab"] {{
    font-family: {FONT_HEADLINE} !important;
    font-size: 1rem !important;
    font-style: italic !important;
    font-weight: 400 !important;
    color: {ON_SURFACE_VAR} !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.6rem 1.2rem !important;
    margin: 0 !important;
    letter-spacing: -0.01em !important;
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
/* Panel spacing */
.stTabs [data-baseweb="tab-panel"] {{
    padding: 2rem 0 0 !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   4. CHAMPS TEXTE — "SIGNATURE LINE"
   ══════════════════════════════════════════════════════════════════════ */
.stTextInput > label {{
    font-family: {FONT_BODY} !important;
    font-size: 0.6rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.14em !important;
    color: {SECONDARY} !important;
}}
.stTextInput input {{
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid {OUTLINE_VAR} !important;
    border-radius: 0 !important;
    padding: 0.75rem 0 !important;
    font-family: {FONT_HEADLINE} !important;
    font-size: 1.5rem !important;
    font-style: italic !important;
    color: {PRIMARY} !important;
    box-shadow: none !important;
    transition: border-color 0.25s !important;
}}
.stTextInput input:focus {{
    border-bottom: 1px solid {PRIMARY} !important;
    box-shadow: none !important;
    outline: none !important;
}}
.stTextInput input::placeholder {{
    color: rgba(68,70,83,0.3) !important;
    font-style: italic !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   5. MÉTRIQUES
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
    color: {ON_SURFACE_VAR} !important;
    overflow: visible !important;
}}
[data-testid="stMetricValue"] > div {{
    font-family: {FONT_HEADLINE} !important;
    font-size: 2.6rem !important;
    font-weight: 900 !important;
    color: {PRIMARY} !important;
    letter-spacing: -0.03em !important;
    line-height: 1 !important;
}}
[data-testid="stMetricDelta"] svg {{ display: none !important; }}
[data-testid="stMetricDelta"] > div {{
    font-family: {FONT_BODY} !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   6. BOUTONS
   ══════════════════════════════════════════════════════════════════════ */
.stButton > button {{
    background-color: {PRIMARY} !important;
    color: white !important;
    border: none !important;
    border-radius: 0.125rem !important;
    font-family: {FONT_BODY} !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.13em !important;
    padding: 0.7rem 2rem !important;
    transition: opacity 0.2s !important;
}}
.stButton > button:hover {{
    opacity: 0.88 !important;
    background-color: {PRIMARY} !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   7. ALERTES & MESSAGES
   ══════════════════════════════════════════════════════════════════════ */
[data-testid="stAlert"] {{
    border-radius: 0 !important;
    border: none !important;
    border-left: 3px solid {PRIMARY} !important;
    background: {SURFACE_LOW} !important;
    padding: 1.25rem 1.5rem 1.25rem 1.75rem !important;
}}
[data-testid="stAlert"] p,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {{
    font-family: {FONT_HEADLINE} !important;
    font-style: italic !important;
    color: {PRIMARY} !important;
    font-size: 1rem !important;
}}
/* Warning → Gold */
div[data-baseweb="notification"][kind="warning"] {{
    border-left-color: {SECONDARY} !important;
}}
div[data-baseweb="notification"][kind="error"] {{
    border-left-color: {TERTIARY} !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   8. DIVIDERS
   ══════════════════════════════════════════════════════════════════════ */
hr {{ border-color: {OUTLINE_VAR} !important; margin: 2rem 0 !important; }}


/* ══════════════════════════════════════════════════════════════════════
   9. SELECTBOX / RADIO / SLIDER
   ══════════════════════════════════════════════════════════════════════ */
.stRadio > label, .stSelectbox > label, .stSlider > label {{
    font-family: {FONT_BODY} !important;
    font-size: 0.6rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    color: {ON_SURFACE_VAR} !important;
}}
.stRadio [data-testid="stMarkdownContainer"] p {{
    font-family: {FONT_BODY} !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}}
/* Active radio */
.stRadio [data-baseweb="radio"] [data-checked="true"] ~ span {{
    color: {PRIMARY} !important;
    font-weight: 700 !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   10. DATAFRAMES
   ══════════════════════════════════════════════════════════════════════ */
.stDataFrame {{
    font-family: {FONT_BODY} !important;
    font-size: 0.8rem !important;
    border: none !important;
}}
.stDataFrame thead th {{
    font-family: {FONT_BODY} !important;
    font-size: 0.55rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: {ON_SURFACE_VAR} !important;
    background: {SURFACE_LOW} !important;
    border: none !important;
}}
.stDataFrame tbody td {{
    font-family: {FONT_BODY} !important;
    border: none !important;
    color: {ON_SURFACE} !important;
}}
.stDataFrame tbody tr:nth-child(even) {{
    background: {SURFACE_LOW} !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   11. SIDEBAR
   ══════════════════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {{
    background-color: {SURFACE_LOW} !important;
    border-right: none !important;
}}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{
    font-family: {FONT_HEADLINE} !important;
    color: {PRIMARY} !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   12. SPINNER
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
   13. COMPOSANTS CUSTOM (classes utilisées dans les HTML injectés)
   ══════════════════════════════════════════════════════════════════════ */

/* Section header */
.es-eyebrow {{
    font-family: {FONT_BODY};
    font-size: 0.55rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: {SECONDARY};
    display: block;
    margin-bottom: 0.75rem;
}}
.es-title {{
    font-family: {FONT_HEADLINE};
    font-weight: 900;
    color: {PRIMARY};
    line-height: 1.05;
    letter-spacing: -0.03em;
    margin: 0;
}}

/* Hero result card */
.es-result-card {{
    background: {SURFACE_LOW};
    padding: 2.5rem 3rem;
    position: relative;
    overflow: hidden;
    margin-bottom: 0;
}}
.es-prenom-name {{
    font-family: {FONT_HEADLINE};
    font-size: clamp(3.5rem, 8vw, 6.5rem);
    font-weight: 900;
    color: {PRIMARY};
    line-height: 1;
    letter-spacing: -0.04em;
    margin: 0 0 0.5rem;
}}
.es-score-block {{
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
    margin: 1.5rem 0 0.5rem;
}}
.es-score-number {{
    font-family: {FONT_HEADLINE};
    font-size: clamp(3rem, 7vw, 5rem);
    font-weight: 900;
    color: {PRIMARY};
    letter-spacing: -0.04em;
    line-height: 1;
}}
.es-score-denom {{
    font-family: {FONT_HEADLINE};
    font-size: 1.5rem;
    font-style: italic;
    color: {SECONDARY};
    line-height: 1;
}}
.es-score-label {{
    font-family: {FONT_BODY};
    font-size: 0.5rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    color: {ON_SURFACE_VAR};
    display: block;
    margin-top: 0.25rem;
}}
.es-badge {{
    font-family: {FONT_BODY};
    font-size: 0.5rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: {SECONDARY};
    border: 1px solid rgba(119,90,25,0.25);
    padding: 0.2rem 0.55rem;
    display: inline-block;
    margin-bottom: 1.5rem;
}}
.es-stat-row {{
    display: flex;
    gap: 2.5rem;
    margin-top: 1.5rem;
    padding-top: 1.25rem;
    border-top: 1px solid {OUTLINE_VAR};
}}
.es-stat {{
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
}}
.es-stat-label {{
    font-family: {FONT_BODY};
    font-size: 0.5rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: rgba(68,70,83,0.6);
}}
.es-stat-value {{
    font-family: {FONT_BODY};
    font-size: 0.9rem;
    font-weight: 700;
    color: {PRIMARY};
}}

/* Verdict card */
.es-verdict-card {{
    background: {PRIMARY};
    color: white;
    padding: 2.25rem 2.5rem;
    margin-bottom: 1rem;
}}
.es-verdict-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.25rem;
}}
.es-verdict-title {{
    font-family: {FONT_HEADLINE};
    font-size: 1.5rem;
    font-style: italic;
    color: white;
    margin: 0;
}}
.es-verdict-star {{ color: {SEC_CONTAINER}; font-size: 1.5rem; }}
.es-verdict-text {{
    font-family: {FONT_BODY};
    font-size: 0.9rem;
    line-height: 1.75;
    color: rgba(186,195,255,0.85);
    margin-bottom: 1.25rem;
}}
.es-verdict-sig {{
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-size: 0.95rem;
    color: white;
}}

/* Percentile chip */
.es-percentile {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: {SURFACE_CONTAINER};
    padding: 0.35rem 0.9rem;
    margin-top: 0.75rem;
}}
.es-percentile-num {{
    font-family: {FONT_HEADLINE};
    font-size: 1.2rem;
    font-weight: 900;
    color: {PRIMARY};
}}
.es-percentile-label {{
    font-family: {FONT_BODY};
    font-size: 0.5rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: {ON_SURFACE_VAR};
}}

/* VS Duel */
.es-vs-badge {{
    width: 3.5rem;
    height: 3.5rem;
    background: {PRIMARY};
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-size: 1.2rem;
    font-weight: 900;
    transform: rotate(45deg);
    flex-shrink: 0;
    box-shadow: 0 4px 20px rgba(0,19,96,0.25);
}}
.es-vs-badge span {{ transform: rotate(-45deg); display: block; }}
.es-duel-card-a {{
    background: {SURFACE_LOW};
    padding: 2rem 2rem 2rem;
    flex: 1;
}}
.es-duel-card-b {{
    background: {SURFACE_CONTAINER};
    padding: 2rem 2rem 2rem;
    flex: 1;
}}
.es-duel-name {{
    font-family: {FONT_HEADLINE};
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 900;
    color: {PRIMARY};
    letter-spacing: -0.03em;
    margin: 0 0 0.25rem;
    line-height: 1;
}}
.es-duel-score {{
    font-family: {FONT_HEADLINE};
    font-size: 2rem;
    font-weight: 900;
    color: {PRIMARY};
    letter-spacing: -0.03em;
    margin: 1rem 0 0.25rem;
}}
.es-bar-container {{
    height: 4px;
    background: {SURFACE_HIGH};
    margin: 0.5rem 0 0.75rem;
    position: relative;
}}
.es-bar-fill-a {{
    height: 100%;
    background: {PRIMARY};
    transition: width 0.8s ease;
}}
.es-bar-fill-b {{
    height: 100%;
    background: {SECONDARY};
    transition: width 0.8s ease;
}}
.es-verdict-caption {{
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-size: 0.8rem;
    color: {ON_SURFACE_VAR};
    line-height: 1.6;
    margin-top: 0.75rem;
    padding-top: 0.75rem;
    border-top: 1px solid {OUTLINE_VAR};
}}

/* Section title */
.es-section-title {{
    font-family: {FONT_HEADLINE};
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 900;
    color: {PRIMARY};
    letter-spacing: -0.03em;
    line-height: 1.05;
    margin: 0 0 0.5rem;
}}
.es-section-subtitle {{
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-size: 1.1rem;
    color: {SECONDARY};
    margin: 0 0 2rem;
}}

/* Absent message */
.es-absent-card {{
    background: {SURFACE_LOW};
    border-left: 3px solid {SECONDARY};
    padding: 1.5rem 2rem;
    margin-bottom: 1rem;
}}
.es-absent-text {{
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-size: 1.05rem;
    color: {ON_SURFACE};
    margin: 0 0 0.5rem;
}}
.es-absent-suggestions {{
    font-family: {FONT_BODY};
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: {ON_SURFACE_VAR};
    margin: 0;
}}
.es-absent-pill {{
    display: inline-block;
    background: {SURFACE_CONTAINER};
    padding: 0.2rem 0.6rem;
    margin: 0.2rem 0.15rem 0 0;
    font-family: {FONT_BODY};
    font-size: 0.7rem;
    font-weight: 600;
    color: {PRIMARY};
    cursor: pointer;
}}

/* Decade generation card */
.es-gen-card {{
    background: {PRIMARY};
    color: white;
    padding: 2rem 2.5rem;
}}
.es-gen-vibe {{
    font-size: 2rem;
    margin-bottom: 0.5rem;
    display: block;
}}
.es-gen-label {{
    font-family: {FONT_HEADLINE};
    font-size: 1.75rem;
    font-weight: 900;
    color: white;
    margin: 0 0 0.25rem;
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

/* Diamond data point (chart decoration) */
.diamond-point {{
    clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
    width: 8px; height: 8px;
    background: {SECONDARY};
    display: inline-block;
}}

/* No-line separator */
.es-rule {{
    border: none;
    border-top: 1px solid {OUTLINE_VAR};
    margin: 2rem 0;
}}

</style>
"""


def inject_css() -> None:
    """Injecte l'intégralité du design system dans l'app Streamlit."""
    st.html(_CSS)
