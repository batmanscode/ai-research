#!/usr/bin/env python3
"""Direct Graph-Atlas audit of the triangle private-cross-edge theorem.

This checker intentionally uses only the definitions of the relevant graph
properties.  It does not call the proof criterion or any project helper.
"""

from __future__ import annotations

import itertools
import json

import networkx as nx


def dominates(graph: nx.Graph, selected: set[int]) -> bool:
    return all(
        vertex in selected
        or any(graph.has_edge(vertex, guard) for guard in selected)
        for vertex in graph
    )


def is_induced_p5(graph: nx.Graph, chosen: tuple[int, ...]) -> bool:
    induced = graph.subgraph(chosen)
    return (
        induced.number_of_edges() == 4
        and nx.is_connected(induced)
        and sorted(dict(induced.degree()).values()) == [1, 1, 2, 2, 2]
    )


def is_p5_free(graph: nx.Graph) -> bool:
    return not any(
        is_induced_p5(graph, chosen)
        for chosen in itertools.combinations(graph, 5)
    )


def is_induced_p3(graph: nx.Graph, chosen: tuple[int, ...]) -> bool:
    induced = graph.subgraph(chosen)
    return (
        induced.number_of_edges() == 2
        and sorted(dict(induced.degree()).values()) == [1, 1, 2]
    )


def is_induced_c5(graph: nx.Graph, chosen: tuple[int, ...]) -> bool:
    induced = graph.subgraph(chosen)
    return (
        induced.number_of_edges() == 5
        and nx.is_connected(induced)
        and all(degree == 2 for _, degree in induced.degree())
    )


def dominating_triangles(graph: nx.Graph):
    for chosen in itertools.combinations(graph, 3):
        triangle = set(chosen)
        if (
            graph.subgraph(chosen).number_of_edges() == 3
            and dominates(graph, triangle)
        ):
            yield triangle


def private_regions(graph: nx.Graph, triangle: set[int]) -> dict[int, set[int]]:
    return {
        hub: {
            vertex
            for vertex in set(graph) - triangle
            if set(graph[vertex]) & triangle == {hub}
        }
        for hub in triangle
    }


def main() -> None:
    counts = {
        "atlas_graphs": 0,
        "p5_free_graphs": 0,
        "dominating_triangles": 0,
        "triangle_cross_edges": 0,
        "cross_edges_with_dominating_p3": 0,
        "cross_edges_with_dominating_c5": 0,
        "theorem_failures": [],
    }

    for graph in nx.graph_atlas_g():
        counts["atlas_graphs"] += 1
        if not is_p5_free(graph):
            continue
        counts["p5_free_graphs"] += 1

        dominating_p3 = any(
            is_induced_p3(graph, chosen) and dominates(graph, set(chosen))
            for chosen in itertools.combinations(graph, 3)
        )
        dominating_c5 = any(
            is_induced_c5(graph, chosen) and dominates(graph, set(chosen))
            for chosen in itertools.combinations(graph, 5)
        )

        for triangle in dominating_triangles(graph):
            counts["dominating_triangles"] += 1
            private = private_regions(graph, triangle)
            for first, second in itertools.combinations(sorted(triangle), 2):
                for x in private[first]:
                    for y in private[second]:
                        if not graph.has_edge(x, y):
                            continue
                        counts["triangle_cross_edges"] += 1
                        counts["cross_edges_with_dominating_p3"] += int(
                            dominating_p3
                        )
                        counts["cross_edges_with_dominating_c5"] += int(
                            dominating_c5
                        )
                        if not dominating_p3:
                            counts["theorem_failures"].append(
                                {
                                    "graph6": nx.to_graph6_bytes(
                                        graph, header=False
                                    ).decode().strip(),
                                    "triangle": sorted(triangle),
                                    "cross_edge": sorted((x, y)),
                                }
                            )

    counts["status"] = "PASS" if not counts["theorem_failures"] else "FAIL"
    print(json.dumps(counts, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

