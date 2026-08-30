#!/usr/bin/env python3
"""Adversarial finite audit of clique-separator rooted gluing lemmas.

This is scratch verification, not a repository artifact.  It directly tests
security of every constructed set and does not use a derived exchange
criterion.
"""

from __future__ import annotations

import itertools
import json
import random
from collections import Counter

import networkx as nx


def dominates(g: nx.Graph, s: set[int], vertices: set[int] | None = None) -> bool:
    vertices = set(g) if vertices is None else vertices
    return all(v in s or any(g.has_edge(v, x) for x in s) for v in vertices)


def secure(g: nx.Graph, s: set[int]) -> bool:
    if not dominates(g, s):
        return False
    return all(
        any(g.has_edge(v, d) and dominates(g, s - {d} | {v}) for d in s)
        for v in set(g) - s
    )


def independent(g: nx.Graph, s: set[int]) -> bool:
    return all(not g.has_edge(x, y) for x, y in itertools.combinations(s, 2))


def alpha(g: nx.Graph, vertices: set[int]) -> int:
    ordered = sorted(vertices)
    for size in range(len(ordered), -1, -1):
        if any(independent(g, set(s)) for s in itertools.combinations(ordered, size)):
            return size
    raise AssertionError


def maximum_independent_sets(g: nx.Graph, vertices: set[int]):
    a = alpha(g, vertices)
    return [set(s) for s in itertools.combinations(sorted(vertices), a) if independent(g, set(s))]


def p5_free(g: nx.Graph) -> bool:
    for vertices in itertools.combinations(g, 5):
        h = g.subgraph(vertices)
        if (
            h.number_of_edges() == 4
            and nx.is_connected(h)
            and sorted(dict(h.degree()).values()) == [1, 1, 2, 2, 2]
        ):
            return False
    return True


def is_clique(g: nx.Graph, vertices: set[int]) -> bool:
    return all(g.has_edge(x, y) for x, y in itertools.combinations(vertices, 2))


def rooted_p4_free(g: nx.Graph, root: int, component: set[int]) -> bool:
    for a, b, c in itertools.permutations(component, 3):
        if (
            g.has_edge(root, a)
            and g.has_edge(a, b)
            and g.has_edge(b, c)
            and not g.has_edge(root, b)
            and not g.has_edge(root, c)
            and not g.has_edge(a, c)
        ):
            return False
    return True


def rooted_completion(g: nx.Graph, root: int, component: set[int]) -> set[int]:
    """Find a D witnessing the rooted lemma, independently by brute force."""
    induced = g.subgraph(component | {root}).copy()
    budget = alpha(g, component)
    for size in range(budget + 1):
        for chosen in itertools.combinations(sorted(component), size):
            d = set(chosen)
            if dominates(g, d, component) and secure(induced, d | {root}):
                return d
    raise AssertionError(("rooted completion missing", root, sorted(component)))


def component_data(g: nx.Graph, clique: set[int]):
    outside = set(g) - clique
    parts = [set(c) for c in nx.connected_components(g.subgraph(outside))]
    attachment = {
        i: {k for k in clique if any(g.has_edge(k, v) for v in c)}
        for i, c in enumerate(parts)
    }
    return parts, attachment


