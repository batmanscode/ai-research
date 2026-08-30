#!/usr/bin/env python3
"""Bounded SAT audit for a private cross edge at a dominating triangle.

The model asks for a graph with a fixed dominating triangle 0,1,2, fixed
private vertices 3,4,5 for the respective hubs, the cross edge 3-4,
induced-P5-freeness, and no dominating induced P3.  The proved theorem rules such a graph out, so UNSAT corroborates it.

No SAT result is used in the mathematical proof.
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path


COMPUTATION = Path(__file__).resolve().parent
sys.path.insert(0, str(COMPUTATION))

from pysat.solvers import Solver  # type: ignore
from clique_branch_search import CliqueBranchEncoder


def build(order: int) -> CliqueBranchEncoder:
    encoder = CliqueBranchEncoder(order, alpha_value=1, secure_size=1)
    encoder.encode_p5_free()
    encoder.encode_no_dominating_induced_p3()

    # Fixed triangle K={0,1,2}.
    for first, second in itertools.combinations(range(3), 2):
        encoder.add([encoder.edge(first, second)], "fixed_triangle")

    # K dominates the graph.
    for vertex in range(3, order):
        encoder.add(
            [encoder.edge(vertex, hub) for hub in range(3)],
            "fixed_triangle_domination",
        )

    # Vertices 3,4,5 are private to 0,1,2 respectively.
    for vertex, private_hub in ((3, 0), (4, 1), (5, 2)):
        for hub in range(3):
            literal = encoder.edge(vertex, hub)
            encoder.add(
                [literal if hub == private_hub else -literal],
                "fixed_private_types",
            )

    encoder.add([encoder.edge(3, 4)], "fixed_private_cross_edge")
    return encoder


def main() -> None:
    rows = []
    for order in range(6, 15):
        encoder = build(order)
        with Solver(name="cadical195", bootstrap_with=encoder.cnf.clauses) as solver:
            status = solver.solve()
        rows.append(
            {
                "order": order,
                "status": "SAT" if status else "UNSAT",
                "variables": encoder.v.next_id - 1,
                "clauses": len(encoder.cnf.clauses),
            }
        )
    print(
        json.dumps(
            {
                "constraints": {
                    "dominating_triangle": [0, 1, 2],
                    "private_vertices": {"0": 3, "1": 4, "2": 5},
                    "private_cross_edge": [3, 4],
                    "induced_P5_free": True,
                    "no_dominating_induced_P3": True,
                },
                "runs": rows,
                "status": (
                    "PASS"
                    if all(row["status"] == "UNSAT" for row in rows)
                    else "FAIL"
                ),
                "scope": "finite corroboration only; no retained proof traces",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

