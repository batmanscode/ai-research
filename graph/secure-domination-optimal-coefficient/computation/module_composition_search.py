#!/usr/bin/env python3
"""Test lexicographic substitutions of known tight P5-free modules."""

from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "vendor"))
sys.path.insert(0, str(HERE))

import networkx as nx  # type: ignore

from atlas_substitution_search import adjacency
from search_extremal import encode_graph6
from structured_search import ICOS_COMPLEMENT, edge_list, independent_masks, secure_sets_of_size, weighted_alpha
from verify_candidate import decode_graph6, induced_p5s


def cycle5() -> list[set[int]]:
    result = [set() for _ in range(5)]
    for v in range(5):
        w = (v + 1) % 5
        result[v].add(w)
        result[w].add(v)
    return result


def substitute(skeleton: list[set[int]], modules: tuple[list[set[int]], ...]) -> list[set[int]]:
    groups: list[list[int]] = []
    cursor = 0
    for module in modules:
        groups.append(list(range(cursor, cursor + len(module))))
        cursor += len(module)
    result = [set() for _ in range(cursor)]
    for index, module in enumerate(modules):
        for u in range(len(module)):
            for v in module[u]:
                result[groups[index][u]].add(groups[index][v])
    for i, j in itertools.combinations(range(len(skeleton)), 2):
        if j not in skeleton[i]:
            continue
        for u in groups[i]:
            for v in groups[j]:
                result[u].add(v)
                result[v].add(u)
    return result


def run(max_order: int = 50) -> dict:
    _, icos = decode_graph6(ICOS_COMPLEMENT)
    options = {
        "K1": ([set()], 1),
        "C5": (cycle5(), 2),
        "IcoBar": (icos, 3),
    }
    names = tuple(options)
    counts = {
        "skeletons": 0,
        "assignments": 0,
        "weighted_alpha_four": 0,
        "within_order_limit": 0,
        "no_secure_five": 0,
    }
    candidate = None
    started = time.time()

    for graph in nx.graph_atlas_g():
        if not (2 <= len(graph) <= 7) or not nx.is_connected(graph):
            continue
        skeleton = adjacency(graph)
        if induced_p5s(skeleton):
            continue
        counts["skeletons"] += 1
        indep = independent_masks(skeleton)
        for assignment in itertools.product(names, repeat=len(skeleton)):
            counts["assignments"] += 1
            alpha_weights = tuple(options[name][1] for name in assignment)
            if weighted_alpha(alpha_weights, indep) != 4:
                continue
            counts["weighted_alpha_four"] += 1
            modules = tuple(options[name][0] for name in assignment)
            order = sum(map(len, modules))
            if order > max_order:
                continue
            counts["within_order_limit"] += 1
            composed = substitute(skeleton, modules)
            secure_five = secure_sets_of_size(composed, 5, stop_after=1)
            if secure_five:
                continue
            counts["no_secure_five"] += 1
            edges = edge_list(composed)
            candidate = {
                "skeleton_graph6": encode_graph6(len(skeleton), edge_list(skeleton)),
                "module_assignment": assignment,
                "order": order,
                "graph6": encode_graph6(order, edges),
                "edges": [list(edge) for edge in edges],
                "induced_p5_count_direct": len(induced_p5s(composed)),
                "secure_six": secure_sets_of_size(composed, 6, stop_after=1),
            }
            break
        if candidate:
            break

    return {
        "scope": {
            "skeletons": "all connected P5-free graph-atlas graphs of order 2..7",
            "modules": {name: {"order": len(module), "alpha": alpha_value} for name, (module, alpha_value) in options.items()},
            "substitution": "complete adjacency between modules exactly on skeleton edges",
            "max_order": max_order,
        },
        "counts": counts,
        "candidate": candidate,
        "seconds": time.time() - started,
    }


if __name__ == "__main__":
    result = run()
    (HERE / "module_compositions.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
