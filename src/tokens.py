"""
Design tokens — *The Editorial Scholar*.

Source unique de vérité pour couleurs / typographie / spacing / tracking /
transitions. Importé par ``src/styles.py`` (CSS) et ``src/plotly_theme.py``
(charts) pour garantir la cohérence visuelle.

Convention :
  - Couleurs : hex direct (compatibles Plotly + CSS)
  - Tailles  : strings ``"0.85rem"`` (CSS-ready)
  - Tracking : strings ``"0.14em"``
"""

# ══════════════════════════════════════════════════════════════════════════════
# COULEURS
# ══════════════════════════════════════════════════════════════════════════════

# Brand
PRIMARY   = "#001360"   # Royal Blue
SECONDARY = "#775a19"   # Editorial Gold
TERTIARY  = "#470003"   # Editorial Red

# Surfaces (échelle parchment)
SURFACE           = "#faf9f5"
SURFACE_LOW       = "#f4f4f0"
SURFACE_CONTAINER = "#efeeea"
SURFACE_HIGH      = "#e9e8e4"
SURFACE_HIGHEST   = "#e3e2df"

# Texte
ON_SURFACE     = "#1b1c1a"   # corps principal
ON_SURFACE_VAR = "#444653"   # texte secondaire
TEXT_MUTED     = "#666666"   # captions, hints
TEXT_SUBTLE    = "#888888"   # micro-labels secondaires
TEXT_FAINT     = "#999999"   # micro-labels tertiaires

# Sur fond Royal Blue
ON_PRIMARY         = "#ffffff"
ON_PRIMARY_STRONG  = "rgba(255,255,255,0.9)"
ON_PRIMARY_MUTED   = "rgba(255,255,255,0.75)"
ON_PRIMARY_FAINT   = "rgba(255,255,255,0.7)"
ON_PRIMARY_EYEBROW = "rgba(186,195,255,0.7)"   # eyebrow sur Royal Blue
GOLD_ACCENT        = "#fed488"                  # accent (étoiles, victoire)

# Outlines neutres (charts, dividers)
OUTLINE_FILL   = "rgba(197,197,213,0.08)"   # fond d'area fill
OUTLINE_FAINT  = "rgba(197,197,213,0.25)"   # grille chart
OUTLINE_VAR    = "rgba(197,197,213,0.3)"    # dividers UI
OUTLINE        = "rgba(197,197,213,0.4)"    # axis lines
OUTLINE_STRONG = "rgba(197,197,213,0.6)"    # hover border / trait principal

# PRIMARY avec opacité (dérivés — pour borders et fonds discrets)
PRIMARY_A_08 = "rgba(0,19,96,0.08)"
PRIMARY_A_10 = "rgba(0,19,96,0.10)"
PRIMARY_A_12 = "rgba(0,19,96,0.12)"
PRIMARY_A_15 = "rgba(0,19,96,0.15)"
PRIMARY_A_25 = "rgba(0,19,96,0.25)"
PRIMARY_A_30 = "rgba(0,19,96,0.30)"
PRIMARY_A_40 = "rgba(0,19,96,0.40)"


# ══════════════════════════════════════════════════════════════════════════════
# TYPOGRAPHIE
# ══════════════════════════════════════════════════════════════════════════════

FONT_HEADLINE = "'Newsreader', Georgia, serif"
FONT_BODY     = "'Inter', system-ui, sans-serif"

# Échelle (rem) — alignée sur l'usage réel du dataset visuel
TEXT_3XS  = "0.5rem"     # micro-labels (stats, hero)
TEXT_2XS  = "0.55rem"    # eyebrows standard
TEXT_XS   = "0.6rem"     # eyebrows wide (input, radio)
TEXT_SM   = "0.7rem"     # captions / footer
TEXT_BASE = "0.85rem"    # corps de texte
TEXT_MD   = "0.9rem"     # paragraphe pondéré
TEXT_LG   = "1rem"       # alerte / verdict
TEXT_XL   = "1.05rem"    # verdict body
TEXT_2XL  = "1.4rem"     # score unit
TEXT_3XL  = "1.75rem"    # input hero
TEXT_4XL  = "2.25rem"    # rank-num
TEXT_5XL  = "2.8rem"     # metric value

# Poids
WEIGHT_NORMAL   = "400"
WEIGHT_MEDIUM   = "500"
WEIGHT_SEMIBOLD = "600"
WEIGHT_BOLD     = "700"
WEIGHT_BLACK    = "900"

# Letter-spacing
TRACK_DISPLAY = "-0.04em"  # gros titres editorial
TRACK_TITLE   = "-0.03em"  # titres moyens
TRACK_NORMAL  = "normal"
TRACK_WIDE    = "0.12em"   # eyebrows standard
TRACK_WIDER   = "0.13em"   # eyebrows medium
TRACK_WIDEST  = "0.14em"   # eyebrows aérés
TRACK_EXTREME = "0.16em"   # eyebrows hero / section header


# ══════════════════════════════════════════════════════════════════════════════
# SPACING
# ══════════════════════════════════════════════════════════════════════════════

SPACE_2XS = "0.25rem"
SPACE_XS  = "0.5rem"
SPACE_SM  = "0.75rem"
SPACE_MD  = "1rem"
SPACE_LG  = "1.5rem"
SPACE_XL  = "2rem"
SPACE_2XL = "2.5rem"
SPACE_3XL = "3rem"
SPACE_4XL = "5rem"


# ══════════════════════════════════════════════════════════════════════════════
# DIVERS
# ══════════════════════════════════════════════════════════════════════════════

RADIUS_NONE = "0"
RADIUS_SM   = "2px"

DURATION_FAST = "0.2s"
DURATION_BASE = "0.25s"
DURATION_SLOW = "0.6s"

# Focus ring (a11y)
FOCUS_RING_WIDTH  = "2px"
FOCUS_RING_OFFSET = "2px"
FOCUS_RING_COLOR  = PRIMARY