def audit_configuration(g: nx.Graph, clique: set[int], totals: Counter) -> None:
    parts, attachment = component_data(g, clique)
    if len(parts) < 2:
        return
    totals["separators"] += 1
    for rsize in range(2, len(clique) + 1):
        for rtup in itertools.combinations(sorted(clique), rsize):
            roots = set(rtup)
            multi_part_roots = {
                root
                for root in roots
                if sum(root in attachment[i] for i in range(len(parts))) >= 2
            }
            choices = [sorted(attachment[i] & multi_part_roots) for i in range(len(parts))]
            if all(choices):
                # Every assignment works; auditing all is still cheap in the Atlas.
                for assignment in itertools.product(*choices):
                    dsets = [rooted_completion(g, root, part) for root, part in zip(assignment, parts)]
                    selected = roots | set().union(*dsets)
                    totals["basic_constructions"] += 1
                    assert secure(g, selected), (
                        "basic gluing failure",
                        nx.to_graph6_bytes(g, header=False).decode().strip(),
                        sorted(clique),
                        sorted(roots),
                        assignment,
                        sorted(selected),
                    )
                    assert len(selected) <= sum(alpha(g, c) for c in parts) + len(roots)

            # Saving construction: r is reserved for a component C0 to which
            # it is complete.  Every other component is rooted outside r.
            for reserved in roots:
                for i0, c0 in enumerate(parts):
                    if not all(g.has_edge(reserved, v) for v in c0):
                        continue
                    other_choices = []
                    for i in range(len(parts)):
                        if i == i0:
                            continue
                        eligible = sorted(attachment[i] & (multi_part_roots - {reserved}))
                        other_choices.append((i, eligible))
                    if not all(opts for _, opts in other_choices):
                        continue
                    for roots_for_others in itertools.product(*(opts for _, opts in other_choices)):
                        dsets = {
                            i: rooted_completion(g, root, parts[i])
                            for (i, _), root in zip(other_choices, roots_for_others)
                        }
                        for independent_set in maximum_independent_sets(g, c0):
                            for omitted in independent_set:
                                x0 = independent_set - {omitted}
                                selected = roots | x0 | set().union(*dsets.values())
                                totals["saving_constructions"] += 1
                                assert secure(g, selected), (
                                    "saving gluing failure",
                                    nx.to_graph6_bytes(g, header=False).decode().strip(),
                                    sorted(clique),
                                    sorted(roots),
                                    reserved,
                                    i0,
                                    roots_for_others,
                                    sorted(independent_set),
                                    omitted,
                                    sorted(selected),
                                )
                                assert len(selected) <= sum(alpha(g, c) for c in parts) + len(roots) - 1

            # Multi-saving construction.  Every saved root is reserved for
            # one distinct complete component; all other components use only
            # mobile roots, whose rooted sets dominate without the root.
            for saved_size in range(1, min(len(roots), len(parts)) + 1):
                for saved_tuple in itertools.combinations(sorted(roots), saved_size):
                    saved = set(saved_tuple)
                    mobile = roots - saved
                    if roots != clique and not mobile:
                        continue
                    for designated_tuple in itertools.permutations(range(len(parts)), saved_size):
                        designated = dict(zip(saved_tuple, designated_tuple))
                        if any(
                            not all(g.has_edge(root, v) for v in parts[index])
                            for root, index in designated.items()
                        ):
                            continue
                        designated_indices = set(designated.values())
                        regular = [i for i in range(len(parts)) if i not in designated_indices]
                        regular_choices = [
                            sorted(attachment[i] & mobile & multi_part_roots)
                            for i in regular
                        ]
                        if not all(regular_choices):
                            continue
                        for regular_roots in itertools.product(*regular_choices):
                            dsets = {
                                i: rooted_completion(g, root, parts[i])
                                for i, root in zip(regular, regular_roots)
                            }
                            independent_options = [
                                [
                                    independent_set - {omitted}
                                    for independent_set in maximum_independent_sets(g, parts[index])
                                    for omitted in independent_set
                                ]
                                for index in designated_tuple
                            ]
                            for cheap_sets in itertools.product(*independent_options):
                                selected = roots | set().union(*dsets.values(), *cheap_sets)
                                totals["multi_saving_constructions"] += 1
                                assert secure(g, selected), (
                                    "multi-saving gluing failure",
                                    nx.to_graph6_bytes(g, header=False).decode().strip(),
                                    sorted(clique),
                                    sorted(roots),
                                    sorted(saved),
                                    designated,
                                    regular_roots,
                                    sorted(selected),
                                )
                                assert len(selected) <= (
                                    sum(alpha(g, c) for c in parts)
                                    + len(roots)
                                    - len(saved)
                                )

            # Stronger disjoint-block theorem.  Each root is labeled either
            # mobile (-1) or reserved for one designated component.  This
            # exhausts every pairwise-disjoint block system for the fixed R.
            for labels in itertools.product(range(-1, len(parts)), repeat=len(roots)):
                root_labels = dict(zip(sorted(roots), labels))
                designated = sorted(set(labels) - {-1})
                if not designated:
                    continue
                mobile = {root for root, label in root_labels.items() if label == -1}
                if roots != clique and not mobile:
                    continue
                blocks = {
                    i: {root for root, label in root_labels.items() if label == i}
                    for i in designated
                }
                if any(not dominates(g, block, parts[i]) for i, block in blocks.items()):
                    continue
                regular = [i for i in range(len(parts)) if i not in blocks]
                regular_choices = [
                    sorted(attachment[i] & mobile & multi_part_roots)
                    for i in regular
                ]
                if not all(regular_choices):
                    continue
                for regular_roots in itertools.product(*regular_choices):
                    dsets = {
                        i: rooted_completion(g, root, parts[i])
                        for i, root in zip(regular, regular_roots)
                    }
                    cheap_sets = []
                    for i in designated:
                        independent_set = maximum_independent_sets(g, parts[i])[0]
                        cheap_sets.append(independent_set - {min(independent_set)})
                    selected = roots | set().union(*dsets.values(), *cheap_sets)
                    totals["block_saving_constructions"] += 1
                    assert secure(g, selected), (
                        "block-saving gluing failure",
                        nx.to_graph6_bytes(g, header=False).decode().strip(),
                        sorted(clique),
                        sorted(roots),
                        root_labels,
                        regular_roots,
                        sorted(selected),
                    )
                    assert len(selected) <= (
                        sum(alpha(g, c) for c in parts)
                        + len(roots)
                        - len(designated)
                    )


