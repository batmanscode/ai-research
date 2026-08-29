#!/usr/bin/env python3
"""Reconstruct the corrected FLIP2 Hydro cross-backbone experiment.

The script downloads the three public Hydro wild-type split files when they
are absent, selects the representation and ridge penalty using training-side
validation only, evaluates each held backbone once, and writes exact results.
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

RECORD = "https://zenodo.org/api/records/18433203/files/hydro"
SPLITS = {
    "P06241": f"{RECORD}/to_P06241.csv.gz/content",
    "P0A9X9": f"{RECORD}/to_P0A9X9.csv.gz/content",
    "P01053": f"{RECORD}/to_P01053.csv.gz/content",
}
NAMES = {"P06241": "FYN-SH3", "P0A9X9": "CspA", "P01053": "CI-2A"}
LENGTH_TO_ACCESSION = {57: "P06241", 65: "P0A9X9", 63: "P01053"}
CORE_POSITIONS = {
    57: [3, 17, 19, 25, 27, 49, 54],
    63: [12, 19, 28, 46, 48, 50, 56],
    65: [5, 17, 26, 28, 47, 49, 63],
}
NATIVE_CORES = {57: "FLFFIIV", 63: "VIIVLVI", 65: "VIVVVFV"}

# Five deliberately small descriptors for the only residues present in Hydro.
# Columns: Kyte-Doolittle hydropathy, residue volume, residue mass, Grantham
# polarity, aromatic indicator.
PROPERTIES = {
    "F": [2.8, 189.9, 165.19, 5.2, 1.0],
    "I": [4.5, 166.7, 131.17, 5.2, 0.0],
    "L": [3.8, 166.7, 131.17, 4.9, 0.0],
    "M": [1.9, 162.9, 149.21, 5.7, 0.0],
    "V": [4.2, 140.0, 117.15, 5.9, 0.0],
}
ALPHAS = [0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0]
FEATURE_SETS = ["signed_absdiff", "count_signed_absdiff", "all_aggregate"]
OFFICIAL_BEST = {
    "P06241": {"rho": 0.444, "model": "SaProt-650M likelihood"},
    "P0A9X9": {"rho": 0.151, "model": "Dayhoff likelihood"},
    "P01053": {"rho": 0.394, "model": "ESMC-300M LoRA"},
}


def download_data(data_dir: Path) -> dict[str, Path]:
    data_dir.mkdir(parents=True, exist_ok=True)
    paths = {}
    for accession, url in SPLITS.items():
        path = data_dir / f"to_{accession}.csv.gz"
        if not path.exists():
            request = urllib.request.Request(url, headers={"User-Agent": "ai-research/1.0"})
            with urllib.request.urlopen(request) as response, path.open("wb") as destination:
                destination.write(response.read())
        paths[accession] = path
    return paths


def core(sequence: str) -> str:
    positions = CORE_POSITIONS[len(sequence)]
    return "".join(sequence[position - 1] for position in positions)


def raw_features(sequence: str) -> tuple[int, np.ndarray, np.ndarray, np.ndarray]:
    observed = core(sequence)
    native = NATIVE_CORES[len(sequence)]
    differences = np.array([
        np.asarray(PROPERTIES[new]) - np.asarray(PROPERTIES[old])
        for new, old in zip(observed, native)
    ])
    count = sum(new != old for new, old in zip(observed, native))
    final_totals = np.array([PROPERTIES[aa] for aa in observed]).sum(axis=0)
    signed_changes = differences.sum(axis=0)
    absolute_changes = np.abs(differences).sum(axis=0)
    return count, final_totals, signed_changes, absolute_changes


def feature_matrix(sequences: pd.Series, feature_set: str) -> np.ndarray:
    rows = []
    for sequence in sequences:
        count, final_totals, signed_changes, absolute_changes = raw_features(sequence)
        if feature_set == "signed_absdiff":
            row = np.r_[signed_changes, absolute_changes]
        elif feature_set == "count_signed_absdiff":
            row = np.r_[count, signed_changes, absolute_changes]
        elif feature_set == "all_aggregate":
            row = np.r_[count, final_totals, signed_changes, absolute_changes]
        else:
            raise ValueError(feature_set)
        rows.append(row)
    return np.vstack(rows)


def safe_spearman(y: np.ndarray, prediction: np.ndarray) -> float:
    return float(spearmanr(y, prediction).statistic)


def within_count_spearman(y: np.ndarray, prediction: np.ndarray, counts: np.ndarray) -> float:
    y_residual = np.asarray(y, dtype=float).copy()
    p_residual = np.asarray(prediction, dtype=float).copy()
    for count in np.unique(counts):
        selected = counts == count
        y_residual[selected] -= y_residual[selected].mean()
        p_residual[selected] -= p_residual[selected].mean()
    return safe_spearman(y_residual, p_residual)


def select_model(training: pd.DataFrame, validation: pd.DataFrame) -> tuple[str, float, list[dict]]:
    trace = []
    best = None
    for feature_set in FEATURE_SETS:
        x_train = feature_matrix(training.sequence, feature_set)
        x_validation = feature_matrix(validation.sequence, feature_set)
        for alpha in ALPHAS:
            model = make_pipeline(StandardScaler(), Ridge(alpha=alpha))
            model.fit(x_train, training.target)
            prediction = model.predict(x_validation)
            scored = validation.assign(prediction=prediction)
            within_scores = []
            full_scores = []
            for _, group in scored.groupby("backbone"):
                within_scores.append(within_count_spearman(
                    group.target.to_numpy(), group.prediction.to_numpy(), group.mutation_count.to_numpy()
                ))
                full_scores.append(safe_spearman(group.target.to_numpy(), group.prediction.to_numpy()))
            record = {
                "feature_set": feature_set,
                "alpha": alpha,
                "validation_macro_within_count_spearman": float(np.mean(within_scores)),
                "validation_macro_full_spearman": float(np.mean(full_scores)),
            }
            trace.append(record)
            key = (
                record["validation_macro_within_count_spearman"],
                record["validation_macro_full_spearman"],
                -alpha,
            )
            if best is None or key > best[0]:
                best = (key, feature_set, alpha)
    assert best is not None
    return best[1], best[2], trace


def stratified_bootstrap_delta(
    y: np.ndarray,
    model_prediction: np.ndarray,
    baseline_prediction: np.ndarray,
    counts: np.ndarray,
    repeats: int,
    rng: np.random.Generator,
) -> list[float]:
    groups = [np.flatnonzero(counts == value) for value in np.unique(counts)]
    deltas = []
    for _ in range(repeats):
        sample = np.concatenate([rng.choice(group, size=len(group), replace=True) for group in groups])
        deltas.append(
            safe_spearman(y[sample], model_prediction[sample])
            - safe_spearman(y[sample], baseline_prediction[sample])
        )
    return deltas


def within_count_permutation_p(
    y: np.ndarray,
    prediction: np.ndarray,
    counts: np.ndarray,
    repeats: int,
    rng: np.random.Generator,
) -> tuple[float, float]:
    observed = within_count_spearman(y, prediction, counts)
    extreme = 0
    for _ in range(repeats):
        permuted = y.copy()
        for value in np.unique(counts):
            selected = np.flatnonzero(counts == value)
            permuted[selected] = rng.permutation(permuted[selected])
        extreme += within_count_spearman(permuted, prediction, counts) >= observed
    return observed, (extreme + 1) / (repeats + 1)


def evaluate(paths: dict[str, Path], bootstrap: int, permutations: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    folds = []
    for held_accession, path in paths.items():
        frame = pd.read_csv(path)
        frame["backbone"] = frame.sequence.str.len().map(LENGTH_TO_ACCESSION)
        frame["mutation_count"] = [raw_features(sequence)[0] for sequence in frame.sequence]
        training = frame[(frame.set == "train") & (~frame.validation)].copy()
        validation = frame[(frame.set == "train") & frame.validation].copy()
        test = frame[frame.set == "test"].copy()

        feature_set, alpha, trace = select_model(training, validation)
        all_training = pd.concat([training, validation], ignore_index=True)
        model = make_pipeline(StandardScaler(), Ridge(alpha=alpha))
        model.fit(feature_matrix(all_training.sequence, feature_set), all_training.target)
        prediction = model.predict(feature_matrix(test.sequence, feature_set))
        y = test.target.to_numpy(dtype=float)
        counts = test.mutation_count.to_numpy(dtype=int)
        baseline = -counts.astype(float)
        model_rho = safe_spearman(y, prediction)
        baseline_rho = safe_spearman(y, baseline)
        deltas = stratified_bootstrap_delta(y, prediction, baseline, counts, bootstrap, rng)
        within_rho, permutation_p = within_count_permutation_p(y, prediction, counts, permutations, rng)
        fold = {
            "accession": held_accession,
            "protein": NAMES[held_accession],
            "n_test": len(test),
            "native_core": NATIVE_CORES[len(test.sequence.iloc[0])],
            "selected_feature_set": feature_set,
            "selected_feature_count": int(feature_matrix(test.sequence.iloc[:1], feature_set).shape[1]),
            "selected_alpha": alpha,
            "baseline_native_count_spearman": baseline_rho,
            "aggregate_model_spearman": model_rho,
            "delta_spearman": model_rho - baseline_rho,
            "delta_spearman_bootstrap_95_ci": [float(np.quantile(deltas, 0.025)), float(np.quantile(deltas, 0.975))],
            "within_native_count_spearman": within_rho,
            "within_count_permutation_p": permutation_p,
            "official_best_spearman": OFFICIAL_BEST[held_accession]["rho"],
            "official_best_model": OFFICIAL_BEST[held_accession]["model"],
            "difference_from_official_best": model_rho - OFFICIAL_BEST[held_accession]["rho"],
            "selection_trace": trace,
        }
        folds.append(fold)
    return {
        "status": "reconstructed exploratory analysis; public test feedback influenced the research path",
        "date": "2026-08-29",
        "dataset": "FLIP2 Hydro held-wild-type splits, Zenodo record 18433203",
        "primary_metric": "Spearman rank correlation",
        "feature_selection": "training-side validation only within each official fold",
        "bootstrap_repeats": bootstrap,
        "permutation_repeats": permutations,
        "seed": seed,
        "folds": folds,
    }


def make_figure(results: dict, output: Path) -> None:
    import matplotlib.pyplot as plt

    folds = results["folds"]
    labels = [f"{item['protein']}\n{item['accession']} · n={item['n_test']:,}" for item in folds]
    baseline = [item["baseline_native_count_spearman"] for item in folds]
    model = [item["aggregate_model_spearman"] for item in folds]
    official = [item["official_best_spearman"] for item in folds]
    x = np.arange(len(folds))
    width = 0.23

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    fig, ax = plt.subplots(figsize=(9.6, 6.15))
    fig.patch.set_facecolor("#f7f3ea")
    ax.set_facecolor("#f7f3ea")
    fig.subplots_adjust(left=0.105, right=0.98, bottom=0.16, top=0.68)
    bars = [
        ax.bar(x - width, baseline, width, label="Native mutation count", color="#8c918c"),
        ax.bar(x, model, width, label="Aggregate chemistry ridge", color="#2455d6"),
        ax.bar(x + width, official, width, label="Best published FLIP2 comparator", color="#d69025"),
    ]
    for group in bars:
        ax.bar_label(group, fmt="%.3f", padding=3, fontsize=9)
    ax.set_xticks(x, labels)
    ax.set_ylim(0, 0.57)
    ax.set_ylabel("Held-backbone Spearman ρ")
    fig.suptitle(
        "A tiny invariant representation transfers across hydrophobic cores",
        x=0.105, y=0.955, ha="left", fontsize=16, weight="bold"
    )
    fig.text(
        0.105, 0.875,
        "EXPLORATORY / POST-HOC  ·  Public test results influenced the research path; prospective validation is required.",
        color="#7d2828", fontsize=9.3, weight="bold", va="center",
        bbox={"boxstyle": "round,pad=0.5", "facecolor": "#f2d9d2", "edgecolor": "#c99183"}
    )
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="y", color="#d9d2c4", linewidth=0.8)
    ax.set_axisbelow(True)
    handles, legend_labels = ax.get_legend_handles_labels()
    fig.legend(
        handles, legend_labels, frameon=False, loc="upper left",
        bbox_to_anchor=(0.095, 0.805), ncol=3, columnspacing=1.7,
        handlelength=1.5, fontsize=9
    )
    fig.text(
        0.105, 0.045,
        "Published comparator changes by fold: SaProt-650M likelihood · Dayhoff likelihood · ESMC-300M LoRA",
        color="#5f625f", fontsize=8.3
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path(".cache/hydro"))
    parser.add_argument("--output", type=Path, default=Path("results/analysis.json"))
    parser.add_argument("--figure", type=Path, default=Path("results/biology_comparison.png"))
    parser.add_argument("--bootstrap", type=int, default=500)
    parser.add_argument("--permutations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260829)
    args = parser.parse_args()
    paths = download_data(args.data_dir)
    results = evaluate(paths, args.bootstrap, args.permutations, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    make_figure(results, args.figure)
    print(json.dumps({
        item["protein"]: {
            "baseline": item["baseline_native_count_spearman"],
            "model": item["aggregate_model_spearman"],
            "within_count": item["within_native_count_spearman"],
            "p": item["within_count_permutation_p"],
        }
        for item in results["folds"]
    }, indent=2))


if __name__ == "__main__":
    main()
