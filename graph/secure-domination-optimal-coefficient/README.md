# The optimal secure-domination coefficient

This is the active continuation of the proved
[12-vertex counterexample](../secure-domination-p5-free/). It asks for the
best constant \(c\) such that every connected induced-\(P_5\)-free graph with
\(\alpha(G)\geq3\) satisfies

\[
\gamma_s(G)\leq c\,\alpha(G).
\]

## Current rigorous boundary

\[
\boxed{\frac43\leq c_{\mathrm{opt}}\leq\frac32}.
\]

The two endpoints come from different theorems:

- **Lower endpoint:** the complement of the icosahedral graph is connected,
  induced-\(P_5\)-free, and has \((\alpha,\gamma_s)=(3,4)\).
- **Upper endpoint:** Gupta, Henning, Maniya, and Pradhan proved
  \(\gamma_s\leq3\alpha/2\) for every induced-\(P_5\)-free graph.

The 12-vertex graph does not contradict the published upper bound:
\(4\leq9/2\). It refutes only the stronger coefficient-one proposal.

## A fully solved slice

Since \(\gamma_s\) is integral, the published theorem gives

\[
\alpha=3\quad\Longrightarrow\quad
\gamma_s\leq\left\lfloor\frac92\right\rfloor=4.
\]

The icosahedral complement attains four. Therefore the exact extremal value
for connected induced-\(P_5\)-free graphs with \(\alpha=3\) is **four**.

This is not an isolated witness. If \(B\) is the icosahedral complement and
\(B[K_t]\) replaces every vertex by a clique of size \(t\), then for every
\(t\geq1\)

\[
\alpha(B[K_t])=3,\qquad \gamma_s(B[K_t])=4.
\]

The \(t\geq2\) statement follows from the published lexicographic-product
formula and an exact weak-Roman calculation, independently audited in this
project. Thus the sharp \(4/3\) ratio already occurs in an infinite connected
family, although only at independence number three.

## High-value theorem/counterexample fork

The strongest live candidate is

\[
\gamma_s(G)\leq\alpha(G)+1.
\]

For \(\alpha\geq3\), this would imply
\(\gamma_s/\alpha\leq4/3\). The icosahedral complement would then make the
coefficient \(4/3\) sharp. A connected induced-\(P_5\)-free graph with
\(\gamma_s\geq\alpha+2\) would refute this route and become the next exact
counterexample target.

The first unresolved slice is \(\alpha=4\):

- a graph with \((\alpha,\gamma_s)=(4,6)\) proves \(3/2\) optimal;
- a proof that every such connected graph has \(\gamma_s\leq5\) is a genuine
  new theorem, but does not by itself settle all \(\alpha\).

## Equality restrictions inherited from the published proof

Any graph attaining \(\gamma_s=3\alpha/2\) must satisfy all of the following:

- \(\alpha\) is even;
- every maximum independent set begins with all its guards problematic in the
  augmentation proof;
- exactly \(\alpha/2\) augmentation steps occur and every step repairs exactly
  two problematic guards; and
- \(n\geq5\alpha/2\).

At minimum order the counting leaves exactly five vertices per exact-payment
pair and suggests paired induced-\(C_5\)-type obstruction cores. A complete
decomposition theorem has not been proved. The central structural question is
whether connectivity can join every allowable exact-payment configuration
without creating a guard saving.

## Computational boundary

A lossless SAT encoding found no connected induced-\(P_5\)-free graph with
\(\alpha=4\) and no secure five-set through order 17. The generalized encoding
also found no graph with \(\alpha=5\) and no secure six-set through order 16.
It fixes a maximum independent set by relabeling, enforces connectivity and
exact induced-\(P_5\)-freeness, and directly encodes failure of every candidate
set.

These are finite computational results, not all-orders theorems. For order 12
in both parameter slices, the experiment now retains complete CNF and DRUP
traces; an independent MapleSAT unit-propagation checker verifies every
retained addition and the final empty clause. The larger frontiers remain
solver results without retained proof traces. All orders have independent
direct-predicate and multi-solver checks, but no finite search can replace an
all-orders proof.

