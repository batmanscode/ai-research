#!/usr/bin/env python3
"""Independent, standard-library-only audit of the failed M-packing lemma.

The graph is given only by its graph6 string.  All graph predicates below are
implemented locally so this check does not import any of the research code.
"""

from __future__ import annotations

import itertools
import json


GRAPH6 = "I{OeEAg}?"
K = (0, 1, 2)
P = (3, 4, 5)
M = (6, 7, 8, 9)


def decode_graph6(s: str) -> list[int]:
    """Decode a short graph6 string into integer adjacency bit rows."""
    n = ord(s[0]) - 63
    bits: list[int] = []
    for ch in s[1:]:
        value = ord(ch) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adj = [0] * n
    cursor = 0
    # graph6 stores (0,1),(0,2),(1,2),(0,3),... in this order.
    for v in range(1, n):
        for u in range(v):
            if bits[cursor]:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
            cursor += 1
    return adj


def mask(vertices: tuple[int, ...] | list[int]) -> int:
    result = 0
    for v in vertices:
        result |= 1 << v
    return result


def vertices_of(s: int) -> list[int]:
    return [v for v in range(N) if s >> v & 1]


def dominates(s: int, universe: int = None) -> bool:
    if universe is None:
        universe = FULL
    covered = s
    for v in vertices_of(s):
        covered |= ADJ[v]
    return covered & universe == universe


def independent(s: int) -> bool:
    for v in vertices_of(s):
        if ADJ[v] & s & ~(1 << v):
            return False
    return True


def secure(s: int, universe: int = None) -> bool:
    """Secure domination in the induced subgraph on ``universe``."""
    if universe is None:
        universe = FULL
    if not dominates(s, universe):
        return False
    for attacked in vertices_of(universe & ~s):
        defenders = ADJ[attacked] & s
        defended = False
        for defender in vertices_of(defenders):
            swapped = (s & ~(1 << defender)) | (1 << attacked)
            if dominates(swapped, universe):
                defended = True
                break
        if not defended:
            return False
    return True


def all_subsets(universe: int, size: int | None = None):
    vs = vertices_of(universe)
    sizes = (size,) if size is not None else range(len(vs) + 1)
    for k in sizes:
        for c in itertools.combinations(vs, k):
            yield mask(c)


def minimum_number(predicate, universe: int) -> tuple[int, list[int]]:
    for k in range(len(vertices_of(universe)) + 1):
        witnesses = [s for s in all_subsets(universe, k) if predicate(s)]
        if witnesses:
            return k, witnesses
    raise AssertionError("no witness")


def connected() -> bool:
    seen = 1
    frontier = 1
    while frontier:
        bit = frontier & -frontier
        frontier ^= bit
        v = bit.bit_length() - 1
        new = ADJ[v] & ~seen
        seen |= new
        frontier |= new
    return seen == FULL


def is_induced_p5(chosen: tuple[int, ...]) -> bool:
    s = mask(chosen)
    degrees = sorted((ADJ[v] & s).bit_count() for v in chosen)
    if degrees != [1, 1, 2, 2, 2]:
        return False
    seen = 1 << chosen[0]
    frontier = seen
    while frontier:
        bit = frontier & -frontier
        frontier ^= bit
        v = bit.bit_length() - 1
        new = ADJ[v] & s & ~seen
        seen |= new
        frontier |= new
    return seen == s


def p5_free() -> bool:
    return not any(is_induced_p5(c) for c in itertools.combinations(range(N), 5))


def domination_number(universe: int) -> tuple[int, list[int]]:
    return minimum_number(lambda s: dominates(s, universe), universe)


def secure_domination_number(universe: int) -> tuple[int, list[int]]:
    return minimum_number(lambda s: secure(s, universe), universe)


def has_dominating_pair() -> bool:
    return any(dominates(mask(c)) for c in itertools.combinations(range(N), 2))


def has_dominating_induced_p3() -> bool:
    for c in itertools.combinations(range(N), 3):
        s = mask(c)
        # Exactly two edges on three vertices is an induced P3.
        edges = sum(bool(ADJ[u] >> v & 1) for u, v in itertools.combinations(c, 2))
        if edges == 2 and dominates(s):
            return True
    return False


