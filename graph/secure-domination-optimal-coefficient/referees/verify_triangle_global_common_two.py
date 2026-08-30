#!/usr/bin/env python3
"""Independent audit for the triangle bad-set common-two argument.

This checker deliberately does not import the author's code.  It has three
parts:

1. mechanically audits every chord in the two induced-P5 templates used by
   the all-orders proof;
2. exhausts singleton representatives for U_0,U_1,U_2 and independent bad
   sets J of orders 1 through 5; and
3. independently reproduces the older 20-case triple-profile certificate.

The finite runs are sanity checks.  The all-orders conclusion rests on the
quantified proof audited in triangle-global-common-two-audit.md.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path


HUBS = range(3)
TYPES = (0b011, 0b101, 0b110, 0b111)


def edge_set(path: tuple[str, ...]) -> set[frozenset[str]]:
    return {frozenset((path[i], path[i + 1])) for i in range(len(path) - 1)}


def assert_exact_path(
    path: tuple[str, ...], present: set[frozenset[str]], absent: set[frozenset[str]]
) -> None:
    required = edge_set(path)
    nonconsecutive = {
        frozenset((path[i], path[j]))
        for i in range(5)
        for j in range(i + 2, 5)
    }
    assert required <= present, (path, "missing path edge", required - present)
    assert nonconsecutive <= absent, (path, "unchecked chord", nonconsecutive - absent)
    assert not (present & absent), (path, "edge both present and absent", present & absent)


def audit_path_templates() -> int:
    """Audit the two local path templates by their graph-theoretic reasons."""
    checks = 0

    # Seen-hub anticompleteness, two-hub type.  U_i is a clique, m sees i,j
    # and misses ell, and u misses m while v sees m.
    for i in HUBS:
        for j in HUBS:
            if j == i:
                continue
            ell = next(h for h in HUBS if h not in (i, j))
            path = ("u", "v", "m", f"k{j}", f"k{ell}")
            present = edge_set(path)
            absent = {
                frozenset(("u", "m")),          # chosen badness witness
                frozenset(("u", f"k{j}")),      # U_i is private to k_i
                frozenset(("u", f"k{ell}")),
                frozenset(("v", f"k{j}")),
                frozenset(("v", f"k{ell}")),
                frozenset(("m", f"k{ell}")),    # m has type {i,j}
            }
            assert_exact_path(path, present, absent)
            checks += 1

    # Seen-hub anticompleteness, all-three-hub type.  Badness at another
    # hub j supplies w in U_j missed by m.
    for i in HUBS:
        for j in HUBS:
            if j == i:
                continue
            path = ("u", "v", "m", f"k{j}", "w")
            present = edge_set(path)
            absent = {
                frozenset(("u", "m")),          # badness at i
                frozenset(("u", f"k{j}")),      # U_i private to i
                frozenset(("u", "w")),          # distinct private regions
                frozenset(("v", f"k{j}")),
                frozenset(("v", "w")),
                frozenset(("m", "w")),          # badness at j
            }
            assert_exact_path(path, present, absent)
            checks += 1

    # If U_i and U_j both fail for an independent J, choose adjacent
    # witnesses m_i of type K-{i} and m_j of type K-{j}; h is the third hub.
    for i, j in itertools.permutations(HUBS, 2):
        h = next(k for k in HUBS if k not in (i, j))
        path = (f"u{i}", f"m{i}", f"k{h}", f"m{j}", f"u{j}")
        present = edge_set(path)
        absent = {
            frozenset((f"u{i}", f"k{h}")),      # U_i private to i
            frozenset((f"u{i}", f"m{j}")),      # m_j sees i, hence misses U_i
            frozenset((f"u{i}", f"u{j}")),      # private regions anticomplete
            frozenset((f"m{i}", f"m{j}")),      # J independent
            frozenset((f"m{i}", f"u{j}")),      # m_i sees j, hence misses U_j
            frozenset((f"k{h}", f"u{j}")),      # U_j private to j
        }
        assert_exact_path(path, present, absent)
        checks += 1
    return checks


def is_induced_p5(vertices: tuple[int, ...], edges: set[frozenset[int]]) -> bool:
    degrees = {v: 0 for v in vertices}
    count = 0
    for x, y in itertools.combinations(vertices, 2):
        if frozenset((x, y)) in edges:
            count += 1
            degrees[x] += 1
            degrees[y] += 1
    if count != 4 or sorted(degrees.values()) != [1, 1, 2, 2, 2]:
        return False
    # A five-vertex graph with four edges and path degree sequence is P5.
    return True


def p5_free(order: int, edges: set[frozenset[int]]) -> bool:
    return not any(is_induced_p5(vs, edges) for vs in itertools.combinations(range(order), 5))


def singleton_abstract_audit(max_j: int = 5) -> list[dict[str, int]]:
    """Exhaust the core abstraction with one selected vertex per U_i.

    Vertices 0,1,2 are hubs; 3,4,5 are u_0,u_1,u_2.  J begins at 6.
    Edges from a member of J to U_i are forced absent whenever its type sees
    hub i by the proved seen-hub lemma.  A two-hub member may or may not see
    the one U at its missed hub.  These are all remaining incidence choices.
    """
    rows = []
    for j_size in range(1, max_j + 1):
        examined = p5free = failures = 0
        for types in itertools.combinations_with_replacement(TYPES, j_size):
            optional = [(member, hub) for member, typ in enumerate(types) for hub in HUBS if not (typ >> hub & 1)]
            for flags in range(1 << len(optional)):
                examined += 1
                edges: set[frozenset[int]] = set()
                # K is a triangle.
                for x, y in itertools.combinations(HUBS, 2):
                    edges.add(frozenset((x, y)))
                # Each u_i is private to hub i; distinct U regions are anti.
                for i in HUBS:
                    edges.add(frozenset((i, 3 + i)))
                # J is independent and has its fixed hub type.
                for member, typ in enumerate(types):
                    vertex = 6 + member
                    for hub in HUBS:
                        if typ >> hub & 1:
                            edges.add(frozenset((vertex, hub)))
                for bit, (member, hub) in enumerate(optional):
                    if flags >> bit & 1:
                        edges.add(frozenset((6 + member, 3 + hub)))
                order = 6 + j_size
                if not p5_free(order, edges):
                    continue
                p5free += 1
                good = 0
                for hub in HUBS:
                    if all(frozenset((3 + hub, 6 + member)) not in edges for member in range(j_size)):
                        good += 1
                if good < 2:
                    failures += 1
        assert failures == 0
        rows.append({"J_size": j_size, "abstract_instances": examined, "p5free_instances": p5free, "common_two_failures": failures})
    return rows


def legacy_triple_certificate() -> list[dict[str, object]]:
    """Independent reproduction of the older 20-profile finite result."""
    profiles = []
    # A failed U has no all-zero pattern and is nonempty.  A profile records
    # which of the seven nonzero labelled J-neighbourhoods occur.
    for family_mask in range(1, 1 << 7):
        profiles.append(tuple(pattern for pattern in range(1, 8) if family_mask >> (pattern - 1) & 1))

    def allowed(profile: tuple[int, ...], hub: int, types: tuple[int, ...]) -> bool:
        for member, typ in enumerate(types):
            if not (typ >> hub & 1):
                continue
            if typ.bit_count() == 2:
                if any(pattern >> member & 1 for pattern in profile):
                    return False
            else:
                if all(pattern >> member & 1 for pattern in profile):
                    return False
        return True

    def orientation(profile: tuple[int, ...], miss: int, see: int) -> bool:
        return any(not (pattern >> miss & 1) and (pattern >> see & 1) for pattern in profile)

    rows = []
    multisets = list(itertools.combinations_with_replacement(TYPES, 3))
    assert len(multisets) == 20
    assert {tuple(sorted(t)) for t in itertools.product(TYPES, repeat=3)} == set(multisets)
    for types in multisets:
        left = [profile for profile in profiles if allowed(profile, 0, types)]
        right = [profile for profile in profiles if allowed(profile, 1, types)]
        survivors = 0
        for first in left:
            for second in right:
                forbidden = False
                for m, n in itertools.permutations(range(3), 2):
                    if not (types[m] >> 2 & 1 and types[n] >> 2 & 1):
                        continue
                    if orientation(first, m, n) and orientation(second, n, m):
                        forbidden = True
                        break
                if not forbidden:
                    survivors += 1
        rows.append({"types": list(types), "U0_candidate_profiles": len(left), "U1_candidate_profiles": len(right), "survivors": survivors})
    assert all(row["survivors"] == 0 for row in rows)
    return rows


def main() -> None:
    project = Path(__file__).resolve().parents[1]
    retained = json.loads(
        (project / "computation" / "results" /
         "triangle_common_two_legacy_profile.json").read_text()
    )
    legacy = legacy_triple_certificate()
    assert legacy == retained["rows"]
    result = {
        "status": "PASS",
        "path_template_checks": audit_path_templates(),
        "singleton_abstract_rows": singleton_abstract_audit(),
        "legacy_type_multisets": len(legacy),
        "legacy_rows_match_retained_json": True,
        "note": "Finite checks support but do not replace the all-orders proof.",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
