"""
Thème Plotly "editorial_scholar".

Palette Royal Blue / Gold, pas de grilles, typographie Inter/Newsreader.
À appliquer via : fig.update_layout(template="editorial_scholar")

Usage dans app.py :
    from src.plotly_theme import apply_theme
    apply_theme()   # à appeler une seule fois au démarrage
"""

import plotly.graph_objects as go
import plotly.io as pio

# ── Tokens ────────────────────────────────────────────────────────────────────
# Source unique : src/tokens.py. On ré-exporte sous les noms historiques pour
# rétrocompat (app.py importe ON_SURF, PRIMARY, SECONDARY, TB_COLORSCALE…).
from src.tokens import (
    ON_SURFACE as ON_SURF,
    ON_SURFACE_VAR as ON_SURF_V,
    PRIMARY,
    SECONDARY,
    SURFACE,
    SURFACE_LOW as SURFACE_L,
    TERTIARY,
)

# Séquence de couleurs catégorielles
COLOR_SEQ = [
    PRIMARY,
    SECONDARY,
    TERTIARY,
    "#2d4de0",
    "#b58900",
    "#78002b",
    "#5f6a8a",
    "#a07830",
]

# Dégradé continu : Parchment → Royal Blue
COLORSCALE = [
    [0.0,  "#faf9f5"],
    [0.25, "#b8c0e0"],
    [0.50, "#7080c0"],
    [0.75, "#3050a0"],
    [1.0,  PRIMARY],
]

# Dégradé continu pour bar charts TB : rouge → vert éditorial
TB_COLORSCALE = [
    [0.0,  TERTIARY],
    [0.35, "#775a19"],
    [0.65, "#3a6ea5"],
    [1.0,  PRIMARY],
]

FONT_BODY     = "Inter, system-ui, sans-serif"
FONT_HEADLINE = "Newsreader, Georgia, serif"


def _make_template() -> go.layout.Template:
    # Defaults choisis pour matcher l'usage réel dans app.py :
    # - showgrid=False (chaque chart active la grille en y si besoin)
    # - showline=False (pas d'axe visible — le design est minimaliste)
    # - gridcolor préréglée pour quand un chart fait showgrid=True
    axis_common = dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        gridcolor="rgba(197,197,213,0.25)",
        linecolor="rgba(197,197,213,0.4)",
        tickfont=dict(family=FONT_BODY, size=10, color=ON_SURF_V),
        title_font=dict(family=FONT_BODY, size=11, color=ON_SURF_V),
    )

    tmpl = go.layout.Template()

    tmpl.layout = go.Layout(
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font=dict(family=FONT_BODY, size=12, color=ON_SURF),
        # Taille 18 = ce qui est utilisé partout dans app.py
        title=dict(
            font=dict(family=FONT_HEADLINE, size=18, color=PRIMARY),
            x=0,
            xanchor="left",
            pad=dict(l=0, b=12),
        ),
        legend=dict(
            font=dict(family=FONT_BODY, size=11, color=ON_SURF_V),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
        ),
        xaxis=axis_common,
        yaxis=axis_common,
        margin=dict(l=0, r=0, t=48, b=16),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="rgba(197,197,213,0.6)",
            font=dict(family=FONT_BODY, size=12, color=ON_SURF),
        ),
        colorway=COLOR_SEQ,
        coloraxis=dict(
            colorbar=dict(
                tickfont=dict(family=FONT_BODY, size=10, color=ON_SURF_V),
                title_font=dict(family=FONT_BODY, size=11, color=ON_SURF_V),
                outlinewidth=0,
                ticks="outside",
                ticklen=4,
                tickcolor="rgba(197,197,213,0.6)",
            )
        ),
    )

    # Valeurs par défaut des traces (API stable)
    tmpl.data.scatter = [go.Scatter(
        line=dict(width=2.5),
        marker=dict(size=7, line=dict(width=1.5, color=SURFACE)),
    )]
    tmpl.data.bar = [go.Bar(
        marker=dict(line=dict(width=0)),
    )]
    tmpl.data.box = [go.Box(
        line=dict(color=PRIMARY),
        fillcolor="rgba(0,19,96,0.07)",
        marker=dict(color=PRIMARY, size=4, opacity=0.5),
    )]

    return tmpl


_TEMPLATE_NAME = "editorial_scholar"


def apply_theme() -> None:
    """
    Enregistre et active le thème Plotly editorial_scholar.
    À appeler une seule fois au démarrage de l'app.
    """
    pio.templates[_TEMPLATE_NAME] = _make_template()
    pio.templates.default = _TEMPLATE_NAME


def gradient_blue(n: int, alpha_start: float = 0.30, alpha_end: float = 0.95) -> list[str]:
    """Génère une liste de ``n`` couleurs ``rgba(0,19,96, α)`` interpolées
    linéairement entre ``alpha_start`` et ``alpha_end``.

    Utile pour les bar charts ordonnés (gradient d'opacité du PRIMARY).
    Centralise la formule qui était dupliquée dans app.py.
    """
    if n <= 0:
        return []
    if n == 1:
        return [f"rgba(0,19,96,{alpha_end:.2f})"]
    span = alpha_end - alpha_start
    return [
        f"rgba(0,19,96,{alpha_start + span * i / (n - 1):.2f})"
        for i in range(n)
    ]
