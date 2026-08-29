#!/usr/bin/env python3
"""Recompute the finite claims in proof_note.md and emit JSON."""

from __future__ import annotations

import json

import networkx as nx

from explore_operations import (
    alpha,
    bounded_compositions,
    gamma_s,
    gamma_s_bit,
    induced_p5_free,
    join_formula,
    join_graph,
    lex,
    secure_false_blowup_counts,
    weak_roman,
)


BASE_CODE = b"KtiSYtlXqwmT"


def atlas_join_audit() -> dict:
    graphs = [g for g in nx.graph_atlas_g() if 1 <= len(g) <= 5]
    checked = 0
    failures = []
    for g in graphs:
        for h in graphs:
            if len(g) + len(h) > 10:
                continue
            checked += 1
            actual = gamma_s(join_graph(g, h))
            predicted = join_formula(g, h)
            if actual != predicted:
                failures.append(
                    {
                        "g": nx.to_graph6_bytes(g, header=False).strip().decode(),
                        "h": nx.to_graph6_bytes(h, header=False).strip().decode(),
                        "actual": actual,
                        "predicted": predicted,
                    }
                )
    assert not failures
    return {"ordered_pairs": checked, "failures": failures}


def weak_roman_audit(base: nx.Graph) -> dict:
    value, witness = weak_roman(base)
    assert value == 4
    return {"value": value, "witness": witness}


def false_twin_audit(base: nx.Graph) -> dict:
    low_weight = {}
    for t in (2, 3, 4):
        by_weight = {}
        for weight in range(1, 4):
            vectors = list(bounded_compositions(weight, len(base), t))
            valid = sum(secure_false_blowup_counts(base, t, f) for f in vectors)
            assert valid == 0
            by_weight[str(weight)] = {"vectors": len(vectors), "valid": valid}
        low_weight[str(t)] = by_weight

    for t in (2, 3, 4, 5, 10):
        witness = (0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2)
        assert secure_false_blowup_counts(base, t, witness)
    return {
        "lower_bound_cases": low_weight,
        "universal_weight4_witness": [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2],
    }


def product_audit(base: nx.Graph) -> dict:
    cycle = nx.cycle_graph(5)
    rows = []
    for left, right, name, expected_alpha, expected_gamma in (
        (cycle, cycle, "C5[C5]", 4, 4),
        (base, cycle, "B[C5]", 6, 4),
        (cycle, base, "C5[B]", 6, 5),
    ):
        product = lex(left, right)
        gamma_value, witness = gamma_s_bit(product, expected_gamma)
        alpha_value = alpha(left) * alpha(right)
        assert alpha_value == expected_alpha
        assert gamma_value == expected_gamma
        rows.append(
            {
                "name": name,
                "order": len(product),
                "alpha": alpha_value,
                "gamma_s": gamma_value,
                "witness": witness,
            }
        )

    clique_checks = []
    for t in (2, 3):
        product = lex(base, nx.complete_graph(t))
        gamma_value, witness = gamma_s_bit(product, 4)
        assert gamma_value == 4
        clique_checks.append({"t": t, "gamma_s": gamma_value, "witness": witness})
    return {"products": rows, "true_twin_checks": clique_checks}


def small_lex_ratio_audit() -> dict:
    graphs = [
        g
        for g in nx.graph_atlas_g()
        if 2 <= len(g) <= 5 and nx.is_connected(g) and induced_p5_free(g)
    ]
    checked = 0
    equality = []
    cached = {
        nx.to_graph6_bytes(g, header=False).strip().decode(): (alpha(g), gamma_s(g))
        for g in graphs
    }
    for g in graphs:
        for h in graphs:
            if len(g) * len(h) > 15:
                continue
            checked += 1
            cg = nx.to_graph6_bytes(g, header=False).strip().decode()
            ch = nx.to_graph6_bytes(h, header=False).strip().decode()
            ag, sg = cached[cg]
            ah, sh = cached[ch]
            product = lex(g, h)
            ap = ag * ah
            sp, _ = gamma_s_bit(product, 8)
            if sp * 2 == ap * 3:
                equality.append((cg, ch, ap, sp))

    direct_increases = []
    for g in graphs:
        for h in graphs:
            if len(g) * len(h) > 15:
                continue
            cg = nx.to_graph6_bytes(g, header=False).strip().decode()
            ch = nx.to_graph6_bytes(h, header=False).strip().decode()
            ag, sg = cached[cg]
            ah, sh = cached[ch]
            ap = ag * ah
            sp, _ = gamma_s_bit(lex(g, h), 8)
            if sp * ag > sg * ap and sp * ah > sh * ap:
                direct_increases.append((cg, ch, ap, sp))
    assert not direct_increases
    return {
        "ordered_pairs": checked,
        "ratio_increases": direct_increases,
        "three_halves_products": equality,
    }


def main() -> None:
    base = nx.from_graph6_bytes(BASE_CODE)
    assert len(base) == 12
    assert alpha(base) == 3
    assert induced_p5_free(base)
    result = {
        "base": {"graph6": BASE_CODE.decode(), "order": len(base), "alpha": 3},
        "join_formula": atlas_join_audit(),
        "weak_roman": weak_roman_audit(base),
        "false_twin": false_twin_audit(base),
        "lexicographic": product_audit(base),
        "small_lex_ratio_audit": small_lex_ratio_audit(),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
