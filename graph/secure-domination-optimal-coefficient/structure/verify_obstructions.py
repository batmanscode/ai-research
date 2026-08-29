#!/usr/bin/env python3
"""Independent plain-set verification of the structural obstructions in NOTES.md."""
from itertools import combinations
import json


def decode_graph6(g):
    n = ord(g[0]) - 63
    bits = []
    for ch in g[1:]:
        value = ord(ch) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adj = [0] * n
    pos = 0
    for j in range(1, n):
        for i in range(j):
            if bits[pos]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            pos += 1
    return adj


def dominates(adj, S):
    covered = S
    for u in range(len(adj)):
        if S >> u & 1:
            covered |= adj[u]
    return covered == (1 << len(adj)) - 1


def secure(adj, S):
    if not dominates(adj, S):
        return False
    for v in range(len(adj)):
        if S >> v & 1:
            continue
        if not any((adj[v] >> u & 1) and
                   dominates(adj, (S & ~(1 << u)) | (1 << v))
                   for u in range(len(adj)) if S >> u & 1):
            return False
    return True


def gamma_s(adj):
    for k in range(1, len(adj) + 1):
        for C in combinations(range(len(adj)), k):
            S = sum(1 << v for v in C)
            if secure(adj, S):
                return k, C
    raise AssertionError


def alpha(adj):
    for k in range(len(adj), 0, -1):
        for C in combinations(range(len(adj)), k):
            if all(not (adj[u] >> v & 1) for u, v in combinations(C, 2)):
                return k, C
    raise AssertionError


def connected(adj, removed=None):
    vertices = [v for v in range(len(adj)) if v != removed]
    if not vertices:
        return True
    seen = 1 << vertices[0]
    todo = seen
    allowed = ((1 << len(adj)) - 1) & ~(0 if removed is None else 1 << removed)
    while todo:
        bit = todo & -todo
        todo ^= bit
        v = bit.bit_length() - 1
        new = adj[v] & allowed & ~seen
        seen |= new
        todo |= new
    return seen == allowed


def induced_c5(adj, C):
    S = sum(1 << v for v in C)
    return all((adj[v] & S).bit_count() == 2 for v in C)


def p5_free(adj):
    for C in combinations(range(len(adj)), 5):
        S = sum(1 << v for v in C)
        degrees = sorted((adj[v] & S).bit_count() for v in C)
        if degrees == [1, 1, 2, 2, 2]:
            # This degree sequence plus connectedness characterizes P5 here.
            first = C[0]
            seen = 1 << first
            todo = seen
            while todo:
                bit = todo & -todo
                todo ^= bit
                v = bit.bit_length() - 1
                new = adj[v] & S & ~seen
                seen |= new
                todo |= new
            if seen == S:
                return False
    return True


def all_induced_c5s(adj):
    return [C for C in combinations(range(len(adj)), 5) if induced_c5(adj, C)]


def verify_c5_shortcut_counterexample():
    adj = decode_graph6("HhfUgCC")
    cycles = all_induced_c5s(adj)
    return {
        "graph6": "HhfUgCC",
        "n": len(adj),
        "connected": connected(adj),
        "p5_free": p5_free(adj),
        "alpha": alpha(adj),
        "gamma_s": gamma_s(adj),
        "dominating_vertex": any(dominates(adj, 1 << u) for u in range(len(adj))),
        "dominating_edge_or_pair": any(dominates(adj, (1 << u) | (1 << v))
                                       for u, v in combinations(range(len(adj)), 2)),
        "induced_c5s": cycles,
        "dominating_induced_c5s": [C for C in cycles if dominates(
            adj, sum(1 << v for v in C))],
    }


def verify_biconnected_fixed_choice_counterexample():
    adj = decode_graph6("LkdB{DEaseKoWg")
    I = (9, 10, 11, 12)
    Imask = sum(1 << v for v in I)
    return {
        "graph6": "LkdB{DEaseKoWg",
        "n": len(adj),
        "connected": connected(adj),
        "biconnected": all(connected(adj, removed=v) for v in range(len(adj))),
        "p5_free": p5_free(adj),
        "alpha": alpha(adj),
        "gamma_s": gamma_s(adj),
        "fixed_I": I,
        "dominating_vertex": any(dominates(adj, 1 << u) for u in range(len(adj))),
        "edge_01_dominates": dominates(adj, 0b11),
        "I_plus_0_secure": secure(adj, Imask | 1),
        "I_plus_1_secure": secure(adj, Imask | 2),
    }


def cone_c5_family(t):
    n = 6 * t
    adj = [0] * n
    def add(u, v):
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    for i, j in combinations(range(t), 2):
        add(i, j)
    for i in range(t):
        C = list(range(t + 5 * i, t + 5 * i + 5))
        for j in range(5):
            add(C[j], C[(j + 1) % 5])
        for v in C:
            add(i, v)
    return adj


def verify_cone_family_instance(t=3):
    adj = cone_c5_family(t)
    return {
        "t": t,
        "n": len(adj),
        "connected": connected(adj),
        "p5_free": p5_free(adj),
        "alpha": alpha(adj),
        "gamma_s": gamma_s(adj),
    }


if __name__ == "__main__":
    results = {
        "c5_shortcut_counterexample": verify_c5_shortcut_counterexample(),
        "biconnected_fixed_choice_counterexample":
            verify_biconnected_fixed_choice_counterexample(),
        "three_cone_c5_modules": verify_cone_family_instance(3),
    }
    assert results["c5_shortcut_counterexample"]["connected"]
    assert results["c5_shortcut_counterexample"]["p5_free"]
    assert not results["c5_shortcut_counterexample"]["dominating_edge_or_pair"]
    assert not results["c5_shortcut_counterexample"]["dominating_induced_c5s"]
    assert results["biconnected_fixed_choice_counterexample"]["biconnected"]
    assert results["biconnected_fixed_choice_counterexample"]["edge_01_dominates"]
    assert not results["biconnected_fixed_choice_counterexample"]["dominating_vertex"]
    assert not results["biconnected_fixed_choice_counterexample"]["I_plus_0_secure"]
    assert not results["biconnected_fixed_choice_counterexample"]["I_plus_1_secure"]
    assert results["three_cone_c5_modules"]["alpha"][0] == 6
    assert results["three_cone_c5_modules"]["gamma_s"][0] == 6
    print(json.dumps(results, indent=2))
