#!/usr/bin/env python3
"""Independent stress audit for the dominating-triangle theorem.

This checker intentionally reimplements all predicates from definitions.  It
checks the complete NetworkX Graph Atlas and a fixed-seed family of larger
random triangle cores.  Its finite output corroborates, but does not replace,
the all-orders proof.
"""

from __future__ import annotations

import itertools
import json
import random
from collections import Counter

import networkx as nx


def subsets(vertices):
    vertices = tuple(vertices)
    for size in range(len(vertices) + 1):
        yield from map(set, itertools.combinations(vertices, size))


def independent(graph: nx.Graph, chosen: set[int]) -> bool:
    return all(not graph.has_edge(u, v) for u, v in itertools.combinations(chosen, 2))


def maximum_independent_sets(graph: nx.Graph, vertices: set[int]) -> list[set[int]]:
    best: list[set[int]] = []
    for chosen in subsets(vertices):
        if independent(graph, chosen):
            if not best or len(chosen) > len(best[0]):
                best = [chosen]
            elif len(chosen) == len(best[0]):
                best.append(chosen)
    return best


def alpha(graph: nx.Graph, vertices: set[int] | None = None) -> int:
    vertices = set(graph) if vertices is None else vertices
    return len(maximum_independent_sets(graph, vertices)[0]) if vertices else 0


def dominates(graph: nx.Graph, chosen: set[int], universe: set[int] | None = None) -> bool:
    universe = set(graph) if universe is None else universe
    covered = set(chosen)
    for vertex in chosen:
        covered.update(graph[vertex])
    return universe <= covered


def secure(graph: nx.Graph, chosen: set[int]) -> bool:
    if not dominates(graph, chosen):
        return False
    for attacker in set(graph) - chosen:
        if not any(
            graph.has_edge(defender, attacker)
            and dominates(graph, (chosen - {defender}) | {attacker})
            for defender in chosen
        ):
            return False
    return True


def induced_p5_free(graph: nx.Graph) -> bool:
    for chosen in itertools.combinations(graph, 5):
        subgraph = graph.subgraph(chosen)
        if subgraph.number_of_edges() == 4 and nx.is_connected(subgraph):
            if sorted(dict(subgraph.degree()).values()) == [1, 1, 2, 2, 2]:
                return False
    return True


def induced_p3(graph: nx.Graph, chosen: set[int]) -> bool:
    subgraph = graph.subgraph(chosen)
    return subgraph.number_of_edges() == 2 and nx.is_connected(subgraph)


def has_dominating_p3(graph: nx.Graph) -> bool:
    return any(
        induced_p3(graph, set(chosen)) and dominates(graph, set(chosen))
        for chosen in itertools.combinations(graph, 3)
    )


def dominating_triangles(graph: nx.Graph):
    for chosen in itertools.combinations(graph, 3):
        triangle = set(chosen)
        if graph.subgraph(triangle).number_of_edges() == 3 and dominates(graph, triangle):
            yield tuple(chosen)


def private_regions(graph: nx.Graph, triangle: tuple[int, int, int]) -> dict[int, set[int]]:
    hubs = set(triangle)
    return {
        hub: {
            vertex
            for vertex in set(graph) - hubs
            if set(graph[vertex]) & hubs == {hub}
        }
        for hub in triangle
    }


def pairwise_anticomplete(graph: nx.Graph, regions: dict[int, set[int]]) -> bool:
    return all(
        not graph.has_edge(u, v)
        for first, second in itertools.combinations(regions, 2)
        for u in regions[first]
        for v in regions[second]
    )


def other_pair(triangle: tuple[int, int, int], omitted: int) -> set[int]:
    return set(triangle) - {omitted}


def closed_neighborhood(graph: nx.Graph, chosen: set[int]) -> set[int]:
    result = set(chosen)
    for vertex in chosen:
        result.update(graph[vertex])
    return result


