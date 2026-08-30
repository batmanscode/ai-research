#!/usr/bin/env python3
"""SAT search restricted to the irreducible dominating-clique branch.

This repository module reuses the
audited generic graph/secure-domination encoder and adds only reductions that
are proved for a counterexample to gamma_s <= alpha + 1:

* 2-connectivity (the cut-vertex theorem),
* no dominating pair (the residual-completion theorem), and
* no dominating induced P3 (the dominating-P3 theorem, for alpha >= 3).

The added selectors are existentially exact.  ``pair_miss[u,v,x]`` certifies
that x is missed by {u,v}; ``p3_miss[a,b,c,x]`` certifies that x is missed by
the induced path a-b-c.  A dominating clique is selected explicitly.  Since
all pairs are non-dominating, any selected dominating clique has minimum size
at least three.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import threading
import time
from pathlib import Path

COMPUTATION = Path(__file__).resolve().parent
sys.path.insert(0, str(COMPUTATION))

from pysat.solvers import Solver  # type: ignore
from search_extremal import Encoder, encode_graph6


class CliqueBranchEncoder(Encoder):
    """The audited base encoder plus exact branch-elimination clauses."""

    def encode_no_dominating_pair(self) -> None:
        # For each unordered pair {u,v}, choose an outside vertex x missed by
        # both.  This encodes the negation of domination exactly.
        for u, v in itertools.combinations(range(self.n), 2):
            witnesses: list[int] = []
            for x in range(self.n):
                if x in (u, v):
                    continue
                witness = self.v.get("pair_miss", u, v, x)
                witnesses.append(witness)
                self.add([-witness, -self.edge(u, x)], "no_dominating_pair")
                self.add([-witness, -self.edge(v, x)], "no_dominating_pair")
            self.add(witnesses, "no_dominating_pair")

    def encode_no_dominating_induced_p3(self) -> None:
        # For every possible centre b and unordered endpoints a,c, if a-b-c
        # is induced, one outside vertex has no neighbour in that path.
        vertices = set(range(self.n))
        for b in range(self.n):
            endpoints = sorted(vertices - {b})
            for a, c in itertools.combinations(endpoints, 2):
                witnesses: list[int] = []
                for x in sorted(vertices - {a, b, c}):
                    witness = self.v.get("p3_miss", a, b, c, x)
                    witnesses.append(witness)
                    self.add([-witness, -self.edge(a, x)], "no_dominating_induced_p3")
                    self.add([-witness, -self.edge(b, x)], "no_dominating_induced_p3")
                    self.add([-witness, -self.edge(c, x)], "no_dominating_induced_p3")
                # The first three literals negate exactly the induced-P3
                # condition e(ab) & e(bc) & !e(ac).
                self.add(
                    [-self.edge(a, b), -self.edge(b, c), self.edge(a, c), *witnesses],
                    "no_dominating_induced_p3",
                )

    def build_branch(self, type_order: bool = True) -> None:
        self.encode_alpha_four()
        if type_order:
            self.encode_outside_type_order()
        self.encode_p5_free()
        self.encode_connectivity()
        self.encode_connected_after_deletion()
        self.encode_domination()
        self.encode_no_secure_five_set()
        self.encode_dominating_clique(minimum_size=1)
        self.encode_no_dominating_pair()
        self.encode_no_dominating_induced_p3()


def solve(args: argparse.Namespace) -> dict:
    secure_size = args.secure_size if args.secure_size is not None else args.alpha + 1
    if args.alpha < 4:
        raise ValueError("this branch search is intended for alpha >= 4")
    started = time.time()
    encoder = CliqueBranchEncoder(args.n, alpha_value=args.alpha, secure_size=secure_size)
    encoder.build_branch(type_order=not args.no_type_order)
    encoding_seconds = time.time() - started

    if args.dimacs:
        encoder.cnf.to_file(args.dimacs)

    solver_started = time.time()
    with Solver(name=args.solver, bootstrap_with=encoder.cnf.clauses) as solver:
        timer = None
        if args.timeout:
            timer = threading.Timer(args.timeout, solver.interrupt)
            timer.start()
            status = solver.solve_limited(expect_interrupt=True)
            timer.cancel()
        else:
            status = solver.solve()
        stats = solver.accum_stats()
        model = solver.get_model() if status is True else None

    result: dict = {
        "order": args.n,
        "solver": args.solver,
        "status": "SAT" if status is True else "UNSAT" if status is False else "UNKNOWN",
        "variables": encoder.v.next_id - 1,
        "clauses": len(encoder.cnf.clauses),
        "clause_families": encoder.counts,
        "encoding_seconds": encoding_seconds,
        "solver_seconds": time.time() - solver_started,
        "solver_stats": stats,
        "proof_trace": None,
        "constraints": {
            "connected": True,
            "two_connected": True,
            "induced_P5_free": True,
            "alpha_exactly": args.alpha,
            "no_secure_set_of_size": secure_size,
            "has_dominating_clique": True,
            "no_dominating_pair": True,
            "no_dominating_induced_P3": True,
            "minimum_dominating_clique_size_at_least": 3,
            "outside_type_order_symmetry_break": not args.no_type_order,
        },
    }
    if model is not None:
        edges = encoder.graph_from_model(model)
        result["edges"] = [list(edge) for edge in edges]
        result["graph6"] = encode_graph6(args.n, edges)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--alpha", type=int, required=True)
    parser.add_argument("--secure-size", type=int, default=None)
    parser.add_argument("--solver", default="glucose42")
    parser.add_argument("--timeout", type=float, default=None)
    parser.add_argument("--no-type-order", action="store_true")
    parser.add_argument("--dimacs", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = solve(args)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()

