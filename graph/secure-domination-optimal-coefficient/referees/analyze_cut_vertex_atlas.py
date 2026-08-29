#!/usr/bin/env python3
"""Exact Graph Atlas audit of articulation reductions for secure domination."""

from __future__ import annotations

from itertools import combinations

import networkx as nx


def dominates(g: nx.Graph, s: set[int]) -> bool:
    return all(v in s or any(u in s for u in g[v]) for v in g)


def secure(g: nx.Graph, s: set[int]) -> bool:
    if not dominates(g, s):
        return False
    for v in set(g) - s:
        if not any(
            dominates(g, s - {u} | {v}) for u in s & set(g[v])
        ):
            return False
    return True


def minimum_secure_sets(g: nx.Graph) -> tuple[int, list[frozenset[int]]]:
    vs = list(g)
    for k in range(1, len(vs) + 1):
        ss = [frozenset(c) for c in combinations(vs, k) if secure(g, set(c))]
        if ss:
            return k, ss
    raise AssertionError("every vertex set is secure")


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
        if h.number_of_edges() == 4 and nx.is_connected(h) and max(dict(h.degree()).values()) == 2:
            return False
    return True


def rooted_sets(g: nx.Graph, x: int, require_minus_x_dominates: bool = False):
    """Minimum secure sets containing x, optionally stable after deleting x."""
    vs = list(g)
    out = []
    for k in range(1, len(vs) + 1):
        for c in combinations(vs, k):
            s = set(c)
            if x not in s or not secure(g, s):
                continue
            if require_minus_x_dominates and not dominates(g.subgraph(set(g) - {x}), s - {x}):
                continue
            out.append(frozenset(s))
        if out:
            return k, out
    return None


def atlas_candidates():
    for graph_id, g0 in enumerate(nx.graph_atlas_g()):
        if not g0 or not nx.is_connected(g0) or not is_p5_free(g0):
            continue
        g = nx.convert_node_labels_to_integers(g0)
        cuts = list(nx.articulation_points(g))
        if cuts:
            yield graph_id, g, cuts


def main() -> None:
    total = 0
    deep_fail = []
    alpha_plus_one_fail = []
    alpha_fail = []
    rooted_a_plus_one_fail = []
    rooted_a_fail = []
    stable_a_plus_one_fail = []
    stable_a_fail = []
    extension_fail = []
    max_is_some_fail = []
    max_is_all_fail = []
    records = []

    for graph_id, g, cuts in atlas_candidates():
        gs, all_sds = minimum_secure_sets(g)
        ag = alpha(g)
        total += 1
        if gs > ag + 1:
            alpha_plus_one_fail.append((graph_id, len(g), ag, gs))
        if gs > ag:
            alpha_fail.append((graph_id, len(g), ag, gs))

        for x in cuts:
            comps = [set(c) for c in nx.connected_components(nx.subgraph_view(g, filter_node=lambda v, x=x: v != x))]
            deep = [c for c in comps if any(not g.has_edge(x, v) for v in c)]
            if len(deep) > 1:
                deep_fail.append((graph_id, x, comps))

            for c in comps:
                h = g.subgraph(c | {x}).copy()
                a = alpha(g.subgraph(c))
                r = rooted_sets(h, x, False)
                sr = rooted_sets(h, x, True)
                if r is None or r[0] > a + 1:
                    rooted_a_plus_one_fail.append((graph_id, x, tuple(sorted(c)), a, r and r[0]))
                if r is None or r[0] > a:
                    rooted_a_fail.append((graph_id, x, tuple(sorted(c)), a, r and r[0]))
                if sr is None or sr[0] > a + 1:
                    stable_a_plus_one_fail.append((graph_id, x, tuple(sorted(c)), a, sr and sr[0]))
                if sr is None or sr[0] > a:
                    stable_a_fail.append((graph_id, x, tuple(sorted(c)), a, sr and sr[0]))

                mis = [
                    set(z)
                    for z in combinations(c, a)
                    if all(not g.has_edge(u, v) for u, v in combinations(z, 2))
                ]
                good_mis = [i for i in mis if secure(h, {x} | i)]
                if not good_mis:
                    max_is_some_fail.append((graph_id, x, tuple(sorted(c)), a))
                if len(good_mis) != len(mis):
                    max_is_all_fail.append(
                        (graph_id, x, tuple(sorted(c)), a, len(good_mis), len(mis))
                    )

            # Check the direct gluing construction: choose a stable rooted SDS
            # in a deep side, plus maximum independent sets of shallow sides.
            if deep:
                c0 = deep[0]
                h = g.subgraph(c0 | {x}).copy()
                sr = rooted_sets(h, x, True)
                if sr is not None:
                    shallow = [c for c in comps if c is not c0]
                    for base in sr[1]:
                        choices = [[]]
                        for c in shallow:
                            hc = g.subgraph(c)
                            ac = alpha(hc)
                            mis = [
                                frozenset(z)
                                for z in combinations(c, ac)
                                if all(not g.has_edge(u, v) for u, v in combinations(z, 2))
                            ]
                            choices = [old + [new] for old in choices for new in mis]
                        if choices:
                            s = set(base).union(*choices[0])
                            if not secure(g, s):
                                extension_fail.append((graph_id, x, tuple(sorted(s))))
                                break
            records.append((graph_id, len(g), x, len(comps), len(deep), ag, gs))

    print(f"articulation P5-free Atlas graphs: {total}")
    print(f"gamma_s > alpha+1: {len(alpha_plus_one_fail)} {alpha_plus_one_fail[:10]}")
    print(f"gamma_s > alpha: {len(alpha_fail)} {alpha_fail[:10]}")
    print(f"more than one deep component: {len(deep_fail)}")
    print(f"rooted secure > alpha(C)+1: {len(rooted_a_plus_one_fail)} {rooted_a_plus_one_fail[:10]}")
    print(f"rooted secure > alpha(C): {len(rooted_a_fail)} {rooted_a_fail[:10]}")
    print(f"stable rooted secure > alpha(C)+1: {len(stable_a_plus_one_fail)} {stable_a_plus_one_fail[:10]}")
    print(f"stable rooted secure > alpha(C): {len(stable_a_fail)} {stable_a_fail[:10]}")
    print(f"direct extension failures: {len(extension_fail)} {extension_fail[:10]}")
    print(f"no max IS I makes {{x}}+I secure: {len(max_is_some_fail)} {max_is_some_fail[:10]}")
    print(f"some max IS I makes {{x}}+I insecure: {len(max_is_all_fail)} {max_is_all_fail[:10]}")


if __name__ == "__main__":
    main()
