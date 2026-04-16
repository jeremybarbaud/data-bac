"""
Normalisation des prénoms — module unique de référence.

Utilisé par scoring.py, insee.py, decades.py et geo.py
pour garantir une seule implémentation de la logique de normalisation.
"""

import unicodedata


def normalize(text: str) -> str:
    """Supprime les accents et met en minuscules pour comparaison souple."""
    return (
        unicodedata.normalize("NFD", str(text))
        .encode("ascii", "ignore")
        .decode()
        .lower()
    )
