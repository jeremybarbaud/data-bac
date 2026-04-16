"""
Composants HTML pour le design system "The Editorial Scholar".

Chaque fonction retourne une chaîne HTML à injecter via
st.markdown(..., unsafe_allow_html=True).

Les classes CSS (.es-*) sont définies dans src/styles.py.
"""


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

def hero_html() -> str:
    """Hero affiché avant toute saisie dans l'onglet Anthologie."""
    return """
<div class="es-hero">
  <span class="es-eyebrow">L'Érudit des Prénoms · Édition 2012-2020</span>
  <h1 class="es-hero-title">Votre prénom<br>méritait-il<br><em>la mention&nbsp;?</em></h1>
  <p class="es-hero-lead">
    2 millions de résultats nominatifs du baccalauréat général et technologique.
    Entrez un prénom ci-dessous pour connaître son <strong>Score de Prestige Académique</strong>.
  </p>
  <div class="es-hero-stats">
    <div>
      <span class="es-hero-stat-l">Prénoms analysés</span>
      <span class="es-hero-stat-n">417</span>
    </div>
    <div>
      <span class="es-hero-stat-l">Bacheliers recensés</span>
      <span class="es-hero-stat-n">2&nbsp;M+</span>
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
    prenom   = result["prenom"]
    score    = result["score"]
    rank_pct = result["rank_pct"]
    effectif = result["effectif_total"]
    years    = result["years_present"]
    sexe     = result["sexe_label"]

    pct_label = _percentile_label(rank_pct)
    bar_width = min(100, rank_pct)

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
    stars   = _stars(result["score"])
    verdict = result["verdict"]

    return f"""
<div class="es-verdict">
  <span class="es-verdict-stars">{stars}</span>
  <span class="es-verdict-eyebrow">Le Verdict du Jury</span>
  <p class="es-verdict-text">{verdict}</p>
</div>
"""


# ── Carte prénom absent ────────────────────────────────────────────────────────

def absent_card_html(prenom: str, message: str, suggestions: list) -> str:
    """Carte gold-bordered pour un prénom absent du dataset."""
    pills = "".join(
        f'<span class="es-pill">{s}</span>' for s in suggestions
    )
    sug_block = (
        f'<div class="es-absent-pills">{pills}</div>'
        if suggestions else ""
    )
    return f"""
<div class="es-absent">
  <p class="es-absent-text">{message}</p>
  {sug_block}
</div>
"""


# ── Section header ─────────────────────────────────────────────────────────────

def section_header_html(eyebrow: str, title: str, subtitle: str = "") -> str:
    """En-tête éditoriale avec eyebrow + titre Newsreader + sous-titre italique."""
    sub = f'<p class="es-lead">{subtitle}</p>' if subtitle else ""
    return f"""
<div class="es-section">
  <span class="es-eyebrow">{eyebrow}</span>
  <h1 class="es-h1">{title}</h1>
  {sub}
</div>
"""


# ── VS Duel ───────────────────────────────────────────────────────────────────

def duel_result_html(res_a: dict, res_b: dict) -> str:
    """Bannière victoire / match nul."""
    diff = res_a["score"] - res_b["score"]
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
    return f"""
<div class="es-duel-result">
  <span style="font-family:'Newsreader',Georgia,serif;font-size:1.4rem;font-weight:900;font-style:italic;color:#fed488">{winner['prenom']}</span>
  <span style="font-family:'Inter',system-ui,sans-serif;font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:rgba(255,255,255,0.7)">domine par {gap:.1f}&thinsp;pt{suffix} — {loser['prenom']} s'incline</span>
</div>
"""


def duel_cards_html(res_a: dict, res_b: dict) -> str:
    """Les deux cartes duel + badge VS en un seul bloc grille."""
    diff      = res_a["score"] - res_b["score"]
    a_wins    = diff > 0
    tie       = abs(diff) < 0.5

    bar_a = min(100, res_a["score"] / 30 * 100)
    bar_b = min(100, res_b["score"] / 30 * 100)

    class_a  = "es-duel-card winner" if (a_wins and not tie) else "es-duel-card"
    class_b  = "es-duel-card winner" if (not a_wins and not tie) else "es-duel-card"
    fill_a   = "#001360" if (a_wins or tie) else "rgba(0,19,96,0.4)"
    fill_b   = "#001360" if (not a_wins or tie) else "rgba(0,19,96,0.4)"

    name_color_a = "inherit"
    name_color_b = "inherit"

    score_color_a = "inherit"
    score_color_b = "inherit"

    return f"""
<div class="es-duel-wrap">
  <div class="{class_a}">
    <div class="es-duel-name">{res_a['prenom']}</div>
    <div class="es-duel-score">{res_a['score']:.1f}&thinsp;<span style="font-size:1rem;font-weight:400;opacity:.7">% TB</span></div>
    <div class="es-duel-bar"><div style="height:100%;background:{fill_a};width:{bar_a:.1f}%"></div></div>
    <div class="es-duel-caption">{res_a['verdict']}</div>
  </div>

  <div class="es-vs">VS</div>

  <div class="{class_b}">
    <div class="es-duel-name">{res_b['prenom']}</div>
    <div class="es-duel-score">{res_b['score']:.1f}&thinsp;<span style="font-size:1rem;font-weight:400;opacity:.7">% TB</span></div>
    <div class="es-duel-bar"><div style="height:100%;background:{fill_b};width:{bar_b:.1f}%"></div></div>
    <div class="es-duel-caption">{res_b['verdict']}</div>
  </div>
</div>
"""


# ── Génération / Décennie ─────────────────────────────────────────────────────

def gen_card_html(vibe: str, label: str, peak_year: int) -> str:
    """Carte génération sur fond Royal Blue."""
    return f"""
<div class="es-gen-card">
  <span class="es-gen-vibe">{vibe}</span>
  <div class="es-gen-label">{label}</div>
  <p class="es-gen-peak">Pic de popularité : {peak_year}</p>
</div>
"""


def gen_rank_html(rank_str: str, total: int, prenom: str) -> str:
    """Bloc de rang dans la décennie."""
    return f"""
<div class="es-rank-card">
  <span class="es-stat-label">Rang dans sa génération</span>
  <div class="es-rank-num">{rank_str}</div>
  <div class="es-rank-caption">parmi {total} prénoms de la même génération</div>
</div>
"""
