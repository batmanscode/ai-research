#!/usr/bin/env python3
"""Independent finite stress audit of the K>=4 private-cross-edge closure.

The all-orders result rests on the handwritten proof.  This script checks the
new local lemmas and the proposed dominating P3 directly, first on an exact
K4 model with four singleton private regions and one arbitrary multi-neighbor,
then on fixed-seed larger random clique/private/multi configurations.
"""

from __future__ import annotations

import itertools
import json
import random
from collections import Counter
from pathlib import Path

import networkx as nx


OUT = (
    Path(__file__).parents[1]
    / "computation"
    / "results"
    / "optimal_four_thirds_audit.json"
)


def induced_p5_free(graph: nx.Graph) -> bool:
    adjacency = {
        vertex: sum(1 << other for other in graph[vertex]) for vertex in graph
    }
    for chosen in itertools.combinations(graph, 5):
        mask = sum(1 << vertex for vertex in chosen)
        degrees = sorted((adjacency[vertex] & mask).bit_count() for vertex in chosen)
        if degrees != [1, 1, 2, 2, 2]:
            continue
        reached = 1 << chosen[0]
        while True:
            expanded = reached
            for vertex in chosen:
                if reached >> vertex & 1:
                    expanded |= adjacency[vertex] & mask
            if expanded == reached:
                break
            reached = expanded
        if reached == mask:
            return False
    return True


def dominates(graph: nx.Graph, chosen: set[int]) -> bool:
    covered = set(chosen)
    for vertex in chosen:
        covered.update(graph[vertex])
    return covered == set(graph)


def cross_parts(
    graph: nx.Graph, regions: dict[int, set[int]]
) -> dict[int, int]:
    private = set().union(*regions.values())
    region_of = {
        vertex: hub for hub, region in regions.items() for vertex in region
    }
    auxiliary = nx.Graph()
    auxiliary.add_nodes_from(private)
    for u, v in itertools.combinations(private, 2):
        if region_of[u] != region_of[v] and not graph.has_edge(u, v):
            auxiliary.add_edge(u, v)
    part_of = {}
    for index, component in enumerate(nx.connected_components(auxiliary)):
        for vertex in component:
            part_of[vertex] = index
    # Independently check the global cross-partition property.
    for u, v in itertools.combinations(private, 2):
        if region_of[u] == region_of[v]:
            continue
        assert graph.has_edge(u, v) == (part_of[u] != part_of[v])
    return part_of


def audit_graph(
    graph: nx.Graph,
    hubs: tuple[int, ...],
    regions: dict[int, set[int]],
    multi: set[int],
    counts: Counter,
) -> None:
    assert all(regions[hub] for hub in hubs)
    assert all(
        set(graph[vertex]) & set(hubs) == {hub}
        for hub in hubs
        for vertex in regions[hub]
    )
    assert all(len(set(graph[vertex]) & set(hubs)) >= 2 for vertex in multi)
    if not induced_p5_free(graph):
        return

    cross_edges = [
        (first, second, x, y)
        for first, second in itertools.combinations(hubs, 2)
        for x in regions[first]
        for y in regions[second]
        if graph.has_edge(x, y)
    ]
    if not cross_edges:
        return
    counts["p5free_cross_graphs"] += 1
    part_of = cross_parts(graph, regions)

    for first, second, x, y in cross_edges:
        counts["cross_edges"] += 1
        assert part_of[x] != part_of[y]

        # Lemma 1: all third private regions see both endpoints.
        for third in set(hubs) - {first, second}:
            for z in regions[third]:
                counts["third_region_vertices"] += 1
                assert graph.has_edge(z, x)
                assert graph.has_edge(z, y)

        # Lemma 2: neither endpoint part meets the opposite region.
        assert all(part_of[z] != part_of[x] for z in regions[second])
        assert all(part_of[z] != part_of[y] for z in regions[first])
        counts["part_exclusion_checks"] += 2

        # Lemma 3 and the final P3.
        for vertex in multi:
            if not graph.has_edge(vertex, first):
                counts["multi_missed_hub_checks"] += 1
                assert graph.has_edge(vertex, x) or graph.has_edge(vertex, y)

        path = {first, x, y}
        assert graph.subgraph(path).number_of_edges() == 2
        assert nx.is_connected(graph.subgraph(path))
        assert dominates(graph, path)
        counts["dominating_p3_checks"] += 1


def exact_singleton_one_multi(counts: Counter) -> None:
    hubs = (0, 1, 2, 3)
    regions = {hub: {4 + hub} for hub in hubs}
    private = tuple(range(4, 8))
    multi_vertex = 8
    hub_types = [
        set(chosen)
        for size in (2, 3, 4)
        for chosen in itertools.combinations(hubs, size)
    ]
    private_pairs = list(itertools.combinations(private, 2))

    for hub_type in hub_types:
        for private_mask in range(1 << len(private)):
            for cross_mask in range(1 << len(private_pairs)):
                graph = nx.Graph()
                graph.add_nodes_from(range(9))
                graph.add_edges_from(itertools.combinations(hubs, 2))
                graph.add_edges_from((hub, 4 + hub) for hub in hubs)
                graph.add_edges_from((multi_vertex, hub) for hub in hub_type)
                graph.add_edges_from(
                    (multi_vertex, private[index])
                    for index in range(len(private))
                    if private_mask >> index & 1
                )
                graph.add_edges_from(
                    private_pairs[index]
                    for index in range(len(private_pairs))
                    if cross_mask >> index & 1
                )
                counts["exact_models"] += 1
                audit_graph(
                    graph, hubs, regions, {multi_vertex}, counts
                )


def random_model(rng: random.Random) -> tuple[
    nx.Graph, tuple[int, ...], dict[int, set[int]], set[int]
]:
    order = rng.choice((4, 5))
    hubs = tuple(range(order))
    graph = nx.Graph()
    graph.add_nodes_from(hubs)
    graph.add_edges_from(itertools.combinations(hubs, 2))
    next_vertex = order
    regions: dict[int, set[int]] = {}
    for hub in hubs:
        region = set(range(next_vertex, next_vertex + rng.randint(1, 2)))
        next_vertex += len(region)
        regions[hub] = region
        graph.add_nodes_from(region)
        graph.add_edges_from((hub, vertex) for vertex in region)
    multi = set(range(next_vertex, next_vertex + rng.randint(0, 2)))
    graph.add_nodes_from(multi)
    for vertex in multi:
        size = rng.randint(2, order)
        graph.add_edges_from(
            (vertex, hub) for hub in rng.sample(list(hubs), size)
        )

    outside = set().union(*regions.values(), multi)
    # Dense outside graphs produce a useful number of P5-free samples while
    # retaining arbitrary within-region, cross-region, and M adjacencies.
    for u, v in itertools.combinations(outside, 2):
        if rng.random() < 0.70:
            graph.add_edge(u, v)
    return graph, hubs, regions, multi


def main() -> None:
    counts = Counter()
    exact_singleton_one_multi(counts)

    rng = random.Random(20260830)
    accepted = 0
    attempts = 0
    while accepted < 50 and attempts < 100_000:
        attempts += 1
        graph, hubs, regions, multi = random_model(rng)
        before = counts["p5free_cross_graphs"]
        audit_graph(graph, hubs, regions, multi, counts)
        if counts["p5free_cross_graphs"] > before:
            accepted += 1
    counts["random_attempts"] = attempts
    counts["random_p5free_cross_graphs"] = accepted
    assert accepted == 50

    payload = {"status": "PASS", **dict(sorted(counts.items()))}
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
