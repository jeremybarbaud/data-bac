"""
Téléchargement et mise en forme des données Coulmont.

Source : https://coulmont.com/bac/data-2020.tsv
Format brut (wide) : prenom | ecart{Y} | N{Y} | proptb{Y} | sexe{Y}  pour Y in 2012..2020
"""

from pathlib import Path

import pandas as pd
import requests

_HERE = Path(__file__).resolve().parent.parent
DATA_URL = "https://coulmont.com/bac/data-2020.tsv"
RAW_PATH = _HERE / "data" / "raw" / "bac_prenoms.tsv"
YEARS = list(range(2012, 2021))

SEXE_LABELS = {0: "♀", 1: "♂", 2: "♀♂"}


def download_data() -> Path:
    """Télécharge le TSV si absent du cache local."""
    if not RAW_PATH.exists():
        RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
        r = requests.get(
            DATA_URL,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0 (data-bac project)"},
        )
        r.raise_for_status()
        RAW_PATH.write_bytes(r.content)
    return RAW_PATH


def _load_wide() -> pd.DataFrame:
    """Retourne le dataframe au format wide (tel que téléchargé)."""
    return pd.read_csv(download_data(), sep="\t")


def load_long() -> pd.DataFrame:
    """
    Retourne le dataframe au format long (tidy) :
    prenom | year | N | proptb | ecart | sexe

    Seules les lignes avec N >= 40 sont conservées (seuil Coulmont).
    """
    df = _load_wide()

    frames = []
    for year in YEARS:
        mapping = {"prenom": "prenom"}
        for metric in ("N", "proptb", "ecart", "sexe"):
            col = f"{metric}{year}"
            if col in df.columns:
                mapping[col] = metric

        if len(mapping) < 3:   # au minimum prenom + N + proptb
            continue

        sub = df[list(mapping.keys())].rename(columns=mapping).copy()
        sub["year"] = year
        frames.append(sub)

    long = pd.concat(frames, ignore_index=True)

    for col in ("N", "proptb", "ecart", "sexe"):
        if col in long.columns:
            long[col] = pd.to_numeric(long[col], errors="coerce")

    long = long[long["N"].notna() & (long["N"] >= 40)].copy()
    long["N"] = long["N"].astype(int)
    long["sexe_label"] = long["sexe"].map(SEXE_LABELS).fillna("?")

    return long
