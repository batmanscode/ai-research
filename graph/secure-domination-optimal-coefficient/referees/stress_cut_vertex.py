#!/usr/bin/env python3
"""Random exact search for failures of the rooted articulation lemma."""

from __future__ import annotations

import argparse
from itertools import combinations
import random

import networkx as nx

from verify_cut_vertex import cut_construction


def dominates(g: nx.Graph, s: set[int], vertices=None) -> bool:
    vertices = set(g) if vertices is None else set(vertices)
    return all(v in s or bool(set(g[v]) & s) for v in vertices)


def secure(g: nx.Graph, s: set[int]) -> bool:
    if not dominates(g, s):
        return False
    return all(
        any(dominates(g, s - {u} | {v}) for u in set(g[v]) & s)
        for v in set(g) - s
    )


def alpha(g: nx.Graph) -> int:
    vs = list(g)
    for k in range(len(vs), -1, -1):
        if any(
            all(not g.has_edge(u, v) for u, v in combinations(c, 2))
            for c in combinations(vs, k)
        ):
            return k
    raise AssertionError


def is_p5_free(g: nx.Graph) -> bool:
    for c in combinations(g, 5):
        h = g.subgraph(c)
        if h.number_of_edges() == 4 and nx.is_connected(h) and sorted(dict(h.degree()).values()) == [1, 1, 2, 2, 2]:
            return False
    return True


def rooted_number(g: nx.Graph, x: int, cap: int) -> tuple[int, tuple[int, ...]] | None:
    c = set(g) - {x}
    for k in range(1, min(cap, len(g)) + 1):
        for z in combinations(g, k):
            s = set(z)
            if x in s and dominates(g.subgraph(c), s - {x}) and secure(g, s):
                return k, z
    return None


def random_root_module_graph(n: int, rng: random.Random) -> nx.Graph:
    """Generate H=C+x with no induced P4 having endpoint x.

    L2 components have uniform neighborhoods into L1, the exact rooted-P4-free
    decomposition.  We reject disconnected C later.
    """
    x = 0
    l1n = rng.randint(1, n - 2)
    l1 = list(range(1, 1 + l1n))
    l2 = list(range(1 + l1n, n))
    g = nx.Graph()
    g.add_nodes_from(range(n))
    g.add_edges_from((x, a) for a in l1)
    for u, v in combinations(l1, 2):
        if rng.random() < 0.5:
            g.add_edge(u, v)

    # Randomly partition L2, then make each part connected.
    parts: list[list[int]] = []
    for v in l2:
        if not parts or rng.random() < 0.4:
            parts.append([v])
        else:
            rng.choice(parts).append(v)
    for q in parts:
        for i in range(1, len(q)):
            g.add_edge(q[i], rng.choice(q[:i]))
        for u, v in combinations(q, 2):
            if not g.has_edge(u, v) and rng.random() < 0.35:
                g.add_edge(u, v)
        neighbors = [a for a in l1 if rng.random() < 0.5]
        if not neighbors:
            neighbors = [rng.choice(l1)]
        g.add_edges_from((a, v) for a in neighbors for v in q)
    return g


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=20000)
    parser.add_argument("--max-n", type=int, default=13)
    parser.add_argument("--seed", type=int, default=20260829)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    accepted = 0
    for trial in range(args.trials):
        n = rng.randint(4, args.max_n)
        h = random_root_module_graph(n, rng)
        c = set(h) - {0}
        if not nx.is_connected(h.subgraph(c)) or not is_p5_free(h):
            continue
        accepted += 1
        a = alpha(h.subgraph(c))
        rooted = rooted_number(h, 0, a + 1)
        if rooted is None:
            print("COUNTEREXAMPLE")
            print(f"trial={trial} n={n} alpha(C)={a}")
            print(nx.to_graph6_bytes(h, header=False).decode().strip())
            print(sorted(h.edges()))
            return
        whole = h.copy()
        shallow = len(whole)
        whole.add_edge(0, shallow)
        try:
            cut_construction(whole, 0)
        except AssertionError as error:
            print("CONSTRUCTION FAILURE")
            print(f"trial={trial} n={n + 1} alpha(C)={a} error={error}")
            print(nx.to_graph6_bytes(whole, header=False).decode().strip())
            print(sorted(whole.edges()))
            return
    print(f"PASS accepted={accepted} trials={args.trials} max_n={args.max_n} seed={args.seed}")


if __name__ == "__main__":
    main()
