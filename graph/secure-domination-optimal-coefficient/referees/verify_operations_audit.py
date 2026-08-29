#!/usr/bin/env python3
"""Independent small-instance checks for the graph-operation referee report."""

from __future__ import annotations

from itertools import combinations, product

import networkx as nx


def dominates(g: nx.Graph, s: set[int]) -> bool:
    return all(v in s or any(u in s for u in g[v]) for v in g)


def secure(g: nx.Graph, s: set[int]) -> bool:
    if not dominates(g, s):
        return False
    for x in set(g) - s:
        if not any(dominates(g, s - {d} | {x}) for d in s & set(g[x])):
            return False
    return True


def gamma_s(g: nx.Graph, cap: int | None = None) -> int | None:
    vertices = tuple(g)
    upper = len(vertices) if cap is None else min(cap, len(vertices))
    for k in range(1, upper + 1):
        if any(secure(g, set(c)) for c in combinations(vertices, k)):
            return k
    return None


def alpha(g: nx.Graph) -> int:
    vertices = tuple(g)
    for k in range(len(vertices), -1, -1):
        for c in combinations(vertices, k):
            if all(not g.has_edge(u, v) for u, v in combinations(c, 2)):
                return k
    raise AssertionError


def p5_free(g: nx.Graph) -> bool:
    for c in combinations(g, 5):
        h = g.subgraph(c)
        if h.number_of_edges() == 4 and nx.is_connected(h) and sorted(dict(h.degree()).values()) == [1, 1, 2, 2, 2]:
            return False
    return True


def one_hub(mask_a: int, mask_c: int) -> nx.Graph:
    g = nx.disjoint_union(nx.cycle_graph(5), nx.cycle_graph(5))
    g.add_node(10)
    for i in range(5):
        if mask_a >> i & 1:
            g.add_edge(10, i)
        if mask_c >> i & 1:
            g.add_edge(10, 5 + i)
    return g


def dihedral_images(mask: int) -> tuple[int, ...]:
    images = []
    for reverse in (False, True):
        for shift in range(5):
            image = 0
            for i in range(5):
                j = (-i if reverse else i) + shift
                image |= ((mask >> i) & 1) << (j % 5)
            images.append(image)
    return tuple(images)


def pair_orbit_key(a: int, c: int) -> tuple[int, int]:
    images = []
    for aa in dihedral_images(a):
        for cc in dihedral_images(c):
            images.append((aa, cc))
            images.append((cc, aa))
    return min(images)


def hub_census() -> dict:
    labeled = []
    for a in range(1, 32):
        for c in range(1, 32):
            g = one_hub(a, c)
            if p5_free(g):
                labeled.append((a, c, alpha(g), gamma_s(g)))
    orbits = {pair_orbit_key(a, c) for a, c, _, _ in labeled}
    return {
        "labeled_p5_free": len(labeled),
        "orbit_count": len(orbits),
        "parameter_rows": sorted({(a, gs) for _, _, a, gs in labeled}),
    }


def atlas_dominating_c5() -> dict:
    cases = failures = 0
    for g in nx.graph_atlas_g():
        if len(g) < 5 or not nx.is_connected(g) or not p5_free(g):
            continue
        for c in combinations(g, 5):
            h = g.subgraph(c)
            if h.number_of_edges() != 5 or sorted(dict(h.degree()).values()) != [2] * 5:
                continue
            cset = set(c)
            if dominates(g, cset):
                cases += 1
                failures += not secure(g, cset)
    return {"cases": cases, "failures": failures}


def atlas_dominating_p3() -> dict:
    cases = failures = 0
    first_failure = None
    for g in nx.graph_atlas_g():
        if len(g) < 3 or not nx.is_connected(g) or not p5_free(g):
            continue
        amax = alpha(g)
        max_sets = [set(c) for c in combinations(g, amax)
                    if all(not g.has_edge(u, v) for u, v in combinations(c, 2))]
        for a, b, c in product(g, repeat=3):
            if len({a, b, c}) < 3 or not g.has_edge(a, b) or not g.has_edge(b, c) or g.has_edge(a, c):
                continue
            if not dominates(g, {a, b, c}):
                continue
            for iset in max_sets:
                if a in iset and c in iset:
                    cases += 1
                    d = iset | {b}
                    if not secure(g, d):
                        failures += 1
                        if first_failure is None:
                            first_failure = (nx.to_graph6_bytes(g, header=False).strip().decode(), (a, b, c), sorted(iset))
    return {"ordered_cases": cases, "failures": failures, "first_failure": first_failure}


def clone_vertex(g: nx.Graph, v: int, clique: bool) -> nx.Graph:
    h = nx.convert_node_labels_to_integers(g)
    v = list(g).index(v)
    w = len(h)
    h.add_node(w)
    for u in list(h[v]):
        h.add_edge(w, u)
    if clique:
        h.add_edge(v, w)
    return h


def atlas_single_clone_bounds() -> dict:
    true_bad = []
    false_bad = []
    checked = 0
    for g in nx.graph_atlas_g():
        if not 1 <= len(g) <= 6:
            continue
        sg = gamma_s(g)
        for v in g:
            checked += 1
            ht = clone_vertex(g, v, True)
            hf = clone_vertex(g, v, False)
            if gamma_s(ht) > sg:
                true_bad.append((nx.to_graph6_bytes(g, header=False).strip().decode(), v, sg, gamma_s(ht)))
            if gamma_s(hf) > sg + 1:
                false_bad.append((nx.to_graph6_bytes(g, header=False).strip().decode(), v, sg, gamma_s(hf)))
    return {"vertex_expansions": checked, "true_bad": true_bad, "false_bad": false_bad}


def universal_hub_cycles(max_k: int = 4) -> list[tuple[int, int, int]]:
    rows = []
    for k in range(2, max_k + 1):
        g = nx.disjoint_union_all([nx.cycle_graph(5) for _ in range(k)])
        z = len(g)
        g.add_node(z)
        g.add_edges_from((z, v) for v in range(z))
        rows.append((k, alpha(g), gamma_s(g, cap=2 * k)))
    return rows


def main() -> None:
    print("one_hub", hub_census())
    print("dominating_c5", atlas_dominating_c5())
    print("dominating_p3", atlas_dominating_p3())
    print("clone_bounds", atlas_single_clone_bounds())
    print("universal_hub_cycles", universal_hub_cycles())


if __name__ == "__main__":
    main()
