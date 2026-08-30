#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE))

import freeze  # noqa: E402
import reveal_evaluate  # noqa: E402


MODELS = [
    "native_count",
    "aggregate_chemistry",
    "additive_position_ridge",
    "onehot_ridge",
    "plm_likelihood",
    "onehot_plus_plm",
    "structure_invariant",
]


class FreezePackageTests(unittest.TestCase):
    def make_inputs(self, root: Path, add_fitness: bool = False) -> dict[str, Path]:
        candidate = root / "candidate_design.tsv"
        candidate_header = list(freeze.DESIGN_COLUMNS) + (["fitness"] if add_fitness else [])
        variants = [
            ("V0", "FFFFFFF"),
            ("V1", "IFFFFFF"),
            ("V2", "IIFFFFF"),
            ("V3", "IIIFFFF"),
            ("V4", "IIIIFFF"),
            ("V5", "LFFFFFF"),
            ("V6", "LLFFFFF"),
            ("V7", "LLLFFFF"),
        ]
        with candidate.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=candidate_header, delimiter="\t")
            writer.writeheader()
            for library_index in range(3):
                for variant, sequence in variants:
                    row = {
                        "observation_id": f"O{library_index}_{variant}",
                        "variant_id": variant,
                        "sequence": sequence,
                        "native_core": "FFFFFFF",
                        "randomized_positions": "1,2,3,4,5,6,7",
                        "alphabet": "F/I/L/M/V",
                        "construct_id": "CANDIDATE_A",
                        "biological_library_id": f"LIB{library_index}",
                        "batch_id": f"BATCH{library_index}",
                        "mutation_count_stratum": str(sum(a != b for a, b in zip(sequence, "FFFFFFF"))),
                    }
                    if add_fitness:
                        row["fitness"] = "0.0"
                    writer.writerow(row)

        predictions = root / "predictions.tsv"
        with predictions.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["variant_id", *MODELS], delimiter="\t")
            writer.writeheader()
            for index, (variant, sequence) in enumerate(variants):
                mutation_count = sum(a != b for a, b in zip(sequence, "FFFFFFF"))
                quality = float(index) + (0.2 if variant.startswith("V5") else 0.0)
                writer.writerow({
                    "variant_id": variant,
                    "native_count": -mutation_count,
                    "aggregate_chemistry": quality,
                    "additive_position_ridge": quality * 0.8,
                    "onehot_ridge": quality * 0.7,
                    "plm_likelihood": quality * 0.6,
                    "onehot_plus_plm": quality * 0.9,
                    "structure_invariant": quality * 0.5,
                })

        structures = root / "structures.lock.json"
        structures.write_text(json.dumps({
            "schema_version": 1,
            "candidate_accession": "TEST_ACCESSION",
            "structure_identifier": "TEST_STRUCTURE_V1",
            "chain": "A",
            "randomized_site_mapping": [1, 2, 3, 4, 5, 6, 7],
        }), encoding="utf-8")

        protocol = json.loads((PACKAGE / "protocol.lock.json").read_text(encoding="utf-8"))
        protocol["bootstrap"]["replicates"] = 30
        protocol["permutation"]["replicates"] = 30
        protocol_path = root / "protocol.lock.json"
        protocol_path.write_text(json.dumps(protocol), encoding="utf-8")

        phenotypes = root / "phenotypes.tsv"
        with phenotypes.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["observation_id", "phenotype"], delimiter="\t")
            writer.writeheader()
            for library_index in range(3):
                for index, (variant, _) in enumerate(variants):
                    writer.writerow({
                        "observation_id": f"O{library_index}_{variant}",
                        "phenotype": index + library_index * 0.01,
                    })
        return {
            "candidate": candidate,
            "predictions": predictions,
            "structures": structures,
            "protocol": protocol_path,
            "phenotypes": phenotypes,
        }

    @staticmethod
    def freeze_args(paths: dict[str, Path], root: Path) -> argparse.Namespace:
        return argparse.Namespace(
            candidate=paths["candidate"],
            predictions=paths["predictions"],
            structures=paths["structures"],
            protocol=paths["protocol"],
            output=root / "manifest.lock.json",
        )

    def test_valid_freeze_and_reveal(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE) as directory:
            root = Path(directory)
            paths = self.make_inputs(root)
            freeze_args = self.freeze_args(paths, root)
            manifest = freeze.freeze(freeze_args)
            self.assertEqual(manifest["status"], "FROZEN_NO_PHENOTYPES")
            self.assertNotIn("phenotypes.tsv", json.dumps(manifest))
            with self.assertRaises(FileExistsError):
                freeze.freeze(freeze_args)

            output = root / "results.json"
            result = reveal_evaluate.evaluate(argparse.Namespace(
                manifest=freeze_args.output,
                phenotypes=paths["phenotypes"],
                output=output,
            ))
            self.assertEqual(set(result["spearman_by_model"]), set(MODELS))
            self.assertGreaterEqual(result["within_count_permutation_p"], 1 / 31)
            result_text = output.read_text(encoding="utf-8")
            self.assertNotIn("O0_V0", result_text)

    def test_rejects_phenotype_column_before_freeze(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE) as directory:
            root = Path(directory)
            paths = self.make_inputs(root, add_fitness=True)
            with self.assertRaisesRegex(ValueError, "prohibited"):
                freeze.freeze(self.freeze_args(paths, root))

    def test_rejects_mutation_count_mismatch(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE) as directory:
            root = Path(directory)
            paths = self.make_inputs(root)
            text = paths["candidate"].read_text(encoding="utf-8")
            paths["candidate"].write_text(text.replace("\t0\n", "\t7\n", 1), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "mutation-count mismatch"):
                freeze.freeze(self.freeze_args(paths, root))

    def test_hash_tamper_fails_before_reveal(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE) as directory:
            root = Path(directory)
            paths = self.make_inputs(root)
            freeze_args = self.freeze_args(paths, root)
            freeze.freeze(freeze_args)
            with paths["predictions"].open("a", encoding="utf-8") as handle:
                handle.write("\n")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                reveal_evaluate.evaluate(argparse.Namespace(
                    manifest=freeze_args.output,
                    phenotypes=paths["phenotypes"],
                    output=root / "results.json",
                ))


if __name__ == "__main__":
    unittest.main()
