#!/usr/bin/env python3
"""Freeze label-free candidate metadata, predictions, and protocol hashes."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


DESIGN_COLUMNS = (
    "observation_id",
    "variant_id",
    "sequence",
    "native_core",
    "randomized_positions",
    "alphabet",
    "construct_id",
    "biological_library_id",
    "batch_id",
    "mutation_count_stratum",
)
PROHIBITED_COLUMNS = {
    "target",
    "targets",
    "label",
    "labels",
    "fitness",
    "score",
    "scores",
    "phenotype",
    "phenotypes",
    "read_count",
    "read_counts",
    "input_count",
    "output_count",
    "measurement",
    "measurements",
}


def normalized(name: str) -> str:
    return name.strip().lower().replace("-", "_").replace(" ", "_")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise ValueError(f"{path.name}: missing header")
        header = [normalized(item) for item in reader.fieldnames]
        if len(header) != len(set(header)):
            raise ValueError(f"{path.name}: duplicate normalized column")
        rows = [{normalized(k): (v or "").strip() for k, v in row.items()} for row in reader]
    if not rows:
        raise ValueError(f"{path.name}: no data rows")
    return header, rows


def reject_label_columns(path: Path, header: Iterable[str]) -> None:
    found = sorted(set(header) & PROHIBITED_COLUMNS)
    if found:
        raise ValueError(f"{path.name}: prohibited pre-reveal column(s): {', '.join(found)}")


def require_columns(path: Path, header: Iterable[str], required: Iterable[str]) -> None:
    missing = sorted(set(required) - set(header))
    if missing:
        raise ValueError(f"{path.name}: missing required column(s): {', '.join(missing)}")


def require_unique(path: Path, rows: list[dict[str, str]], column: str) -> None:
    values = [row[column] for row in rows]
    if any(not value for value in values):
        raise ValueError(f"{path.name}: blank {column}")
    if len(values) != len(set(values)):
        raise ValueError(f"{path.name}: duplicate {column}")


def contains_placeholder(value: object) -> bool:
    if isinstance(value, str):
        return "REPLACE_BEFORE_FREEZE" in value or value == "REPLACE_ME"
    if isinstance(value, list):
        return any(contains_placeholder(item) for item in value)
    if isinstance(value, dict):
        return any(contains_placeholder(item) for item in value.values())
    return False


def parse_args() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, default=here / "candidate_design.tsv")
    parser.add_argument("--predictions", type=Path, default=here / "predictions.tsv")
    parser.add_argument("--structures", type=Path, default=here / "structures.lock.json")
    parser.add_argument("--protocol", type=Path, default=here / "protocol.lock.json")
    parser.add_argument("--output", type=Path, default=here / "manifest.lock.json")
    return parser.parse_args()


def freeze(args: argparse.Namespace) -> dict[str, object]:
    here = Path(__file__).resolve().parent
    project = here.parent
    candidate = args.candidate.resolve()
    predictions = args.predictions.resolve()
    structures = args.structures.resolve()
    protocol_path = args.protocol.resolve()
    output = args.output.resolve()

    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing freeze: {output}")

    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    design_header, design_rows = read_tsv(candidate)
    reject_label_columns(candidate, design_header)
    require_columns(candidate, design_header, DESIGN_COLUMNS)
    if tuple(design_header) != DESIGN_COLUMNS:
        raise ValueError(f"{candidate.name}: header must exactly match the frozen schema")
    require_unique(candidate, design_rows, "observation_id")

    design_rule = protocol["candidate_design"]
    allowed_alphabet = "/".join(design_rule["allowed_alphabet"])
    core_length = int(design_rule["core_length"])
    variant_metadata: dict[str, tuple[str, str, str, str]] = {}
    libraries = {row["biological_library_id"] for row in design_rows}
    if len(libraries) < int(design_rule["minimum_biological_libraries"]):
        raise ValueError("candidate_design.tsv: too few biological libraries")
    variant_libraries: dict[str, set[str]] = {}
    assignments: set[tuple[str, str]] = set()
    for row in design_rows:
        if row["alphabet"] != allowed_alphabet:
            raise ValueError(f"candidate_design.tsv: wrong alphabet for {row['variant_id']}")
        if len(row["native_core"]) != core_length:
            raise ValueError(f"candidate_design.tsv: wrong native-core length for {row['variant_id']}")
        positions = [int(value) for value in row["randomized_positions"].split(",")]
        if len(positions) != core_length or len(set(positions)) != core_length:
            raise ValueError(f"candidate_design.tsv: expected seven distinct positions for {row['variant_id']}")
        if positions != sorted(positions) or min(positions) < 1 or max(positions) > len(row["sequence"]):
            raise ValueError(f"candidate_design.tsv: invalid randomized positions for {row['variant_id']}")
        observed_core = "".join(row["sequence"][position - 1] for position in positions)
        mutation_count = sum(a != b for a, b in zip(observed_core, row["native_core"]))
        if row["mutation_count_stratum"] != str(mutation_count):
            raise ValueError(f"candidate_design.tsv: mutation-count mismatch for {row['variant_id']}")
        metadata = (row["sequence"], row["native_core"], row["randomized_positions"], row["alphabet"])
        if row["variant_id"] in variant_metadata and variant_metadata[row["variant_id"]] != metadata:
            raise ValueError(f"candidate_design.tsv: inconsistent variant metadata for {row['variant_id']}")
        variant_metadata[row["variant_id"]] = metadata
        assignment = (row["variant_id"], row["biological_library_id"])
        if assignment in assignments:
            raise ValueError(f"candidate_design.tsv: duplicate variant/library assignment: {assignment}")
        assignments.add(assignment)
        variant_libraries.setdefault(row["variant_id"], set()).add(row["biological_library_id"])
    incomplete = [variant for variant, assigned in variant_libraries.items() if assigned != libraries]
    if incomplete:
        raise ValueError(f"candidate_design.tsv: {len(incomplete)} variant(s) missing a biological-library assignment")

    prediction_header, prediction_rows = read_tsv(predictions)
    reject_label_columns(predictions, prediction_header)
    required_predictions = ["variant_id", *protocol["required_prediction_columns"]]
    require_columns(predictions, prediction_header, required_predictions)
    if prediction_header != required_predictions:
        raise ValueError(f"{predictions.name}: header must exactly match the frozen schema")
    require_unique(predictions, prediction_rows, "variant_id")
    for row in prediction_rows:
        for column in protocol["required_prediction_columns"]:
            value = float(row[column])
            if not math.isfinite(value):
                raise ValueError(f"predictions.tsv: non-finite {column} for {row['variant_id']}")

    design_variants = {row["variant_id"] for row in design_rows}
    prediction_variants = {row["variant_id"] for row in prediction_rows}
    missing_predictions = sorted(design_variants - prediction_variants)
    if missing_predictions:
        raise ValueError(f"predictions.tsv: missing {len(missing_predictions)} design variant(s)")

    structure_spec = json.loads(structures.read_text(encoding="utf-8"))
    if contains_placeholder(structure_spec):
        raise ValueError("structures.lock.json still contains a placeholder")

    locked = [
        candidate,
        predictions,
        structures,
        protocol_path,
        project / "native_core_transfer.py",
        here / "freeze.py",
        here / "reveal_evaluate.py",
    ]
    for path in locked:
        if not path.is_file():
            raise FileNotFoundError(path)

    def display_path(path: Path) -> str:
        try:
            return path.relative_to(project).as_posix()
        except ValueError:
            return path.as_posix()

    manifest = {
        "schema_version": 1,
        "status": "FROZEN_NO_PHENOTYPES",
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "candidate_observations": len(design_rows),
        "candidate_variants": len(design_variants),
        "prediction_variants": len(prediction_variants),
        "roles": {
            "candidate_design": display_path(candidate),
            "predictions": display_path(predictions),
            "structures": display_path(structures),
            "protocol": display_path(protocol_path),
        },
        "files": {
            display_path(path): {"sha256": sha256_file(path), "bytes": path.stat().st_size}
            for path in locked
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return manifest


def main() -> None:
    manifest = freeze(parse_args())
    print(json.dumps({
        "status": manifest["status"],
        "candidate_observations": manifest["candidate_observations"],
        "candidate_variants": manifest["candidate_variants"],
    }, indent=2))


if __name__ == "__main__":
    main()