def audit_residual_choice(
    graph: nx.Graph,
    triangle: tuple[int, int, int],
    regions: dict[int, set[int]],
    independent_sets: tuple[set[int], set[int], set[int]],
    omitted: tuple[int, int, int],
    counts: Counter,
) -> None:
    hubs = set(triangle)
    p = sum(len(chosen) for chosen in independent_sets)
    x_guard = set().union(
        *(chosen - {missing} for chosen, missing in zip(independent_sets, omitted))
    )
    closed_x = closed_neighborhood(graph, x_guard)
    residual = {
        hub: regions[hub] - closed_x
        for hub in triangle
    }

    for hub in triangle:
        assert residual[hub]
        assert independent(graph, set())
        assert all(
            graph.has_edge(u, v)
            for u, v in itertools.combinations(residual[hub], 2)
        )

    multi = {
        vertex
        for vertex in set(graph) - hubs
        if len(set(graph[vertex]) & hubs) >= 2
    }
    bad = {
        vertex
        for vertex in multi
        if not (set(graph[vertex]) & x_guard)
        and all(
            not residual[hub] <= set(graph[vertex])
            for hub in set(graph[vertex]) & hubs
        )
    }

    # Seen-region anticompleteness, including the three-hub case.
    for vertex in bad:
        for hub in set(graph[vertex]) & hubs:
            counts["seen_region_checks"] += 1
            assert not (set(graph[vertex]) & residual[hub])

    # Check every independent subset, not just a maximum one.
    for witness_set in subsets(bad):
        if not independent(graph, witness_set):
            continue
        good_hubs = []
        for hub in triangle:
            if any(not (set(graph[u]) & witness_set) for u in residual[hub]):
                good_hubs.append(hub)
        counts["common_two_sets"] += 1
        assert len(good_hubs) >= 2

    max_bad_sets = maximum_independent_sets(graph, bad) if bad else [set()]
    alpha_bad = len(max_bad_sets[0])
    alpha_graph = alpha(graph)
    assert alpha_bad <= alpha_graph - p + 1

    # A maximum independent set dominates its induced graph and is the Y used
    # in the bad-M completion.  Check the resulting set directly by definition.
    y_guard = max_bad_sets[0]
    assert dominates(graph, y_guard, bad)
    secure_set = hubs | x_guard | y_guard
    assert len(secure_set) <= alpha_graph + 1
    assert secure(graph, secure_set)
    counts["residual_choices"] += 1
    counts["nonempty_bad_choices"] += bool(bad)
    counts["three_hub_bad_vertices"] += sum(
        len(set(graph[v]) & hubs) == 3 for v in bad
    )


def audit_graph(graph: nx.Graph, counts: Counter) -> None:
    if graph.number_of_nodes() < 3 or not induced_p5_free(graph):
        return
    alpha_graph = alpha(graph)
    triangles = list(dominating_triangles(graph))
    if triangles and alpha_graph >= 3:
        counts["direct_full_graph_checks"] += 1
        assert any(
            secure(graph, chosen)
            for size in range(alpha_graph + 2)
            for chosen in map(set, itertools.combinations(graph, size))
        )
    for triangle in triangles:
        counts["dominating_triangles"] += 1
        regions = private_regions(graph, triangle)

        empty = [hub for hub in triangle if not regions[hub]]
        if empty:
            counts["empty_private_cases"] += 1
            # For each empty region, the other two hubs dominate.
            assert all(dominates(graph, other_pair(triangle, hub)) for hub in empty)
            continue

        if not pairwise_anticomplete(graph, regions):
            counts["private_cross_edge_cases"] += 1
            assert has_dominating_p3(graph)
            continue

        counts["bad_m_cases"] += 1
        max_sets = [maximum_independent_sets(graph, regions[hub]) for hub in triangle]
        for independent_sets in itertools.product(*max_sets):
            for omitted in itertools.product(*[tuple(chosen) for chosen in independent_sets]):
                audit_residual_choice(
                    graph,
                    triangle,
                    regions,
                    independent_sets,
                    omitted,
                    counts,
                )

def random_triangle_graph(rng: random.Random) -> nx.Graph:
    graph = nx.Graph()
    triangle = (0, 1, 2)
    graph.add_nodes_from(triangle)
    graph.add_edges_from(itertools.combinations(triangle, 2))
    next_vertex = 3
    private: list[list[int]] = []
    for hub in triangle:
        region = list(range(next_vertex, next_vertex + rng.randint(1, 3)))
        next_vertex += len(region)
        private.append(region)
        graph.add_nodes_from(region)
        graph.add_edges_from((vertex, hub) for vertex in region)
        for u, v in itertools.combinations(region, 2):
            if rng.random() < 0.72:
                graph.add_edge(u, v)
    multi = list(range(next_vertex, next_vertex + rng.randint(0, 4)))
    graph.add_nodes_from(multi)
    for vertex in multi:
        seen = rng.choice(((0, 1), (0, 2), (1, 2), (0, 1, 2)))
        graph.add_edges_from((vertex, hub) for hub in seen)
    outside = [vertex for region in private for vertex in region] + multi
    # Preserve pairwise anticompleteness of the private regions; make every
    # other outside edge independently and fairly densely.
    region_of = {
        vertex: index
        for index, region in enumerate(private)
        for vertex in region
    }
    for u, v in itertools.combinations(outside, 2):
        if graph.has_edge(u, v):
            continue
        if u in region_of and v in region_of and region_of[u] != region_of[v]:
            continue
        if rng.random() < 0.67:
            graph.add_edge(u, v)
    return graph


def main() -> None:
    counts = Counter()
    for graph in nx.graph_atlas_g():
        counts["atlas_graphs"] += 1
        audit_graph(nx.convert_node_labels_to_integers(graph), counts)

    rng = random.Random(20260830)
    accepted = 0
    attempts = 0
    while accepted < 2_000 and attempts < 100_000:
        attempts += 1
        graph = random_triangle_graph(rng)
        if not induced_p5_free(graph):
            continue
        accepted += 1
        audit_graph(graph, counts)
    counts["random_attempts"] = attempts
    counts["random_p5free"] = accepted
    assert accepted == 2_000

    payload = {"status": "PASS", **dict(sorted(counts.items()))}
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