A second exact selector isolates the most promising structural subcase. When
the minimum dominating clique has size at least three, no graph with
`gamma_s > alpha` was found through order 15 for `alpha=4` or order 14 for
`alpha=5`. Those larger instances have no retained proof trace and remain
finite hypothesis-mining evidence.

## Structural leads

- Every connected induced-\(P_5\)-free graph with \(\alpha\geq3\) that has a
  dominating induced \(P_3\) satisfies \(\gamma_s\leq\alpha+1\). Together
  with the Bacsó–Tuza structure theorem, this reduces the global candidate to
  the dominating-clique branch.
- Every connected induced-\(P_5\)-free graph with a cut vertex satisfies
  \(\gamma_s\leq\alpha+1\). The proof gives an explicit secure set and
  shows that every counterexample to the candidate bound must be
  2-connected; this is an all-orders theorem, not a minimality assumption.
- For every dominating set \(D\) with nonempty outside graph,
  \(\gamma_s(G)\leq |D|+\min\{\gamma(G-D),\alpha(G-D)-1\}\). Hence every
  graph with a dominating pair satisfies \(\gamma_s\leq\alpha+1\); the
  dominating-edge branch is solved without a \(P_5\)-free assumption.
- Any connected counterexample to coefficient one must contain an induced
  claw, triangle, \(C_4\), \(C_5\), paw, \(P_3\cup P_1\), and
  \(K_2\cup2K_1\).
- A dominating induced \(C_5\) is itself a secure set.
- If \(\alpha\geq3\) and a dominating induced path \(a-b-c\) has both
  endpoints in a maximum independent set \(I\), then \(I\cup\{b\}\) is secure.
- External private-neighbor representatives of an inclusion-minimal
  dominating clique induce a complete multipartite graph.
- For a dominating clique \(K\), security of a set \(K\cup X\) is equivalent
  to an explicit residual-coverage condition on the vertices left
  undominated by \(X\). No cluster structure is assumed for a singleton
  private region; such a region can contain an induced \(C_5\).
- For an inclusion-minimal dominating clique \(K\), maximum-independent
  residual choices in its singleton-private regions plus a dominating set of
  the multi-\(K\)-neighbor region give the general bound recorded in
  [`structure/dominating-set-residual.md`](structure/dominating-set-residual.md).
  An infinite two-region family shows that charging those regions separately
  against \(\alpha\) can fail by an unbounded amount; cross-region exchanges
  are essential.
- When deleting a dominating clique leaves several components, rooted
  completions can be glued through a small set of clique guards.  The
  [component-gluing theorems](structure/clique-component-gluing.md) give the
  exact budgets \(\alpha(G-K)+|R|\) for mobile root covers and
  \(\alpha(G-K)+|R|-m\) when \(m\) components are assigned pairwise-disjoint
  reserved root blocks.  They close every configuration with
  \(|R|-m\leq\alpha(G)-\alpha(G-K)+1\).  For each clique vertex, at most one
  attached outside component can fail to be complete to it.
- If a dominating triangle has an edge between two distinct singleton-private
  regions, then the graph has a dominating induced \(P_3\).  The
  [triangle private-cross-edge theorem](structure/triangle-private-cross-edge.md)
  therefore closes that entire branch by the dominating-path theorem.  In the
  still-open triangle residue, the three singleton-private regions are
  pairwise anticomplete and every remaining cross-region interaction passes
  through vertices with at least two triangle neighbours.
- A multi-neighbour/private edge at a dominating triangle yields an induced
  \(P_3\) that dominates everything outside one private region.  The
  [multi-region absorption lemma](structure/triangle-multi-absorption.md)
  turns every such edge into a concrete independent-witness charge in that
  region; globally coupling those charges is still open.
- Joins, universal vertices, clique blow-ups, and the tested substitution
  families collapse rather than preserve the large ratio.

