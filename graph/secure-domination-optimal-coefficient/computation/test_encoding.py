#!/usr/bin/env python3
"""Cross-check the SAT encoding against direct predicates on fixed graphs."""

from __future__ import annotations

import itertools
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "vendor"))

from pysat.solvers import Solver  # type: ignore

from search_extremal import Encoder
from verify_candidate import alpha, connected, decode_graph6, defense_map, induced_p5s


def direct(adj: list[set[int]], alpha_value: int, secure_size: int) -> bool:
    if not connected(adj) or induced_p5s(adj) or alpha(adj)[0] != alpha_value:
        return False
    return not any(
        defense_map(adj, frozenset(chosen)) is not None
        for chosen in itertools.combinations(range(len(adj)), secure_size)
    )


def run(n: int, alpha_value: int, secure_size: int, samples: int, seed: int) -> None:
    encoder = Encoder(n, alpha_value=alpha_value, secure_size=secure_size)
    # Type sorting is not a property of a fixed arbitrary labeling, so disable
    # that lossless graph-level symmetry break for edge-assignment tests.
    encoder.build(type_order=False)
    pairs = list(itertools.combinations(range(n), 2))
    fixed_absent = set(itertools.combinations(range(alpha_value), 2))
    free_pairs = [pair for pair in pairs if pair not in fixed_absent]
    rng = random.Random(seed)
    checked = 0
    qualifying = 0
    with Solver(name="cadical195", bootstrap_with=encoder.cnf.clauses) as solver:
        for index in range(samples):
            if index == 0:
                mask = 0
            elif index == 1:
                mask = (1 << len(free_pairs)) - 1
            else:
                mask = rng.getrandbits(len(free_pairs))
            edges = {
                pair for bit, pair in enumerate(free_pairs) if mask & (1 << bit)
            }
            adj = [set() for _ in range(n)]
            for a, b in edges:
                adj[a].add(b)
                adj[b].add(a)
            expected = direct(adj, alpha_value, secure_size)
            assumptions = [
                encoder.edge(a, b) if (a, b) in edges else -encoder.edge(a, b)
                for a, b in pairs
            ]
            actual = solver.solve(assumptions=assumptions)
            if actual != expected:
                raise AssertionError(
                    f"mismatch at sample {index}: expected {expected}, SAT said {actual}, edges={sorted(edges)}"
                )
            checked += 1
            qualifying += expected
    print({
        "n": n,
        "alpha": alpha_value,
        "secure_size": secure_size,
        "samples": checked,
        "qualifying": qualifying,
        "seed": seed,
        "status": "PASS",
    })


def run_positive_fixture(type_order: bool) -> None:
    """Require the known alpha-three obstruction to satisfy the SAT formula."""
    graph6 = "KtiSYtlXqwmT"
    n, original = decode_graph6(graph6)
    alpha_value, maximum_sets = alpha(original)
    independent = tuple(maximum_sets[0])

    # Put a maximum independent set first, then sort the remaining vertices by
    # the exact type order used by the optional symmetry break.
    outsiders = [v for v in range(n) if v not in independent]
    outsiders.sort(
        key=lambda v: sum(1 << bit for bit, u in enumerate(independent) if v in original[u])
    )
    order = list(independent) + outsiders
    old_to_new = {old: new for new, old in enumerate(order)}
    edges = {
        tuple(sorted((old_to_new[u], old_to_new[v])))
        for u in range(n)
        for v in original[u]
        if u < v
    }

    encoder = Encoder(n, alpha_value=alpha_value, secure_size=alpha_value)
    encoder.build(type_order=type_order)
    assumptions = [
        encoder.edge(u, v) if (u, v) in edges else -encoder.edge(u, v)
        for u, v in itertools.combinations(range(n), 2)
    ]
    with Solver(name="cadical195", bootstrap_with=encoder.cnf.clauses) as solver:
        if not solver.solve(assumptions=assumptions):
            raise AssertionError(
                f"positive fixture rejected (type_order={type_order})"
            )
    print({
        "graph6": graph6,
        "alpha": alpha_value,
        "secure_size_excluded": alpha_value,
        "type_order": type_order,
        "status": "PASS",
    })


if __name__ == "__main__":
    run(n=7, alpha_value=4, secure_size=5, samples=10_000, seed=20260829)
    run(n=8, alpha_value=5, secure_size=6, samples=10_000, seed=20260830)
    run_positive_fixture(type_order=False)
    run_positive_fixture(type_order=True)
