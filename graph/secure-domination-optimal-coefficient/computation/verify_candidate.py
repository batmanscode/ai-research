#!/usr/bin/env python3
"""Plain-Python independent verifier for secure-domination candidates."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


def decode_graph6(text: str) -> tuple[int, list[set[int]]]:
    raw = text.strip().encode("ascii")
    if not raw or not (63 <= raw[0] <= 125):
        raise ValueError("compact graph6 encoding required")
    n = raw[0] - 63
    bits: list[int] = []
    for byte in raw[1:]:
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = n * (n - 1) // 2
    if len(bits) < needed:
        raise ValueError("truncated graph6")
    adj = [set() for _ in range(n)]
    cursor = 0
    for j in range(1, n):
        for i in range(j):
            if bits[cursor]:
                adj[i].add(j)
                adj[j].add(i)
            cursor += 1
    return n, adj


def connected(adj: list[set[int]]) -> bool:
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == len(adj)


def dominates(adj: list[set[int]], chosen: frozenset[int]) -> bool:
    return all(v in chosen or bool(adj[v] & chosen) for v in range(len(adj)))


def defense_map(adj: list[set[int]], chosen: frozenset[int]) -> dict[str, list[dict]] | None:
    if not dominates(adj, chosen):
        return None
    result: dict[str, list[dict]] = {}
    for attacked in range(len(adj)):
        if attacked in chosen:
            continue
        valid: list[dict] = []
        for defender in sorted(chosen & adj[attacked]):
            swapped = frozenset((chosen - {defender}) | {attacked})
            if dominates(adj, swapped):
                valid.append({"defender": defender, "swapped_set": sorted(swapped)})
        if not valid:
            return None
        result[str(attacked)] = valid
    return result


def secure_failure(adj: list[set[int]], chosen: frozenset[int]) -> dict:
    if not dominates(adj, chosen):
        return {
            "kind": "not_dominating",
            "missed": [v for v in range(len(adj)) if v not in chosen and not (adj[v] & chosen)],
        }
    for attacked in range(len(adj)):
        if attacked in chosen:
            continue
        failures = []
        for defender in sorted(chosen & adj[attacked]):
            swapped = frozenset((chosen - {defender}) | {attacked})
            missed = [v for v in range(len(adj)) if v not in swapped and not (adj[v] & swapped)]
            if not missed:
                break
            failures.append({"defender": defender, "missed": missed})
        else:
            return {"kind": "bad_attack", "attacked": attacked, "failures": failures}
    raise AssertionError("set is secure")


def alpha(adj: list[set[int]]) -> tuple[int, list[list[int]]]:
    last: list[list[int]] = []
    for size in range(1, len(adj) + 1):
        found = [
            list(chosen)
            for chosen in itertools.combinations(range(len(adj)), size)
            if all(v not in adj[u] for u, v in itertools.combinations(chosen, 2))
        ]
        if not found:
            return size - 1, last
        last = found
    return len(adj), last


def induced_p5s(adj: list[set[int]]) -> list[list[int]]:
    result = []
    for chosen in itertools.combinations(range(len(adj)), 5):
        subset = set(chosen)
        degrees = [len(adj[v] & subset) for v in chosen]
        if sorted(degrees) != [1, 1, 2, 2, 2]:
            continue
        seen = {chosen[0]}
        stack = [chosen[0]]
        while stack:
            u = stack.pop()
            for v in adj[u] & subset:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        if len(seen) == 5:
            result.append(list(chosen))
    return result


def verify(graph6: str, failure_size: int = 5) -> dict:
    n, adj = decode_graph6(graph6)
    edge_list = [[u, v] for u in range(n) for v in sorted(adj[u]) if u < v]
    independence, max_sets = alpha(adj)
    paths = induced_p5s(adj)

    first_secure: dict[int, list[int]] = {}
    failures: dict[str, dict] = {}
    gamma = None
    defense = None
    for size in range(1, n + 1):
        for chosen_tuple in itertools.combinations(range(n), size):
            chosen = frozenset(chosen_tuple)
            mapping = defense_map(adj, chosen)
            if mapping is not None:
                gamma = size
                first_secure[size] = list(chosen_tuple)
                defense = mapping
                break
            if size == failure_size:
                failures[",".join(map(str, chosen_tuple))] = secure_failure(adj, chosen)
        if gamma is not None:
            break

    return {
        "graph6": graph6,
        "order": n,
        "edges": edge_list,
        "degree_sequence": sorted((len(x) for x in adj), reverse=True),
        "connected": connected(adj),
        "alpha": independence,
        "maximum_independent_sets": max_sets,
        "induced_p5_count": len(paths),
        "induced_p5s": paths,
        "gamma_s": gamma,
        "example_secure_set": first_secure.get(gamma) if gamma is not None else None,
        "example_defense_map": defense,
        "target_failure_size": failure_size,
        "target_set_failure_count": len(failures),
        "target_set_failures": failures,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph6")
    parser.add_argument("--failure-size", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(args.graph6, failure_size=args.failure_size)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(json.dumps({key: result[key] for key in (
        "graph6", "order", "connected", "alpha", "induced_p5_count", "gamma_s",
        "target_failure_size", "target_set_failure_count",
    )}, indent=2))


if __name__ == "__main__":
    main()
