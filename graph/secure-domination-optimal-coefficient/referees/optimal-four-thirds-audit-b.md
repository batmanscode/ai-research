# Independent final-closure referee report

## Verdict

**PASS.**  Conditional on the already-passed pairwise-private theorem and
global cross-`Q` partition theorem, the new higher-order cross-edge argument
is airtight.  Together with the previously audited dominating-pair,
dominating-`P3`, and dominating-triangle branches and the Bacsó--Tuza
structure theorem, it proves

\[
\gamma_s(G)\leq\alpha(G)+1
\]

for every connected induced-`P5`-free graph with `alpha(G)>=3`.
Consequently the optimal multiplicative coefficient on this class is exactly
`4/3`.

I reconstructed the cross-edge proof without relying on its summary,
verified every induced-path chord and every domination class, and ran a
separate direct finite checker.  I found no missing case or counterexample.

## 1. Setup and accepted dependencies

Let

\[
K=\{k_1,\ldots,k_t\},\qquad t\geq4,
\]

be an inclusion-minimal dominating clique of an induced-`P5`-free graph.
For each hub define

\[
P_i=\{v\notin K:N(v)\cap K=\{k_i\}\}.
\]

Every `P_i` is nonempty.  Indeed, if `K-{k_i}` failed to dominate, its
missed vertex cannot be `k_i` because `K` is a clique of order at least two;
it is therefore an outside vertex whose only neighbour in `K` is `k_i`.

Let `M` consist of the outside vertices having at least two neighbours in
`K`.  The vertex set is partitioned by

\[
K,\quad P_1,\ldots,P_t,\quad M.
\tag{1}
\]

The accepted global cross-partition theorem supplies a partition of
`P=union_i P_i` into cross parts such that, whenever
`u in P_i,v in P_j` and `i!=j`,

\[
uv\in E(G)
\quad\Longleftrightarrow\quad
u,v\text{ belong to different cross parts}.
\tag{Q}
\]

No assertion about two vertices in the same `P_i` is used.

## 2. Third private regions see both endpoints

Fix a cross edge

\[
x\in P_i,\qquad y\in P_j,\qquad i\neq j,
\qquad xy\in E(G).
\tag{2}
\]

Let `z in P_l`, where `l notin {i,j}`.

First, `z` sees at least one of `x,y`.  If it missed both, then

\[
z-k_l-k_i-x-y
\]

would have the four displayed path edges.  Its six nonconsecutive pairs are

\[
zk_i,\ zx,\ zy,\ k_lx,\ k_ly,\ k_iy.
\]

The three private types remove the hub/private pairs and the hypothesis
removes `zx,zy`.  This is an induced `P5`, impossible.

Suppose now that `zy` is present but `zx` is absent.  Because `t>=4`, choose
a hub `k_h` with `h notin {i,j,l}`.  Then

\[
k_h-k_i-x-y-z
\]

has path edges `k_hk_i,k_ix,xy,yz`.  Its six nonconsecutive pairs are

\[
k_hx,\ k_hy,\ k_hz,\ k_iy,\ k_iz,\ xz.
\]

The first five are absent by the exact private types and distinct indices;
the last is the chosen miss.  The symmetric one-sided case is identical.
Therefore

> **Double-adjacency lemma.** Every vertex of every third private region is
> adjacent to both endpoints of a private cross edge.

The fourth hub is genuinely needed in the second step and is why this lemma
is stated only for `t>=4`.

## 3. Endpoint parts avoid the opposite endpoint regions

Let `A` be the cross part of `x` and `B` the cross part of `y`.  Equation
(Q) and `xy in E(G)` imply `A!=B`.

I verify

\[
A\cap P_j=\varnothing,
\qquad
B\cap P_i=\varnothing.
\tag{3}
\]

Suppose `z in A cap P_j`.  Choose an index `l` outside `{i,j}` and any
`w in P_l`, possible because the clique is inclusion-minimal.  The
double-adjacency lemma applied to `xy` gives

\[
wx,wy\in E(G).
\]

If `C` is the cross part of `w`, equation (Q) implies

\[
C\neq A,\qquad C\neq B.
\]

Since `z in P_j,w in P_l` have different private types and parts, (Q) makes
`zw` an edge.  Apply the double-adjacency lemma again to the cross edge
`zw`; the vertex `x in P_i` lies in a third private region, so the lemma
forces `xz in E(G)`.  But `x,z` belong to distinct private regions and the
same part `A`, so (Q) says `xz notin E(G)`.  This contradiction proves the
first assertion.  Interchanging the endpoint labels proves the second.

All uses of (Q) are between different private regions.  No within-region
adjacency is inferred.

An immediate consequence needed below is

\[
x\text{ is adjacent to every vertex of }P_j.
\tag{4}
\]

Indeed, (3) puts every member of `P_j` outside `A`, and (Q) then supplies
the edge to `x`.

## 4. Multi-neighbours are covered

Let `m in M` miss `k_i`.  I verify that `m` must see at least one of `x,y`.

Suppose it missed all three.  Since `m` has at least two clique neighbours,
there is a hub

