"""
Classement des décennies.

Pour chaque prénom présent dans le dataset Coulmont (bac), on détermine
sa décennie de pic de popularité (INSEE naissances), puis on croise
avec le score de prestige académique.
"""

import pandas as pd

from src.normalize import normalize

DECADE_LABELS = {
    1950: "Années 50",
    1960: "Années 60",
    1970: "Années 70",
    1980: "Années 80",
    1990: "Années 90",
    2000: "Années 2000",
    2010: "Années 2010",
}

DECADE_VIBES = {
    1950: "📻",
    1960: "✌️",
    1970: "🕺",
    1980: "📼",
    1990: "📟",
    2000: "💿",
    2010: "📱",
}


def build_peak_years(nat_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule, pour chaque prénom normalisé, l'année de pic de naissances.
    Retourne : prenom_norm | peak_year | decade

    Implémentation vectorisée : trie par valeur décroissante puis garde la
    première occurrence par prénom. ~20× plus rapide qu'un groupby.apply
    sur les ~4M lignes INSEE nationales.
    """
    # On agrège d'abord par (prenom_norm, periode) pour sommer les deux sexes.
    agg = (
        nat_df.groupby(["prenom_norm", "periode"], sort=False, as_index=False)["valeur"]
        .sum()
    )
    peak = (
        agg.sort_values("valeur", ascending=False, kind="stable")
           .drop_duplicates("prenom_norm", keep="first")
           .rename(columns={"periode": "peak_year"})
           .loc[:, ["prenom_norm", "peak_year"]]
           .reset_index(drop=True)
    )
    peak["peak_year"] = peak["peak_year"].astype(int)
    peak["decade"] = (peak["peak_year"] // 10) * 10
    return peak


def build_decade_scores(scores: pd.DataFrame, peak_df: pd.DataFrame) -> pd.DataFrame:
    """
    Fusionne les scores Coulmont avec les décennies INSEE.
    Retourne un DataFrame enrichi avec decade et decade_label.
    """
    scores_copy = scores.copy()
    scores_copy["prenom_norm"] = scores_copy["prenom"].apply(normalize)

    merged = scores_copy.merge(peak_df, on="prenom_norm", how="left")
    merged = merged[merged["decade"].notna()].copy()
    merged["decade"] = merged["decade"].astype(int)

    # Filtre : décennies exploitables (assez de prénoms)
    merged = merged[merged["decade"].between(1950, 2010)]
    merged["decade_label"] = merged["decade"].map(DECADE_LABELS)
    merged["decade_vibe"]  = merged["decade"].map(DECADE_VIBES)

    return merged.sort_values("score", ascending=False)


def decade_summary(decade_scores: pd.DataFrame) -> pd.DataFrame:
    """
    Agrégat par décennie : score moyen, top prénom, bottom prénom.
    """
    def _agg(g: pd.DataFrame) -> pd.Series:
        top    = g.nlargest(1, "score").iloc[0]
        bottom = g.nsmallest(1, "score").iloc[0]
        return pd.Series({
            "score_moyen":  round(g["score"].mean(), 2),
            "nb_prenoms":   len(g),
            "top_prenom":   top["prenom"],
            "top_score":    round(top["score"], 1),
            "bottom_prenom": bottom["prenom"],
            "bottom_score": round(bottom["score"], 1),
        })

    summary = (
        decade_scores.groupby(["decade", "decade_label", "decade_vibe"], sort=True)
        .apply(_agg, include_groups=False)
        .reset_index()
        .sort_values("decade")
    )
    return summary
