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


# ── Section header ─────────────────────────────────────────────────────────────

def section_header_html(
    eyebrow: str,
    title: str,
    subtitle: str = "",
) -> str:
    """En-tête éditoriale avec eyebrow + titre Newsreader + sous-titre italique."""
    sub = f'<p class="es-section-subtitle">{subtitle}</p>' if subtitle else ""
    return f"""
<div style="margin-bottom:2rem">
  <span class="es-eyebrow">{eyebrow}</span>
  <h1 class="es-section-title">{title}</h1>
  {sub}
</div>
"""


# ── Hero de l'app ──────────────────────────────────────────────────────────────

def hero_html() -> str:
    """Hero affiché avant toute saisie dans l'onglet Anthologie."""
    return """
<div style="padding:3rem 0 2.5rem">
  <span class="es-eyebrow">L'Érudit des Prénoms · Édition 2012-2020</span>
  <h1 class="es-title" style="font-size:clamp(3rem,8vw,6rem);margin:0 0 1rem">
    Votre prénom<br>méritait-il<br><em>la mention&nbsp;?</em>
  </h1>
  <p style="font-family:'Inter',sans-serif;font-size:0.95rem;
            color:#444653;max-width:520px;line-height:1.8;margin:0 0 2rem">
    2 millions de résultats nominatifs du baccalauréat général et technologique.
    Entrez un prénom ci-dessous pour connaître son <strong>Score de Prestige Académique</strong>.
  </p>
  <div style="display:flex;gap:2rem;border-top:1px solid rgba(197,197,213,0.3);
              padding-top:1.25rem;margin-top:1rem">
    <div>
      <div style="font-family:'Inter',sans-serif;font-size:0.5rem;font-weight:700;
                  text-transform:uppercase;letter-spacing:.14em;color:#444653;margin-bottom:.25rem">
        Prénoms analysés
      </div>
      <div style="font-family:'Newsreader',serif;font-size:1.75rem;font-weight:900;
                  color:#001360;letter-spacing:-.03em">
        417
      </div>
    </div>
    <div>
      <div style="font-family:'Inter',sans-serif;font-size:0.5rem;font-weight:700;
                  text-transform:uppercase;letter-spacing:.14em;color:#444653;margin-bottom:.25rem">
        Bacheliers recensés
      </div>
      <div style="font-family:'Newsreader',serif;font-size:1.75rem;font-weight:900;
                  color:#001360;letter-spacing:-.03em">
        2&nbsp;M+
      </div>
    </div>
    <div>
      <div style="font-family:'Inter',sans-serif;font-size:0.5rem;font-weight:700;
                  text-transform:uppercase;letter-spacing:.14em;color:#444653;margin-bottom:.25rem">
        Années couvertes
      </div>
      <div style="font-family:'Newsreader',serif;font-size:1.75rem;font-weight:900;
                  color:#001360;letter-spacing:-.03em">
        2012–2020
      </div>
    </div>
  </div>
</div>
"""


# ── Carte résultat principal ───────────────────────────────────────────────────

def result_card_html(result: dict) -> str:
    """
    Carte éditoriale complète pour un prénom trouvé.

    result = dict retourné par scoring.lookup()
    """
    prenom   = result["prenom"]
    score    = result["score"]
    rank_pct = result["rank_pct"]
    effectif = result["effectif_total"]
    years    = result["years_present"]
    sexe     = result["sexe_label"]

    pct_label = _percentile_label(rank_pct)

    return f"""
<div class="es-result-card">
  <div class="es-badge">{sexe}</div>
  <div class="es-prenom-name">{prenom}</div>

  <div class="es-score-block">
    <span class="es-score-number">{score:.1f}</span>
    <span class="es-score-denom">%&nbsp;TB</span>
  </div>
  <span class="es-score-label">Score de Prestige Académique · moyenne pondérée Très Bien</span>

  <div class="es-percentile">
    <span class="es-percentile-num">{rank_pct:.0f}<sup style="font-size:.5em">e</sup></span>
    <span class="es-percentile-label">percentile · {pct_label}</span>
  </div>

  <div class="es-stat-row">
    <div class="es-stat">
      <span class="es-stat-label">Bacheliers analysés</span>
      <span class="es-stat-value">{effectif:,}</span>
    </div>
    <div class="es-stat">
      <span class="es-stat-label">Années de données</span>
      <span class="es-stat-value">{years}&thinsp;/&thinsp;9</span>
    </div>
    <div class="es-stat">
      <span class="es-stat-label">Classement</span>
      <span class="es-stat-value">Top&nbsp;{100 - rank_pct:.0f}&nbsp;%</span>
    </div>
  </div>
</div>
"""


