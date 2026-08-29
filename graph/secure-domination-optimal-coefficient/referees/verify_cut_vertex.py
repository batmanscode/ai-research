#!/usr/bin/env python3
"""Constructive Graph Atlas audit of the cut-vertex theorem.

For every connected induced-P5-free Atlas graph and every articulation
vertex, independently build the secure set from the proof in report.md.
"""

from __future__ import annotations

from itertools import combinations
import json

import networkx as nx


def dominates(graph: nx.Graph, chosen: set[int], vertices=None) -> bool:
    vertices = set(graph) if vertices is None else set(vertices)
    return all(
        vertex in chosen or bool(set(graph[vertex]) & chosen)
        for vertex in vertices
    )


def secure(graph: nx.Graph, chosen: set[int]) -> bool:
    if not dominates(graph, chosen):
        return False
    for attacked in set(graph) - chosen:
        if not any(
            dominates(graph, (chosen - {defender}) | {attacked})
            for defender in chosen & set(graph[attacked])
        ):
            return False
    return True


def maximum_independent_set(graph: nx.Graph, vertices) -> set[int]:
    ordered = sorted(vertices)
    for size in range(len(ordered), -1, -1):
        for chosen in combinations(ordered, size):
            if all(
                not graph.has_edge(u, v)
                for u, v in combinations(chosen, 2)
            ):
                return set(chosen)
    raise AssertionError


def maximal_independent_set(graph: nx.Graph, vertices) -> set[int]:
    chosen: set[int] = set()
    for vertex in sorted(vertices):
        if not (set(graph[vertex]) & chosen):
            chosen.add(vertex)
    return chosen


def independence_number(graph: nx.Graph, vertices=None) -> int:
    vertices = set(graph) if vertices is None else set(vertices)
    return len(maximum_independent_set(graph, vertices))


def is_p5_free(graph: nx.Graph) -> bool:
    for vertices in combinations(graph, 5):
        induced = graph.subgraph(vertices)
        if (
            induced.number_of_edges() == 4
            and nx.is_connected(induced)
            and sorted(dict(induced.degree()).values()) == [1, 1, 2, 2, 2]
        ):
            return False
    return True


def root_has_induced_p4(graph: nx.Graph, root: int, component: set[int]) -> bool:
    """Whether graph[root+component] has an induced P4 ending at root."""
    for a, b, c in (
        (a, b, c)
        for a in component
        for b in component
        for c in component
        if len({a, b, c}) == 3
    ):
        path = (root, a, b, c)
        if all(graph.has_edge(path[i], path[i + 1]) for i in range(3)) and all(
            not graph.has_edge(path[i], path[j])
            for i, j in ((0, 2), (0, 3), (1, 3))
        ):
            return True
    return False


def rooted_completion(
    graph: nx.Graph, root: int, component: set[int]
) -> tuple[set[int], dict]:
    """Build D with |D|<=alpha(component), D dominating component,
    and {root}+D secure in graph[root+component].
    """
    first_layer = set(graph[root]) & component
    residual = component - first_layer
    residual_components = [
        set(part) for part in nx.connected_components(graph.subgraph(residual))
    ]
    for part in residual_components:
        for boundary in first_layer:
            degree_into_part = sum(
                graph.has_edge(boundary, vertex) for vertex in part
            )
            if degree_into_part not in (0, len(part)):
                raise AssertionError("boundary adjacency is not all-or-nothing")

    clique_parts: list[set[int]] = []
    nonclique_parts: list[set[int]] = []
    independent: dict[frozenset[int], set[int]] = {}
    for part in residual_components:
        indep = maximum_independent_set(graph, part)
        independent[frozenset(part)] = indep
        (clique_parts if len(indep) == 1 else nonclique_parts).append(part)

    selected: set[int] = set()
    # A representative handles each clique residual component.
    for part in clique_parts:
        selected.add(min(part))

    # Assign every nonclique component to one complete boundary anchor.
    groups: dict[int, list[set[int]]] = {}
    for part in nonclique_parts:
        anchors = [
            boundary
            for boundary in first_layer
            if all(graph.has_edge(boundary, vertex) for vertex in part)
        ]
        if not anchors:
            raise AssertionError("residual component has no complete boundary anchor")
        groups.setdefault(min(anchors), []).append(part)

    designated: dict[int, set[int]] = {}
    for anchor, parts in groups.items():
        selected.add(anchor)
        ordered_parts = sorted(parts, key=lambda part: tuple(sorted(part)))
        special = ordered_parts[0]
        designated[anchor] = special
        for part in ordered_parts:
            indep = independent[frozenset(part)]
            selected |= indep if part is not special else indep - {min(indep)}

    # Complete domination of the boundary.  Every still-undominated boundary
    # vertex is anticomplete to every residual component.
    undominated_boundary = {
        vertex
        for vertex in first_layer
        if vertex not in selected and not (set(graph[vertex]) & selected)
    }
    boundary_completion = maximal_independent_set(graph, undominated_boundary)
    selected |= boundary_completion

    induced = graph.subgraph(component | {root}).copy()
    if not dominates(graph, selected, component):
        raise AssertionError("rootless part does not dominate the deep component")
    if not secure(induced, selected | {root}):
        raise AssertionError("rooted completion is not secure")
    if len(selected) > independence_number(graph, component):
        raise AssertionError("rooted completion overspends alpha(component)")

    return selected, {
        "first_layer": sorted(first_layer),
        "residual_components": [sorted(part) for part in residual_components],
        "anchors": {str(a): [sorted(p) for p in ps] for a, ps in groups.items()},
        "boundary_completion": sorted(boundary_completion),
    }


