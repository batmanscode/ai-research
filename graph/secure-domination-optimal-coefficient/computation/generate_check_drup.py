#!/usr/bin/env python3
"""Emit and independently check a DRUP trace for a bounded UNSAT instance.

The producer and checker are selected on the command line.  The retained
certificates were produced by Glucose 4.2 and checked with MapleSAT's unit-
propagation primitive.  Deletion lines are conservatively ignored; retaining
previously derived clauses is sound for a DRUP check.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "vendor"))

from pysat.solvers import Solver  # type: ignore

from search_extremal import Encoder


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--alpha", type=int, required=True)
    parser.add_argument("--secure-size", type=int, required=True)
    parser.add_argument("--prefix", type=Path, required=True)
    parser.add_argument("--producer", default="glucose42")
    parser.add_argument("--checker", default="maplesat")
    args = parser.parse_args()

    encoder = Encoder(args.n, args.alpha, args.secure_size)
    encoder.build()
    args.prefix.parent.mkdir(parents=True, exist_ok=True)
    cnf_path = args.prefix.with_suffix(".cnf")
    proof_path = args.prefix.with_suffix(".drup")
    audit_path = args.prefix.with_suffix(".proof-audit.json")
    encoder.cnf.to_file(cnf_path)

    solve_started = time.time()
    with Solver(name=args.producer, bootstrap_with=encoder.cnf.clauses, with_proof=True) as producer:
        status = producer.solve()
        if status is not False:
            raise AssertionError(f"expected UNSAT, got {status}")
        proof = producer.get_proof()
    solve_seconds = time.time() - solve_started
    if proof is None:
        raise AssertionError(f"{args.producer} returned no proof")
    proof_path.write_text("\n".join(proof) + "\n", encoding="ascii")

    additions: list[list[int]] = []
    deletions = 0
    for line in proof:
        if line.startswith("d "):
            deletions += 1
            continue
        fields = [int(value) for value in line.split()]
        if not fields or fields[-1] != 0:
            raise AssertionError(f"malformed proof line: {line!r}")
        additions.append(fields[:-1])

    checked_started = time.time()
    failures = []
    with Solver(name=args.checker, bootstrap_with=encoder.cnf.clauses) as checker:
        for index, clause in enumerate(additions):
            consistent, _ = checker.propagate(assumptions=[-lit for lit in clause])
            if consistent:
                failures.append(index)
                if len(failures) >= 10:
                    break
            checker.add_clause(clause)
    check_seconds = time.time() - checked_started
    empty_indices = [i for i, clause in enumerate(additions) if not clause]
    passed = not failures and bool(empty_indices)
    audit = {
        "order": args.n,
        "alpha": args.alpha,
        "secure_size": args.secure_size,
        "producer": args.producer,
        "checker_propagator": args.checker,
        "original_variables": encoder.v.next_id - 1,
        "original_clauses": len(encoder.cnf.clauses),
        "proof_lines": len(proof),
        "addition_lines": len(additions),
        "deletion_lines_ignored": deletions,
        "empty_clause_indices": empty_indices,
        "non_rup_addition_indices": failures,
        "solve_seconds": solve_seconds,
        "check_seconds": check_seconds,
        "status": "PASS" if passed else "FAIL",
        "method": "Every retained addition is RUP by unit propagation; the trace derives the empty clause. Deletions are ignored.",
    }
    audit_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
