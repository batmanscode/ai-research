#!/usr/bin/env python3
"""Seeded random stress test of the dominating-P3 equality construction."""

from __future__ import annotations

import argparse
from itertools import combinations
import random

import networkx as nx


def independent(g, chosen):
    return all(not g.has_edge(u, v) for u, v in combinations(chosen, 2))


def maximum_independent_sets(g, vertices):
    ordered = tuple(sorted(vertices))
    for size in range(len(ordered), -1, -1):
        found = [set(s) for s in combinations(ordered, size) if independent(g, s)]
        if found:
            return size, found
    raise AssertionError


def dominates(g, chosen):
    return all(v in chosen or bool(set(g[v]) & chosen) for v in g)


def secure(g, chosen):
    if not dominates(g, chosen):
        return False
    return all(
        any(dominates(g, chosen - {d} | {v}) for d in set(g[v]) & chosen)
        for v in set(g) - chosen
    )


def p5_free(g):
    for chosen in combinations(g, 5):
        h = g.subgraph(chosen)
        if (
            h.number_of_edges() == 4
            and nx.is_connected(h)
            and sorted(dict(h.degree()).values()) == [1, 1, 2, 2, 2]
        ):
            return False
    return True


def random_instance(n, rng):
    g = nx.Graph()
    g.add_nodes_from(range(n))
    g.add_edges_from([(0, 1), (1, 2)])
    for v in range(3, n):
        mask = rng.randrange(1, 8)
        for d in range(3):
            if mask & (1 << d):
                g.add_edge(d, v)
    density = rng.choice((0.15, 0.3, 0.5, 0.7, 0.85))
    for u, v in combinations(range(3, n), 2):
        if rng.random() < density:
            g.add_edge(u, v)
    return g


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=100000)
    parser.add_argument("--max-n", type=int, default=12)
    parser.add_argument("--seed", type=int, default=20260829)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    accepted = equality = constructions = 0
    for trial in range(args.trials):
        n = rng.randint(6, args.max_n)
        g = random_instance(n, rng)
        if not p5_free(g):
            continue
        accepted += 1
        alpha_g, _ = maximum_independent_sets(g, g.nodes())
        h_vertices = set(range(3, n))
        alpha_h, sets_h = maximum_independent_sets(g, h_vertices)
        if alpha_g < 3 or alpha_h != alpha_g:
            continue
        equality += 1
        degree = {v: len(set(g[v]) & {0, 1, 2}) for v in h_vertices}
        weight = lambda chosen: sum(degree[v] for v in chosen)
        min_weight = min(map(weight, sets_h))
        for independent_set in sets_h:
            if weight(independent_set) != min_weight:
                continue
            pairs = list(combinations(sorted(independent_set), 2))
            top = max(degree[x] + degree[y] for x, y in pairs)
            for x, y in pairs:
                if degree[x] + degree[y] != top:
                    continue
                constructions += 1
                chosen = {0, 1, 2} | (independent_set - {x, y})
                if not secure(g, chosen):
                    print("FAIL", trial, nx.to_graph6_bytes(g, header=False).decode().strip())
                    print(sorted(g.edges()), sorted(independent_set), (x, y), sorted(chosen))
                    raise SystemExit(1)
    print(
        f"PASS trials={args.trials} accepted_p5free={accepted} "
        f"equality_instances={equality} constructions={constructions} "
        f"max_n={args.max_n} seed={args.seed}"
    )


if __name__ == "__main__":
    main()