def cut_construction(graph: nx.Graph, root: int) -> tuple[set[int], dict]:
    components = [
        set(part)
        for part in nx.connected_components(graph.subgraph(set(graph) - {root}))
    ]
    deep = [
        part
        for part in components
        if any(not graph.has_edge(root, vertex) for vertex in part)
    ]
    if len(deep) > 1:
        raise AssertionError("P5-free cut has multiple deep components")

    if not deep:
        outside_independent = maximum_independent_set(graph, set(graph) - {root})
        chosen = {root} | outside_independent
        details = {"deep": None, "shallow_sets": [sorted(outside_independent)]}
    else:
        deep_part = deep[0]
        if root_has_induced_p4(graph, root, deep_part):
            raise AssertionError("deep side has a root-ended induced P4")
        rooted, rooted_details = rooted_completion(graph, root, deep_part)
        shallow = [part for part in components if part != deep_part]
        shallow_sets = [maximum_independent_set(graph, part) for part in shallow]
        expected_alpha = independence_number(graph, deep_part) + sum(
            len(independent) for independent in shallow_sets
        )
        if independence_number(graph) != expected_alpha:
            raise AssertionError("cut independence accounting failed")
        chosen = {root} | rooted | set().union(*shallow_sets)
        details = {
            "deep": sorted(deep_part),
            "rooted": rooted_details,
            "shallow_sets": [sorted(part) for part in shallow_sets],
        }

    if not secure(graph, chosen):
        raise AssertionError("global construction is not secure")
    if len(chosen) > independence_number(graph) + 1:
        raise AssertionError("global construction exceeds alpha+1")
    return chosen, details


def audit_naive_shortcut_failure() -> str:
    """Check the explicit example showing why arbitrary max-IS gluing fails."""
    # 0=x, 1=p, 2=u1, 3=u2, 4=v, 5=w1, 6=w2, 7=y.
    graph = nx.Graph()
    graph.add_nodes_from(range(8))
    graph.add_edges_from([(0, 1), (0, 7)])
    graph.add_edges_from((1, vertex) for vertex in range(2, 7))
    graph.add_edges_from([(2, 4), (3, 4), (2, 5), (3, 6), (5, 6)])
    if not is_p5_free(graph) or 0 not in set(nx.articulation_points(graph)):
        raise AssertionError("shortcut example has the wrong structure")
    deep = set(range(1, 7))
    independent = {2, 3}
    if len(independent) != independence_number(graph, deep):
        raise AssertionError("claimed deep set is not maximum independent")
    naive = {0, 2, 3, 7}
    if secure(graph, naive):
        raise AssertionError("naive shortcut unexpectedly secure")
    if dominates(graph, (naive - {2}) | {4}) or dominates(
        graph, (naive - {3}) | {4}
    ):
        raise AssertionError("claimed failed attack is not certified")
    return nx.to_graph6_bytes(graph, header=False).decode().strip()


def main() -> None:
    shortcut_graph6 = audit_naive_shortcut_failure()
    graph_count = 0
    cut_count = 0
    deep_cut_count = 0
    largest_order = 0
    max_slack = 0
    example = None
    for atlas_id, original in enumerate(nx.graph_atlas_g()):
        if not original or not nx.is_connected(original) or not is_p5_free(original):
            continue
        graph = nx.convert_node_labels_to_integers(original)
        cuts = list(nx.articulation_points(graph))
        if not cuts:
            continue
        graph_count += 1
        largest_order = max(largest_order, len(graph))
        for root in cuts:
            cut_count += 1
            chosen, details = cut_construction(graph, root)
            if details["deep"] is not None:
                deep_cut_count += 1
            slack = independence_number(graph) + 1 - len(chosen)
            max_slack = max(max_slack, slack)
            if example is None and details["deep"] is not None:
                example = {
                    "atlas_id": atlas_id,
                    "graph6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
                    "root": root,
                    "alpha": independence_number(graph),
                    "chosen": sorted(chosen),
                    "details": details,
                }
    print(
        json.dumps(
            {
                "status": "PASS",
                "failures": 0,
                "graphs": graph_count,
                "articulation_choices": cut_count,
                "deep_articulation_choices": deep_cut_count,
                "largest_order": largest_order,
                "maximum_unused_budget": max_slack,
                "naive_shortcut_counterexample_graph6": shortcut_graph6,
                "example": example,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