The remaining proof bottleneck is now entirely a collective packing/exchange
problem on the dominating-clique side of the standard connected-
\(P_5\)-free structural split.  For a triangle core, singleton-private
regions may be assumed pairwise anticomplete, so the unresolved coupling is
concentrated in the multi-neighbour region.  A minimum dominating clique of
size at most two already gives
\(\gamma_s\leq\alpha+1\) from the general
\(\gamma_s\leq\gamma+\alpha-1\) bound. Larger cliques require selecting
representatives that simultaneously cover all multi-clique-neighbor attacks
within the \(\alpha+1\) budget. Several simpler local statements are false;
their smallest checked obstructions are retained so the failed routes are not
repeated.

An earlier draft incorrectly claimed that every singleton private region of a
dominating clique is a cluster graph. The cone-\(C_5\) family in this package
contradicts that claim, and the faulty path argument overlooked chords from
the hub. The false sublemma and its component-selection consequence have been
removed; the exact residual-security criterion, which follows directly from
external private neighborhoods, is unaffected.

An exact infinite family makes the word “collective” essential: take a clique
of \(t\) hubs and attach a private induced \(C_5\) to each hub. Every maximum
independent set and every one-hub repair remains insecure on other blocks, yet
the whole graph satisfies \(\gamma_s=\alpha=2t\) through a simultaneous
exchange. The obstruction is to the proof strategy, not to the candidate
bound.

## Claim status

| Statement | Status |
|---|---|
| The extremal value at \(\alpha=3\) is four. | **Theorem**, by the published upper bound plus the exact witness. |
| No \(\alpha=4,\gamma_s=6\) graph exists through order 17. | **Finite SAT evidence**; order 12 has a checked clausal proof, larger orders are solver-only. |
| No \(\alpha=5,\gamma_s\geq7\) graph exists through order 16. | **Finite SAT evidence**; order 12 has a checked clausal proof, larger orders are solver-only. |
| A dominating pair implies \(\gamma_s\leq\alpha+1\). | **Theorem**, from the general dominating-set residual completion bound. |
| A cut vertex implies \(\gamma_s\leq\alpha+1\) in a connected induced-\(P_5\)-free graph. | **Theorem**, by the constructive rooted-completion argument. |
| A dominating induced \(P_3\) implies \(\gamma_s\leq\alpha+1\) when \(\alpha\geq3\). | **Theorem**, by the minimum-weight equality construction. |
| A clique-separator root cover with \(m\) disjoint saved blocks satisfies \(\gamma_s\leq\alpha(G-K)+|R|-m\). | **Theorem**, by rooted and residual completion gluing. |
| A private cross edge at a dominating triangle forces a dominating induced \(P_3\). | **Theorem**, by the induced-\(C_5\) witness argument and independent referee audit. |
| A multi/private edge at a dominating triangle leaves undominated vertices only in its source private region. | **Theorem**, by the multi-region absorption lemma. |
| Minimum dominating clique at least three implies \(\gamma_s\leq\alpha\). | **Open structural subclaim**; exact untraced SAT supports it through order 15 at \(\alpha=4\) and order 14 at \(\alpha=5\). |
| Connected graphs satisfy \(\gamma_s\leq\alpha+1\). | **Open candidate**, under active proof and counterexample attack. |
| \(4/3\leq c_{\mathrm{opt}}\leq3/2\). | **Theorem**, from the exact witness and the published upper bound. |
| The exact value of \(c_{\mathrm{opt}}\). | **Open.** It could be either endpoint or a value strictly between them. |

## Reproduce and audit

- [`computation/`](computation/) contains the generalized SAT encoder, direct
  verifier, retained order-12 CNF/DRUP proofs, finite result JSON, and exact
  reproduction instructions.
- [`referees/sat-audit.md`](referees/sat-audit.md) is an independent semantic
  and proof-trace audit. It passed the encoding with publication-wording
  corrections already applied here.
