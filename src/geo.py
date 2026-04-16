"""
Carte choroplèthe par département.

Calcule l'indice de surreprésentation d'un prénom par département :
  indice = (% prénom dans dpt) / (% prénom en France)
  indice > 1 → sur-représenté, < 1 → sous-représenté
"""

import pandas as pd

from src.normalize import normalize

GEOJSON_URL = (
    "https://raw.githubusercontent.com/gregoiredavid/france-geojson/"
    "master/departements-version-simplifiee.geojson"
)


def get_dept_data(
    dpt_df: pd.DataFrame,
    prenom_input: str,
    total_by_dpt: pd.DataFrame,
) -> pd.DataFrame | None:
    """
    Retourne un DataFrame par département avec :
      dpt | count_prenom | pct | indice

    ``total_by_dpt`` est le total de naissances par département
    pré-calculé une seule fois (évite de re-agréger 3.6M lignes).

    Retourne None si le prénom est absent.
    """
    norm = normalize(prenom_input)
    matches = dpt_df[dpt_df["prenom_norm"] == norm]

    if matches.empty:
        return None

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

    return merged[["dpt", "count_prenom", "pct", "indice"]]
