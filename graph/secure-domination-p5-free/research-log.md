# Research log: what worked, what failed, and why

This is a concise methodological record, not a transcript of private model
reasoning.

## 1. The first strengthening

The published question asks whether the coefficient \(3/2\) can be improved
under connectivity. The first concrete candidate tested was
\(\gamma_s\leq\alpha\). Exhaustive enumeration of every unlabeled graph through
10 vertices found no violation among 381,716 eligible connected induced-
\(P_5\)-free graphs, making the candidate look plausible.

## 2. Structural reductions

Several reductions narrowed the search for a hypothetical minimum-order
counterexample. In
particular, cut vertices, universal vertices, complete joins, and reducible
true-twin structure can be removed from such a counterexample. This made the
remaining target 2-connected, co-connected, and structurally rigid.

These reductions are useful even though the coefficient-one statement turned
out to be false: they explain why small, decomposable constructions did not
work and why the first example is highly symmetric.

## 3. False proof routes caught by computation

- An arbitrary maximum independent set need not be secure.
- A dominating \(P_3\) need not itself provide a secure set.
- The tempting lemma “every dominating edge extends to a secure triple” is
  false. A 12-vertex witness killed it before it was used in a proof.
- Connecting copies of the tight disconnected \(C_5\) example generally
  lowers the ratio instead of preserving \(3/2\).

The role of these failures was productive: each one removed a broad but false
proof strategy before a long case analysis was built on it.

## 4. Targeted SAT search

Instead of enumerating every graph at order 12, a SAT model encoded:

1. connectivity;
2. induced-\(P_5\)-freeness;
3. \(\alpha=3\); and
4. failure of every triple to be secure.

The targeted SAT search returned graph6 `KtiSYtlXqwmT`. Recognition
identified it as the complement of the icosahedron. This was then discarded as
a solver-only result until a separate plain-set verifier reproduced every
substantive property.

## 5. Independent exact verification

The current verifier does not share SAT clauses or bit-mask routines. It
enumerates the relevant subsets directly and emits a witness for every failed
triple plus a complete defense map for a secure four-set. Symmetry compresses
the 220 triples into five orbits, but the machine-readable certificate keeps
all 220 cases.

## 6. Subsequent resolution

This counterexample establishes \(c_{\rm opt}\geq4/3\).  The sibling
`secure-domination-optimal-coefficient` project subsequently proves the
all-orders bound \(\gamma_s\leq\alpha+1\) for connected induced-\(P_5\)-free
graphs with \(\alpha\geq3\).  Hence \(c_{\rm opt}=4/3\) exactly.  The earlier
finite UNSAT searches were useful proof guidance but are not dependencies of
that theorem.
