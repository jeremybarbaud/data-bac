"""
Fusion du dataset TSV Coulmont avec le cache de scraping.

Le TSV (`load_long`) couvre ~417 prénoms avec détail par année.
Le cache enrichi (`load_enriched`) ajoute ~N prénoms supplémentaires,
mais seulement en cumulé 2012-2020 (pas de détail par année).

Cette fusion produit un `scores` unifié où chaque ligne porte un champ
``source`` ∈ {"tsv", "scrape"} et ``history_available`` (bool).
"""

from __future__ import annotations

import pandas as pd

from src.coulmont_scrape import load_enriched
from src.insee import load_nat
from src.normalize import normalize

# Mapping sexe INSEE : 1=M, 2=F
_SEXE_INSEE = {1: "♂", 2: "♀"}


def _dominant_sexe_from_insee(nat_df: pd.DataFrame) -> dict[str, str]:
    """Pour chaque prénom normalisé, retourne le label de sexe majoritaire."""
    if nat_df is None or nat_df.empty:
        return {}
    # sexe INSEE = 1 (M) ou 2 (F)
    agg = (
        nat_df.groupby(["prenom_norm", "sexe"])["valeur"].sum()
        .reset_index()
    )
    # Pour chaque prénom, garde le sexe max
    idx = agg.groupby("prenom_norm")["valeur"].idxmax()
    best = agg.loc[idx, ["prenom_norm", "sexe"]]
    best["sexe_num"] = pd.to_numeric(best["sexe"], errors="coerce")
    return {
        row["prenom_norm"]: _SEXE_INSEE.get(int(row["sexe_num"]), "?")
        for _, row in best.iterrows()
        if pd.notna(row["sexe_num"])
    }


def build_enriched_scores(
    tsv_scores: pd.DataFrame,
    nat_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Produit un ``scores`` unifié à partir :
      - du ``tsv_scores`` déjà calculé par ``compute_scores(long)``
      - du cache de scraping Coulmont

    Schema de sortie (colonnes ajoutées) :
      source : "tsv" | "scrape"
      history_available : bool
      sexe_label : label genre (inféré INSEE pour les scrapes)
      pct_oral, pct_passable, pct_ab, pct_bien, pct_tb : facultatifs (scrape only)

    Les colonnes ``score``, ``effectif_total``, ``years_present`` sont
    harmonisées entre les deux sources.
    """
    # 1) Marque le TSV
    tsv = tsv_scores.copy()
    tsv["source"] = "tsv"
    tsv["history_available"] = True

    # 2) Charge le cache enrichi
    enriched = load_enriched()
    if enriched.empty:
        # Pas de scrape : on ré-ordonne le ranking et on sort.
        tsv["rank_pct"] = tsv["score"].rank(pct=True) * 100
        return tsv.sort_values("score", ascending=False).reset_index(drop=True)

    # 3) Transforme le scrape au même schéma que le TSV
    scrape = pd.DataFrame({
        "prenom":          enriched["prenom"],
        "score":           enriched["pct_tb"].astype(float),
        "effectif_total":  enriched["total"].astype(int),
        "years_present":   9,  # cumul 2012-2020
        "pct_oral":        enriched["pct_oral"],
        "pct_passable":    enriched["pct_passable"],
        "pct_ab":          enriched["pct_ab"],
        "pct_bien":        enriched["pct_bien"],
        "pct_tb":          enriched["pct_tb"],
    })
    scrape["source"] = "scrape"
    scrape["history_available"] = False
    scrape["prenom_lower"] = scrape["prenom"].str.lower()
    scrape["prenom_norm"]  = scrape["prenom"].map(normalize)

    # 4) Genre depuis INSEE (si dispo)
    sexe_map = _dominant_sexe_from_insee(nat_df) if nat_df is not None else {}
    scrape["sexe_label"] = scrape["prenom_norm"].map(sexe_map).fillna("?")

    # 5) Dedup : si un prénom est présent dans TSV ET scrape, on garde le TSV.
    tsv_norms = set(tsv["prenom_norm"])
    scrape = scrape[~scrape["prenom_norm"].isin(tsv_norms)].copy()

    # 6) Concaténation + rank_pct recalculé sur l'union
    combined = pd.concat([tsv, scrape], ignore_index=True, sort=False)
    combined["rank_pct"] = combined["score"].rank(pct=True) * 100
    combined = combined.sort_values("score", ascending=False).reset_index(drop=True)

    return combined
