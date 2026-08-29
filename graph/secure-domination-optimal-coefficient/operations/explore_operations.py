#!/usr/bin/env python3
"""Exact small-graph experiments for secure domination under compositions."""

from __future__ import annotations

from itertools import combinations
from itertools import product

import networkx as nx


def dominates(g: nx.Graph, s: set[int]) -> bool:
    return all(v in s or any(u in s for u in g[v]) for v in g)


def secure(g: nx.Graph, s: set[int]) -> bool:
    if not dominates(g, s):
        return False
    for v in set(g) - s:
        if not any(dominates(g, s - {u} | {v}) for u in s & set(g[v])):
            return False
    return True


def gamma_s(g: nx.Graph) -> int:
    vertices = list(g)
    for k in range(1, len(vertices) + 1):
        if any(secure(g, set(c)) for c in combinations(vertices, k)):
            return k
    raise AssertionError


def gamma_s_bit(g: nx.Graph, limit: int | None = None) -> tuple[int, tuple[int, ...]]:
    g = nx.convert_node_labels_to_integers(g)
    n = len(g)
    full = (1 << n) - 1
    closed = [1 << v | sum(1 << u for u in g[v]) for v in range(n)]

    def dominated(mask: int) -> bool:
        covered = 0
        while mask:
            bit = mask & -mask
            covered |= closed[bit.bit_length() - 1]
            mask ^= bit
        return covered == full

    def sec(mask: int) -> bool:
        if not dominated(mask):
            return False
        outside = full ^ mask
        while outside:
            bitv = outside & -outside
            v = bitv.bit_length() - 1
            defenders = mask & closed[v] & ~(1 << v)
            ok = False
            while defenders:
                bitu = defenders & -defenders
                if dominated((mask ^ bitu) | bitv):
                    ok = True
                    break
                defenders ^= bitu
            if not ok:
                return False
            outside ^= bitv
        return True

    vertices = range(n)
    upper = n if limit is None else min(limit, n)
    for k in range(1, upper + 1):
        for c in combinations(vertices, k):
            mask = sum(1 << v for v in c)
            if sec(mask):
                return k, c
    raise ValueError(f"no secure set through {upper}")


def alpha(g: nx.Graph) -> int:
    vertices = list(g)
    for k in range(len(vertices), 0, -1):
        for c in combinations(vertices, k):
            if all(not g.has_edge(u, v) for u, v in combinations(c, 2)):
                return k
    return 0


def gamma(g: nx.Graph) -> int:
    vertices = list(g)
    for k in range(1, len(vertices) + 1):
        if any(dominates(g, set(c)) for c in combinations(vertices, k)):
            return k
    raise AssertionError


def join_graph(g: nx.Graph, h: nx.Graph) -> nx.Graph:
    j = nx.disjoint_union(g, h)
    n = len(g)
    for u in range(n):
        for v in range(n, n + len(h)):
            j.add_edge(u, v)
    return j


def protection_completion_number(g: nx.Graph) -> int:
    vertices = list(g)
    for k in range(1, len(vertices) + 1):
        for c in combinations(vertices, k):
            a = set(c)
            if all(
                (set(g[x]) & a) or dominates(g, a | {x})
                for x in set(vertices) - a
            ):
                return k
    raise AssertionError


def join_formula(g: nx.Graph, h: nx.Graph) -> int:
    pg = protection_completion_number(g)
    ph = protection_completion_number(h)
    mixed = min(
        a + b
        for a in range(1, len(g) + 1)
        for b in range(1, len(h) + 1)
        if (b >= 2 or a >= pg) and (a >= 2 or b >= ph)
    )
    candidates = [mixed]
    sg, sh = gamma_s(g), gamma_s(h)
    if len(g) >= 2:
        candidates.append(max(2, sg))
    if len(h) >= 2:
        candidates.append(max(2, sh))
    if all(g.degree(v) == len(g) - 1 for v in g) and all(h.degree(v) == len(h) - 1 for v in h):
        candidates.append(1)
    return min(candidates)


def lex(g: nx.Graph, h: nx.Graph) -> nx.Graph:
    return nx.convert_node_labels_to_integers(nx.lexicographic_product(g, h))


def secure_false_blowup_counts(g: nx.Graph, t: int, f: tuple[int, ...]) -> bool:
    vertices = list(g)

    def dom(a: tuple[int, ...]) -> bool:
        return all(a[v] == t or any(a[u] > 0 for u in g[v]) for v in vertices)

    if not dom(f):
        return False
    for v in vertices:
        if f[v] == t:
            continue
        defended = False
        for u in g[v]:
            if f[u] == 0:
                continue
            moved = list(f)
            moved[u] -= 1
            moved[v] += 1
            if dom(tuple(moved)):
                defended = True
                break
        if not defended:
            return False
    return True