\[
k_a\in N_K(m)-\{k_j\}.
\]

The index `a` differs from `j` by choice and from `i` because `m` misses
`k_i`.  Then

\[
m-k_a-k_i-x-y
\]

has its four displayed path edges.  Its six nonconsecutive pairs are

\[
mk_i,\ mx,\ my,\ k_ax,\ k_ay,\ k_iy.
\]

The first three are the assumed misses; the last three are absent by the
exact private types and the distinct indices.  This induced `P5` is
impossible.  Thus every member of `M` is either adjacent to `k_i` or to one
of the cross-edge endpoints.

The choice of `k_a` is valid even when `m` sees `k_j`: at least one of its
at least two clique neighbours is different from `k_j`.  If it misses
`k_j`, any clique neighbour may be chosen.

## 5. The forced dominating induced path

The set

\[
D=\{k_i,x,y\}
\]

induces the path `k_i-x-y`: the first two displayed edges are present and
`k_i y` is absent because `y` is private to `k_j`.

It dominates every class in (1):

- `k_i` dominates all of `K` and all of `P_i`;
- equation (4) says `x` dominates all of `P_j`;
- the double-adjacency lemma dominates every `P_l`,
  `l notin {i,j}`, by both `x` and `y`; and
- every member of `M` either sees `k_i`, or the result of Section 4 makes it
  see `x` or `y`.

These classes exhaust `V(G)`.  Therefore:

> **Higher-order private-cross-edge theorem.**  If an inclusion-minimal
> dominating clique of order at least four in an induced-`P5`-free graph has
> an edge between distinct private regions, that edge extends to a
> dominating induced `P3`.

The proof is all-orders and has no computational dependency.

## 6. Assembly of the global additive theorem

Let `G` now be connected, induced-`P5`-free, and have `alpha(G)>=3`.
The Bacsó--Tuza structure theorem supplies either a dominating induced `P3`
or a dominating clique.

- A dominating induced `P3` is covered by the previously audited
  dominating-path theorem.
- From a dominating clique, repeatedly delete a vertex while domination is
  preserved.  This produces an inclusion-minimal dominating subclique `K`.
- If `|K|<=2`, the general dominating-set residual completion gives
  `gamma_s(G)<=alpha(G)+1`.
- If `|K|=3`, the previously audited dominating-triangle theorem gives the
  same bound.
- Suppose `|K|>=4`.  If its private regions are pairwise anticomplete, the
  already-passed pairwise-private theorem applies.  Otherwise there is a
  private cross edge, Section 5 supplies a dominating induced `P3`, and the
  dominating-path theorem applies.

The alternatives are exhaustive.  Hence

\[
\boxed{\gamma_s(G)\leq\alpha(G)+1.}
\tag{5}
\]

No connected-residual minimal-counterexample argument, typed-cycle count,
or finite SAT frontier is needed in this assembly.

## 7. Sharp coefficient

For every integer `alpha>=3`,

\[
\alpha+1\leq\frac43\alpha.
\]

Equation (5) therefore gives the universal coefficient `4/3`.

The graph6 graph

```text
KtiSYtlXqwmT
```

is the complement of the icosahedral graph.  A fresh run of the project's
plain-set verifier reproduced

```text
order=12
connected=true
alpha=3
induced_p5_count=0
gamma_s=4
insecure 3-subsets=220
```

Thus its ratio is exactly `4/3`, and no smaller universal coefficient can
hold.  Combining the upper and lower bounds proves

\[
\boxed{c_{\mathrm{opt}}=\frac43.}
\]

This improves the published `3alpha/2` theorem; it does not refute or
contradict that valid weaker upper bound.

## 8. Independent finite stress audit

`verify_cross_edge_closure.py` reimplements induced-`P5` detection,
domination, the private partition, the global cross components, and all three
new local conclusions.  It does not import the author's closure checker.

The exact portion enumerates all 11,264 graphs consisting of a fixed `K4`,
one singleton in every private region, one arbitrary multi-neighbour with
every possible clique type and private adjacency mask, and every possible
edge set among the four private vertices.  A separate fixed-seed generator
adds larger private regions and clique orders four and five.  The retained
result is:

```text
PASS
exact_models=11264
random_p5free_cross_graphs=50 (from 7503 attempts)
p5free_cross_graphs=84
cross_edges=648
third_region_vertices=1497
part_exclusion_checks=1296
multi_missed_hub_checks=48
dominating_p3_checks=648
```

Every cross edge passed the direct dominating-`P3` predicate.  The
multi-neighbour and opposite-part checks are nonvacuous.  These finite
results corroborate the proof but are not used in Sections 2--7.

## Dependency verdict

The final conclusion is conditional on accepting these separately audited
inputs:

1. the Bacsó--Tuza dominating-clique-or-`P3` structure theorem;
2. the project’s dominating-set residual, dominating-`P3`, and
   dominating-triangle theorems;
3. the pairwise-private higher-order theorem; and
4. the global cross-`Q` partition theorem.

Starting from those inputs, the new cross-edge closure and the coefficient
calculation contain no gap.  **Final referee verdict: PASS.**
