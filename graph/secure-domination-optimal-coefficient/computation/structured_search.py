#!/usr/bin/env python3
"""Search module substitutions for extremal secure-domination graphs.

The main family replaces vertices of the icosahedral complement by independent
sets of false twins.  Substitution preserves induced-P5-freeness because P5 is
prime.  Every reported hit is nevertheless checked directly.
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from search_extremal import encode_graph6
from verify_candidate import decode_graph6, induced_p5s, alpha as brute_alpha


ICOS_COMPLEMENT = "KtiSYtlXqwmT"


def independent_masks(adj: list[set[int]]) -> list[int]:
    n = len(adj)
    result = []
    for mask in range(1 << n):
        if all(not (mask >> u & 1 and mask >> v & 1) for u in range(n) for v in adj[u] if u < v):
            result.append(mask)
    return result


def weighted_alpha(weights: tuple[int, ...], independent: list[int]) -> int:
    return max(sum(weights[v] for v in range(len(weights)) if mask >> v & 1) for mask in independent)


def stable_blowup(adj: list[set[int]], weights: tuple[int, ...]) -> list[set[int]]:
    modules: list[list[int]] = []
    cursor = 0
    for weight in weights:
        modules.append(list(range(cursor, cursor + weight)))
        cursor += weight
    result = [set() for _ in range(cursor)]
    for u, v in itertools.combinations(range(len(adj)), 2):
        if v not in adj[u]:
            continue
        for a in modules[u]:
            for b in modules[v]:
                result[a].add(b)
                result[b].add(a)
    return result


def secure_sets_of_size(adj: list[set[int]], size: int, stop_after: int = 1) -> list[list[int]]:
    n = len(adj)
    universe = (1 << n) - 1
    closed = [(1 << v) | sum(1 << u for u in adj[v]) for v in range(n)]

    def coverage(chosen: tuple[int, ...]) -> int:
        value = 0
        for v in chosen:
            value |= closed[v]
        return value

    result = []
    for chosen in itertools.combinations(range(n), size):
        cov = coverage(chosen)
        if cov != universe:
            continue
        chosen_mask = sum(1 << v for v in chosen)
        secure = True
        for attacked in range(n):
            if chosen_mask >> attacked & 1:
                continue
            for defender in chosen:
                if attacked not in adj[defender]:
                    continue
                swapped = tuple(v for v in chosen if v != defender) + (attacked,)
                if coverage(swapped) == universe:
                    break
            else:
                secure = False
                break
        if secure:
            result.append(list(chosen))
            if len(result) >= stop_after:
                return result
    return result


def edge_list(adj: list[set[int]]) -> list[tuple[int, int]]:
    return [(u, v) for u in range(len(adj)) for v in sorted(adj[u]) if u < v]


def search_icos_false_twins(max_weight: int = 2) -> dict:
    _, base = decode_graph6(ICOS_COMPLEMENT)
    indep = independent_masks(base)
    counts = {"weight_vectors": 0, "alpha_four": 0, "no_secure_five": 0}
    best: dict | None = None
    gamma5_min_count = None
    gamma5_example = None

    for weights in itertools.product(range(1, max_weight + 1), repeat=len(base)):
        counts["weight_vectors"] += 1
        if weighted_alpha(weights, indep) != 4:
            continue
        counts["alpha_four"] += 1
        graph = stable_blowup(base, weights)
        secure_five = secure_sets_of_size(graph, 5, stop_after=1)
        if secure_five:
            if gamma5_min_count is None or sum(weights) < gamma5_min_count:
                gamma5_min_count = sum(weights)
                gamma5_example = {"weights": weights, "secure_five": secure_five[0]}
            continue
        counts["no_secure_five"] += 1
        secure_six = secure_sets_of_size(graph, 6, stop_after=1)
        candidate_edges = edge_list(graph)
        best = {
            "family": "independent-set blowup of complement of icosahedron",
            "base_graph6": ICOS_COMPLEMENT,
            "weights": list(weights),
            "order": len(graph),
            "graph6": encode_graph6(len(graph), candidate_edges),
            "edges": [list(e) for e in candidate_edges],
            "secure_six": secure_six[0] if secure_six else None,
            "brute_alpha": brute_alpha(graph)[0],
            "induced_p5_count": len(induced_p5s(graph)),
        }
        break

    return {
        "search": f"all false-twin weights in [1,{max_weight}]^12",
        "counts": counts,
        "first_extremal": best,
        "smallest_seen_with_secure_five": gamma5_example,
    }


def main() -> None:
    result = search_icos_false_twins(max_weight=2)
    output = HERE / "structured_icos_false_twins.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
