"""
Composants HTML pour le design system "The Editorial Scholar".

Chaque fonction retourne une chaîne HTML à injecter via
st.markdown(..., unsafe_allow_html=True).

Les classes CSS (.es-*) sont définies dans src/styles.py.

⚠️ Sécurité : toute valeur provenant directement ou indirectement d'une
saisie utilisateur passe par html.escape() avant interpolation pour
neutraliser les XSS (unsafe_allow_html=True est actif).
"""

from html import escape as _esc


# ── Utilitaires internes ───────────────────────────────────────────────────────

def _stars(score: float) -> str:
    """Retourne 1 à 5 étoiles selon le score."""
    if score >= 22:
        return "★★★★★"
    if score >= 17:
        return "★★★★☆"
    if score >= 13:
        return "★★★☆☆"
    if score >= 8:
        return "★★☆☆☆"
    return "★☆☆☆☆"


def _percentile_label(pct: float) -> str:
    if pct >= 90:
        return "Élite académique"
    if pct >= 75:
        return "Haute performance"
    if pct >= 50:
        return "Au-dessus de la médiane"
    if pct >= 25:
        return "Dans la norme"
    return "Bas du classement"


# ── Hero ───────────────────────────────────────────────────────────────────────

def _format_n(n: int) -> str:
    """Format compact : 1756 → '1 756', 2_300_000 → '2,3 M', 950000 → '950 k'."""
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}".rstrip("0").rstrip(".").replace(".", ",") + " M"
    if n >= 100_000:
        return f"{n/1000:.0f} k"
    # Espaces fines insécables comme séparateur de milliers (typo française)
    return f"{n:,}".replace(",", " ")


def hero_html(n_prenoms: int = 417, n_bacheliers: int = 2_000_000) -> str:
    """Hero affiché avant toute saisie dans l'onglet Anthologie.

    Args:
        n_prenoms: nombre de prénoms dans le dataset unifié (TSV + scrape).
        n_bacheliers: somme des effectifs (cumul TSV année/année + scrape cumulé).
    """
    n_p = _format_n(int(n_prenoms))
    n_b = _format_n(int(n_bacheliers))
    return f"""
<div class="es-hero">
  <span class="es-eyebrow">L'Érudit des Prénoms · Édition 2012-2020</span>
  <h1 class="es-hero-title">Votre prénom<br>méritait-il<br><em>la mention&nbsp;?</em></h1>
  <p class="es-hero-lead">
    {n_b}&nbsp;de résultats nominatifs du baccalauréat général et technologique.
    Entrez un prénom ci-dessous pour connaître son <strong>Score de Prestige Académique</strong>.
  </p>
  <div class="es-hero-stats">
    <div>
      <span class="es-hero-stat-l">Prénoms analysés</span>
      <span class="es-hero-stat-n">{n_p}</span>
    </div>
    <div>
      <span class="es-hero-stat-l">Bacheliers recensés</span>
      <span class="es-hero-stat-n">{n_b}</span>
    </div>
    <div>
      <span class="es-hero-stat-l">Années couvertes</span>
      <span class="es-hero-stat-n">2012–2020</span>
    </div>
  </div>
</div>
"""


# ── Carte résultat ─────────────────────────────────────────────────────────────

def result_card_html(result: dict) -> str:
    """
    Carte résultat principale pour un prénom trouvé.
    result keys: prenom, score, rank_pct, effectif_total, years_present, sexe_label, verdict
    """
    prenom   = _esc(str(result["prenom"]))
    score    = float(result["score"])
    rank_pct = float(result["rank_pct"])
    effectif = int(result["effectif_total"])
    years    = int(result["years_present"])
    sexe     = _esc(str(result["sexe_label"]))

    pct_label = _percentile_label(rank_pct)
    bar_width = min(100.0, rank_pct)

    return f"""
<div class="es-result">
  <span class="es-gender-pill">{sexe}</span>
  <div class="es-name">{prenom}</div>

  <div class="es-score-row">
    <span class="es-score-num">{score:.1f}</span>
    <span class="es-score-unit">%&nbsp;TB</span>
  </div>
  <span class="es-score-caption">Score de Prestige Académique</span>

  <div class="es-pct-bar-wrap">
    <div class="es-pct-bar-track">
      <div class="es-pct-bar-fill" style="width:{bar_width:.1f}%"></div>
    </div>
    <span class="es-pct-label">{rank_pct:.0f}e&nbsp;percentile — {pct_label}</span>
  </div>

  <div class="es-stats-row">
    <div class="es-stat-item">
      <span class="es-stat-label">Bacheliers analysés</span>
      <span class="es-stat-val">{effectif:,}</span>
    </div>
    <div class="es-stat-item">
      <span class="es-stat-label">Années de données</span>
      <span class="es-stat-val">{years}&thinsp;/&thinsp;9</span>
    </div>
    <div class="es-stat-item">
      <span class="es-stat-label">Classement</span>
      <span class="es-stat-val">Top&nbsp;{100 - rank_pct:.0f}&nbsp;%</span>
    </div>
  </div>
</div>
"""


def verdict_card_html(result: dict) -> str:
    """Carte verdict sur fond Royal Blue."""
    stars   = _stars(float(result["score"]))
    verdict = _esc(str(result["verdict"]))

    return f"""
<div class="es-verdict">
  <span class="es-verdict-stars">{stars}</span>
  <span class="es-verdict-eyebrow">Le Verdict du Jury</span>
  <p class="es-verdict-text">{verdict}</p>
</div>
"""


# ── Carte prénom absent ────────────────────────────────────────────────────────

