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

## 10. Previous checkpoint boundary

At the first reproducible checkpoint, independent proof, counterexample,
operation, SAT, and referee tracks had found no counterexample to
`gamma_s <= alpha+1`, but had not proved the all-orders collective-selection
lemma.  Sections 11 onward record the continuing work past that checkpoint;
the project is active, not frozen, and no open candidate is promoted to a
theorem without a complete proof.

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

## 12. Dominating-set residual completion

A replacement argument proved the general bound

`gamma_s(G) <= |D| + alpha(G-D) - 1`

for every dominating set `D` with nonempty outside graph. Choose a maximum
independent set outside `D` and omit one member; the still-undominated
outside residual must be a clique, which makes every attack defendable. The
construction was then checked directly over the complete Graph Atlas.

A complementary construction takes a dominating set of `G-D` instead. It
gives `gamma_s(G) <= |D| + gamma(G-D)` because every attack then has an
added guard as a defender while `D` remains intact. Another 163,903 direct
Atlas constructions passed. The combined minimum of the domination and
independence-residual terms is the useful working bound.

Consequently, every graph with a dominating pair satisfies
`gamma_s <= alpha+1`. This closes the dominating-edge branch that repeatedly
appeared in the finite obstruction mining. It does not close the full
candidate: larger dominating cores still require a collective replacement
or a sharper global accounting argument.

A clique-specific refinement constructs a secure set of size

`sum_k alpha(G[P_k]) + gamma(G[M])`,

where `M` is the outside region with multiple clique neighbors. It passed
5,830 direct constructions across every minimal dominating clique in the
Graph Atlas. A complete-bipartite two-private-region family disproves the
tempting next inequality that the sum of private-region independence numbers
is at most `alpha+1`; its gap is unbounded even though a cross-region secure
four-set keeps the target bound true. Future work must exploit those cross
edges rather than budget each private region independently.

## 13. Cut-vertex theorem

The earlier minimal-counterexample reduction has been replaced by a stronger
all-orders theorem: every connected induced-`P5`-free graph with a cut vertex
satisfies `gamma_s <= alpha+1`. At an articulation `x`, at most one component
of `G-x` can contain a nonneighbor of `x`. The deep component has no induced
`P4` rooted at `x`, forcing every first-layer vertex to be complete or
anticomplete to each second-layer component.

That module structure supports an explicit anchor-group construction. It
builds a secure set on the deep side within its independence budget and keeps
the side dominated even if the articulation guard moves. Maximum independent
sets on the shallow components then glue without defender conflicts. The
construction passed every relevant Graph Atlas articulation choice and a
seeded random stress portfolio. A separate implementation checked 5,001
proof-permitted choices over 2,196 rooted Atlas instances. Therefore every
counterexample to the candidate bound must be 2-connected.

## 14. Dominating-path theorem

The whole dominating-induced-`P3` branch is now closed for `alpha>=3`. The
general residual bound handles `alpha(G-D)<=alpha(G)-1`. In the equality
case, choose a maximum independent set of `G-D` minimizing total attachment
degree into the three-vertex path, omit its two highest-attachment members,
and retain the path. Any failed attack creates singleton-attachment witnesses
and an alternative maximum independent set. Minimum weight forces a short
degree inequality; induced-`P5`-freeness eliminates every remaining equality
pattern.

The exact construction passed 1,991 complete-Atlas choices, 240 choices on
the tight icosahedral complement, and 14,659 constructions in a 100,000-trial
seeded stress test. Fresh clean-room referees independently checked the
witness bookkeeping, weight inequality, all induced-path chord exclusions,
and enlargement contradictions.

By the Bacsó–Tuza theorem, every connected induced-`P5`-free graph has a
dominating clique or a dominating induced `P3`. The `alpha+1` candidate is
therefore reduced to dominating cliques; orders one and two are already
closed by the general completion theorem. The sole remaining structural core
is a dominating clique of order at least three.

## 15. Clique-component gluing

Let `K` be a dominating clique and let `H=G-K` have at least two connected
components.  Three all-orders gluing theorems now convert attachment covers
into explicit secure dominating sets.  A mobile root cover `R` costs at most
`alpha(H)+|R|`.  If designated components are dominated by pairwise-disjoint
reserved root blocks and the other components use only mobile roots, each
designated component saves one guard, giving

`gamma_s(G) <= alpha(H)+|R|-m`,

where `m` is the number of saved components.  Since a clique changes
independence by only `Delta=alpha(G)-alpha(H) in {0,1}`, every such cover with
`|R|-m<=Delta+1` proves the target `alpha+1` bound.

The proof uses the rooted completion from the cut-vertex theorem.  A clique
root touching two outside components cannot start an induced rooted `P4`, or
a neighbor in the second component would extend it to an induced `P5`.
Rootless local domination then prevents shared-root failures.  The reserved
blocks use the general residual-completion theorem and are kept immobile for
all other components.  A further structural lemma shows that each fixed
clique vertex is incomplete to at most one outside component to which it
attaches.

A clean-room referee passed every exchange and edge case.  The direct checker
found zero failures among 21,942 basic, 25,495 one-saving, 37,947 singleton-
block, and 57,722 general block constructions in the complete Graph Atlas,
plus 267,692 corresponding randomized constructions.  These counts validate
the constructions but are not proof ingredients.  The remaining disconnected
clique branch is therefore an explicit attachment-hypergraph obstruction:
every low-mobile root cover and disjoint saved-block system must fail its
budget inequality.

## 16. Triangle private-region reductions

Fix a dominating triangle `K={a,b,c}` and write `P_a,P_b,P_c` for vertices
whose unique neighbour on `K` is the indicated hub.  A new all-orders theorem
shows that an edge between two distinct private regions forces a dominating
induced `P3`.  The proof starts with a private cross edge, repeatedly turns a
hypothetical missed path into an induced `C5`, and uses anticomplete cycle
witnesses to force a final induced `P5`.  The independently refereed proof
therefore closes this branch through the already proved dominating-path
theorem.

The unresolved triangle core can consequently assume that `P_a,P_b,P_c` are
pairwise anticomplete.  Its remaining interactions pass through `M`, the
vertices adjacent to at least two hubs.  A second lemma handles one such
interaction: if `m in M_{ij}` sees `y in P_i`, then `y-m-k_j` is an induced
path that dominates everything outside `P_i`.  When dominating paths have
already been excluded, this forces an independent witness in `P_i` missed by
both `m` and `y`.

Direct Graph Atlas checks passed all 521 private-cross-edge instances and all
1,277 multi/private tuples.  A separate CNF model forbidding every dominating
induced `P3` in the cross-edge setting was UNSAT through order 14; those
untraced runs are finite corroboration only.  The remaining task is global:
combine the local independent-witness charges across `M` without double
counting, or exploit the alternative one-hub residual completion when the
naive charge is insufficient.
