"""Unification de données multi-sources pour entraînement d'un modèle humanitaire.

Objectif:
- agréger plusieurs fichiers CSV de sources hétérogènes
- harmoniser les noms de colonnes vers un schéma commun
- produire un dataset d'entraînement consolidé par (zone, date)
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Iterable

COMMON_NUMERIC_FIELDS = [
    "affected_population",
    "health_severity",
    "access_difficulty",
    "vulnerability",
    "local_stock",
    "rainfall_mm",
    "food_insecurity_index",
]


@dataclass
class SourceConfig:
    name: str
    path: Path
    column_mapping: dict[str, str]


def _to_float(value: str | float | int | None) -> float | None:
    if value in (None, "", "NA", "N/A", "null"):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def load_and_map_source(config: SourceConfig) -> list[dict[str, object]]:
    """Lit une source CSV et mappe ses colonnes vers le schéma commun."""
    rows: list[dict[str, object]] = []
    with config.path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            mapped: dict[str, object] = {"source": config.name}
            for src_col, common_col in config.column_mapping.items():
                mapped[common_col] = raw.get(src_col)

            mapped["zone"] = str(mapped.get("zone", "")).strip()
            mapped["date"] = str(mapped.get("date", "")).strip()

            for field in COMMON_NUMERIC_FIELDS + ["target_priority"]:
                if field in mapped:
                    mapped[field] = _to_float(mapped[field])
            rows.append(mapped)
    return rows


def consolidate_records(records: Iterable[dict[str, object]]) -> list[dict[str, float | str]]:
    """Consolide les lignes multi-sources par (zone, date) en moyennant les champs numériques."""
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in records:
        zone = str(row.get("zone", "")).strip()
        date = str(row.get("date", "")).strip()
        if not zone or not date:
            continue
        grouped[(zone, date)].append(row)

    consolidated: list[dict[str, float | str]] = []
    for (zone, date), rows in grouped.items():
        item: dict[str, float | str] = {
            "zone": zone,
            "date": date,
            "sources_count": float(len(rows)),
        }
        for field in COMMON_NUMERIC_FIELDS + ["target_priority"]:
            values = [r[field] for r in rows if isinstance(r.get(field), (int, float))]
            if values:
                item[field] = float(mean(values))
        consolidated.append(item)

    consolidated.sort(key=lambda x: (str(x["date"]), str(x["zone"])))
    return consolidated


def write_consolidated_csv(rows: list[dict[str, float | str]], output_path: Path) -> None:
    fields = [
        "zone",
        "date",
        "sources_count",
        *COMMON_NUMERIC_FIELDS,
        "target_priority",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})
