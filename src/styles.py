"""
Design System : *The Editorial Scholar*.
Injection CSS complète pour l'app Streamlit.

Tous les tokens proviennent de ``src/tokens.py``. Les constantes ré-exportées
ici (``PRIMARY``, ``SURFACE``…) servent uniquement la rétrocompat avec les
modules qui les importent encore (``app.py``, ``components.py``).

Palette :
  Primary   (Royal Blue) : #001360
  Secondary (Gold)       : #775a19
  Tertiary  (Red)        : #470003
  Surface   (Parchment)  : #faf9f5
"""

import streamlit as st

from src.tokens import (
    DURATION_BASE,
    DURATION_FAST,
    DURATION_SLOW,
    FOCUS_RING_COLOR,
    FOCUS_RING_OFFSET,
    FOCUS_RING_WIDTH,
    FONT_BODY,
    FONT_HEADLINE,
    GOLD_ACCENT,
    ON_PRIMARY,
    ON_PRIMARY_EYEBROW,
    ON_PRIMARY_FAINT,
    ON_PRIMARY_MUTED,
    ON_PRIMARY_STRONG,
    ON_SURFACE,
    ON_SURFACE_VAR,
    OUTLINE_FAINT,
    PRIMARY,
    PRIMARY_A_08,
    PRIMARY_A_10,
    PRIMARY_A_12,
    PRIMARY_A_15,
    PRIMARY_A_30,
    RADIUS_NONE,
    RADIUS_SM,
    SECONDARY,
    SPACE_2XL,
    SPACE_2XS,
    SPACE_3XL,
    SPACE_LG,
    SPACE_MD,
    SPACE_SM,
    SPACE_XL,
    SPACE_XS,
    SURFACE,
    SURFACE_HIGH,
    SURFACE_LOW,
    TERTIARY,
    TEXT_2XL,
    TEXT_2XS,
    TEXT_3XL,
    TEXT_3XS,
    TEXT_4XL,
    TEXT_5XL,
    TEXT_BASE,
    TEXT_FAINT,
    TEXT_LG,
    TEXT_MD,
    TEXT_MUTED,
    TEXT_SM,
    TEXT_SUBTLE,
    TEXT_XL,
    TEXT_XS,
    TRACK_DISPLAY,
    TRACK_EXTREME,
    TRACK_TITLE,
    TRACK_WIDE,
    TRACK_WIDER,
    TRACK_WIDEST,
    WEIGHT_BLACK,
    WEIGHT_BOLD,
    WEIGHT_MEDIUM,
    WEIGHT_NORMAL,
    WEIGHT_SEMIBOLD,
)

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
    padding-top: {SPACE_2XL} !important;
    padding-bottom: 5rem !important;
    max-width: 860px !important;
}}

h1, h2, h3, h4, h5, h6 {{
    font-family: {FONT_HEADLINE} !important;
    color: {PRIMARY} !important;
}}

p {{ font-family: {FONT_BODY}; }}


/* ══════════════════════════════════════════════════════════════════════
   2bis. A11Y — focus ring global
   ══════════════════════════════════════════════════════════════════════ */
