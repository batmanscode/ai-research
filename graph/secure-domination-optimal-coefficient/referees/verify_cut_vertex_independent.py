#!/usr/bin/env python3
"""Independent exhaustive audit of the rooted cut-vertex construction.

This deliberately does not import the supplied verifier.  It checks every
rooted Graph Atlas instance through seven vertices satisfying the exact local
hypothesis (C=H-x connected, x has a neighbour and non-neighbour in C, and
no induced P4 starts at x).  For each instance it enumerates *all* choices
allowed by the proof: maximum independent sets, clique representatives,
complete anchors, designated components, omitted representatives, and
maximal independent boundary completions.

The local audit is stronger than needed: it does not assume H is P5-free.
"""

from __future__ import annotations

from itertools import combinations, product

import networkx as nx


def dominates(g: nx.Graph, s: frozenset[int] | set[int]) -> bool:
    return all(v in s or any(u in s for u in g[v]) for v in g)


def secure(g: nx.Graph, s: set[int]) -> bool:
    if not dominates(g, s):
        return False
    for v in set(g) - s:
        if not any(dominates(g, s - {u} | {v}) for u in s & set(g[v])):
            return False
    return True


def independent(g: nx.Graph, s) -> bool:
    return all(not g.has_edge(u, v) for u, v in combinations(s, 2))


def all_maximum_independent(g: nx.Graph, vertices) -> list[frozenset[int]]:
    vertices = tuple(sorted(vertices))
    for k in range(len(vertices), -1, -1):
        ans = [frozenset(s) for s in combinations(vertices, k) if independent(g, s)]
        if ans:
            return ans
    raise AssertionError


def all_maximal_independent(g: nx.Graph, vertices) -> list[frozenset[int]]:
    vertices = tuple(sorted(vertices))
    out = []
    for k in range(len(vertices) + 1):
        for s0 in combinations(vertices, k):
            s = frozenset(s0)
            if independent(g, s) and all(
                v in s or any(g.has_edge(v, u) for u in s) for v in vertices
            ):
                out.append(s)
    return out


def rooted_p4(g: nx.Graph, x: int, c: set[int]) -> bool:
    for a, b, d in product(c, repeat=3):
        if len({a, b, d}) < 3:
            continue
        if (
            g.has_edge(x, a)
            and g.has_edge(a, b)
            and g.has_edge(b, d)
            and not g.has_edge(x, b)
            and not g.has_edge(x, d)
            and not g.has_edge(a, d)
        ):
            return True
    return False


def choice_products(items):
    return product(*items) if items else [()]


def audit_root(g: nx.Graph, x: int) -> int:
    """Return number of allowed proof constructions checked."""
    c = set(g) - {x}
    l = c & set(g[x])
    r = c - l
    parts = [set(q) for q in nx.connected_components(g.subgraph(r))]

    # Check the structural module and attachment assertions directly.
    for q in parts:
        complete = []
        for a in l:
            n = sum(g.has_edge(a, v) for v in q)
            assert n in (0, len(q)), ("nonuniform boundary", x, a, q)
            if n == len(q):
                complete.append(a)
        assert complete, ("unanchored residual component", x, q)

    mis_options = [all_maximum_independent(g, q) for q in parts]
    clique_indices = [i for i, opts in enumerate(mis_options) if len(next(iter(opts))) == 1]
    nonclique_indices = [i for i in range(len(parts)) if i not in clique_indices]
    representative_options = [tuple(sorted(parts[i])) for i in clique_indices]
    anchor_options = [
        tuple(a for a in sorted(l) if all(g.has_edge(a, v) for v in parts[i]))
        for i in nonclique_indices
    ]

    alpha_c = len(next(iter(all_maximum_independent(g, c))))
    checked = 0
    for mis_tuple in choice_products(mis_options):
        mis = dict(enumerate(mis_tuple))
        for reps in choice_products(representative_options):
            clique_selected = set(reps)
            for anchor_tuple in choice_products(anchor_options):
                anchor_of = dict(zip(nonclique_indices, anchor_tuple))
                groups: dict[int, list[int]] = {}
                for i, a in anchor_of.items():
                    groups.setdefault(a, []).append(i)
                group_items = sorted(groups.items())
                designated_options = [tuple(indices) for _, indices in group_items]
                for designated_tuple in choice_products(designated_options):
                    designated = {
                        a: i for (a, _), i in zip(group_items, designated_tuple)
                    }
                    omitted_options = [tuple(sorted(mis[i])) for i in designated.values()]
                    for omitted_tuple in choice_products(omitted_options):
                        omitted = {
                            i: v for i, v in zip(designated.values(), omitted_tuple)
                        }
                        d0 = set(clique_selected) | set(groups)
                        for i in nonclique_indices:
                            d0 |= set(mis[i]) - ({omitted[i]} if i in omitted else set())
                        u = {
                            v for v in l
                            if v not in d0 and not (set(g[v]) & d0)
                        }
                        assert all(not g.has_edge(v, z) for v in u for z in r)
                        for j in all_maximal_independent(g, u):
                            d = d0 | set(j)
                            s = d | {x}
                            assert len(d) <= alpha_c, (
                                "budget failure", x, sorted(d), alpha_c
                            )
                            assert dominates(g.subgraph(c), d), (
                                "D does not dominate C", x, sorted(d)
                            )
                            assert secure(g, s), (
                                "rooted set insecure", x, sorted(s)
                            )
                            checked += 1
    return checked


def main() -> None:
    rooted_instances = 0
    constructions = 0
    largest = 0
    for atlas_id, g0 in enumerate(nx.graph_atlas_g()):
        if not g0:
            continue
        g = nx.convert_node_labels_to_integers(g0)
        for x in g:
            c = set(g) - {x}
            if not c or not nx.is_connected(g.subgraph(c)):
                continue
            l = c & set(g[x])
            r = c - l
            if not l or not r or rooted_p4(g, x, c):
                continue
            rooted_instances += 1
            largest = max(largest, len(g))
            try:
                constructions += audit_root(g, x)
            except AssertionError as exc:
                print("FAIL", atlas_id, nx.to_graph6_bytes(g, header=False).decode().strip(), x, exc)
                raise
    print(
        f"PASS rooted_instances={rooted_instances} "
        f"allowed_constructions={constructions} largest_order={largest}"
    )


if __name__ == "__main__":
    main()
