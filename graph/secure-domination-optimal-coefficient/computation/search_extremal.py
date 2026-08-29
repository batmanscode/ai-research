#!/usr/bin/env python3
"""Exact SAT search for alpha=4, gamma_s>=6 induced-P5-free graphs.

The graph has vertices 0,...,n-1.  Vertices 0,1,2,3 are fixed as an
independent set; this is lossless because any graph with alpha=4 can be
relabeled so that a maximum independent set has those labels.

The key encoding defines, for every 5-set T:

* q[T,y] iff y outside T has no neighbor in T;
* d[T] iff T is a dominating set.

A dominating 5-set S is forced to have an attacked vertex x for which every
adjacent defender u produces a non-dominating swap S-u+x.  Hence no 5-set is
secure.  Secure domination is upward-closed, so this rules out all secure
sets of size at most five.

Connectivity is certified by layered reachability from vertex 0.  An induced
P5 is excluded for every 5-subset and every one of its 60 path orderings.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import threading
import time
from collections.abc import Iterable
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENDOR = HERE / "vendor"
if VENDOR.exists():
    sys.path.insert(0, str(VENDOR))

from pysat.formula import CNF  # type: ignore  # vendored for this experiment
from pysat.solvers import Solver  # type: ignore


class Variables:
    def __init__(self) -> None:
        self.next_id = 1
        self.names: dict[tuple, int] = {}

    def get(self, *key: object) -> int:
        name = tuple(key)
        value = self.names.get(name)
        if value is None:
            value = self.next_id
            self.next_id += 1
            self.names[name] = value
        return value


class Encoder:
    def __init__(self, n: int, alpha_value: int = 4, secure_size: int = 5) -> None:
        if alpha_value < 1:
            raise ValueError("alpha must be positive")
        if secure_size < 1 or n <= secure_size:
            raise ValueError("need 1 <= secure_size < n")
        if n < alpha_value:
            raise ValueError("n must be at least alpha")
        self.n = n
        self.alpha_value = alpha_value
        self.secure_size = secure_size
        self.v = Variables()
        self.cnf = CNF()
        self.counts: dict[str, int] = {}
        self.p5_vertex_sets = list(itertools.combinations(range(n), 5))
        self.secure_sets = list(itertools.combinations(range(n), secure_size))

    def add(self, clause: Iterable[int], family: str) -> None:
        self.cnf.append(list(clause))
        self.counts[family] = self.counts.get(family, 0) + 1

    def edge(self, a: int, b: int) -> int:
        if a == b:
            raise ValueError("loops are not graph variables")
        if a > b:
            a, b = b, a
        return self.v.get("e", a, b)

    def q(self, chosen: tuple[int, ...], y: int) -> int:
        return self.v.get("q", chosen, y)

    def dom(self, chosen: tuple[int, ...]) -> int:
        return self.v.get("d", chosen)

    def attack(self, chosen: tuple[int, ...], x: int) -> int:
        return self.v.get("a", chosen, x)

    def encode_alpha_four(self) -> None:
        # A fixed independent alpha-set is a lossless witness after relabeling.
        for a, b in itertools.combinations(range(self.alpha_value), 2):
            self.add([-self.edge(a, b)], "fixed_independent_set")

        # Every (alpha+1)-set contains an edge, so alpha is at most the target.
        for chosen in itertools.combinations(range(self.n), self.alpha_value + 1):
            self.add(
                [self.edge(a, b) for a, b in itertools.combinations(chosen, 2)],
                "no_larger_independent_set",
            )

    def encode_p5_free(self) -> None:
        # Each undirected path ordering is represented once by requiring the
        # first endpoint to be smaller than the last endpoint.
        for chosen in self.p5_vertex_sets:
            for order in itertools.permutations(chosen):
                if order[0] > order[-1]:
                    continue
                path_pairs = {
                    tuple(sorted((order[i], order[i + 1]))) for i in range(4)
                }
                clause: list[int] = []
                for i, j in itertools.combinations(range(5), 2):
                    a, b = sorted((order[i], order[j]))
                    edge = self.edge(a, b)
                    clause.append(-edge if (a, b) in path_pairs else edge)
                self.add(clause, "induced_p5_forbidden")

    def encode_connectivity(self) -> None:
        # r[k,v] means the chosen certificate reaches v from 0 in <= k steps.
        # Only the reverse implication is needed: every claimed reachability
        # must be supported by the previous layer or by a real incident edge.
        for vertex in range(self.n):
            initial = self.v.get("r", 0, vertex)
            self.add([initial if vertex == 0 else -initial], "reachability_initial")

        for layer in range(1, self.n):
            for vertex in range(self.n):
                current = self.v.get("r", layer, vertex)
                previous = self.v.get("r", layer - 1, vertex)
                supports: list[int] = [previous]
                for parent in range(self.n):
                    if parent == vertex:
                        continue
                    witness = self.v.get("z", layer, parent, vertex)
                    supports.append(witness)
                    self.add(
                        [-witness, self.v.get("r", layer - 1, parent)],
                        "reachability_witness",
                    )
                    self.add(
                        [-witness, self.edge(parent, vertex)],
                        "reachability_witness",
                    )
                self.add([-current, *supports], "reachability_support")

        for vertex in range(self.n):
            self.add([self.v.get("r", self.n - 1, vertex)], "reachability_final")

    def encode_connected_after_deletion(self) -> None:
        """Certify that deletion of every vertex leaves a connected graph."""
        for deleted in range(self.n):
            remaining = [v for v in range(self.n) if v != deleted]
            root = remaining[0]
            last_layer = len(remaining) - 1
            for vertex in remaining:
                initial = self.v.get("rdel", deleted, 0, vertex)
                self.add(
                    [initial if vertex == root else -initial],
                    "biconnectivity_initial",
                )
            for layer in range(1, len(remaining)):
                for vertex in remaining:
                    current = self.v.get("rdel", deleted, layer, vertex)
                    previous = self.v.get("rdel", deleted, layer - 1, vertex)
                    supports = [previous]
                    for parent in remaining:
                        if parent == vertex:
                            continue
                        witness = self.v.get("zdel", deleted, layer, parent, vertex)
                        supports.append(witness)
                        self.add(
                            [-witness, self.v.get("rdel", deleted, layer - 1, parent)],
                            "biconnectivity_witness",
                        )
                        self.add(
                            [-witness, self.edge(parent, vertex)],
                            "biconnectivity_witness",
                        )
                    self.add([-current, *supports], "biconnectivity_support")
            for vertex in remaining:
                self.add(
                    [self.v.get("rdel", deleted, last_layer, vertex)],
                    "biconnectivity_final",
                )

    def encode_complement_connectivity(self) -> None:
        """Certify connectivity in the complement using nonedges as links."""
        for vertex in range(self.n):
            initial = self.v.get("rc", 0, vertex)
            self.add([initial if vertex == 0 else -initial], "co_reachability_initial")
        for layer in range(1, self.n):
            for vertex in range(self.n):
                current = self.v.get("rc", layer, vertex)
                previous = self.v.get("rc", layer - 1, vertex)
                supports = [previous]
                for parent in range(self.n):
                    if parent == vertex:
                        continue
                    witness = self.v.get("zc", layer, parent, vertex)
                    supports.append(witness)
                    self.add(
                        [-witness, self.v.get("rc", layer - 1, parent)],
                        "co_reachability_witness",
                    )
                    self.add(
                        [-witness, -self.edge(parent, vertex)],
                        "co_reachability_witness",
                    )
                self.add([-current, *supports], "co_reachability_support")
        for vertex in range(self.n):
            self.add([self.v.get("rc", self.n - 1, vertex)], "co_reachability_final")

    def encode_true_twin_free(self) -> None:
        for u, v in itertools.combinations(range(self.n), 2):
            distinguishers = []
            for w in range(self.n):
                if w in (u, v):
                    continue
                xor = self.v.get("xor", u, v, w)
                distinguishers.append(xor)
                edge_uw = self.edge(u, w)
                edge_vw = self.edge(v, w)
                self.add([-xor, edge_uw, edge_vw], "true_twin_distinguisher")
                self.add([-xor, -edge_uw, -edge_vw], "true_twin_distinguisher")
            self.add([-self.edge(u, v), *distinguishers], "true_twin_free")

    def encode_dominating_clique(self, minimum_size: int = 1) -> None:
        selected = [self.v.get("clique", v) for v in range(self.n)]
        for u, v in itertools.combinations(range(self.n), 2):
            self.add(
                [-selected[u], -selected[v], self.edge(u, v)],
                "selected_clique",
            )
        for attacked in range(self.n):
            witnesses = []
            for member in range(self.n):
                if member == attacked:
                    continue
                witness = self.v.get("clique_dom", attacked, member)
                witnesses.append(witness)
                self.add([-witness, selected[member]], "selected_clique_domination")
                self.add(
                    [-witness, self.edge(attacked, member)],
                    "selected_clique_domination",
                )
            self.add(
                [selected[attacked], *witnesses],
                "selected_clique_domination",
            )

        if minimum_size >= 2:
            # No universal vertex, hence no dominating clique of size one.
            for vertex in range(self.n):
                self.add(
                    [-self.edge(vertex, other) for other in range(self.n) if other != vertex],
                    "no_dominating_vertex",
                )
        if minimum_size >= 3:
            # Every edge misses some vertex, hence no dominating edge.
            for u, v in itertools.combinations(range(self.n), 2):
                missed_witnesses = []
                for x in range(self.n):
                    if x in (u, v):
                        continue
                    witness = self.v.get("edge_miss", u, v, x)
                    missed_witnesses.append(witness)
                    self.add([-witness, -self.edge(u, x)], "no_dominating_edge")
                    self.add([-witness, -self.edge(v, x)], "no_dominating_edge")
                self.add([-self.edge(u, v), *missed_witnesses], "no_dominating_edge")

    def encode_domination(self) -> None:
        vertices = set(range(self.n))
        for chosen in self.secure_sets:
            outside = sorted(vertices - set(chosen))
            undominated_vars: list[int] = []
            for y in outside:
                q = self.q(chosen, y)
                undominated_vars.append(q)
                incident = [self.edge(y, z) for z in chosen]
                # q iff all five incident edges are absent.
                for edge in incident:
                    self.add([-q, -edge], "undominated_equivalence")
                self.add([q, *incident], "undominated_equivalence")

            d = self.dom(chosen)
            # d iff none of the outside vertices is undominated.
            for q in undominated_vars:
                self.add([-d, -q], "domination_equivalence")
            self.add([d, *undominated_vars], "domination_equivalence")

    def encode_no_secure_five_set(self) -> None:
        vertices = set(range(self.n))
        for chosen in self.secure_sets:
            outside = sorted(vertices - set(chosen))
            attacks = [self.attack(chosen, x) for x in outside]
            # If S dominates, choose an attack x defeating every defender.
            self.add([-self.dom(chosen), *attacks], "failed_secure_set")
            chosen_set = set(chosen)
            for x, attack in zip(outside, attacks, strict=True):
                for defender in chosen:
                    swapped = tuple(sorted((chosen_set - {defender}) | {x}))
                    # attack -> (defender not adjacent to x OR swap fails).
                    self.add(
                        [-attack, -self.edge(defender, x), -self.dom(swapped)],
                        "failed_defense",
                    )

    def encode_outside_type_order(self) -> None:
        """Sort outside vertices by their 4-bit neighborhood in the fixed IS.

        This is lossless: vertices 4,...,n-1 have no distinguished labels and
        may always be relabeled into nondecreasing type order.
        """
        for vertex in range(self.alpha_value, self.n):
            self.add(
                [self.edge(i, vertex) for i in range(self.alpha_value)],
                "outside_nonempty_type",
            )
        for left in range(self.alpha_value, self.n - 1):
            right = left + 1
            for left_mask in range(1, 1 << self.alpha_value):
                for right_mask in range(1, left_mask):
                    clause: list[int] = []
                    for bit in range(self.alpha_value):
                        left_edge = self.edge(bit, left)
                        right_edge = self.edge(bit, right)
                        clause.append(-left_edge if left_mask & (1 << bit) else left_edge)
                        clause.append(-right_edge if right_mask & (1 << bit) else right_edge)
                    self.add(clause, "outside_type_order")

    def build(
        self,
        type_order: bool = True,
        minimal_reductions: bool = False,
        dominating_clique: bool = False,
        minimum_dominating_clique_size: int = 1,
    ) -> None:
        self.encode_alpha_four()
        if type_order:
            self.encode_outside_type_order()
        self.encode_p5_free()
        self.encode_connectivity()
        if minimal_reductions:
            self.encode_connected_after_deletion()
            self.encode_complement_connectivity()
            self.encode_true_twin_free()
        self.encode_domination()
        self.encode_no_secure_five_set()
        if dominating_clique:
            self.encode_dominating_clique(minimum_size=minimum_dominating_clique_size)

    def graph_from_model(self, model: list[int]) -> list[tuple[int, int]]:
        truth = set(value for value in model if value > 0)
        return [
            (a, b)
            for a, b in itertools.combinations(range(self.n), 2)
            if self.edge(a, b) in truth
        ]


def encode_graph6(n: int, edges: list[tuple[int, int]]) -> str:
    if not (0 <= n <= 62):
        raise ValueError("only compact graph6 orders are supported")
    edge_set = {tuple(sorted(edge)) for edge in edges}
    bits = [
        1 if (i, j) in edge_set else 0
        for j in range(1, n)
        for i in range(j)
    ]
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(n + 63) + "".join(payload)


def solve(args: argparse.Namespace) -> dict:
    started = time.time()
    secure_size = args.secure_size if args.secure_size is not None else args.alpha + 1
    encoder = Encoder(args.n, alpha_value=args.alpha, secure_size=secure_size)
    encoder.build(
        type_order=not args.no_type_order,
        minimal_reductions=args.minimal_reductions,
        dominating_clique=args.dominating_clique,
        minimum_dominating_clique_size=args.min_dominating_clique_size,
    )
    encoded_seconds = time.time() - started

    if args.dimacs:
        Path(args.dimacs).parent.mkdir(parents=True, exist_ok=True)
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

    result = {
        "order": args.n,
        "solver": args.solver,
        "status": "SAT" if status is True else "UNSAT" if status is False else "UNKNOWN",
        "variables": encoder.v.next_id - 1,
        "clauses": len(encoder.cnf.clauses),
        "clause_families": encoder.counts,
        "encoding_seconds": encoded_seconds,
        "solver_seconds": time.time() - solver_started,
        "solver_stats": stats,
        "proof_trace": None,
        "constraints": {
            "connected": True,
            "induced_P5_free": True,
            "alpha_exactly": args.alpha,
            "no_secure_set_of_size": secure_size,
            "outside_type_order_symmetry_break": not args.no_type_order,
            "minimal_counterexample_reductions": args.minimal_reductions,
            "has_dominating_clique": args.dominating_clique,
            "minimum_dominating_clique_size": (
                args.min_dominating_clique_size if args.dominating_clique else None
            ),
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
    parser.add_argument("--alpha", type=int, default=4)
    parser.add_argument("--secure-size", type=int, default=None)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--timeout", type=float, default=None)
    parser.add_argument("--dimacs", default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--no-type-order", action="store_true")
    parser.add_argument(
        "--minimal-reductions",
        action="store_true",
        help="add 2-connectivity, co-connectivity, and true-twin-free constraints",
    )
    parser.add_argument("--dominating-clique", action="store_true")
    parser.add_argument("--min-dominating-clique-size", type=int, default=1)
    args = parser.parse_args()
    result = solve(args)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
