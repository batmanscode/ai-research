#!/usr/bin/env python3
"""Verify a pre-reveal freeze and run every prespecified evaluation."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Iterable

from freeze import sha256_file


def parse_args() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=here / "manifest.lock.json")
    parser.add_argument("--phenotypes", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise ValueError(f"{path.name}: missing header")
        header = [item.strip().lower() for item in reader.fieldnames]
        rows = [{k.strip().lower(): (v or "").strip() for k, v in row.items()} for row in reader]
    return header, rows


def resolve_locked(project: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (project / path).resolve()


def verify_freeze(manifest_path: Path) -> tuple[dict[str, object], Path]:
    here = Path(__file__).resolve().parent
    project = here.parent
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("status") != "FROZEN_NO_PHENOTYPES":
        raise ValueError("manifest does not record a phenotype-free freeze")
    for display, record in manifest["files"].items():
        path = resolve_locked(project, display)
        if not path.is_file():
            raise FileNotFoundError(path)
        if sha256_file(path) != record["sha256"]:
            raise ValueError(f"frozen hash mismatch: {display}")
    return manifest, project


def average_ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    start = 0
    while start < len(order):
        end = start + 1
        while end < len(order) and values[order[end]] == values[order[start]]:
            end += 1
        rank = (start + 1 + end) / 2.0
        for index in order[start:end]:
            ranks[index] = rank
        start = end
    return ranks


def pearson(left: list[float], right: list[float]) -> float:
    if len(left) != len(right) or len(left) < 3:
        raise ValueError("correlation requires at least three paired values")
    left_mean, right_mean = mean(left), mean(right)
    numerator = sum((x - left_mean) * (y - right_mean) for x, y in zip(left, right))
    left_ss = sum((x - left_mean) ** 2 for x in left)
    right_ss = sum((y - right_mean) ** 2 for y in right)
    if left_ss == 0 or right_ss == 0:
        return float("nan")
    return numerator / math.sqrt(left_ss * right_ss)


def spearman(left: list[float], right: list[float]) -> float:
    return pearson(average_ranks(left), average_ranks(right))


def residualized_within_count(
    variants: list[str], predictions: dict[str, float], phenotypes: dict[str, float], strata: dict[str, str]
) -> float:
    grouped: dict[str, list[str]] = defaultdict(list)
    for variant in variants:
        grouped[strata[variant]].append(variant)
    pred_residual, phenotype_residual = [], []
    for members in grouped.values():
        p_mean = mean(predictions[v] for v in members)
        y_mean = mean(phenotypes[v] for v in members)
        for variant in members:
            pred_residual.append(predictions[variant] - p_mean)
            phenotype_residual.append(phenotypes[variant] - y_mean)
    return spearman(pred_residual, phenotype_residual)


def stable_order(variants: Iterable[str], scores: dict[str, float], seed: int) -> list[str]:
    def tie_key(variant: str) -> str:
        return hashlib.sha256(f"{seed}|{variant}".encode()).hexdigest()
    return sorted(variants, key=lambda v: (-scores[v], tie_key(v)))


def precision_at(
    variants: list[str], predictions: dict[str, float], phenotypes: dict[str, float], fraction: float, seed: int
) -> float:
    count = max(1, math.ceil(len(variants) * fraction))
    predicted = set(stable_order(variants, predictions, seed)[:count])
    positive = set(stable_order(variants, phenotypes, seed)[:count])
    return len(predicted & positive) / count


def percentile(values: list[float], probability: float) -> float:
    ordered = sorted(value for value in values if math.isfinite(value))
    if not ordered:
        return float("nan")
    position = (len(ordered) - 1) * probability
    low, high = math.floor(position), math.ceil(position)
    if low == high:
        return ordered[low]
    return ordered[low] * (high - position) + ordered[high] * (position - low)


def aggregate_observations(rows: list[dict[str, object]]) -> dict[str, float]:
    values: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        values[str(row["variant_id"])].append(float(row["phenotype"]))
    return {variant: mean(items) for variant, items in values.items()}


def bootstrap_deltas(
    observations: list[dict[str, object]],
    predictions: dict[str, dict[str, float]],
    strata: dict[str, str],
    replicates: int,
    seed: int,
) -> list[float]:
    rng = random.Random(seed)
    by_library_batch: dict[str, dict[str, list[dict[str, object]]]] = defaultdict(lambda: defaultdict(list))
    for row in observations:
        by_library_batch[str(row["biological_library_id"])][str(row["batch_id"])].append(row)
    libraries = sorted(by_library_batch)
    deltas = []
    for _ in range(replicates):
        sampled_rows: list[dict[str, object]] = []
        for library in rng.choices(libraries, k=len(libraries)):
            batches = sorted(by_library_batch[library])
            for batch in rng.choices(batches, k=len(batches)):
                sampled_rows.extend(by_library_batch[library][batch])
        phenotype = aggregate_observations(sampled_rows)
        available = sorted(set(phenotype) & set(predictions))
        by_stratum: dict[str, list[str]] = defaultdict(list)
        for variant in available:
            by_stratum[strata[variant]].append(variant)
        sampled_variants: list[str] = []
        for members in by_stratum.values():
            sampled_variants.extend(rng.choices(members, k=len(members)))
        if len(sampled_variants) < 3:
            continue
        y = [phenotype[v] for v in sampled_variants]
        aggregate = [predictions[v]["aggregate_chemistry"] for v in sampled_variants]
        baseline = [predictions[v]["native_count"] for v in sampled_variants]
        delta = spearman(aggregate, y) - spearman(baseline, y)
        if math.isfinite(delta):
            deltas.append(delta)
    if len(deltas) < max(20, replicates // 2):
        raise ValueError("too few valid block-bootstrap replicates")
    return deltas


def permutation_p_value(
    observations: list[dict[str, object]],
    aggregate_prediction: dict[str, float],
    strata: dict[str, str],
    observed: float,
    replicates: int,
    seed: int,
) -> float:
    rng = random.Random(seed)
    blocks: dict[tuple[str, str, str], list[int]] = defaultdict(list)
    for index, row in enumerate(observations):
        key = (
            str(row["biological_library_id"]),
            str(row["batch_id"]),
            str(row["mutation_count_stratum"]),
        )
        blocks[key].append(index)
    extreme = 0
    for _ in range(replicates):
        shuffled = [float(row["phenotype"]) for row in observations]
        for indices in blocks.values():
            values = [shuffled[index] for index in indices]
            rng.shuffle(values)
            for index, value in zip(indices, values):
                shuffled[index] = value
        permuted_rows = [dict(row, phenotype=shuffled[index]) for index, row in enumerate(observations)]
        phenotype = aggregate_observations(permuted_rows)
        variants = sorted(phenotype)
        statistic = residualized_within_count(variants, aggregate_prediction, phenotype, strata)
        if math.isfinite(statistic) and statistic >= observed:
            extreme += 1
    return (extreme + 1) / (replicates + 1)


def evaluate(args: argparse.Namespace) -> dict[str, object]:
    manifest_path = args.manifest.resolve()
    manifest, project = verify_freeze(manifest_path)
    roles = manifest["roles"]
    candidate_path = resolve_locked(project, roles["candidate_design"])
    prediction_path = resolve_locked(project, roles["predictions"])
    protocol_path = resolve_locked(project, roles["protocol"])
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))

    _, design_rows = read_tsv(candidate_path)
    _, prediction_rows = read_tsv(prediction_path)
    phenotype_header, phenotype_rows = read_tsv(args.phenotypes.resolve())
    if phenotype_header != ["observation_id", "phenotype"]:
        raise ValueError("phenotypes.tsv must contain exactly observation_id and phenotype")

    design_by_observation = {row["observation_id"]: row for row in design_rows}
    phenotype_by_observation = {row["observation_id"]: row for row in phenotype_rows}
    if len(phenotype_by_observation) != len(phenotype_rows):
        raise ValueError("phenotypes.tsv: duplicate observation_id")
    if set(phenotype_by_observation) != set(design_by_observation):
        raise ValueError("phenotype observation IDs do not exactly match the frozen design")

    observations: list[dict[str, object]] = []
    for observation_id, design in design_by_observation.items():
        value = float(phenotype_by_observation[observation_id]["phenotype"])
        if not math.isfinite(value):
            raise ValueError(f"non-finite phenotype: {observation_id}")
        observations.append(dict(design, phenotype=value))

    required_models = protocol["required_prediction_columns"]
    predictions: dict[str, dict[str, float]] = {}
    for row in prediction_rows:
        model_scores = {model: float(row[model]) for model in required_models}
        if not all(math.isfinite(value) for value in model_scores.values()):
            raise ValueError(f"non-finite prediction: {row['variant_id']}")
        predictions[row["variant_id"]] = model_scores

    phenotype = aggregate_observations(observations)
    variants = sorted(phenotype)
    if set(variants) - set(predictions):
        raise ValueError("revealed variants lack frozen predictions")
    strata: dict[str, str] = {}
    for row in design_rows:
        variant = row["variant_id"]
        stratum = row["mutation_count_stratum"]
        if variant in strata and strata[variant] != stratum:
            raise ValueError(f"variant spans mutation-count strata: {variant}")
        strata[variant] = stratum

    model_predictions = {
        model: {variant: predictions[variant][model] for variant in variants}
        for model in required_models
    }
    spearman_by_model = {
        model: spearman([scores[v] for v in variants], [phenotype[v] for v in variants])
        for model, scores in model_predictions.items()
    }
    primary_delta = spearman_by_model["aggregate_chemistry"] - spearman_by_model["native_count"]
    within_count = residualized_within_count(
        variants, model_predictions["aggregate_chemistry"], phenotype, strata
    )

    fractions = [0.05, *protocol["secondary_precision_fractions"]]
    fractions = sorted(set(float(value) for value in fractions))
    precision = {
        f"{fraction:.2f}": {
            model: precision_at(variants, scores, phenotype, fraction, int(protocol["bootstrap"]["seed"]))
            for model, scores in model_predictions.items()
        }
        for fraction in fractions
    }

    boot = protocol["bootstrap"]
    deltas = bootstrap_deltas(
        observations, predictions, strata, int(boot["replicates"]), int(boot["seed"])
    )
    tail = (1.0 - float(boot["confidence"])) / 2.0
    primary_ci = [percentile(deltas, tail), percentile(deltas, 1.0 - tail)]

    permutation = protocol["permutation"]
    p_value = permutation_p_value(
        observations,
        model_predictions["aggregate_chemistry"],
        strata,
        within_count,
        int(permutation["replicates"]),
        int(permutation["seed"]),
    )
    precision_005 = precision["0.05"]
    result = {
        "schema_version": 1,
        "freeze_manifest_sha256": sha256_file(manifest_path),
        "phenotype_file_sha256": sha256_file(args.phenotypes.resolve()),
        "variants": len(variants),
        "observations": len(observations),
        "spearman_by_model": spearman_by_model,
        "primary_spearman_delta": primary_delta,
        "primary_bootstrap_ci": primary_ci,
        "within_native_count_spearman": within_count,
        "within_count_permutation_p": p_value,
        "precision_by_fraction_and_model": precision,
        "applied_precision_at_5_percent_delta": (
            precision_005["aggregate_chemistry"] - precision_005["native_count"]
        ),
        "replication_criterion_met": bool(
            primary_ci[0] > 0 and p_value <= float(permutation["alpha"])
        ),
        "protocol": protocol,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
    return result


def main() -> None:
    result = evaluate(parse_args())
    print(json.dumps({
        "primary_spearman_delta": result["primary_spearman_delta"],
        "primary_bootstrap_ci": result["primary_bootstrap_ci"],
        "within_count_permutation_p": result["within_count_permutation_p"],
        "replication_criterion_met": result["replication_criterion_met"],
    }, indent=2))


if __name__ == "__main__":
    main()
