"""Matching d'archétypes théoriques (Mintzberg et autres).

Calcule la distance euclidienne pondérée entre la signature observée du graphe
et celle de chaque archétype défini dans la bibliothèque de blocs.
"""

import math
from app.schemas.block import Block
from app.schemas.diagnosis import ArchetypeMatch


# Pondérations des dimensions de la signature structurelle
# Modifiables pour ajuster l'importance relative de chaque dimension
DIMENSION_WEIGHTS: dict[str, float] = {
    "depth": 1.0,
    "span": 1.0,
    "density": 2.0,
    "modularity": 2.0,
    "supervisor_ratio": 1.5,
}


def euclidean_distance(
    observed: dict[str, float],
    target: dict[str, float],
    weights: dict[str, float] | None = None,
) -> tuple[float, dict[str, float]]:
    """Calcule la distance euclidienne pondérée entre deux signatures.

    Retourne (distance, écarts par dimension).
    """
    w = weights or DIMENSION_WEIGHTS
    dims = set(observed.keys()) | set(target.keys())
    gaps: dict[str, float] = {}
    total = 0.0
    for d in dims:
        diff = observed.get(d, 0.0) - target.get(d, 0.0)
        gaps[d] = round(diff, 4)
        total += w.get(d, 1.0) * (diff ** 2)
    return math.sqrt(total), gaps


def match_archetypes(
    observed_signature: dict[str, float],
    archetypes: list[Block],
) -> list[ArchetypeMatch]:
    """Compare la signature observée à chaque archétype.

    Retourne la liste triée par similarité décroissante.
    """
    matches: list[ArchetypeMatch] = []
    for arch in archetypes:
        distance, gaps = euclidean_distance(observed_signature, arch.signature)
        similarity = 1.0 / (1.0 + distance)
        matches.append(
            ArchetypeMatch(
                archetype_name=arch.name,
                school=arch.school,
                distance=round(distance, 4),
                similarity=round(similarity, 4),
                dimensional_gaps=gaps,
            )
        )
    return sorted(matches, key=lambda m: -m.similarity)


def best_match(
    observed_signature: dict[str, float],
    archetypes: list[Block],
) -> ArchetypeMatch | None:
    """Retourne le meilleur archétype matché, ou None si la liste est vide."""
    matches = match_archetypes(observed_signature, archetypes)
    return matches[0] if matches else None