def atlas_audit() -> Counter:
    totals = Counter()
    for g in nx.graph_atlas_g():
        if len(g) < 3 or not nx.is_connected(g) or not p5_free(g):
            continue
        totals["eligible_graphs"] += 1
        vertices = sorted(g)
        for size in range(2, len(g)):
            for chosen in itertools.combinations(vertices, size):
                clique = set(chosen)
                if is_clique(g, clique) and dominates(g, clique):
                    audit_configuration(g, clique, totals)
    return totals


def random_audit(seed: int = 892743, trials: int = 20_000) -> Counter:
    rng = random.Random(seed)
    totals = Counter()
    for _ in range(trials):
        t = rng.randint(2, 4)
        q = rng.randint(2, 4)
        sizes = [rng.randint(1, 3) for _ in range(q)]
        n = t + sum(sizes)
        if n > 11:
            continue
        g = nx.Graph()
        g.add_nodes_from(range(n))
        clique = set(range(t))
        g.add_edges_from(itertools.combinations(clique, 2))
        cursor = t
        for csize in sizes:
            component = list(range(cursor, cursor + csize))
            cursor += csize
            # Connected internal graph.
            g.add_edges_from(zip(component, component[1:]))
            for x, y in itertools.combinations(component, 2):
                if rng.random() < 0.35:
                    g.add_edge(x, y)
            # K dominates; independently vary attachments.
            for v in component:
                neighbours = [k for k in clique if rng.random() < 0.45]
                if not neighbours:
                    neighbours = [rng.choice(sorted(clique))]
                g.add_edges_from((v, k) for k in neighbours)
        if not p5_free(g):
            continue
        totals["eligible_graphs"] += 1
        audit_configuration(g, clique, totals)
    return totals


def main() -> None:
    result = {
        "atlas": dict(atlas_audit()),
        "random": dict(random_audit()),
        "status": "PASS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
