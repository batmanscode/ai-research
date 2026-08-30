#!/usr/bin/env python3
"""Exact Atlas audit for the dominating-P3 equality construction.

The theorem audited here is the following constructive equality lemma.
Let D={a,b,c} induce and dominate a P3 in an induced-P5-free graph G, and
assume alpha(G-D)=alpha(G)=q>=3.  Among the maximum independent sets I of
G-D, choose one of minimum D-weight

    w_D(I) = sum(|N_G(u) intersect D| for u in I).

Choose ANY pair x,y in I maximizing their total D-degree, put
X=I-{x,y}, and S=D union X.  Then S is secure dominating.

This program exhausts every relevant graph in the NetworkX Graph Atlas,
every dominating induced P3, every minimum-weight maximum independent set,
and every maximum-sum pair.  Security is tested directly from its definition;
the proof's witness argument is not used by the checker.

Output is deterministic JSON followed by a one-line PASS/FAIL verdict.
Requires NetworkX >= 3.0.  It performs no network access.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from itertools import combinations
from typing import Iterable, Iterator

import networkx as nx


def is_independent(graph: nx.Graph, vertices: Iterable[int]) -> bool:
    vertices = tuple(vertices)
    return all(not graph.has_edge(u, v) for u, v in combinations(vertices, 2))


def maximum_independent_sets(graph: nx.Graph) -> tuple[int, list[frozenset[int]]]:
    vertices = tuple(graph.nodes())
    for size in range(len(vertices), -1, -1):
        found = [
            frozenset(chosen)
            for chosen in combinations(vertices, size)
            if is_independent(graph, chosen)
        ]
        if found:
            return size, found
    raise AssertionError("the empty set should always be independent")


def dominates(graph: nx.Graph, guards: Iterable[int]) -> bool:
    guards = frozenset(guards)
    return all(
        vertex in guards
        or any(graph.has_edge(vertex, guard) for guard in guards)
        for vertex in graph.nodes()
    )


def is_secure_dominating(graph: nx.Graph, guards: Iterable[int]) -> bool:
    guards = frozenset(guards)
    if not dominates(graph, guards):
        return False
    for attack in set(graph.nodes()) - guards:
        defended = any(
            graph.has_edge(attack, guard)
            and dominates(graph, (guards - {guard}) | {attack})
            for guard in guards
        )
        if not defended:
            return False
    return True


def is_induced_p5_free(graph: nx.Graph) -> bool:
    for vertices in combinations(graph.nodes(), 5):
        induced = graph.subgraph(vertices)
        if (
            induced.number_of_edges() == 4
            and nx.is_connected(induced)
            and sorted(dict(induced.degree()).values()) == [1, 1, 2, 2, 2]
        ):
            return False
    return True


def dominating_induced_p3s(graph: nx.Graph) -> Iterator[tuple[int, int, int]]:
    """Yield each three-set once, ordered endpoint-middle-endpoint."""
    for chosen in combinations(graph.nodes(), 3):
        induced = graph.subgraph(chosen)
        degrees = dict(induced.degree())
        if sorted(degrees.values()) != [1, 1, 2]:
            continue
        middle = next(vertex for vertex in chosen if degrees[vertex] == 2)
        endpoints = sorted(vertex for vertex in chosen if degrees[vertex] == 1)
        path = (endpoints[0], middle, endpoints[1])
        if dominates(graph, path):
            yield path


def graph6(graph: nx.Graph) -> str:
    relabeled = nx.convert_node_labels_to_integers(graph, ordering="sorted")
    return nx.to_graph6_bytes(relabeled, header=False).decode("ascii").strip()


def audit_atlas() -> dict:
    totals = Counter()
    by_order: dict[int, Counter] = {}
    failures: list[dict] = []
    construction_records: list[str] = []

    for graph in nx.graph_atlas_g():
        order = graph.number_of_nodes()
        if order < 6 or not nx.is_connected(graph) or not is_induced_p5_free(graph):
            continue

        alpha_g, _ = maximum_independent_sets(graph)
        if alpha_g < 3:
            continue

        paths = tuple(dominating_induced_p3s(graph))
        if not paths:
            continue
        totals["applicable_graphs"] += 1
        row = by_order.setdefault(order, Counter())
        row["applicable_graphs"] += 1

        for path in paths:
            D = frozenset(path)
            outside = graph.subgraph(set(graph.nodes()) - D).copy()
            alpha_h, independent_sets = maximum_independent_sets(outside)
            if alpha_h != alpha_g:
                continue

            totals["equality_path_instances"] += 1
            row["equality_path_instances"] += 1

            d_degree = {
                vertex: sum(graph.has_edge(vertex, guard) for guard in D)
                for vertex in outside.nodes()
            }
            weights = {
                independent: sum(d_degree[vertex] for vertex in independent)
                for independent in independent_sets
            }
            minimum_weight = min(weights.values())
            selected_independent_sets = sorted(
                (independent for independent in independent_sets if weights[independent] == minimum_weight),
                key=lambda independent: tuple(sorted(independent)),
            )

            totals["minimum_weight_independent_sets"] += len(selected_independent_sets)
            row["minimum_weight_independent_sets"] += len(selected_independent_sets)

            for independent in selected_independent_sets:
                pairs = tuple(combinations(sorted(independent), 2))
                maximum_pair_weight = max(d_degree[x] + d_degree[y] for x, y in pairs)
                selected_pairs = tuple(
                    pair
                    for pair in pairs
                    if d_degree[pair[0]] + d_degree[pair[1]] == maximum_pair_weight
                )

                for pair in selected_pairs:
                    X = set(independent) - set(pair)
                    secure_set = D | X
                    totals["constructed_sets"] += 1
                    row["constructed_sets"] += 1
                    construction_records.append(
                        f"{graph6(graph)}|{path}|{tuple(sorted(independent))}|{pair}|{tuple(sorted(secure_set))}"
                    )
                    if not is_secure_dominating(graph, secure_set):
                        failure = {
                            "graph6": graph6(graph),
                            "order": order,
                            "alpha": alpha_g,
                            "path": path,
                            "independent_set": sorted(independent),
                            "omitted_pair": pair,
                            "constructed_set": sorted(secure_set),
                        }
                        failures.append(failure)
                        row["failures"] += 1
                        totals["failures"] += 1

    digest = hashlib.sha256("\n".join(construction_records).encode("utf-8")).hexdigest()
    return {
        "scope": "complete NetworkX Graph Atlas (all graphs through order 7)",
        "selection_rule": {
            "independent_set": "every maximum I in G-D of minimum total D-degree",
            "omitted_pair": "every pair in I of maximum total D-degree; no tie rule",
            "constructed_set": "D union (I minus omitted_pair)",
        },
        "totals": dict(sorted(totals.items())),
        "by_order": {
            str(order): dict(sorted(counts.items()))
            for order, counts in sorted(by_order.items())
        },
        "construction_record_sha256": digest,
        "failures": failures,
        "status": "PASS" if not failures else "FAIL",
    }


def audit_icosahedral_complement() -> dict:
    graph = nx.complement(nx.icosahedral_graph())
    alpha_g, _ = maximum_independent_sets(graph)
    equality_paths = 0
    constructed_sets = 0
    failures = 0

    for path in dominating_induced_p3s(graph):
        D = frozenset(path)
        outside = graph.subgraph(set(graph.nodes()) - D).copy()
        alpha_h, independent_sets = maximum_independent_sets(outside)
        if alpha_h != alpha_g:
            continue
        equality_paths += 1
        d_degree = {
            vertex: sum(graph.has_edge(vertex, guard) for guard in D)
            for vertex in outside.nodes()
        }
        weights = {
            independent: sum(d_degree[vertex] for vertex in independent)
            for independent in independent_sets
        }
        minimum_weight = min(weights.values())
        for independent in independent_sets:
            if weights[independent] != minimum_weight:
                continue
            pairs = tuple(combinations(sorted(independent), 2))
            maximum_pair_weight = max(d_degree[x] + d_degree[y] for x, y in pairs)
            for pair in pairs:
                if d_degree[pair[0]] + d_degree[pair[1]] != maximum_pair_weight:
                    continue
                constructed_sets += 1
                secure_set = D | (set(independent) - set(pair))
                failures += not is_secure_dominating(graph, secure_set)

    return {
        "graph": "complement of the icosahedral graph",
        "graph6": graph6(graph),
        "alpha": alpha_g,
        "gamma_s": next(
            size
            for size in range(graph.number_of_nodes() + 1)
            if any(
                is_secure_dominating(graph, chosen)
                for chosen in combinations(graph.nodes(), size)
            )
        ),
        "equality_path_instances": equality_paths,
        "constructed_sets": constructed_sets,
        "failures": failures,
        "status": "PASS" if failures == 0 else "FAIL",
    }


def main() -> int:
    atlas = audit_atlas()
    icosahedral = audit_icosahedral_complement()
    result = {
        "theorem": "dominating-P3 equality construction",
        "networkx_version": nx.__version__,
        "atlas": atlas,
        "icosahedral_complement": icosahedral,
        "status": (
            "PASS"
            if atlas["status"] == "PASS" and icosahedral["status"] == "PASS"
            else "FAIL"
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