def verdict_card_html(result: dict) -> str:
    """Carte verdict sur fond Royal Blue."""
    stars   = _stars(result["score"])
    verdict = result["verdict"]
    prenom  = result["prenom"]

    return f"""
<div class="es-verdict-card">
  <div class="es-verdict-header">
    <h3 class="es-verdict-title">Le Verdict du Jury</h3>
    <span class="es-verdict-star">{stars}</span>
  </div>
  <p class="es-verdict-text">{verdict}</p>
  <div class="es-verdict-sig">— L'Érudit des Prénoms, à propos de <em>{prenom}</em></div>
</div>
"""


# ── Carte prénom absent ────────────────────────────────────────────────────────

def absent_card_html(prenom: str, message: str, suggestions: list[str]) -> str:
    """Carte gold-bordered pour un prénom absent du dataset."""
    pills = "".join(
        f'<span class="es-absent-pill">{s}</span>' for s in suggestions
    )
    sug_block = (
        f'<div style="margin-top:.75rem">'
        f'<p class="es-absent-suggestions">Prénoms voisins disponibles</p>'
        f'<div style="margin-top:.35rem">{pills}</div>'
        f'</div>'
        if suggestions else ""
    )
    return f"""
<div class="es-absent-card">
  <p class="es-absent-text">{message}</p>
  {sug_block}
</div>
"""


# ── VS Duel ───────────────────────────────────────────────────────────────────

def duel_header_html() -> str:
    """Badge VS centré entre deux colonnes."""
    return """
<div style="display:flex;align-items:center;justify-content:center;
            padding:1.5rem 0;gap:0">
  <div class="es-vs-badge"><span>VS</span></div>
</div>
"""


def duel_card_html(result: dict, side: str = "a") -> str:
    """
    Carte pour un côté du duel (side='a' ou 'b').
    Couleur de fond différente selon le côté.
    """
    prenom  = result["prenom"]
    score   = result["score"]
    verdict = result["verdict"]
    sexe    = result["sexe_label"]
    rank    = result["rank_pct"]

    css_class = "es-duel-card-a" if side == "a" else "es-duel-card-b"
    bar_class = "es-bar-fill-a" if side == "a" else "es-bar-fill-b"
    bar_width = min(100, score / 30 * 100)

    return f"""
<div class="{css_class}" style="height:100%">
  <div class="es-badge" style="margin-bottom:1rem">{sexe}</div>
  <div class="es-duel-name">{prenom}</div>
  <div class="es-duel-score">{score:.1f}&thinsp;%&nbsp;<span style="font-size:1rem;font-weight:400;color:#444653">TB</span></div>
  <div class="es-bar-container">
    <div class="{bar_class}" style="width:{bar_width:.1f}%"></div>
  </div>
  <div style="font-family:'Inter',sans-serif;font-size:0.55rem;font-weight:700;
              text-transform:uppercase;letter-spacing:.12em;color:rgba(68,70,83,.6)">
    {rank:.0f}e&nbsp;percentile
  </div>
  <div class="es-verdict-caption">{verdict}</div>
</div>
"""


def duel_result_html(res_a: dict, res_b: dict) -> str:
    """Bannière victoire / match nul."""
    diff = res_a["score"] - res_b["score"]
    if abs(diff) < 0.5:
        return """
<div style="background:#efeeea;padding:1.25rem 2rem;
            display:flex;align-items:center;gap:1rem;margin-bottom:1rem">
  <span style="font-family:'Newsreader',serif;font-size:1.25rem;font-style:italic;color:#001360">
    Match nul — Vos prénoms sont statistiquement à égalité. Décidez à la courte paille.
  </span>
</div>
"""
    winner = res_a if diff > 0 else res_b
    loser  = res_b if diff > 0 else res_a
    gap    = abs(diff)
    return f"""
<div style="background:#001360;padding:1.25rem 2rem;
            display:flex;align-items:baseline;gap:1rem;margin-bottom:1rem">
  <span style="font-family:'Newsreader',serif;font-size:1.5rem;font-weight:900;
               font-style:italic;color:#fed488">
    {winner['prenom']}
  </span>
  <span style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:700;
               text-transform:uppercase;letter-spacing:.12em;color:rgba(186,195,255,.8)">
    domine par {gap:.1f}&thinsp;pt{'s' if gap >= 2 else ''} — {loser['prenom']} s'incline
  </span>
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
<div style="background:#f4f4f0;padding:1.5rem 2rem">
  <span style="font-family:'Inter',sans-serif;font-size:0.5rem;font-weight:700;
               text-transform:uppercase;letter-spacing:.14em;color:#444653;display:block;margin-bottom:.5rem">
    Rang dans sa génération
  </span>
  <div style="font-family:'Newsreader',serif;font-size:2rem;font-weight:900;
              color:#001360;letter-spacing:-.03em;line-height:1">
    {rank_str}
  </div>
  <div style="font-family:'Inter',sans-serif;font-size:0.7rem;color:#444653;margin-top:.4rem">
    parmi {total} prénoms de la même génération
  </div>
</div>
"""