- [`structure/proof-fragments.md`](structure/proof-fragments.md) contains the
  proof-grade bad-cycle, dominating-cycle, dominating-path, and
  dominating-clique reductions.
- [`structure/dominating-set-residual.md`](structure/dominating-set-residual.md)
  proves the general dominating-set completion theorem and the solved
  dominating-pair branch. Its direct Atlas audit is
  [`referees/verify_dominating_set_residual.py`](referees/verify_dominating_set_residual.py).
- [`structure/cut-vertices.md`](structure/cut-vertices.md) proves the
  cut-vertex theorem. The constructive audit is
  [`referees/verify_cut_vertex.py`](referees/verify_cut_vertex.py), with a
  [separate exhaustive audit](referees/cut-vertex-audit.md) and seeded stress
  test beside it.
- [`structure/dominating-p3.md`](structure/dominating-p3.md) proves the
  dominating-path theorem. Its exact constructor audit is
  [`referees/verify_dominating_p3.py`](referees/verify_dominating_p3.py),
  with two [independent](referees/dominating-p3-audit-a.md)
  [referee notes](referees/dominating-p3-audit-b.md) and a seeded stress test
  beside it.
- [`structure/clique-component-gluing.md`](structure/clique-component-gluing.md)
  proves the root-cover, reserved-root, and disjoint-block gluing theorems for
  disconnected clique residuals.  Its direct Atlas/random checker is
  [`referees/verify_clique_component_gluing.py`](referees/verify_clique_component_gluing.py),
  and the independent proof review is
  [`referees/clique-component-gluing-audit.md`](referees/clique-component-gluing-audit.md).
- [`structure/triangle-private-cross-edge.md`](structure/triangle-private-cross-edge.md)
  proves that a private cross edge at a dominating triangle forces a
  dominating induced path.  Its direct Atlas checker is
  [`referees/verify_triangle_private_cross_edge.py`](referees/verify_triangle_private_cross_edge.py),
  the bounded corroborating SAT model is
  [`computation/triangle_private_cross_edge_sat.py`](computation/triangle_private_cross_edge_sat.py),
  and the clean-room proof audit is
  [`referees/triangle-private-cross-edge-audit.md`](referees/triangle-private-cross-edge-audit.md).
- [`structure/triangle-multi-absorption.md`](structure/triangle-multi-absorption.md)
  proves the local multi/private absorption lemma.  Its direct Atlas audit is
  [`referees/verify_triangle_multi_absorption.py`](referees/verify_triangle_multi_absorption.py).
- [`structure/private-clique-obstructions.md`](structure/private-clique-obstructions.md)
  proves the complete-multipartite private-witness lemma and records exact
  counterexamples to discarded shortcuts. Run
  `python structure/verify_obstructions.py` to check its finite claims.
- [`operations/proof-note.md`](operations/proof-note.md) proves the operation
  results, including the infinite \(B[K_t]\) family; the independent audit is
  [`referees/operations-audit.md`](referees/operations-audit.md).
- [`referees/structural-correction.md`](referees/structural-correction.md)
  documents the removed private-region cluster claim, its cone-\(C_5\)
  counterexample, the surviving exact criterion, and a dependency audit.

Install the SAT dependencies only when running the computational portfolio:

```bash
cd graph/secure-domination-optimal-coefficient/computation
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python test_encoding.py
```

The structural verifier uses only the Python standard library. Operation and
Graph Atlas referee checks additionally require NetworkX.

## Primary sources

- U. K. Gupta, M. A. Henning, P. V. Maniya, and D. Pradhan,
  [*Secure domination in \(P_5\)-free graphs*](https://doi.org/10.1016/j.disc.2025.114905),
  *Discrete Mathematics* 349(4) (2026), 114905.
- S. Degawa and A. Saito,
  [*A note on secure domination in \(C_5\)-free graphs*](https://doi.org/10.1016/j.dam.2023.03.016),
  *Discrete Applied Mathematics* 333 (2023), 82–83.
