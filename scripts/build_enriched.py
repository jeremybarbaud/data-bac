"""
Script one-off : construit le cache des prénoms enrichis via scraping
du backend coulmont.com/bac/results.php.

Usage :
    python -m scripts.build_enriched              # tourne jusqu'au bout
    python -m scripts.build_enriched --limit 50   # test rapide
    python -m scripts.build_enriched --sleep 0.5  # plus agressif
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from src.coulmont_scrape import build_enriched, ENRICHED_CACHE  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/raw/candidates_to_scrape.csv",
                    help="CSV avec colonne 'search_name'")
    ap.add_argument("--limit", type=int, default=None,
                    help="Limite le nombre de prénoms (debug)")
    ap.add_argument("--sleep", type=float, default=1.0,
                    help="Délai entre requêtes (secondes)")
    args = ap.parse_args()

    candidates = pd.read_csv(args.input)
    names = candidates["search_name"].tolist()
    if args.limit:
        names = names[:args.limit]

    print(f"[build] {len(names)} prénoms à traiter (cache : {ENRICHED_CACHE})")
    df = build_enriched(names, sleep=args.sleep)
    print(f"[build] Terminé — {len(df)} prénoms enrichis dans le cache.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
