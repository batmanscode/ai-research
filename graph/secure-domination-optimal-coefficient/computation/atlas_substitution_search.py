#!/usr/bin/env python3
"""Exhaust stable-set substitutions of small connected P5-free skeletons."""

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

from search_extremal import encode_graph6
from structured_search import (
    edge_list,
    independent_masks,
    secure_sets_of_size,
    stable_blowup,
    weighted_alpha,
)
from verify_candidate import alpha as brute_alpha, induced_p5s


def adjacency(graph: nx.Graph) -> list[set[int]]:
    mapping = {vertex: i for i, vertex in enumerate(graph.nodes())}
    result = [set() for _ in graph]
    for u, v in graph.edges():
        a, b = mapping[u], mapping[v]
        result[a].add(b)
        result[b].add(a)
    return result


def run(max_weight: int = 3, max_order: int = 21) -> dict:
    started = time.time()
    counts = {
        "atlas_graphs": 0,
        "connected_p5free_skeletons": 0,
        "weight_vectors": 0,
        "alpha_four": 0,
        "no_secure_five": 0,
    }
    best_secure_five_count = None
    best_example = None
    candidate = None

    for graph in nx.graph_atlas_g():
        if not (2 <= len(graph) <= 7):
            continue
        counts["atlas_graphs"] += 1
        if not nx.is_connected(graph):
            continue
        base = adjacency(graph)
        if induced_p5s(base):
            continue
        counts["connected_p5free_skeletons"] += 1
        indep = independent_masks(base)

        for weights in itertools.product(range(1, max_weight + 1), repeat=len(base)):
            if sum(weights) > max_order:
                continue
            counts["weight_vectors"] += 1
            if weighted_alpha(weights, indep) != 4:
                continue
            counts["alpha_four"] += 1
            blown = stable_blowup(base, weights)
            secure_five = secure_sets_of_size(blown, 5, stop_after=2)
            current_count = len(secure_five)
            if best_secure_five_count is None or current_count < best_secure_five_count:
                best_secure_five_count = current_count
                best_example = {
                    "skeleton_graph6": encode_graph6(len(base), edge_list(base)),
                    "weights": list(weights),
                    "order": len(blown),
                    "secure_five_examples_found_before_stop": secure_five,
                }
            if secure_five:
                continue
            counts["no_secure_five"] += 1
            edges = edge_list(blown)
            candidate = {
                "skeleton_graph6": encode_graph6(len(base), edge_list(base)),
                "weights": list(weights),
                "order": len(blown),
                "graph6": encode_graph6(len(blown), edges),
                "edges": [list(e) for e in edges],
                "brute_alpha": brute_alpha(blown)[0],
                "induced_p5_count": len(induced_p5s(blown)),
                "secure_six": secure_sets_of_size(blown, 6, stop_after=1),
            }
            break
        if candidate:
            break

    return {
        "scope": {
            "skeletons": "all graph-atlas connected induced-P5-free graphs of orders 2..7",
            "substitution": f"each vertex replaced by an independent set of size 1..{max_weight}",
            "maximum_result_order": max_order,
        },
        "counts": counts,
        "candidate": candidate,
        "best_example": best_example,
        "seconds": time.time() - started,
    }


if __name__ == "__main__":
    result = run()
    output = HERE / "atlas_stable_substitutions.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
