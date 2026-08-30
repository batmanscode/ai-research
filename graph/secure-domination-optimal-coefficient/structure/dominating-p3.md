# Dominating-path branch of the secure-domination problem

## Outcome

The remaining equality case can be closed.  Combined with the general
dominating-set completion lemma, this proves:

> **Theorem (dominating induced path).**  Let `G` be a connected
> induced-`P5`-free graph with independence number at least three.  If `G`
> has a dominating induced path `a-b-c`, then
> \[
> \gamma_s(G)\leq \alpha(G)+1.
> \]

The proof actually gives an explicit secure set in the only case not already
covered by the general completion lemma.  No novelty claim is made here
without a full literature review and human mathematical review.

## The equality lemma

Let

\[
D=\{a,b,c\},\qquad H=G-D,
\]

where `a-b-c` is an induced path and `D` dominates `G`.  Suppose

\[
\alpha(H)=\alpha(G)=q\geq3.
\]

For `u in H`, write

\[
\delta_D(u)=|N(u)\cap D|.
\]

Choose a maximum independent set `I` of `H` minimizing

\[
w_D(I)=\sum_{u\in I}\delta_D(u).
\]

Choose `x,y in I` whose sum `delta_D(x)+delta_D(y)` is as large as possible
among pairs in `I`, and put

\[
X=I\setminus\{x,y\},\qquad S=D\cup X.
\]

Then `S` is a secure dominating set.  In particular,

\[
|S|=3+(q-2)=q+1.
\]

### Proof

The set `S` dominates because it contains the dominating set `D`.  An attack
at a vertex adjacent to some member of `X` is defended by that member: after
the exchange, all vertices remain dominated by the untouched set `D`.

Assume for a contradiction that an attack `v` with no neighbor in `X` is not
defendable.  Put

\[
r=\delta_D(v),\qquad
m=\delta_D(x)+\delta_D(y).
\]

The domination of `D` gives `r>=1`. For every `d in N(v) intersect D`,
exchanging `d` for `v` fails. The removed path vertex `d` remains dominated
by another vertex of the path, so there is a vertex

\[
p_d\in (V(G)\setminus S)\setminus N[v]
\]

that is undominated after the exchange. It lies in `H` and is distinct from
`v`. Necessarily

\[
N(p_d)\cap S=\{d\},\qquad p_dv\notin E(G).
\]

Thus `p_d` has no neighbor in `X`, has `d` as its unique neighbor in `D`, and
is nonadjacent to `v`. Consequently

Witnesses for different path vertices are distinct: if `d != e`, one vertex
cannot have both `N(p_d) intersect S={d}` and
`N(p_e) intersect S={e}`.

\[
J_d=X\cup\{v,p_d\}
\]

is an independent set of `H` of order `q`.  The minimum-weight choice of `I`
therefore gives

\[
m\leq r+1. \tag{1}
\]

Every maximum independent set of `H` contains a neighbor in `H` of each of
`a`, `b`, and `c`: otherwise that missed path vertex could be added to obtain
an independent set of `G` of order `q+1`. Moreover, `I` cannot contain both an
`a`-only vertex and a `c`-only vertex.  Such two vertices are nonadjacent and,
together with `a-b-c`, would induce a `P5`.  It follows that `I` contains a
vertex with at least two neighbors in `D`.  Every vertex of `I` has at least
one neighbor in `D`, so the two largest `D`-degrees satisfy

\[
m\geq3. \tag{2}
\]

Since `r<=3`, (1) and (2) leave only `m=3` or `m=4`.

If `r=3`, consider the witnesses `p_b,p_c`.  They must be adjacent;
otherwise

\[
X\cup\{v,p_b,p_c\}
\]

would be an independent set of order `q+1`.  But then

\[
a-v-c-p_c-p_b
\]

is an induced `P5`: `v` sees all of `D`, each `p_d` sees only its named
vertex in `D`, and both witnesses are nonadjacent to `v`.  Hence `r` cannot
be three.  Equations (1) and (2) now force

\[
r=2,\qquad m=3. \tag{3}
\]

Because `x,y` have the two largest `D`-degrees in `I`, and every member of
`I` has positive `D`-degree, (3) says that `I` has exactly one vertex of
`D`-degree two and every other member of `I` has `D`-degree one. In
particular, `X` is nonempty (as `q>=3`) and every vertex of `X` is of
singleton attachment type.

There are three possibilities for `N(v) intersect D`.

1. Suppose it is `{a,c}`.  The witnesses `p_a,p_c` must be adjacent, since
   otherwise `X union {v,p_a,p_c}` is independent of order `q+1`. Choose any
   `z in X`. According as the unique neighbor of `z` in `D` is `a`, `b`, or
   `c`, one of

   \[
   c-p_c-p_a-a-z,\qquad
   z-b-a-p_a-p_c,\qquad
   a-p_a-p_c-c-z
   \]

   is an induced `P5`.

