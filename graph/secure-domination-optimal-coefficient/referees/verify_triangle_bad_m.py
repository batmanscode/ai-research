#!/usr/bin/env python3
"""Independent randomized/targeted audit of the bad-M completion lemma.

This is deliberately self-contained: it does not import the author's checker.
The theorem under audit uses only the dominating-triangle partition and
pairwise anticompleteness of the three private regions, so most random trials
do not impose P5-freeness.  A separate crafted tight example is P5-free.
"""

from __future__ import annotations

import itertools
import json
import random
from functools import lru_cache


def add_edge(adj: list[int], u: int, v: int) -> None:
    adj[u] |= 1 << v
    adj[v] |= 1 << u


def independent(adj: list[int], vertices: tuple[int, ...] | list[int]) -> bool:
    return all(not (adj[u] >> v) & 1 for u, v in itertools.combinations(vertices, 2))


def maximum_independent_sets(adj: list[int], vertices: list[int]) -> list[set[int]]:
    for size in range(len(vertices), 0, -1):
        answer = [set(s) for s in itertools.combinations(vertices, size) if independent(adj, s)]
        if answer:
            return answer
    return [set()]


def alpha(adj: list[int]) -> int:
    @lru_cache(None)
    def solve(mask: int) -> int:
        if not mask:
            return 0
        bit = mask & -mask
        v = bit.bit_length() - 1
        without = mask ^ bit
        return max(solve(without), 1 + solve(without & ~adj[v]))

    return solve((1 << len(adj)) - 1)


def dominates(adj: list[int], selected: int, target: int | None = None) -> bool:
    if target is None:
        target = (1 << len(adj)) - 1
    covered = selected
    guards = selected
    while guards:
        bit = guards & -guards
        guards ^= bit
        covered |= adj[bit.bit_length() - 1]
    return target & ~covered == 0


def secure(adj: list[int], selected: int) -> bool:
    all_vertices = (1 << len(adj)) - 1
    if not dominates(adj, selected):
        return False
    attacks = all_vertices & ~selected
    while attacks:
        attack_bit = attacks & -attacks
        attacks ^= attack_bit
        attack = attack_bit.bit_length() - 1
        candidate_guards = selected & adj[attack]
        defended = False
        while candidate_guards:
            guard_bit = candidate_guards & -candidate_guards
            candidate_guards ^= guard_bit
            if dominates(adj, (selected ^ guard_bit) | attack_bit):
                defended = True
                break
        if not defended:
            return False
    return True


def minimum_dominating_set(adj: list[int], target_vertices: set[int]) -> set[int]:
    if not target_vertices:
        return set()
    target_mask = sum(1 << v for v in target_vertices)
    ordered = sorted(target_vertices)
    for size in range(1, len(ordered) + 1):
        for chosen in itertools.combinations(ordered, size):
            chosen_mask = sum(1 << v for v in chosen)
            if dominates(adj, chosen_mask, target_mask):
                return set(chosen)
    raise AssertionError("the whole induced target must dominate itself")


def is_p5_free(adj: list[int]) -> bool:
    for chosen in itertools.combinations(range(len(adj)), 5):
        chosen_mask = sum(1 << v for v in chosen)
        degrees = sorted((adj[v] & chosen_mask).bit_count() for v in chosen)
        edges = sum((adj[v] & chosen_mask).bit_count() for v in chosen) // 2
        if edges == 4 and degrees == [1, 1, 2, 2, 2]:
            return False
    return True


def audit_choice(
    adj: list[int],
    private: dict[int, list[int]],
    multi: set[int],
    picked: dict[int, set[int]],
    omitted: dict[int, int],
    *,
    p5_free: bool | None = None,
) -> dict[str, object]:
    hubs = {0, 1, 2}
    x_set = set().union(*(picked[k] - {omitted[k]} for k in hubs))
    x_mask = sum(1 << x for x in x_set)
    closed_x = x_mask
    for x in x_set:
        closed_x |= adj[x]
    residual = {
        k: {u for u in private[k] if not (closed_x >> u) & 1}
        for k in hubs
    }
    bad = {
        v
        for v in multi
        if not (adj[v] & x_mask)
        and all(
            any(not ((adj[v] >> u) & 1) for u in residual[k])
            for k in hubs
            if (adj[v] >> k) & 1
        )
    }
    y_set = minimum_dominating_set(adj, bad)
    selected = hubs | x_set | y_set
    selected_mask = sum(1 << v for v in selected)
    p = sum(len(picked[k]) for k in hubs)
    graph_alpha = alpha(adj)
    tight_ok = True
    if p == graph_alpha:
        for v in bad:
            hub_type = {k for k in hubs if (adj[v] >> k) & 1}
            if len(hub_type) != 2:
                tight_ok = False
                break
            missed_hub = next(iter(hubs - hub_type))
            if any(not ((adj[v] >> u) & 1) for u in residual[missed_hub]):
                tight_ok = False
                break
    bad_is_clique = independent(adj, list(bad)) if len(bad) <= 1 else all(
        (adj[u] >> v) & 1 for u, v in itertools.combinations(bad, 2)
    )
    corollary_ok = (not bad_is_clique) or len(selected) <= graph_alpha + 1
    tight_clique_ok = not (p == graph_alpha and p5_free) or bad_is_clique
    return {
        "secure": secure(adj, selected_mask),
        "p": p,
        "alpha": graph_alpha,
        "tight": p == graph_alpha,
        "tight_ok": tight_ok,
        "bad": sorted(bad),
        "bad_is_empty_or_clique": bad_is_clique,
        "corollary_ok": corollary_ok,
        "tight_clique_ok": tight_clique_ok,
        "residual": {str(k): sorted(vs) for k, vs in residual.items()},
        "X": sorted(x_set),
        "Y": sorted(y_set),
    }


