#!/usr/bin/env python3
"""Independent Graph Atlas audit of the dominating-clique residual criterion."""

from __future__ import annotations

import itertools
import json

import networkx as nx


def dominates(graph: nx.Graph, chosen: set[int]) -> bool:
    return all(
        vertex in chosen
        or any(graph.has_edge(vertex, guard) for guard in chosen)
        for vertex in graph
    )


def secure(graph: nx.Graph, chosen: set[int]) -> bool:
    if not dominates(graph, chosen):
        return False
    for attacked in set(graph) - chosen:
        if not any(
            graph.has_edge(attacked, defender)
            and dominates(graph, (chosen - {defender}) | {attacked})
            for defender in chosen
        ):
            return False
    return True


def residual_condition(graph: nx.Graph, clique: set[int], added: set[int]) -> bool:
    selected = clique | added
    for attacked in set(graph) - selected:
        if any(graph.has_edge(attacked, guard) for guard in added):
            continue
        defended = False
        for guard in clique:
            if not graph.has_edge(attacked, guard):
                continue
            private_region = {
                vertex
                for vertex in set(graph) - clique
                if {
                    member
                    for member in clique
                    if graph.has_edge(vertex, member)
                }
                == {guard}
            }
            residual = {
                vertex
                for vertex in private_region - added
                if not any(graph.has_edge(vertex, x) for x in added)
            }
            if all(
                vertex == attacked or graph.has_edge(attacked, vertex)
                for vertex in residual
            ):
                defended = True
                break
        if not defended:
            return False
    return True


def main() -> None:
    cases = 0
    for graph in nx.graph_atlas_g():
        if len(graph) < 2:
            continue
        vertices = set(graph)
        for size in range(2, len(graph) + 1):
            for chosen in itertools.combinations(graph, size):
                clique = set(chosen)
                if not all(
                    graph.has_edge(u, v)
                    for u, v in itertools.combinations(clique, 2)
                ) or not dominates(graph, clique):
                    continue
                outside = sorted(vertices - clique)
                for bits in range(1 << len(outside)):
                    added = {
                        outside[i]
                        for i in range(len(outside))
                        if bits >> i & 1
                    }
                    direct = secure(graph, clique | added)
                    reduced = residual_condition(graph, clique, added)
                    cases += 1
                    if direct != reduced:
                        raise AssertionError(
                            {
                                "graph6": nx.to_graph6_bytes(
                                    graph, header=False
                                ).decode().strip(),
                                "clique": sorted(clique),
                                "added": sorted(added),
                                "direct": direct,
                                "reduced": reduced,
                            }
                        )
    print(json.dumps({"cases": cases, "mismatches": 0, "status": "PASS"}))


if __name__ == "__main__":
    main()
