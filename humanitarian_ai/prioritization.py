"""Prototype minimal pour prioriser des zones humanitaires.

Objectif:
- calculer un score de priorité explicable
- proposer une allocation initiale de kits
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class Zone:
    name: str
    affected_population: int
    health_severity: float  # 0-1
    access_difficulty: float  # 0-1
    vulnerability: float  # 0-1
    local_stock: int


def priority_score(zone: Zone, weights: dict[str, float]) -> float:
    """Calcule un score de priorité (plus haut = plus urgent)."""
    pop_term = zone.affected_population / 10_000
    stock_penalty = zone.local_stock / 1_000

    score = (
        weights["population"] * pop_term
        + weights["health"] * zone.health_severity
        + weights["access"] * zone.access_difficulty
        + weights["vulnerability"] * zone.vulnerability
        - weights["stock"] * stock_penalty
    )
    return round(score, 3)


def rank_zones(zones: Iterable[Zone], weights: dict[str, float]) -> list[tuple[Zone, float]]:
    ranked = [(z, priority_score(z, weights)) for z in zones]
    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked


def allocate_kits(
    ranked: list[tuple[Zone, float]],
    total_kits: int,
    min_per_zone: int = 10,
) -> dict[str, int]:
    """Allocation heuristique proportionnelle au score, avec minimum par zone."""
    allocations = {zone.name: min_per_zone for zone, _ in ranked}
    remaining = max(total_kits - min_per_zone * len(ranked), 0)

    score_sum = sum(score for _, score in ranked) or 1
    for zone, score in ranked:
        extra = int(remaining * (score / score_sum))
        allocations[zone.name] += extra

    # Ajustement final (arrondis)
    distributed = sum(allocations.values())
    i = 0
    while distributed < total_kits and ranked:
        allocations[ranked[i % len(ranked)][0].name] += 1
        distributed += 1
        i += 1

    return allocations


def demo() -> None:
    zones = [
        Zone("Nord", 22000, 0.8, 0.7, 0.9, 80),
        Zone("Est", 15000, 0.6, 0.5, 0.7, 140),
        Zone("Sud", 32000, 0.7, 0.9, 0.8, 60),
        Zone("Ouest", 12000, 0.4, 0.3, 0.6, 220),
    ]

    weights = {
        "population": 0.35,
        "health": 0.25,
        "access": 0.15,
        "vulnerability": 0.2,
        "stock": 0.1,
    }

    ranked = rank_zones(zones, weights)
    allocations = allocate_kits(ranked, total_kits=1_000, min_per_zone=40)

    print("Priorisation des zones:")
    for zone, score in ranked:
        print(f"- {zone.name}: score={score}")

    print("\nAllocation initiale des kits:")
    for zone_name, kits in allocations.items():
        print(f"- {zone_name}: {kits} kits")


if __name__ == "__main__":
    demo()
