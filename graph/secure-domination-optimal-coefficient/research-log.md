# Research log: the connected optimal coefficient

This is a concise methodological record. It distinguishes proved statements,
finite computation, failed constructions, and live conjectures.

## 1. Why this is a separate project

The sibling project proves a fixed 12-vertex counterexample to
\(\gamma_s\leq\alpha\). This project addresses the larger all-orders question:
whether the published coefficient \(3/2\) is optimal under connectivity or can
be reduced. Keeping them separate prevents an open search from obscuring a
finished theorem.

## 2. The exact α = 3 result

The published integer bound gives \(\gamma_s\leq4\) when \(\alpha=3\), and the
icosahedral complement attains four. Thus this complete slice is solved even
though the global coefficient is not.

## 3. Equality analysis

Tracing every inequality in the published augmentation algorithm shows that
equality at \(3\alpha/2\) requires even \(\alpha\), exactly \(\alpha/2\) repair
steps, and no step that repairs three or more problematic guards. Every guard
in the starting maximum independent set must have an external private
neighbor. Counting the independent set, those private neighbors, and the
distinct attack vertices gives \(n\geq5\alpha/2\).

For \(\alpha=4\), equality therefore needs two exact-payment groups. At the
minimum possible order the accounting suggests two induced-\(C_5\)-like cores,
and the disconnected graph \(2C_5\) realizes that pattern. This is not yet a
classification theorem: cross-edges and larger-order configurations remain to
be analyzed.

## 4. Construction routes tested

The following natural operations did not produce a connected equality graph:

- joining or adding a universal vertex to tight \(C_5\) pieces;
- clique and true-twin blow-ups;
- false-twin expansions;
- lexicographic products such as \(C_5[C_5]\);
- substitutions between \(C_5\) modules and the icosahedral complement;
- uniform attachments and small quotient/module products; and
- connected circulants through order 16.

The failure is informative. Dense joins lower the independence number or make
small secure sets possible; sparse links tend to create an induced \(P_5\).
Two exhaustive portfolios each tested 1,199,511 small-skeleton substitutions.
Among 69,769 stable-set blow-ups and 68,486 `K1`/`C5`/icosahedral-complement
substitutions in the target `alpha=4` slice, every graph had a secure five-set.
The only operation-stable connected gap-positive family found was the
icosahedral complement and its true-twin blow-ups, all with `alpha=3` and gap
one.

## 5. Exact computational search

The current SAT model asks for a connected induced-\(P_5\)-free graph with
\(\alpha=4\) and no secure set of size five. It found every instance
unsatisfiable through order 17. A generalized model found no
\(\alpha=5\) graph without a secure six-set through order 16. Order 12 in each
slice was repeated with three CDCL solvers, and 10,000 randomly fixed graphs
per slice were checked against a separate direct implementation with no
mismatch. Complete order-12 CNF and DRUP traces were additionally checked by a
different solver's unit-propagation engine through the final empty clause.

The result is deliberately labeled finite evidence. Order 12 is
proof-carrying; the larger-order UNSAT results do not preserve DRAT/LRAT traces.
The searches directly test the stronger candidate
\(\gamma_s\leq\alpha+1\) at its first two unresolved parameter slices.

An exact selector then isolated graphs whose minimum dominating clique has
size at least three. The stronger `gamma_s <= alpha` subclaim survived through
order 15 for `alpha=4` and order 14 for `alpha=5`. These runs are untraced
finite evidence. A positive `alpha=3` control recovered a checked
secure-domination obstruction with a dominating edge.

## 6. Proof routes that survived

- A dominating induced \(C_5\) is secure: any outside vertex with only one
  cycle neighbor would expose an induced \(P_5\), and the remaining attachment
  types permit an exchange.
- For \(\alpha\geq3\) and a dominating induced \(P_3=a-b-c\), if a maximum
  independent set contains \(a,c\), adding \(b\) produces a secure set of size
  \(\alpha+1\).
- Equality at \(\alpha=4\) would require two exact two-for-one payment steps;
  the resemblance to two \(C_5\) cores is a construction heuristic, not a
  proved decomposition.
- A connector meeting two anticomplete induced five-cycles partially creates
  an induced-\(P_5\) boundary obstruction; the remaining one-hub attachment
  cases have a secure four-set.
- Private representatives of an inclusion-minimal dominating clique induce a
  complete multipartite graph.
- Relative to a dominating clique, security reduces exactly to a collective
  residual-coverage condition. No cluster structure follows for a
  single-clique-neighbor region: the cone-`C5` family gives an immediate
  counterexample to that discarded shortcut.

## 7. False or incomplete routes

- “Every dominating edge extends to a secure triple” is false.
- “Every dominating \(P_3\) has endpoints in a common maximum independent set”
  is false.
- Choosing a more favorable maximum independent set does not guarantee that
  one Gupta-style augmentation repairs every bad vertex: an exact 11-vertex
  witness defeats that local strategy for all 25 of its maximum independent
  sets, despite satisfying \(\gamma_s=\alpha=4\) through a non-independent
  secure set.
- Adding one vertex from a dominating clique to a fixed maximum independent
  set can fail even in a biconnected graph with a dominating edge.
- Neither “a non-dominating \(C_5\) forces a dominating edge” nor “a
  \(P_5\)-free graph containing \(C_5\) has ordinary domination number at most
  three” is true. Exact 9- and 11-vertex witnesses refute the respective
  shortcuts while still satisfying \(\gamma_s\leq\alpha\).
- Arbitrary joins and substitutions do not preserve the desired ratio.
- Bounded UNSAT, even when exact, cannot establish an all-orders theorem.

The exact infinite family consisting of a clique of hubs with one private
cone-`C5` per hub explains why the local routes fail: every one-hub or one-cycle
repair leaves another block insecure. A simultaneous exchange gives
`gamma_s=alpha=2t`, so the family obstructs the proof method while supporting
the candidate bound.

## 8. Literature correction

A 2026 paper prints a coefficient-one theorem for all
\(\{P_5,\text{claw}\}\)-free graphs with \(\alpha\geq3\). The disconnected
statement is false: \(2C_5\) has \((\alpha,\gamma_s)=(4,6)\). Its proof does,
however, validly establish the connected claw-free version. Accordingly, any
connected coefficient-one counterexample must contain an induced claw. Future
citations must state this qualification explicitly.

## 9. Decision rule

The project upgrades a claim only when one of two things happens:

1. a construction is independently verified by a plain-set implementation and
   has a human-checkable certificate; or
2. a structural proof survives a separate line-by-line referee pass.

Everything else remains a conjecture, finite evidence, or a failed route.

## 10. Current stopping boundary

Independent proof, counterexample, operation, SAT, and referee tracks all
converged on the same conclusion: no counterexample to
`gamma_s <= alpha+1` was found, but the all-orders collective-selection lemma
was not proved. The separate project is therefore frozen as a reproducible
active-research milestone rather than promoted to a solved theorem.

## 11. Structural correction, 29 August 2026

During the continued proof search, the claimed cluster structure of each
singleton private region `P_k` was found to be false. If `a-b-c` is an
induced path inside `P_k`, the formerly displayed walk
`ell-k-a-b-c` has chords `kb` and `kc`; it is not an induced `P5`. In the
already verified cone-`C5` family, each `P_k` is itself a `C5`.

This correction removes the component-representative consequence but does
not affect the exact residual-security equivalence, the computational
frontiers, the coefficient interval, the alpha-three theorem, or the
operation results.
