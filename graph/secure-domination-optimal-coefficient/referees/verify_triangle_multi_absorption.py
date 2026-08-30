#!/usr/bin/env python3
"""Independent audit of the triangle/multi-region absorption lemma.

This uses the definitions directly on every triangle of every P5-free Graph
Atlas graph.  It is not a proof substitute; it guards the exact region and
index bookkeeping in the accompanying lemma note.
"""

from __future__ import annotations

import itertools
import json
import networkx as nx


def induced_p5_free(graph: nx.Graph) -> bool:
    for chosen in itertools.combinations(graph, 5):
        subgraph = graph.subgraph(chosen)
        if subgraph.number_of_edges() == 4 and nx.is_connected(subgraph) and sorted(dict(subgraph.degree()).values()) == [1, 1, 2, 2, 2]:
            return False
    return True


def dominates(graph: nx.Graph, selected: set[int]) -> bool:
    return all(vertex in selected or bool(set(graph[vertex]) & selected) for vertex in graph)


def private_and_multi(graph: nx.Graph, clique: tuple[int, int, int]):
    kset = set(clique)
    private = {hub: set() for hub in clique}
    multi: dict[frozenset[int], set[int]] = {}
    for vertex in set(graph) - kset:
        attachment = frozenset(set(graph[vertex]) & kset)
        if len(attachment) == 1:
            private[next(iter(attachment))].add(vertex)
        elif len(attachment) >= 2:
            multi.setdefault(attachment, set()).add(vertex)
    return private, multi


def main() -> None:
    counts = {
        "p5free_graphs": 0,
        "triangles": 0,
        "relevant_m_y_tuples": 0,
        "third_private_cover_checks": 0,
        "multi_cover_checks": 0,
        "induced_p3_checks": 0,
        "all_but_source_private_dominated_checks": 0,
        "status": "PASS",
    }
    for graph in nx.graph_atlas_g():
        if not induced_p5_free(graph):
            continue
        counts["p5free_graphs"] += 1
        for clique in itertools.combinations(graph, 3):
            if not all(graph.has_edge(u, v) for u, v in itertools.combinations(clique, 2)):
                continue
            if not dominates(graph, set(clique)):
                continue
            counts["triangles"] += 1
            private, multi = private_and_multi(graph, clique)
            for i, j in itertools.combinations(clique, 2):
                ell = next(hub for hub in clique if hub not in {i, j})
                for middle in multi.get(frozenset({i, j}), set()):
                    for source in (i, j):
                        other = j if source == i else i
                        for y in private[source] & set(graph[middle]):
                            counts["relevant_m_y_tuples"] += 1
                            p3 = {y, middle, other}
                            assert graph.has_edge(y, middle)
                            assert graph.has_edge(middle, other)
                            assert not graph.has_edge(y, other)
                            counts["induced_p3_checks"] += 1

                            # P_ell is covered by y or middle.
                            for z in private[ell]:
                                counts["third_private_cover_checks"] += 1
                                assert graph.has_edge(z, y) or graph.has_edge(z, middle), {
                                    "kind": "third_private", "graph6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
                                    "K": clique, "m": middle, "y": y, "z": z,
                                }

                            # The only multi class not automatically seen by the retained
                            # hub 'other' is the class attached to source and ell.
                            for z in multi.get(frozenset({source, ell}), set()):
                                counts["multi_cover_checks"] += 1
                                assert graph.has_edge(z, y) or graph.has_edge(z, middle), {
                                    "kind": "multi", "graph6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
                                    "K": clique, "m": middle, "y": y, "z": z,
                                }

                            covered = set(p3)
                            for vertex in p3:
                                covered.update(graph[vertex])
                            asserted_region = private[source] - covered
                            actual_missed = set(graph) - covered
                            counts["all_but_source_private_dominated_checks"] += 1
                            assert actual_missed == asserted_region, {
                                "kind": "exact_remainder", "graph6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
                                "K": clique, "m": middle, "y": y,
                                "expected": sorted(asserted_region), "actual": sorted(actual_missed),
                            }
    print(json.dumps(counts, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

