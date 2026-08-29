#!/usr/bin/env python3
"""Independent Graph Atlas audit of dominating-set residual completion."""

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


def maximum_independent_sets(graph: nx.Graph, vertices: set[int]) -> list[set[int]]:
    maximum: list[set[int]] = []
    ordered = sorted(vertices)
    for size in range(len(ordered) + 1):
        current = [
            set(chosen)
            for chosen in itertools.combinations(ordered, size)
            if all(
                not graph.has_edge(u, v)
                for u, v in itertools.combinations(chosen, 2)
            )
        ]
        if not current:
            return maximum
        maximum = current
    return maximum


def minimum_dominating_sets(graph: nx.Graph, vertices: set[int]) -> list[set[int]]:
    if not vertices:
        return [set()]
    ordered = sorted(vertices)
    for size in range(1, len(ordered) + 1):
        current = [
            set(chosen)
            for chosen in itertools.combinations(ordered, size)
            if all(
                vertex in chosen
                or any(graph.has_edge(vertex, guard) for guard in chosen)
                for vertex in vertices
            )
        ]
        if current:
            return current
    raise AssertionError("the full vertex set must dominate itself")


def audit_private_completion(graph: nx.Graph) -> tuple[int, int]:
    vertices = set(graph)
    clique_count = 0
    construction_count = 0
    for size in range(2, len(graph) + 1):
        for chosen in itertools.combinations(sorted(vertices), size):
            clique = set(chosen)
            if not all(
                graph.has_edge(u, v)
                for u, v in itertools.combinations(clique, 2)
            ) or not dominates(graph, clique):
                continue
            if any(dominates(graph, clique - {guard}) for guard in clique):
                continue
            clique_count += 1
            regions = {
                guard: {
                    vertex
                    for vertex in vertices - clique
                    if {
                        member
                        for member in clique
                        if graph.has_edge(vertex, member)
                    }
                    == {guard}
                }
                for guard in clique
            }
            if any(not region for region in regions.values()):
                raise AssertionError("minimal clique has an empty private region")
            multi = {
                vertex
                for vertex in vertices - clique
                if sum(graph.has_edge(vertex, guard) for guard in clique) >= 2
            }
            local_options = []
            for guard in sorted(clique):
                options = {
                    frozenset(independent - {omitted})
                    for independent in maximum_independent_sets(
                        graph, regions[guard]
                    )
                    for omitted in independent
                }
                local_options.append([set(option) for option in options])
            for local_choice in itertools.product(*local_options):
                local_guards = set().union(*local_choice)
                for multi_guards in minimum_dominating_sets(graph, multi):
                    construction_count += 1
                    selected = clique | local_guards | multi_guards
                    if not secure(graph, selected):
                        raise AssertionError(
                            {
                                "graph6": nx.to_graph6_bytes(
                                    graph, header=False
                                ).decode().strip(),
                                "clique": sorted(clique),
                                "local_guards": sorted(local_guards),
                                "multi_guards": sorted(multi_guards),
                            }
                        )
    return clique_count, construction_count


def main() -> None:
    graphs = 0
    dominating_sets = 0
    constructions = 0
    minimal_cliques = 0
    private_constructions = 0
    for graph in nx.graph_atlas_g():
        vertices = set(graph)
        if not vertices:
            continue
        graphs += 1
        for size in range(1, len(graph) + 1):
            for chosen in itertools.combinations(sorted(vertices), size):
                dominating = set(chosen)
                outside = vertices - dominating
                if not outside or not dominates(graph, dominating):
                    continue
                dominating_sets += 1
                for independent in maximum_independent_sets(graph, outside):
                    for omitted in independent:
                        selected = dominating | (independent - {omitted})
                        constructions += 1
                        if not secure(graph, selected):
                            raise AssertionError(
                                {
                                    "graph6": nx.to_graph6_bytes(
                                        graph, header=False
                                    ).decode().strip(),
                                    "dominating": sorted(dominating),
                                    "independent": sorted(independent),
                                    "omitted": omitted,
                                }
                            )
        graph_cliques, graph_private = audit_private_completion(graph)
        minimal_cliques += graph_cliques
        private_constructions += graph_private
    print(
        json.dumps(
            {
                "graphs": graphs,
                "dominating_sets": dominating_sets,
                "constructions": constructions,
                "minimal_dominating_cliques": minimal_cliques,
                "private_constructions": private_constructions,
                "failures": 0,
                "status": "PASS",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
