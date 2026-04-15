"""
Calcul du Score de Prestige Académique et génération des verdicts.

Score = moyenne pondérée du % mention TB sur toutes les années disponibles
        pondération = N (effectif) par année
"""

import unicodedata

import pandas as pd


def _normalize(text: str) -> str:
    """Supprime les accents et met en minuscules pour comparaison souple."""
    return unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode().lower()

# Seuils pour le verdict (% TB moyen pondéré)
# Moyenne nationale : ~10-15 % toutes séries confondues (général + techno)
VERDICTS = [
    (22, "Vous étiez manifestement destiné·e à intégrer HEC, Cambridge ou Sciences Po. "
         "Vos parents savaient ce qu'ils faisaient."),
    (17, "Solide. Ce prénom fleure bon les premières rangées en amphi."),
    (13, "Dans la bonne moyenne. Ni flamboyant, ni catastrophique. Respectable."),
    (8,  "Le talent n'a pas besoin de mention. Demandez à Bill Gates."),
    (0,  "Votre prénom a d'autres qualités. On est sûr. Continuez à chercher."),
]


def compute_scores(long: pd.DataFrame) -> pd.DataFrame:
    """
    Retourne un DataFrame avec une ligne par prénom :
    prenom | score | effectif_total | years_present | rank_pct
    """
    def _agg(g: pd.DataFrame) -> pd.Series:
        valid = g[g["proptb"].notna()]
        if valid.empty or valid["N"].sum() == 0:
            return pd.Series({"score": float("nan"), "effectif_total": 0, "years_present": 0})
        score = (valid["proptb"] * valid["N"]).sum() / valid["N"].sum()
        return pd.Series({
            "score": score,
            "effectif_total": int(valid["N"].sum()),
            "years_present": int(valid["year"].nunique()),
        })

    scores = long.groupby("prenom", sort=False).apply(_agg).reset_index()
    scores = scores[scores["score"].notna()].copy()
    scores["rank_pct"] = scores["score"].rank(pct=True) * 100
    scores = scores.sort_values("score", ascending=False).reset_index(drop=True)
    return scores


def get_verdict(score: float) -> str:
    for threshold, text in VERDICTS:
        if score >= threshold:
            return text
    return VERDICTS[-1][1]


def lookup(prenom: str, long: pd.DataFrame, scores: pd.DataFrame) -> dict | None:
    """
    Retourne les infos complètes d'un prénom, ou None si absent du dataset.
    La recherche est insensible à la casse.
    """
    key = prenom.strip()
    key_norm = _normalize(key)
    # Correspondance : exact d'abord, puis sans accents
    match_scores = scores[scores["prenom"].str.lower() == key.lower()]
    if match_scores.empty:
        match_scores = scores[scores["prenom"].apply(_normalize) == key_norm]
    if match_scores.empty:
        return None

    row = match_scores.iloc[0]
    canonical = match_scores.iloc[0]["prenom"]
    hist = long[long["prenom"] == canonical].sort_values("year")

    # Récupère le label de genre dominant
    sexe_label = "?"
    if not hist.empty and "sexe_label" in hist.columns:
        sexe_label = hist["sexe_label"].mode().iloc[0]

    return {
        "prenom": row["prenom"],
        "score": float(row["score"]),
        "rank_pct": float(row["rank_pct"]),
        "effectif_total": int(row["effectif_total"]),
        "years_present": int(row["years_present"]),
        "sexe_label": sexe_label,
        "verdict": get_verdict(float(row["score"])),
        "history": hist[["year", "N", "proptb"]].to_dict(orient="records"),
    }