:focus-visible {{
    outline: {FOCUS_RING_WIDTH} solid {FOCUS_RING_COLOR} !important;
    outline-offset: {FOCUS_RING_OFFSET} !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   3. NAVIGATION PAR ONGLETS
   ══════════════════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {{
    background: transparent !important;
    border-bottom: 1px solid {PRIMARY_A_12} !important;
    gap: 0 !important;
    padding: 0 !important;
}}
.stTabs [data-baseweb="tab"] {{
    font-family: {FONT_BODY} !important;
    font-size: {TEXT_BASE} !important;
    font-style: normal !important;
    font-weight: {WEIGHT_MEDIUM} !important;
    color: {TEXT_MUTED} !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.6rem 1.4rem !important;
    margin: 0 !important;
    letter-spacing: normal !important;
    transition: color {DURATION_FAST} !important;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color: {PRIMARY} !important;
    background: transparent !important;
}}
.stTabs [aria-selected="true"] {{
    color: {PRIMARY} !important;
    font-weight: {WEIGHT_BOLD} !important;
    border-bottom: 2px solid {PRIMARY} !important;
    background: transparent !important;
}}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {{
    display: none !important;
}}
.stTabs [data-baseweb="tab-panel"] {{
    padding: {SPACE_XL} 0 0 !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   4. CHAMPS TEXTE — SIGNATURE LINE
   ══════════════════════════════════════════════════════════════════════ */
.stTextInput > label,
.stTextInput label p {{
    font-family: {FONT_BODY} !important;
    font-size: {TEXT_XS} !important;
    font-weight: {WEIGHT_BOLD} !important;
    text-transform: uppercase !important;
    letter-spacing: {TRACK_WIDEST} !important;
    color: {SECONDARY} !important;
}}
.stTextInput [data-baseweb="input"] {{
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid {PRIMARY_A_15} !important;
    border-radius: {RADIUS_NONE} !important;
    box-shadow: none !important;
    padding: 0 !important;
    transition: border-color {DURATION_BASE} !important;
}}
.stTextInput [data-baseweb="input"]:focus-within {{
    border-bottom: 2px solid {PRIMARY} !important;
    box-shadow: none !important;
}}
.stTextInput input {{
    background: transparent !important;
    border: none !important;
    border-radius: {RADIUS_NONE} !important;
    padding: 0.9rem 0 !important;
    font-family: {FONT_HEADLINE} !important;
    font-size: {TEXT_3XL} !important;
    font-style: italic !important;
    color: {PRIMARY} !important;
    box-shadow: none !important;
}}
/* a11y : on supprime l'outline natif (laid sur input editorial),
   le focus est signalé par le doublement d'épaisseur du border-bottom.
   Pour les utilisateurs clavier, le focus-visible global ci-dessus reste actif. */
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
    font-size: {TEXT_XS} !important;
    font-weight: {WEIGHT_BOLD} !important;
    text-transform: uppercase !important;
    letter-spacing: {TRACK_WIDE} !important;
    color: {ON_SURFACE_VAR} !important;
}}
.stRadio [data-testid="stMarkdownContainer"] p {{
    font-family: {FONT_BODY} !important;
    font-size: {TEXT_BASE} !important;
    font-weight: {WEIGHT_MEDIUM} !important;
    color: {ON_SURFACE} !important;
}}
[data-baseweb="radio"] [role="radio"] {{
    border-color: {PRIMARY_A_30} !important;
    background: transparent !important;
}}
[data-baseweb="radio"] [role="radio"][aria-checked="true"] {{
    background: {PRIMARY} !important;
    border-color: {PRIMARY} !important;
}}
[data-baseweb="radio"] [role="radio"][aria-checked="true"]::after {{
    background: {ON_PRIMARY} !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   6. SLIDER
   ══════════════════════════════════════════════════════════════════════ */
.stSlider > label,
.stSlider label p {{
    font-family: {FONT_BODY} !important;
    font-size: {TEXT_XS} !important;
    font-weight: {WEIGHT_BOLD} !important;
    text-transform: uppercase !important;
    letter-spacing: {TRACK_WIDE} !important;
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
    font-size: {TEXT_SM} !important;
    font-weight: {WEIGHT_BOLD} !important;
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
    font-size: {TEXT_2XS} !important;
    font-weight: {WEIGHT_BOLD} !important;
    text-transform: uppercase !important;
    letter-spacing: {TRACK_WIDER} !important;
    color: {TEXT_MUTED} !important;
    overflow: visible !important;
}}
[data-testid="stMetricValue"] > div {{
    font-family: {FONT_HEADLINE} !important;
    font-size: {TEXT_5XL} !important;
    font-weight: {WEIGHT_BLACK} !important;
    color: {PRIMARY} !important;
    letter-spacing: {TRACK_DISPLAY} !important;
    line-height: 1 !important;
}}
[data-testid="stMetricDelta"] svg {{ display: none !important; }}


/* ══════════════════════════════════════════════════════════════════════
   8. BOUTONS
   ══════════════════════════════════════════════════════════════════════ */
.stButton > button {{
    background-color: {PRIMARY} !important;
    color: {ON_PRIMARY} !important;
    border: none !important;
    border-radius: {RADIUS_SM} !important;
    font-family: {FONT_BODY} !important;
    font-size: {TEXT_XS} !important;
    font-weight: {WEIGHT_BOLD} !important;
    text-transform: uppercase !important;
    letter-spacing: {TRACK_WIDE} !important;
    padding: 0.7rem {SPACE_XL} !important;
    transition: opacity {DURATION_FAST}, transform {DURATION_FAST} !important;
}}
.stButton > button:hover {{
    opacity: 0.88 !important;
    background-color: {PRIMARY} !important;
}}
.stButton > button:active {{
    transform: translateY(1px) !important;
}}
.stButton > button:disabled,
.stButton > button[disabled] {{
    opacity: 0.4 !important;
    cursor: not-allowed !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   9. ALERTES & MESSAGES
   ══════════════════════════════════════════════════════════════════════ */
[data-testid="stAlert"] {{
    border-radius: {RADIUS_NONE} !important;
    border: none !important;
    border-left: 3px solid {PRIMARY} !important;
    background: {SURFACE_LOW} !important;
    padding: 1.25rem {SPACE_LG} 1.25rem 1.75rem !important;
}}
[data-testid="stAlert"] p,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {{
    font-family: {FONT_HEADLINE} !important;
    font-style: italic !important;
    color: {PRIMARY} !important;
    font-size: {TEXT_LG} !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   10. DIVIDERS
   ══════════════════════════════════════════════════════════════════════ */
hr {{ border-color: {PRIMARY_A_10} !important; margin: {SPACE_2XL} 0 !important; }}


/* ══════════════════════════════════════════════════════════════════════
   11. SELECTBOX
   ══════════════════════════════════════════════════════════════════════ */
.stSelectbox > label,
.stSelectbox label p {{
    font-family: {FONT_BODY} !important;
    font-size: {TEXT_XS} !important;
    font-weight: {WEIGHT_BOLD} !important;
    text-transform: uppercase !important;
    letter-spacing: {TRACK_WIDE} !important;
    color: {ON_SURFACE_VAR} !important;
}}
.stSelectbox [data-baseweb="select"] {{
    background: transparent !important;
    border-bottom: 1px solid {PRIMARY_A_15} !important;
    border-top: none !important;
    border-left: none !important;
    border-right: none !important;
    border-radius: {RADIUS_NONE} !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   12. DATAFRAMES
   ══════════════════════════════════════════════════════════════════════ */
.stDataFrame {{
    font-family: {FONT_BODY} !important;
    font-size: {TEXT_BASE} !important;
    border: none !important;
}}
.stDataFrame thead th {{
    font-family: {FONT_BODY} !important;
    font-size: {TEXT_2XS} !important;
    font-weight: {WEIGHT_BOLD} !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: {TEXT_MUTED} !important;
    background: {SURFACE_LOW} !important;
    border: none !important;
}}
.stDataFrame tbody td {{
    font-family: {FONT_BODY} !important;
    font-size: {TEXT_BASE} !important;
    border: none !important;
    color: {ON_SURFACE} !important;
}}
.stDataFrame tbody tr:nth-child(even) {{
    background: rgba(0,0,0,0.02) !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   13. SPINNER
   ══════════════════════════════════════════════════════════════════════ */
[data-testid="stSpinner"] p {{
    font-family: {FONT_BODY} !important;
    font-size: {TEXT_SM} !important;
    font-style: italic !important;
    color: {ON_SURFACE_VAR} !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}}


/* ══════════════════════════════════════════════════════════════════════
   14. EYEBROW (label uppercase tracé) — composant unifié
   ══════════════════════════════════════════════════════════════════════
   Une seule classe de base, 3 modifiers de couleur. Toutes les anciennes
   classes (.es-stat-label, .es-hero-stat-l, .es-score-caption,
   .es-verdict-eyebrow, .es-gen-peak) sont aliasées vers le même socle
   pour rétrocompat sans casser le HTML existant.
   ══════════════════════════════════════════════════════════════════════ */
.es-eyebrow,
.es-stat-label,
.es-hero-stat-l,
.es-score-caption,
.es-verdict-eyebrow,
.es-gen-peak {{
    font-family: {FONT_BODY};
    font-size: {TEXT_2XS};
    font-weight: {WEIGHT_BOLD};
    text-transform: uppercase;
    letter-spacing: {TRACK_WIDEST};
    display: block;
    margin: 0;
    color: {SECONDARY};                 /* couleur par défaut : gold */
}}
/* Variantes par contexte */
.es-eyebrow {{ letter-spacing: {TRACK_EXTREME}; margin-bottom: 0.6rem; }}
.es-stat-label {{ font-size: {TEXT_3XS}; letter-spacing: {TRACK_WIDE}; color: {TEXT_FAINT}; }}
.es-hero-stat-l {{ font-size: {TEXT_3XS}; color: {TEXT_SUBTLE}; margin-bottom: 0.2rem; }}
.es-score-caption {{ font-size: {TEXT_3XS}; color: {TEXT_SUBTLE}; margin-top: 0.2rem; }}
.es-verdict-eyebrow {{ font-size: {TEXT_3XS}; color: {ON_PRIMARY_EYEBROW}; margin-bottom: 0.75rem; }}
.es-gen-peak {{ letter-spacing: {TRACK_WIDER}; color: {ON_PRIMARY_EYEBROW}; }}


/* ══════════════════════════════════════════════════════════════════════
   15. COMPOSANTS CUSTOM (.es-*)
   ══════════════════════════════════════════════════════════════════════ */

/* Input hero wrapper */
.es-input-hero {{
    padding: {SPACE_2XL} 0 {SPACE_MD};
    border-bottom: 1px solid {PRIMARY_A_08};
    margin-bottom: {SPACE_XL};
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
    font-weight: {WEIGHT_BLACK};
    color: {PRIMARY};
    letter-spacing: {TRACK_DISPLAY};
    line-height: 0.95;
    margin: 0 0 {SPACE_2XS};
}}

/* Gender pill */
.es-gender-pill {{
    font-family: {FONT_BODY};
    font-size: {TEXT_2XS};
    font-weight: {WEIGHT_BOLD};
    text-transform: uppercase;
    letter-spacing: {TRACK_WIDEST};
    border: 1px solid rgba(119,90,25,0.3);
    padding: 0.2rem 0.6rem;
    color: {SECONDARY};
    display: inline-block;
    margin-bottom: {SPACE_LG};
}}

/* Score row */
.es-score-row {{
    display: flex;
    align-items: baseline;
    gap: 0.6rem;
    margin: {SPACE_XS} 0 {SPACE_2XS};
}}
.es-score-num {{
    font-family: {FONT_HEADLINE};
    font-size: clamp(3rem, 7vw, 5rem);
    font-weight: {WEIGHT_BLACK};
    color: {PRIMARY};
    letter-spacing: {TRACK_DISPLAY};
    line-height: 1;
}}
.es-score-unit {{
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-size: 1.4rem;
    color: {SECONDARY};
}}

/* Percentile bar */
.es-pct-bar-wrap {{
    margin: 1.25rem 0 {SPACE_XS};
    max-width: 420px;
}}
.es-pct-bar-track {{
    height: 4px;
    background: {SURFACE_HIGH};
    border-radius: {RADIUS_SM};
    position: relative;
    margin-bottom: 0.4rem;
}}
.es-pct-bar-fill {{
    height: 100%;
    background: {PRIMARY};
    border-radius: {RADIUS_SM};
    transition: width {DURATION_SLOW} ease;
}}
.es-pct-label {{
    font-family: {FONT_BODY};
    font-size: {TEXT_XS};
    font-weight: {WEIGHT_SEMIBOLD};
    color: {TEXT_MUTED};
}}

/* Stats row */
.es-stats-row {{
    display: flex;
    gap: {SPACE_XL};
    margin-top: 1.25rem;
    padding-top: {SPACE_MD};
    border-top: 1px solid {PRIMARY_A_08};
}}
.es-stat-item {{
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}}
.es-stat-val {{
    font-family: {FONT_BODY};
    font-size: {TEXT_MD};
    font-weight: {WEIGHT_BOLD};
    color: {PRIMARY};
}}

/* Verdict */
.es-verdict {{
    margin-top: {SPACE_LG};
    padding: 1.75rem {SPACE_XL};
    background: {PRIMARY};
    color: {ON_PRIMARY};
}}
.es-verdict-stars {{
    color: {GOLD_ACCENT};
    font-size: {TEXT_LG};
    float: right;
}}
.es-verdict-text {{
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-size: {TEXT_XL};
    color: {ON_PRIMARY_STRONG};
    line-height: 1.8;
    margin: 0;
}}

/* Data note (prénoms scrape-only) — composant dédié */
.es-data-note {{
    margin-top: {SPACE_LG};
    padding: {SPACE_MD} 1.25rem;
    background: {SURFACE_LOW};
    border-left: 3px solid {SECONDARY};
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-size: {TEXT_MD};
    color: {ON_SURFACE_VAR};
}}

/* Absent */
.es-absent {{
    border-left: 3px solid {SECONDARY};
    background: {SURFACE_LOW};
    padding: 1.25rem 1.75rem;
    margin-bottom: {SPACE_MD};
}}
.es-absent-text {{
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-size: {TEXT_LG};
    color: {ON_SURFACE};
    margin: 0 0 {SPACE_XS};
}}
.es-absent-pills {{ margin-top: {SPACE_XS}; }}

/* Pill (suggestion clickable) — a11y : hover + focus visibles */
.es-pill {{
    font-family: {FONT_BODY};
    font-size: {TEXT_SM};
    font-weight: {WEIGHT_SEMIBOLD};
    background: {SURFACE_HIGH};
    padding: 0.2rem 0.65rem;
    display: inline-block;
    margin: 0.2rem 0.15rem 0 0;
    color: {PRIMARY};
    cursor: pointer;
    border-radius: {RADIUS_SM};
    transition: background {DURATION_FAST}, color {DURATION_FAST};
}}
.es-pill:hover {{
    background: {PRIMARY};
    color: {ON_PRIMARY};
}}
.es-pill:focus-visible {{
    outline: {FOCUS_RING_WIDTH} solid {FOCUS_RING_COLOR};
    outline-offset: {FOCUS_RING_OFFSET};
}}

/* Duel */
.es-duel-wrap {{
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: {SPACE_XS};
    align-items: stretch;
    margin-bottom: {SPACE_LG};
}}
.es-duel-card {{
    padding: 1.75rem {SPACE_XL};
    background: {SURFACE_LOW};
}}
.es-duel-card.winner {{
    background: {PRIMARY};
    color: {ON_PRIMARY};
}}
.es-duel-name {{
    font-family: {FONT_HEADLINE};
    font-size: clamp(1.75rem, 4vw, 2.75rem);
    font-weight: {WEIGHT_BLACK};
    letter-spacing: {TRACK_TITLE};
    margin: 0 0 {SPACE_2XS};
}}
.es-duel-score {{
    font-family: {FONT_HEADLINE};
    font-size: {TEXT_4XL};
    font-weight: {WEIGHT_BLACK};
    letter-spacing: {TRACK_TITLE};
    margin: {SPACE_SM} 0 {SPACE_2XS};
}}
.es-duel-score-unit {{
    font-size: {TEXT_LG};
    font-weight: {WEIGHT_NORMAL};
    opacity: 0.7;
}}
.es-duel-bar {{
    height: 3px;
    background: {PRIMARY_A_15};
    margin: {SPACE_XS} 0 {SPACE_SM};
}}
.es-duel-caption {{
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-size: 0.8rem;
    color: {TEXT_MUTED};
    line-height: 1.6;
    margin-top: {SPACE_SM};
}}
.es-duel-card.winner .es-duel-caption {{
    color: {ON_PRIMARY_MUTED};
}}
.es-vs {{
    width: {SPACE_3XL};
    height: {SPACE_3XL};
    background: {PRIMARY};
    color: {ON_PRIMARY};
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-weight: {WEIGHT_BLACK};
    font-size: 1.1rem;
    align-self: center;
    flex-shrink: 0;
}}
.es-duel-result {{
    padding: {SPACE_MD} 1.75rem;
    background: {PRIMARY};
    color: {ON_PRIMARY};
    margin-bottom: {SPACE_LG};
    display: flex;
    align-items: baseline;
    gap: {SPACE_MD};
}}
.es-duel-result-winner {{
    font-family: {FONT_HEADLINE};
    font-size: {TEXT_2XL};
    font-weight: {WEIGHT_BLACK};
    font-style: italic;
    color: {GOLD_ACCENT};
}}
.es-duel-result-meta {{
    font-family: {FONT_BODY};
    font-size: {TEXT_SM};
    font-weight: {WEIGHT_BOLD};
    text-transform: uppercase;
    letter-spacing: {TRACK_WIDE};
    color: {ON_PRIMARY_FAINT};
}}
.es-duel-result-tie {{
    font-family: {FONT_HEADLINE};
    font-size: 1.1rem;
    font-style: italic;
    color: {ON_PRIMARY_STRONG};
}}

/* Section */
.es-section {{ margin-bottom: 1.75rem; }}
.es-h1 {{
    font-family: {FONT_HEADLINE};
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: {WEIGHT_BLACK};
    color: {PRIMARY};
    letter-spacing: {TRACK_TITLE};
    margin: 0 0 0.4rem;
    line-height: 1.05;
}}
.es-lead {{
    font-family: {FONT_HEADLINE};
    font-style: italic;
    font-size: {TEXT_LG};
    color: {TEXT_MUTED};
    margin: 0 0 {SPACE_LG};
}}

/* Generation cards */
.es-gen-card {{
    padding: 1.75rem {SPACE_XL};
    background: {PRIMARY};
    color: {ON_PRIMARY};
}}
.es-gen-vibe {{
    font-size: {SPACE_XL};
    display: block;
    margin-bottom: {SPACE_XS};
}}
.es-gen-label {{
    font-family: {FONT_HEADLINE};
    font-size: {TEXT_3XL};
    font-weight: {WEIGHT_BLACK};
    color: {ON_PRIMARY};
    margin: 0 0 0.2rem;
}}

/* Rank card */
.es-rank-card {{
    padding: 1.75rem {SPACE_XL};
    background: {SURFACE_LOW};
}}
.es-rank-num {{
    font-family: {FONT_HEADLINE};
    font-size: {TEXT_4XL};
    font-weight: {WEIGHT_BLACK};
    color: {PRIMARY};
    letter-spacing: {TRACK_TITLE};
}}
.es-rank-caption {{
    font-family: {FONT_BODY};
    font-size: {TEXT_SM};
    color: {TEXT_MUTED};
    margin-top: 0.35rem;
}}

/* Top/Flop 3 generation */
.es-genflop {{
    margin-top: {SPACE_LG};
    display: flex;
    gap: {SPACE_XL};
}}
.es-genflop-list {{
    font-family: {FONT_HEADLINE};
    font-size: {TEXT_LG};
    font-weight: {WEIGHT_BOLD};
    color: {PRIMARY};
}}
.es-genflop-list--flop {{ color: {TERTIARY}; }}

/* Hero */
.es-hero {{ padding: {SPACE_3XL} 0 {SPACE_XL}; }}
.es-hero-title {{
    font-family: {FONT_HEADLINE};
    font-size: clamp(3rem, 8vw, 5.5rem);
    font-weight: {WEIGHT_BLACK};
    color: {PRIMARY};
    letter-spacing: {TRACK_DISPLAY};
    line-height: 1;
    margin: 0 0 {SPACE_MD};
}}
.es-hero-lead {{
    font-family: {FONT_BODY};
    font-size: 0.95rem;
    color: #444;
    max-width: 500px;
    line-height: 1.85;
    margin: 0 0 {SPACE_XL};
}}
.es-hero-stats {{
    display: flex;
    gap: {SPACE_2XL};
    border-top: 1px solid {PRIMARY_A_08};
    padding-top: 1.25rem;
}}
.es-hero-stat-n {{
    font-family: {FONT_HEADLINE};
    font-size: {TEXT_3XL};
    font-weight: {WEIGHT_BLACK};
    color: {PRIMARY};
    letter-spacing: {TRACK_TITLE};
}}

/* Footer */
.es-footer {{
    border-top: 1px solid {OUTLINE_FAINT};
    margin-top: {SPACE_3XL};
    padding-top: {SPACE_LG};
}}
.es-footer p {{
    font-family: {FONT_BODY};
    font-size: {TEXT_XS};
    color: {ON_SURFACE_VAR};
    line-height: 2;
}}
.es-footer a {{ color: {PRIMARY}; }}

/* Carto subtitle (total naissances) */
.es-carto-meta {{
    font-family: {FONT_BODY};
    font-size: {TEXT_SM};
    font-weight: {WEIGHT_SEMIBOLD};
    text-transform: uppercase;
    letter-spacing: {TRACK_WIDE};
    color: {ON_SURFACE_VAR};
    margin-bottom: {SPACE_LG};
}}
.es-carto-meta strong {{ color: {PRIMARY}; }}

/* Rule */
.es-rule {{
    border: none;
    border-top: 1px solid {PRIMARY_A_10};
    margin: {SPACE_2XL} 0;
}}

</style>
"""


def inject_css() -> None:
    """Injecte l'intégralité du design system dans l'app Streamlit."""
    st.html(_CSS)
