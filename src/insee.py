"""
Chargement des données INSEE Fichier des prénoms (1900-2024).

National     : sexe;prenom;periode;valeur
Départemental: sexe;prenom;periode;dpt;valeur

Les fichiers sont téléchargés une seule fois puis mis en cache en parquet.
"""

import io
import unicodedata
import zipfile
from pathlib import Path

import pandas as pd
import requests

NAT_URL = "https://www.insee.fr/fr/statistiques/fichier/8595130/prenoms-2024-nat_csv.zip"
DPT_URL = "https://www.insee.fr/fr/statistiques/fichier/8595130/prenoms-2024-dpt_csv.zip"

NAT_CACHE = Path("data/raw/insee_nat.parquet")
DPT_CACHE = Path("data/raw/insee_dpt.parquet")

HEADERS = {"User-Agent": "Mozilla/5.0 (data-bac project)"}


def normalize(text: str) -> str:
    """Supprime accents et met en minuscules pour jointures souples."""
    return unicodedata.normalize("NFD", str(text)).encode("ascii", "ignore").decode().lower()


def _load_zip_csv(url: str, cache: Path) -> pd.DataFrame:
    if cache.exists():
        return pd.read_parquet(cache)

    cache.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, timeout=120, headers=HEADERS)
    r.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        csv_name = next(n for n in z.namelist() if n.endswith(".csv"))
        with z.open(csv_name) as f:
            df = pd.read_csv(f, sep=";", encoding="utf-8", dtype=str, low_memory=False)

    df.columns = df.columns.str.strip().str.lower()
    df["valeur"]  = pd.to_numeric(df["valeur"],  errors="coerce")
    df["periode"] = pd.to_numeric(df["periode"], errors="coerce")
    df = df[df["valeur"].notna() & df["periode"].notna()].copy()
    df["periode"] = df["periode"].astype(int)
    df["valeur"]  = df["valeur"].astype(float)

    # Prénoms normalisés pour jointures
    df["prenom_norm"] = df["prenom"].apply(normalize)

    # Filtre : France métropolitaine uniquement (codes dpt 01-95 + 2A + 2B)
    if "dpt" in df.columns:
        metro = set([f"{i:02d}" for i in range(1, 96)] + ["2A", "2B", "20"])
        df = df[df["dpt"].isin(metro)].copy()

    df.to_parquet(cache, index=False)
    return df


def load_nat() -> pd.DataFrame:
    """Fichier national : une ligne par (sexe, prenom, annee)."""
    return _load_zip_csv(NAT_URL, NAT_CACHE)


def load_dpt() -> pd.DataFrame:
    """Fichier départemental : une ligne par (sexe, prenom, annee, dpt)."""
    return _load_zip_csv(DPT_URL, DPT_CACHE)
