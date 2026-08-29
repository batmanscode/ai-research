#!/usr/bin/env python3
"""Search connected P5-free graphs containing a fixed C5 and gamma >= 4."""

from __future__ import annotations

import argparse
import itertools
import sys
import time
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
COMPUTATION = PROJECT / "computation"
sys.path.insert(0, str(COMPUTATION))

from pysat.solvers import Solver  # type: ignore
from search_extremal import Encoder, encode_graph6  # type: ignore


class GammaEncoder(Encoder):
    def __init__(self, n: int) -> None:
        # Parent fields are useful even though alpha / secure clauses are omitted.
        super().__init__(n, alpha_value=1, secure_size=1)

    def encode_fixed_c5(self) -> None:
        cycle = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
        for i, j in itertools.combinations(range(5), 2):
            self.add([self.edge(i, j) if (i, j) in cycle else -self.edge(i, j)], "fixed_c5")

    def encode_no_dominating_triple(self) -> None:
        vertices = set(range(self.n))
        for chosen in itertools.combinations(range(self.n), 3):
            witnesses = []
            for y in sorted(vertices - set(chosen)):
                q = self.v.get("anti", chosen, y)
                incident = [self.edge(y, z) for z in chosen]
                for edge in incident:
                    self.add([-q, -edge], "anti_equivalence")
                self.add([q, *incident], "anti_equivalence")
                witnesses.append(q)
            self.add(witnesses, "no_dominating_triple")

    def build_gamma(self) -> None:
        self.encode_fixed_c5()
        self.encode_p5_free()
        self.encode_connectivity()
        self.encode_no_dominating_triple()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--solver", default="cadical195")
    args = parser.parse_args()
    t = time.time()
    enc = GammaEncoder(args.n)
    enc.build_gamma()
    built = time.time() - t
    with Solver(name=args.solver, bootstrap_with=enc.cnf.clauses) as solver:
        status = solver.solve()
        model = solver.get_model() if status else None
    out = {"n": args.n, "status": "SAT" if status else "UNSAT", "vars": enc.v.next_id - 1,
           "clauses": len(enc.cnf.clauses), "build_seconds": built, "total_seconds": time.time()-t}
    if model:
        truth = {x for x in model if x > 0}
        edges = [(i,j) for i,j in itertools.combinations(range(args.n),2) if enc.edge(i,j) in truth]
        out["edges"] = edges
        out["graph6"] = encode_graph6(args.n, edges)
    print(out)


if __name__ == "__main__":
    main()
