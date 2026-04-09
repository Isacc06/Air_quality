"""Entraîne un modèle simple sur un dataset humanitaire consolidé.

Le modèle est une régression linéaire entraînée par descente de gradient,
sans dépendances externes, pour rester portable dans des environnements terrain.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

FEATURES = [
    "affected_population",
    "health_severity",
    "access_difficulty",
    "vulnerability",
    "local_stock",
    "rainfall_mm",
    "food_insecurity_index",
    "sources_count",
]


def load_training_data(path: Path) -> tuple[list[list[float]], list[float]]:
    X: list[list[float]] = []
    y: list[float] = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            target = row.get("target_priority")
            if target in (None, ""):
                continue

            features_row: list[float] = []
            missing = False
            for feature in FEATURES:
                val = row.get(feature)
                if val in (None, ""):
                    missing = True
                    break
                features_row.append(float(val))
            if missing:
                continue

            X.append(features_row)
            y.append(float(target))
    return X, y


def standardize(X: list[list[float]]) -> tuple[list[list[float]], list[float], list[float]]:
    cols = len(X[0])
    means = [sum(row[i] for row in X) / len(X) for i in range(cols)]
    stds = []
    for i in range(cols):
        var = sum((row[i] - means[i]) ** 2 for row in X) / len(X)
        std = var ** 0.5
        stds.append(std if std > 1e-8 else 1.0)

    Xn = [[(row[i] - means[i]) / stds[i] for i in range(cols)] for row in X]
    return Xn, means, stds


def train_linear_regression(
    X: list[list[float]],
    y: list[float],
    learning_rate: float = 0.03,
    epochs: int = 1500,
) -> tuple[float, list[float]]:
    n = len(X)
    m = len(X[0])
    bias = 0.0
    weights = [0.0] * m

    for _ in range(epochs):
        grad_b = 0.0
        grad_w = [0.0] * m
        for i in range(n):
            pred = bias + sum(weights[j] * X[i][j] for j in range(m))
            err = pred - y[i]
            grad_b += err
            for j in range(m):
                grad_w[j] += err * X[i][j]

        bias -= learning_rate * grad_b / n
        for j in range(m):
            weights[j] -= learning_rate * grad_w[j] / n

    return bias, weights


def mse(X: list[list[float]], y: list[float], bias: float, weights: list[float]) -> float:
    errs = []
    for i in range(len(X)):
        pred = bias + sum(weights[j] * X[i][j] for j in range(len(weights)))
        errs.append((pred - y[i]) ** 2)
    return sum(errs) / len(errs)


def save_model(path: Path, bias: float, weights: list[float], means: list[float], stds: list[float]) -> None:
    payload = {
        "model_type": "linear_regression",
        "features": FEATURES,
        "bias": bias,
        "weights": weights,
        "normalization": {"means": means, "stds": stds},
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Entraîner un modèle humanitaire sur dataset consolidé")
    parser.add_argument("--data", type=Path, required=True, help="CSV consolidé avec target_priority")
    parser.add_argument("--out", type=Path, default=Path("humanitarian_ai/model.json"), help="Chemin de sortie modèle")
    args = parser.parse_args()

    X, y = load_training_data(args.data)
    if len(X) < 10:
        raise SystemExit("Dataset insuffisant: il faut au moins 10 lignes complètes avec target_priority")

    Xn, means, stds = standardize(X)
    bias, weights = train_linear_regression(Xn, y)
    error = mse(Xn, y, bias, weights)
    save_model(args.out, bias, weights, means, stds)

    print(f"Modèle entraîné: {args.out}")
    print(f"Nombre d'exemples: {len(X)}")
    print(f"MSE entraînement: {error:.4f}")


if __name__ == "__main__":
    main()
