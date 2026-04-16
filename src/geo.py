"""
Carte choroplèthe par département.

Calcule l'indice de surreprésentation d'un prénom par département :
  indice = (% prénom dans dpt) / (% prénom en France)
  indice > 1 → sur-représenté, < 1 → sous-représenté
"""

import pandas as pd
import requests

from src.insee import normalize

GEOJSON_URL = (
    "https://raw.githubusercontent.com/gregoiredavid/france-geojson/"
    "master/departements-version-simplifiee.geojson"
)

# Cache module-level (évite de re-télécharger le GeoJSON à chaque appel)
_geojson_cache: dict | None = None


def load_geojson() -> dict:
    global _geojson_cache
    if _geojson_cache is None:
        r = requests.get(GEOJSON_URL, timeout=30)
        r.raise_for_status()
        _geojson_cache = r.json()
    return _geojson_cache


def get_dept_data(dpt_df: pd.DataFrame, prenom_input: str) -> pd.DataFrame | None:
    """
    Retourne un DataFrame par département avec :
      dpt | count_prenom | total_dpt | pct | indice | label

    Retourne None si le prénom est absent.
    """
    norm = normalize(prenom_input)
    matches = dpt_df[dpt_df["prenom_norm"] == norm].copy()

    if matches.empty:
        return None

    # Total naissances par département (toutes années, tous prénoms)
    total_by_dpt = (
        dpt_df.groupby("dpt")["valeur"]
        .sum()
        .reset_index(name="total_dpt")
    )

    # Naissances du prénom cible par département
    name_by_dpt = (
        matches.groupby("dpt")["valeur"]
        .sum()
        .reset_index(name="count_prenom")
    )

    merged = total_by_dpt.merge(name_by_dpt, on="dpt", how="left").fillna(0)
    merged["pct"] = merged["count_prenom"] / merged["total_dpt"] * 100

    nat_pct = merged["count_prenom"].sum() / merged["total_dpt"].sum() * 100
    if nat_pct == 0:
        return None

    merged["indice"] = (merged["pct"] / nat_pct).round(2)

    # Normalise le code département : "1" → "01", "2A" reste "2A"
    merged["dpt"] = merged["dpt"].astype(str).str.zfill(2)

    # Label lisible pour le hover
    merged["label"] = (
        "Dept " + merged["dpt"] + " : "
        + merged["count_prenom"].astype(int).astype(str)
        + " naissances — indice "
        + merged["indice"].astype(str)
    )

    return merged[["dpt", "count_prenom", "pct", "indice", "label"]]