def random_instance(rng: random.Random) -> tuple[list[int], dict[int, list[int]], set[int]]:
    private_sizes = [rng.randint(1, 3) for _ in range(3)]
    private: dict[int, list[int]] = {}
    next_vertex = 3
    for hub, size in enumerate(private_sizes):
        private[hub] = list(range(next_vertex, next_vertex + size))
        next_vertex += size
    multi = set(range(next_vertex, next_vertex + rng.randint(0, 4)))
    adj = [0] * (next_vertex + len(multi))
    for u, v in itertools.combinations(range(3), 2):
        add_edge(adj, u, v)
    for hub, vertices in private.items():
        for v in vertices:
            add_edge(adj, hub, v)
        for u, v in itertools.combinations(vertices, 2):
            if rng.random() < 0.45:
                add_edge(adj, u, v)
    hub_types = [(0, 1), (0, 2), (1, 2), (0, 1, 2)]
    for v in multi:
        for hub in rng.choice(hub_types):
            add_edge(adj, v, hub)
        for private_vertex in range(3, next_vertex):
            if rng.random() < 0.38:
                add_edge(adj, v, private_vertex)
    for u, v in itertools.combinations(multi, 2):
        if rng.random() < 0.45:
            add_edge(adj, u, v)
    return adj, private, multi


def crafted_tight_instance(
    kind: str = "one",
) -> tuple[list[int], dict[int, list[int]], set[int]]:
    private = {0: [3, 4], 1: [5, 6], 2: [7, 8]}
    multi = {9} if kind == "one" else {9, 10}
    adj = [0] * (9 + len(multi))
    for u, v in itertools.combinations(range(3), 2):
        add_edge(adj, u, v)
    for hub, vertices in private.items():
        for v in vertices:
            add_edge(adj, hub, v)
    edges = [(9, 0), (9, 1), (9, 7)]
    if kind == "same_type_pair":
        edges += [(10, 0), (10, 1), (10, 7), (9, 10)]
    elif kind == "different_type_pair":
        edges += [(10, 0), (10, 2), (10, 6), (9, 10)]
    elif kind != "one":
        raise ValueError(kind)
    for edge in edges:
        add_edge(adj, *edge)
    return adj, private, multi


def main() -> None:
    rng = random.Random(20260830)
    counts = {
        "random_graphs": 0,
        "residual_choices": 0,
        "secure_constructions": 0,
        "empty_or_clique_corollary_checks": 0,
        "tight_choices": 0,
        "tight_bad_vertex_checks": 0,
        "p5free_tight_choices": 0,
        "p5free_tight_bad_pairs": 0,
        "non_p5free_tight_nonclique_choices": 0,
        "failures": [],
    }
    for _ in range(2500):
        adj, private, multi = random_instance(rng)
        graph_is_p5_free = is_p5_free(adj)
        max_sets = {k: maximum_independent_sets(adj, private[k]) for k in range(3)}
        choices = list(itertools.product(*(max_sets[k] for k in range(3))))
        rng.shuffle(choices)
        for tuple_choice in choices[:3]:
            picked = dict(enumerate(tuple_choice))
            omissions = list(itertools.product(*(sorted(picked[k]) for k in range(3))))
            rng.shuffle(omissions)
            for omission_tuple in omissions[:3]:
                omitted = dict(enumerate(omission_tuple))
                result = audit_choice(
                    adj,
                    private,
                    multi,
                    picked,
                    omitted,
                    p5_free=graph_is_p5_free,
                )
                counts["residual_choices"] += 1
                counts["secure_constructions"] += int(bool(result["secure"]))
                counts["empty_or_clique_corollary_checks"] += int(
                    bool(result["bad_is_empty_or_clique"])
                )
                counts["tight_choices"] += int(bool(result["tight"]))
                if result["tight"]:
                    counts["tight_bad_vertex_checks"] += len(result["bad"])
                if result["tight"] and graph_is_p5_free:
                    counts["p5free_tight_choices"] += 1
                    counts["p5free_tight_bad_pairs"] += len(result["bad"]) * (len(result["bad"]) - 1) // 2
                if (
                    result["tight"]
                    and not graph_is_p5_free
                    and not result["bad_is_empty_or_clique"]
                ):
                    counts["non_p5free_tight_nonclique_choices"] += 1
                if (
                    not result["secure"]
                    or not result["tight_ok"]
                    or not result["corollary_ok"]
                    or not result["tight_clique_ok"]
                ):
                    counts["failures"].append(result)
                    break
        counts["random_graphs"] += 1

    picked = {0: {3, 4}, 1: {5, 6}, 2: {7, 8}}
    omitted = {0: 4, 1: 6, 2: 7}
    crafted_results = {}
    for kind in ("one", "same_type_pair", "different_type_pair"):
        adj, private, multi = crafted_tight_instance(kind)
        graph_is_p5_free = is_p5_free(adj)
        crafted = audit_choice(
            adj, private, multi, picked, omitted, p5_free=graph_is_p5_free
        )
        crafted["p5_free"] = graph_is_p5_free
        crafted_results[kind] = crafted
    counts["crafted_tight_examples"] = crafted_results
    counts["status"] = "PASS" if (
        not counts["failures"]
        and all(
            item["secure"] and item["tight_ok"] and item["tight_clique_ok"]
            for item in crafted_results.values()
        )
    ) else "FAIL"
    print(json.dumps(counts, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