def absent_card_html(prenom: str, message: str, suggestions: list) -> str:
    """Carte gold-bordered pour un prénom absent du dataset.

    ⚠️ prenom et message contiennent de la saisie utilisateur : escape obligatoire.
    """
    safe_message = _esc(str(message))
    pills = "".join(
        f'<span class="es-pill">{_esc(str(s))}</span>' for s in (suggestions or [])
    )
    sug_block = (
        f'<div class="es-absent-pills">{pills}</div>'
        if suggestions else ""
    )
    # prenom n'est pas affiché ici (il est déjà dans message), mais on garde
    # la signature pour rétrocompat.
    _ = prenom  # volontairement inutilisé dans le rendu
    return f"""
<div class="es-absent">
  <p class="es-absent-text">{safe_message}</p>
  {sug_block}
</div>
"""


# ── Section header ─────────────────────────────────────────────────────────────

def section_header_html(eyebrow: str, title: str, subtitle: str = "") -> str:
    """En-tête éditoriale avec eyebrow + titre Newsreader + sous-titre italique."""
    e = _esc(str(eyebrow))
    t = _esc(str(title))
    sub = f'<p class="es-lead">{_esc(str(subtitle))}</p>' if subtitle else ""
    return f"""
<div class="es-section">
  <span class="es-eyebrow">{e}</span>
  <h1 class="es-h1">{t}</h1>
  {sub}
</div>
"""


# ── VS Duel ───────────────────────────────────────────────────────────────────

def duel_result_html(res_a: dict, res_b: dict) -> str:
    """Bannière victoire / match nul."""
    diff = float(res_a["score"]) - float(res_b["score"])
    if abs(diff) < 0.5:
        return """
<div class="es-duel-result">
  <span style="font-family:'Newsreader',Georgia,serif;font-size:1.1rem;font-style:italic;color:rgba(255,255,255,0.9)">
    Match nul — Vos prénoms sont statistiquement à égalité. Décidez à la courte paille.
  </span>
</div>
"""
    winner = res_a if diff > 0 else res_b
    loser  = res_b if diff > 0 else res_a
    gap    = abs(diff)
    suffix = "s" if gap >= 2 else ""
    w_name = _esc(str(winner["prenom"]))
    l_name = _esc(str(loser["prenom"]))
    return f"""
<div class="es-duel-result">
  <span style="font-family:'Newsreader',Georgia,serif;font-size:1.4rem;font-weight:900;font-style:italic;color:#fed488">{w_name}</span>
  <span style="font-family:'Inter',system-ui,sans-serif;font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:rgba(255,255,255,0.7)">domine par {gap:.1f}&thinsp;pt{suffix} — {l_name} s'incline</span>
</div>
"""


def duel_cards_html(res_a: dict, res_b: dict) -> str:
    """Les deux cartes duel + badge VS en un seul bloc grille."""
    score_a = float(res_a["score"])
    score_b = float(res_b["score"])
    diff      = score_a - score_b
    a_wins    = diff > 0
    tie       = abs(diff) < 0.5

    bar_a = min(100.0, score_a / 30 * 100)
    bar_b = min(100.0, score_b / 30 * 100)

    class_a  = "es-duel-card winner" if (a_wins and not tie) else "es-duel-card"
    class_b  = "es-duel-card winner" if (not a_wins and not tie) else "es-duel-card"
    fill_a   = "#001360" if (a_wins or tie) else "rgba(0,19,96,0.4)"
    fill_b   = "#001360" if (not a_wins or tie) else "rgba(0,19,96,0.4)"

    name_a = _esc(str(res_a["prenom"]))
    name_b = _esc(str(res_b["prenom"]))
    verd_a = _esc(str(res_a["verdict"]))
    verd_b = _esc(str(res_b["verdict"]))

    return f"""
<div class="es-duel-wrap">
  <div class="{class_a}">
    <div class="es-duel-name">{name_a}</div>
    <div class="es-duel-score">{score_a:.1f}&thinsp;<span style="font-size:1rem;font-weight:400;opacity:.7">% TB</span></div>
    <div class="es-duel-bar"><div style="height:100%;background:{fill_a};width:{bar_a:.1f}%"></div></div>
    <div class="es-duel-caption">{verd_a}</div>
  </div>

  <div class="es-vs">VS</div>

  <div class="{class_b}">
    <div class="es-duel-name">{name_b}</div>
    <div class="es-duel-score">{score_b:.1f}&thinsp;<span style="font-size:1rem;font-weight:400;opacity:.7">% TB</span></div>
    <div class="es-duel-bar"><div style="height:100%;background:{fill_b};width:{bar_b:.1f}%"></div></div>
    <div class="es-duel-caption">{verd_b}</div>
  </div>
</div>
"""


# ── Génération / Décennie ─────────────────────────────────────────────────────

def gen_card_html(vibe: str, label: str, peak_year: int) -> str:
    """Carte génération sur fond Royal Blue."""
    v = _esc(str(vibe))
    l = _esc(str(label))
    p = int(peak_year)
    return f"""
<div class="es-gen-card">
  <span class="es-gen-vibe">{v}</span>
  <div class="es-gen-label">{l}</div>
  <p class="es-gen-peak">Pic de popularité : {p}</p>
</div>
"""


def gen_rank_html(rank_str: str, total: int, prenom: str) -> str:
    """Bloc de rang dans la décennie."""
    r = _esc(str(rank_str))
    t = int(total)
    _ = prenom  # non affiché directement, mais gardé dans la signature
    return f"""
<div class="es-rank-card">
  <span class="es-stat-label">Rang dans sa génération</span>
  <div class="es-rank-num">{r}</div>
  <div class="es-rank-caption">parmi {t} prénoms de la même génération</div>
</div>
"""