2. Suppose it is `{a,b}`.  If some `z in X` has unique `D`-neighbor `c`,
   then

   \[
   z-c-b-a-p_a
   \]

   is an induced `P5`.  Hence every vertex of `X` has singleton type `a` or
   `b`.  But the independent `q`-set

   \[
   J_a=X\cup\{v,p_a\}
   \]

   is then anticomplete to `c`.  Adding `c` produces an independent set of
   `G` of order `q+1`, a contradiction.

3. The case `{b,c}` is symmetric.  An `a`-type vertex of `X` produces the
   induced path `z-a-b-c-p_c`; without one, the independent set
   `J_c=X union {v,p_c}` is anticomplete to `a` and can be enlarged by `a`.

Every possible failed attack gives a contradiction.  Thus `S` is secure.
\(\square\)

## From the equality lemma to the branch theorem

For any dominating set `D` with `G-D` nonempty, the previously proved
completion lemma gives

\[
\gamma_s(G)\leq |D|+\alpha(G-D)-1.
\]

For a dominating `P3`, if `alpha(G-D)<=alpha(G)-1`, this is at most
`alpha(G)+1`. If equality holds and `alpha(G)>=3`, the lemma above gives the
same bound. Thus the entire dominating-induced-`P3` branch is closed.

The standard connected-`P5`-free structure theorem supplies either a
dominating clique or a dominating `P3`.  Consequently, the still-open
`gamma_s<=alpha+1` candidate is reduced to the dominating-clique branch
(and dominating cliques of order at most two are already handled by the
general completion lemma).

This does **not** disprove the published `3 alpha / 2` theorem.  It improves
the bound on one structural branch and leaves the clique-core branch as the
remaining obstacle.

## Independent checks and failed shortcuts

The constructive equality lemma was tested over the complete NetworkX Graph
Atlas.  Among graphs of independence number at least three there were 1,071
eligible `(G,D)` instances.  Across every minimum-weight maximum independent
set and every permitted top-degree pair, 1,991 constructed sets were checked
directly; all 1,991 were secure.  The checker uses the definition of secure
domination rather than the proof criterion.

For the complement of the icosahedral graph, all 240 choices produced across
60 equality-case dominating `P3` instances passed the construction. This
is an important stress test
because that graph has `(alpha,gamma_s)=(3,4)` and is tight for the new
`alpha+1` branch bound.

A separate seeded generator sampled 100,000 graphs through order 12 with a
fixed dominating induced `P3`. Of 35,273 induced-`P5`-free samples, 7,024 met
the equality hypothesis; all 14,659 permitted constructions were secure.
These finite checks exercise the construction but are not proof ingredients.

A clean-room referee used three different non-Atlas generators through order
20 and checked all 366,730 permitted constructions across 34,369 equality
paths, again with zero failures. Its independent counterexample SAT encoding
was UNSAT in all 42 parameter cases through order 14; those runs have no
retained traces and are reported only as corroboration.

Several simpler strengthenings are false and should not be reused:

- `I union {b}` need not be secure for a prescribed maximum independent set
  `I`; an alpha-three order-nine witness is graph6 `Hlydlad`.
- Equality does not force a dominating pair; an alpha-three order-eight
  witness is graph6 `Gma`qw`.
- A single added vertex need not repair the path: the alpha-four order-seven
  witness `FhGe?` has no secure set `D union {x}`. The analogous alpha-five
  witness `GhG`E?` occurs at order eight.
- For a prescribed maximum independent set, every set
  `D union (I minus {x,y})` can fail; an alpha-three order-eleven witness is
  graph6 `Jmz``[mLXr_`.  The minimum-weight choice of `I` in the theorem is
  therefore substantive, not cosmetic.

Each displayed witness was decoded and rechecked by direct predicates for
connectivity, induced-`P5`-freeness, independence number, domination, and
security.  The bounded SAT searches used to find them had no retained proof
traces, so the finite UNSAT frontiers are hypothesis-mining evidence rather
than proof ingredients.  The theorem above is independent of those solver
runs.

Two independent proof referees audited the replacement inequality, the
possibility that a witness equals one of the two omitted independent
vertices, every displayed induced path, and both enlargement contradictions.
Both returned `PASS` on the clean proof above.  One referee independently
repeated the complete Atlas audit and the icosahedral-complement stress test.

## Publication assessment

Mathematically, this is a genuine general theorem and a useful structural
reduction.  It is potentially suitable for a short note or as a theorem in
the larger optimal-coefficient project, subject to:

1. a conventional literature/novelty search;
2. line-by-line review by a human graph theorist;
3. integration with the already audited dominating-set completion lemma; and
4. a small standalone verifier retained with the research package.

The strongest framing is not that the original theorem is wrong.  It is that
the proposed coefficient-one-plus-additive-one bound is now proved on the
whole dominating-path side of the canonical `P5`-free structural split.

## Primary structural source

- G. Bacsó and Z. Tuza,
  [*Dominating cliques in \(P_5\)-free graphs*](https://doi.org/10.1007/BF02352694),
  *Periodica Mathematica Hungarica* 21 (1990), 303–308.
