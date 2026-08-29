#!/usr/bin/env python3
"""Independent exhaustive verifier for the 12-vertex counterexample.

The core checks use only Python's standard library. NetworkX is optional and
is used only for graph recognition and automorphism-orbit compression.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

GRAPH6 = "KtiSYtlXqwmT"


def decode_graph6(text: str) -> tuple[int, list[set[int]]]:
    raw = text.strip().encode("ascii")
    if not raw or not (63 <= raw[0] <= 125):
        raise ValueError("Only the compact graph6 order encoding is supported")
    n = raw[0] - 63
    bits: list[int] = []
    for byte in raw[1:]:
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = n * (n - 1) // 2
    if len(bits) < needed:
        raise ValueError("Truncated graph6 string")
    adj = [set() for _ in range(n)]
    cursor = 0
    for j in range(1, n):
        for i in range(j):
            if bits[cursor]:
                adj[i].add(j)
                adj[j].add(i)
            cursor += 1
    return n, adj


def edges(adj: list[set[int]]) -> list[list[int]]:
    return [[u, v] for u in range(len(adj)) for v in sorted(adj[u]) if u < v]


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


def defense_map(adj: list[set[int]], chosen: frozenset[int]) -> dict[str, dict] | None:
    if not dominates(adj, chosen):
        return None
    result: dict[str, dict] = {}
    for attacked in range(len(adj)):
        if attacked in chosen:
            continue
        defenders = sorted(chosen & adj[attacked])
        valid = []
        for defender in defenders:
            swapped = frozenset((chosen - {defender}) | {attacked})
            if dominates(adj, swapped):
                valid.append({"defender": defender, "swapped_set": sorted(swapped)})
        if not valid:
            return None
        result[str(attacked)] = {"valid_defenses": valid}
    return result


def triple_failure(adj: list[set[int]], chosen: frozenset[int]) -> dict:
    if not dominates(adj, chosen):
        missed = [v for v in range(len(adj)) if v not in chosen and not (adj[v] & chosen)]
        return {"kind": "not_dominating", "missed_vertices": missed}
    for attacked in range(len(adj)):
        if attacked in chosen:
            continue
        failures = []
        for defender in sorted(chosen & adj[attacked]):
            swapped = frozenset((chosen - {defender}) | {attacked})
            missed = [v for v in range(len(adj)) if v not in swapped and not (adj[v] & swapped)]
            if not missed:
                break
            failures.append({"defender": defender, "missed_vertices": missed})
        else:
            return {
                "kind": "bad_attack",
                "attacked_vertex": attacked,
                "failed_defenses": failures,
            }
    raise AssertionError("Triple unexpectedly passed the secure-domination test")


def independence_number(adj: list[set[int]]) -> tuple[int, list[list[int]]]:
    maximum: list[list[int]] = []
    for size in range(1, len(adj) + 1):
        current = []
        for subset in itertools.combinations(range(len(adj)), size):
            if all(v not in adj[u] for u, v in itertools.combinations(subset, 2)):
                current.append(list(subset))
        if not current:
            return size - 1, maximum
        maximum = current
    return len(adj), maximum


def induced_p5_count(adj: list[set[int]]) -> int:
    total = 0
    for subset in itertools.combinations(range(len(adj)), 5):
        chosen = set(subset)
        degrees = [len(adj[v] & chosen) for v in subset]
        edge_count = sum(degrees) // 2
        if edge_count != 4 or sorted(degrees) != [1, 1, 2, 2, 2]:
            continue
        seen = {subset[0]}
        frontier = [subset[0]]
        while frontier:
            u = frontier.pop()
            for v in adj[u] & chosen:
                if v not in seen:
                    seen.add(v)
                    frontier.append(v)
        total += len(seen) == 5
    return total


def isomorphisms(source: list[set[int]], target: list[set[int]]):
    """Yield all adjacency-preserving bijections from source to target."""
    n = len(source)
    if n != len(target) or sorted(map(len, source)) != sorted(map(len, target)):
        return
    mapping: dict[int, int] = {}
    used: set[int] = set()

    def search():
        if len(mapping) == n:
            yield dict(mapping)
            return
        remaining = [u for u in range(n) if u not in mapping]
        u = max(remaining, key=lambda x: (sum(v in mapping for v in source[x]), len(source[x])))
        candidates = [v for v in range(n) if v not in used and len(target[v]) == len(source[u])]
        for v in candidates:
            if any(((other in source[u]) != (mapping[other] in target[v])) for other in mapping):
                continue
            mapping[u] = v
            used.add(v)
            yield from search()
            used.remove(v)
            del mapping[u]

    yield from search()


def canonical_icosahedron() -> list[set[int]]:
    phi = (1 + 5 ** 0.5) / 2
    coordinates = []
    for a in (-1.0, 1.0):
        for b in (-phi, phi):
            coordinates.extend([(0.0, a, b), (a, b, 0.0), (b, 0.0, a)])
    adj = [set() for _ in coordinates]
    for i, j in itertools.combinations(range(len(coordinates)), 2):
        distance_sq = sum((coordinates[i][k] - coordinates[j][k]) ** 2 for k in range(3))
        if abs(distance_sq - 4.0) < 1e-8:
            adj[i].add(j)
            adj[j].add(i)
    assert sorted(map(len, adj)) == [5] * 12
    return adj


def symmetry_audit(adj: list[set[int]], triples: list[frozenset[int]]) -> dict:
    automorphisms = list(isomorphisms(adj, adj))
    unseen = set(triples)
    orbits = []
    while unseen:
        representative = min(unseen, key=lambda x: tuple(sorted(x)))
        orbit = {
            frozenset(mapping[v] for v in representative)
            for mapping in automorphisms
        }
        unseen -= orbit
        orbits.append({
            "representative": sorted(representative),
            "size": len(orbit),
            "failure": triple_failure(adj, representative),
        })
    complement = [set(range(len(adj))) - {u} - adj[u] for u in range(len(adj))]
    recognized = next(isomorphisms(complement, canonical_icosahedron()), None) is not None
    return {
        "recognized_as_complement_icosahedron": recognized,
        "automorphism_group_order": len(automorphisms),
        "triple_orbits": sorted(orbits, key=lambda item: item["representative"]),
    }


def verify() -> dict:
    n, adj = decode_graph6(GRAPH6)
    edge_list = edges(adj)
    assert n == 12
    assert len(edge_list) == 36
    assert sorted(map(len, adj)) == [6] * 12
    assert connected(adj)

    alpha, independent_sets = independence_number(adj)
    p5_count = induced_p5_count(adj)
    assert alpha == 3
    assert p5_count == 0

    triples = [frozenset(s) for s in itertools.combinations(range(n), 3)]
    triple_certificates = {
        ",".join(map(str, sorted(chosen))): triple_failure(adj, chosen)
        for chosen in triples
    }
    failure_counts = {
        kind: sum(cert["kind"] == kind for cert in triple_certificates.values())
        for kind in ("not_dominating", "bad_attack")
    }
    assert failure_counts == {"not_dominating": 120, "bad_attack": 100}

    four_sets = [frozenset(s) for s in itertools.combinations(range(n), 4)]
    secure_four_sets = []
    four_defenses = {}
    for chosen in four_sets:
        mapping = defense_map(adj, chosen)
        if mapping is not None:
            secure_four_sets.append(sorted(chosen))
            four_defenses[tuple(sorted(chosen))] = mapping
    assert len(secure_four_sets) == 435
    example = [0, 1, 2, 3]
    assert example in secure_four_sets

    dominating_edges = [edge for edge in edge_list if dominates(adj, frozenset(edge))]
    assert dominating_edges == [[0, 1], [2, 9], [3, 7], [4, 10], [5, 8], [6, 11]]

    symmetry = symmetry_audit(adj, triples)
    result = {
        "name": "complement of the icosahedral graph",
        "graph6": GRAPH6,
        "order": n,
        "size": len(edge_list),
        "vertices": list(range(n)),
        "edges": edge_list,
        "degree_sequence": sorted((len(neighbors) for neighbors in adj), reverse=True),
        "connected": True,
        "independence_number": alpha,
        "maximum_independent_sets": independent_sets,
        "induced_p5_count": p5_count,
        "five_subsets_checked": 792,
        "secure_triple_count": 0,
        "triple_failure_counts": failure_counts,
        "triple_certificates": triple_certificates,
        "secure_four_set_count": len(secure_four_sets),
        "example_secure_four_set": example,
        "example_defense_map": four_defenses[tuple(example)],
        "secure_domination_number": 4,
        "dominating_edges": dominating_edges,
        **symmetry,
        "conclusion": "connected and induced-P5-free, with gamma_s=4>3=alpha",
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/counterexample_certificate.json"))
    args = parser.parse_args()
    result = verify()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "graph6": result["graph6"],
        "order": result["order"],
        "size": result["size"],
        "alpha": result["independence_number"],
        "induced_p5_count": result["induced_p5_count"],
        "secure_triple_count": result["secure_triple_count"],
        "secure_four_set_count": result["secure_four_set_count"],
        "gamma_s": result["secure_domination_number"],
        "recognized": result["recognized_as_complement_icosahedron"],
        "automorphisms": result["automorphism_group_order"],
    }, indent=2))


if __name__ == "__main__":
    main()