def bounded_compositions(weight: int, length: int, cap: int):
    current = [0] * length

    def rec(index: int, remaining: int):
        if index == length:
            if remaining == 0:
                yield tuple(current)
            return
        for value in range(min(cap, remaining) + 1):
            current[index] = value
            yield from rec(index + 1, remaining - value)

    yield from rec(0, weight)


def gamma_s_false_blowup(g: nx.Graph, t: int) -> tuple[int, tuple[int, ...]]:
    n = len(g)
    for weight in range(1, t * n + 1):
        for f in bounded_compositions(weight, n, t):
            if secure_false_blowup_counts(g, t, f):
                return weight, f
    raise AssertionError


def weak_roman(g: nx.Graph) -> tuple[int, tuple[int, ...]]:
    vertices = list(g)

    def support_dominates(f: tuple[int, ...]) -> bool:
        support = {v for v in vertices if f[v] > 0}
        return dominates(g, support)

    for weight in range(1, 2 * len(g) + 1):
        for f in product(range(3), repeat=len(g)):
            if sum(f) != weight or not support_dominates(f):
                continue
            valid = True
            for v in vertices:
                if f[v] > 0:
                    continue
                if not any(
                    f[u] > 0
                    and support_dominates(
                        tuple(
                            f[x] - (x == u) + (x == v)
                            for x in vertices
                        )
                    )
                    for u in g[v]
                ):
                    valid = False
                    break
            if valid:
                return weight, f
    raise AssertionError


def gamma_w(g: nx.Graph, w: tuple[int, int, int]) -> tuple[int, tuple[int, ...]]:
    vertices = list(g)
    for weight in range(1, 2 * len(g) + 1):
        for f in bounded_compositions(weight, len(g), 2):
            if all(sum(f[u] for u in g[v]) >= w[f[v]] for v in vertices):
                return weight, f
    raise AssertionError


def induced_p5_free(g: nx.Graph) -> bool:
    for vertices in combinations(g.nodes(), 5):
        h = g.subgraph(vertices)
        if h.number_of_edges() == 4 and nx.is_connected(h) and sorted(dict(h.degree()).values()) == [1, 1, 2, 2, 2]:
            return False
    return True


def main() -> None:
    atlas = [g for g in nx.graph_atlas_g() if 1 <= len(g) <= 5]
    for code in (b"CF", b"Bo", b"CB", b"Dhc", b"DBC", b"D?{"):
        g = nx.from_graph6_bytes(code)
        print("identify", code, len(g), sorted(g.edges()), "a", alpha(g), "gam", gamma(g), "gs", gamma_s(g))
    print("true-twin blowup tests")
    failures = []
    for g in atlas:
        for t in (2, 3):
            b = lex(g, nx.complete_graph(t))
            if len(b) > 15:
                continue
            gs, bs = gamma_s(g), gamma_s(b)
            if gs != bs:
                failures.append((nx.to_graph6_bytes(g, header=False).strip(), t, gs, bs))
    print("failures", failures[:30], "count", len(failures))

    print("false-twin blowup tests")
    failures = []
    ratio_increases = []
    for g in atlas:
        for t in (2, 3):
            b = lex(g, nx.empty_graph(t))
            if len(b) > 15:
                continue
            gs, bs = gamma_s(g), gamma_s(b)
            if bs != t * gs:
                failures.append((nx.to_graph6_bytes(g, header=False).strip(), t, gs, bs, alpha(g), alpha(b)))
            if bs * alpha(g) > gs * alpha(b):
                ratio_increases.append((nx.to_graph6_bytes(g, header=False).strip(), t, gs, bs, alpha(g), alpha(b)))
    print("not multiplicative", failures[:50], "count", len(failures))
    print("ratio increases", ratio_increases, "count", len(ratio_increases))

    print("join formula samples")
    stats = {}
    for g in atlas:
        for h in atlas:
            if len(g) + len(h) > 10:
                continue
            j = join_graph(g, h)
            key = (gamma_s(g), gamma_s(h), gamma(g), gamma(h))
            stats.setdefault(key, set()).add(gamma_s(j))
    bad = [(k, sorted(v)) for k, v in stats.items() if len(v) > 1]
    print("same coarse parameters, varying join gamma_s", bad[:30], "count", len(bad))
    formula_failures = []
    for g in atlas:
        for h in atlas:
            if len(g) + len(h) <= 10 and gamma_s(join_graph(g, h)) != join_formula(g, h):
                formula_failures.append((nx.to_graph6_bytes(g, header=False).strip(), nx.to_graph6_bytes(h, header=False).strip()))
    print("join exact formula failures", formula_failures)


if __name__ == "__main__":
    main()