def packing_value() -> tuple[int, list[dict]]:
    """Compute max |R| + alpha(M - N(R)), including all R subset P."""
    best = -1
    witnesses: list[dict] = []
    for r in range(len(P) + 1):
        for chosen in itertools.combinations(P, r):
            rmask = mask(chosen)
            compatible = mask(tuple(v for v in M if not (ADJ[v] & rmask)))
            alpha_m = max(
                (len(vertices_of(s)) for s in all_subsets(compatible) if independent(s)),
                default=0,
            )
            i_witnesses = [
                s for s in all_subsets(compatible)
                if independent(s) and len(vertices_of(s)) == alpha_m
            ]
            value = r + alpha_m
            rows = [
                {"private": list(chosen), "multi": vertices_of(s)}
                for s in i_witnesses
            ]
            if value > best:
                best, witnesses = value, rows
            elif value == best:
                witnesses.extend(rows)
    return best, witnesses


ADJ = decode_graph6(GRAPH6)
N = len(ADJ)
FULL = (1 << N) - 1
K_MASK = mask(K)
P_MASK = mask(P)
M_MASK = mask(M)
H_MASK = P_MASK | M_MASK


def main() -> None:
    alpha, alpha_witnesses = max(
        (len(vertices_of(s)), s) for s in all_subsets(FULL) if independent(s)
    ), []
    alpha_value = alpha[0]
    alpha_witnesses = [
        vertices_of(s)
        for s in all_subsets(FULL)
        if independent(s) and len(vertices_of(s)) == alpha_value
    ]
    gamma_m, gamma_m_witnesses = domination_number(M_MASK)
    gamma_hs, gamma_hs_witnesses = secure_domination_number(H_MASK)
    gamma_s, gamma_s_witnesses = secure_domination_number(FULL)
    packing, packing_witnesses = packing_value()

    # Verify that the named partition really is the K-neighborhood partition.
    k_neighborhoods = {
        v: [k for k in K if ADJ[v] >> k & 1] for v in range(3, N)
    }
    private = {k: [v for v in range(3, N) if k_neighborhoods[v] == [k]] for k in K}
    multi = [v for v in range(3, N) if len(k_neighborhoods[v]) >= 2]

    # The one-hub lift check: adding any one K vertex to a minimum H-SDS
    # gives a secure dominating set of G (size 1 + gamma_s(H) = 6).
    chosen_h = gamma_hs_witnesses[0]
    lifts = {
        str(h): secure(chosen_h | (1 << h)) for h in K
    }

    result = {
        "graph6": GRAPH6,
        "n": N,
        "edges": [
            [u, v] for u, v in itertools.combinations(range(N), 2)
            if ADJ[u] >> v & 1
        ],
        "K": list(K),
        "P": list(P),
        "M": list(M),
        "K_neighborhoods_outside": k_neighborhoods,
        "private_partition": private,
        "multi_vertices": multi,
        "connected": connected(),
        "induced_P5_free": p5_free(),
        "K_is_dominating_triangle": (
            all(ADJ[u] >> v & 1 for u, v in itertools.combinations(K, 2))
            and dominates(K_MASK)
        ),
        "private_regions_pairwise_anticomplete": all(
            not (ADJ[u] >> v & 1) for u, v in itertools.combinations(P, 2)
        ),
        "alpha": alpha_value,
        "alpha_witness": alpha_witnesses[0],
        "gamma_M": gamma_m,
        "gamma_M_witnesses": [vertices_of(s) for s in gamma_m_witnesses],
        "gamma_s_G": gamma_s,
        "gamma_s_G_witnesses": [vertices_of(s) for s in gamma_s_witnesses],
        "secure_sets_by_size_G": {
            str(k): sum(secure(s) for s in all_subsets(FULL, k))
            for k in range(N + 1)
        },
        "gamma_s_G_minus_K": gamma_hs,
        "gamma_s_G_minus_K_witnesses": [
            vertices_of(s) for s in gamma_hs_witnesses
        ],
        "one_hub_lift_bound": 1 + gamma_hs,
        "one_hub_lift_secure_for_hubs": lifts,
        "has_dominating_pair": has_dominating_pair(),
        "has_dominating_induced_P3": has_dominating_induced_p3(),
        "local_completion_bound": len(P) + gamma_m,
        "packing_B": packing,
        "packing_target_gamma_M_plus_2": gamma_m + 2,
        "packing_witnesses": packing_witnesses,
    }

    assert result["connected"]
    assert result["induced_P5_free"]
    assert result["K_is_dominating_triangle"]
    assert result["private_regions_pairwise_anticomplete"]
    assert result["private_partition"] == {0: [3], 1: [4], 2: [5]}
    assert result["multi_vertices"] == list(M)
    assert alpha_value == 5
    assert gamma_m == 4
    assert gamma_s == 4
    assert gamma_hs == 5
    assert not result["has_dominating_pair"]
    assert not result["has_dominating_induced_P3"]
    assert packing == 5 < gamma_m + 2
    assert result["local_completion_bound"] == 7
    assert result["one_hub_lift_bound"] == 6
    assert all(lifts.values())
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

