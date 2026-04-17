"""
Scraping de coulmont.com/bac/results.php pour enrichir le dataset.

Le TSV public (data-2020.tsv) ne contient que ~417 prénoms (seuil N ≥ 200/an).
Le backend PHP expose un jeu bien plus large (seuil ~N ≥ 40 cumulés 2012-2020).

Le scraper récupère par prénom :
  prenom | total | pct_oral | pct_passable | pct_ab | pct_bien | pct_tb

⚠ Les valeurs sont CUMULÉES sur 2012-2020 (pas de détail par année).
"""

from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Optional

import pandas as pd
import requests

_HERE = Path(__file__).resolve().parent.parent
ENRICHED_CACHE = _HERE / "data" / "raw" / "coulmont_enriched.parquet"

BASE_URL = "https://coulmont.com/bac/results.php"
HEADERS = {"User-Agent": "Mozilla/5.0 (data-bac project · enrichment)"}

# Extrait "670 Renaud ont eu 8 ou plus" — capture le total
_RE_TOTAL = re.compile(
    r"<strong>\s*(\d+)\s+[^<]*?ont eu 8 ou plus",
    re.IGNORECASE | re.DOTALL,
)

# Extrait les lignes data.addRows([['Oral', 17, ...], ['Passable', 29, ...], ...])
_RE_ROW = re.compile(
    r"\[\s*'(Oral|Passable|AB|Bien|TB)'\s*,\s*([\d.]+)",
    re.IGNORECASE,
)

_CATEGORIES = ("Oral", "Passable", "AB", "Bien", "TB")


def scrape_prenom(prenom: str, session: Optional[requests.Session] = None,
                  timeout: int = 15) -> Optional[dict]:
    """Fetch + parse une fiche prénom. Retourne None si le prénom est absent
    ou si le parsing échoue.

    Returns:
        dict(prenom, total, pct_oral, pct_passable, pct_ab, pct_bien, pct_tb)
        ou None.
    """
    http = session or requests
    try:
        r = http.get(BASE_URL, params={"search": prenom},
                     headers=HEADERS, timeout=timeout)
        r.raise_for_status()
    except requests.RequestException:
        return None

    html = r.text

    m_total = _RE_TOTAL.search(html)
    if not m_total:
        return None
    total = int(m_total.group(1))
    if total < 40:  # seuil Coulmont
        return None

    rows = dict(_RE_ROW.findall(html))
    # Normalise en minuscules pour tolérer les variantes de casse
    rows_norm = {k.lower(): float(v) for k, v in rows.items()}
    if len(rows_norm) < 5:
        return None

    return {
        "prenom": prenom,
        "total": total,
        "pct_oral":     rows_norm.get("oral"),
        "pct_passable": rows_norm.get("passable"),
        "pct_ab":       rows_norm.get("ab"),
        "pct_bien":     rows_norm.get("bien"),
        "pct_tb":       rows_norm.get("tb"),
    }


def build_enriched(prenom_list: list[str],
                   sleep: float = 1.0,
                   progress_every: int = 25,
                   existing_cache: Path = ENRICHED_CACHE) -> pd.DataFrame:
    """Itère sur ``prenom_list`` et scrape chaque prénom.

    - Reprend à partir du cache s'il existe (idempotent).
    - Respecte un délai ``sleep`` entre requêtes (défaut 1 s).
    - Écrit le cache tous les 25 prénoms.
    """
    existing = (
        pd.read_parquet(existing_cache)
        if existing_cache.exists() else pd.DataFrame()
    )
    done = set(existing["prenom"].str.lower()) if not existing.empty else set()

    todo = [p for p in prenom_list if p.lower() not in done]
    print(f"[scrape] {len(done)} déjà en cache, {len(todo)} à scraper.")

    rows: list[dict] = existing.to_dict(orient="records") if not existing.empty else []
    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        for i, prenom in enumerate(todo, 1):
            res = scrape_prenom(prenom, session=session)
            if res is not None:
                rows.append(res)
            if i % progress_every == 0:
                pd.DataFrame(rows).to_parquet(existing_cache, index=False)
                print(f"[scrape] {i}/{len(todo)} — cache sauvé ({len(rows)} hits)")
            time.sleep(sleep)
    finally:
        df = pd.DataFrame(rows)
        existing_cache.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(existing_cache, index=False)

    return df


def load_enriched() -> pd.DataFrame:
    """Charge le cache enrichi ou retourne un DataFrame vide si absent."""
    if ENRICHED_CACHE.exists():
        return pd.read_parquet(ENRICHED_CACHE)
    return pd.DataFrame(columns=[
        "prenom", "total", "pct_oral", "pct_passable",
        "pct_ab", "pct_bien", "pct_tb",
    ])
