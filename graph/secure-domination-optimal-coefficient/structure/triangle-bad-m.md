# Bad multi-neighbours at a dominating triangle

This note continues the dominating-triangle branch after the
[private-cross-edge theorem](triangle-private-cross-edge.md).  It proves three
all-orders results:

1. if the outside graph of any nonempty clique is induced-`C5`-free, the
   `alpha+1` bound follows by a one-hub lift; and
2. an exact bad-multi-neighbour completion replaces the entire multi-region
   by a smaller obstruction set; and
3. a global common-two lemma closes every private-budget value, proving the
   `alpha+1` bound for all connected induced-`P5`-free graphs with a
   dominating triangle and `alpha>=3`.

The global `alpha+1` candidate remains open only beyond the triangle branch.

## One-hub lift and the `C5`-free residual

> **One-hub lift.**  Let `K` be a nonempty clique of a graph `G`, put
> `H=G-K`, and suppose `H` is nonempty.  If `T` securely dominates `H`, then
> `T union {k}` securely dominates `G` for every `k in K`.

For an attack in `H-T`, use its defender in `T`; after the swap, `H` remains
dominated and `k` dominates `K`.  For an attack in `K-{k}`, use `k`; the
attacker then dominates the clique while `T` still dominates `H`.  These are
all possible attacks.

Degawa and Saito proved that every induced-`C5`-free graph `F` satisfies
`gamma_s(F)<=alpha(F)`.  Applying their theorem to `H` gives the following
lossless split.

> **`C5`-free residual corollary.**  If `K` is a nonempty clique of a graph
> `G` and `G-K` is induced-`C5`-free, then
> \[
> \gamma_s(G)\leq\alpha(G)+1.
> \]

When `H=G-K` is nonempty, choose `T` with
`|T|<=alpha(H)` and apply the lift:

\[
\gamma_s(G)\leq1+|T|\leq1+\alpha(H)\leq1+\alpha(G).
\]

If `H` is empty, `G=K` is a nonempty clique and one vertex is a secure
dominating set.  The lift itself needs no connectivity, domination, or
`P5`-free hypothesis on `K` or `G`.

## The bad-`M` completion

Let `G` now be induced-`P5`-free and let `K={a,b,c}` be an
inclusion-minimal dominating triangle.  For `k in K`, define

\[
P_k=\{v\notin K:N(v)\cap K=\{k\}\},
\]

and let `M` be the vertices outside `K` with at least two neighbours in `K`.
Inclusion-minimality makes every `P_k` nonempty.  We work after excluding the
private-cross-edge branch, so `P_a,P_b,P_c` are pairwise anticomplete.

Choose a maximum independent set `I_k` in each `P_k` and a vertex `x_k in
I_k`.  Put

\[
X=\bigcup_{k\in K}(I_k-\{x_k\}),\qquad
U_k=P_k\setminus N[X],
\]

where `N[X]` is the closed neighbourhood in `G`.  Each `U_k` is nonempty
(it contains `x_k`) and is a clique: two nonadjacent vertices in `U_k`,
together with `I_k-{x_k}`, would exceed `alpha(P_k)`.

Define

\[
B_X=\left\{v\in M:
N(v)\cap X=\varnothing\text{ and, for every }k\in N(v)\cap K,
U_k\nsubseteq N(v)
\right\}.
\]

We use the convention that the domination number of the empty graph is zero.

> **Bad-`M` completion lemma.**  If `Y` dominates `G[B_X]`, then
> `K union X union Y` is secure.  Consequently, with
> \(p=\sum_{k\in K}\alpha(P_k)\),
> \[
> \gamma_s(G)\leq p+\gamma(G[B_X]). \tag{BM}
> \]

**Proof.**  The selected set contains the dominating triangle.  If an
outside attacker has a neighbour in `X union Y`, that outside guard defends:
all of `K` remains selected after the exchange and continues to dominate the
graph.

Suppose the attacker has no such neighbour.  If it lies in `P_k`, it belongs
to the clique `U_k`.  The actual external private neighbours of hub `k` are
contained in `U_k`, so `k` defends the attack.  If the attacker lies in `M`,
it is not in `B_X`, because `Y` dominates `B_X`.  Some adjacent hub `k`
therefore satisfies `U_k subseteq N(v)`, and that hub defends.  The cases are
exhaustive.

Finally, `|K|+|X|=3+(p-3)=p`; taking a minimum dominating set of `B_X`
proves (BM).  `square`

Pairwise anticompleteness makes the union of the three `I_k` independent, so
`p<=alpha(G)`.  Thus every residual choice with

\[
\gamma(G[B_X])\leq\alpha(G)+1-p \tag{1}
\]

closes the branch.  In particular, an empty or nonempty-clique `B_X` is
enough.

## The tight private budget

> **Tight-budget theorem.**  Under the preceding hypotheses, if
> \[
> p=\sum_{k\in K}\alpha(P_k)=\alpha(G),
> \]
> then `B_X` is a clique for every permitted residual choice.  Hence
> \(\gamma_s(G)\leq\alpha(G)+1\).

We first record the attachment rule that makes the proof short.

> **Uniform attachment.**  If `m in B_X` has triangle-neighbourhood
> `{a,b}`, then `m` is anticomplete to `U_a,U_b` and complete to `U_c`.

Badness supplies `u in U_a-N(m)`.  If `m` had a neighbour `v in U_a`, then
`U_a` being a clique would make

\[
u-v-m-b-c
\]

an induced `P5`: the private type removes all edges from `u,v` to `b,c`,
while `um` and `mc` are absent.  Hence `m` is anticomplete to `U_a`, and
symmetrically to `U_b`.

No bad vertex sees all three hubs.  Otherwise, choosing one missed vertex
from each `U_k` and adding it to `X union {m}` gives an independent set of
order `p+1`.  A type-`{a,b}` bad vertex must be complete to `U_c`: if it
missed a vertex there, the same independent-set count using its badness
witnesses in `U_a,U_b` would again have order `p+1`.  This proves the rule.

Now two bad vertices of distinct hub types are adjacent.  Suppose instead
that `m` has type `{a,b}`, `n` has type `{a,c}`, and `mn` is absent.  For
arbitrary `u in U_b` and `v in U_c`, uniform attachment makes

\[
u-n-a-m-v
\]

an induced `P5`.  The nonconsecutive pairs are absent by the private types,
the two uniform anticompleteness statements, pairwise anticompleteness of the
private regions, and the assumed nonedge `mn`.

Therefore every independent set in `B_X` has one common hub type.  If
`m,n` were a nonadjacent same-type pair, say of type `{a,b}`, uniform
attachment would make both anticomplete to all of `U_a,U_b`.  For arbitrary
`u_a in U_a,u_b in U_b`,

\[
X\cup\{m,n,u_a,u_b\}
\]

would be independent of order `(p-3)+4=p+1`, contradicting
`p=alpha(G)`.  Hence `B_X` is a clique.  Applying (BM), with domination
number zero for an empty bad set and one for a nonempty clique, gives

\[
\gamma_s(G)\leq p+1=\alpha(G)+1.
\]

## Global common-two lemma

The tight proof has an equality-free form.

> **Seen-region anticompleteness.**  For every `m in B_X` and every hub
> `i in N(m) intersect K`, the vertex `m` is anticomplete to `U_i`.

By badness choose `u in U_i` missed by `m`, and suppose `m` sees some
`v in U_i`.  Since `U_i` is a clique, `uv` is an edge.  If `m` has exactly
two hub neighbours `{i,j}`, with third hub `k`, then

\[
u-v-m-j-k
\]

is induced: privacy removes all edges from `u,v` to `j,k`, while `um` and
`mk` are absent.  If `m` sees all three hubs, choose `j!=i` and a badness
witness `w in U_j-N(m)`.  Then

\[
u-v-m-j-w
\]

is induced; the two residual cliques lie in distinct pairwise-anticomplete
private regions, and privacy plus the chosen misses remove every chord.
Both cases contradict induced-`P5`-freeness.

> **Global common-two lemma.**  Every independent set `J` of `G[B_X]` has
> two distinct indices `r,s` for which `U_r` and `U_s` each contain a vertex
> anticomplete to all of `J`.

Call `U_i` failed if it has no such common witness.  Failure implies that
some `u_i in U_i` has a neighbour `m_i in J`.  Seen-region
anticompleteness says `m_i` cannot see hub `i`; since it is a
multi-neighbour vertex of a triangle, its exact hub type is `K-{i}`.

If two different cliques `U_i,U_j` failed, let `k` be the third hub.  The
corresponding `m_i,m_j` are nonadjacent because `J` is independent, and

\[
u_i-m_i-k-m_j-u_j
\]

is an induced `P5`.  Indeed, `u_i,u_j` have distinct private types;
`m_j` sees `i` and is therefore anticomplete to `U_i`; `m_i` sees `j` and
is anticomplete to `U_j`; and the private vertices miss hub `k`.  Thus at
most one residual clique fails.

Let `J` now be a maximum independent set of `G[B_X]`.  With common witnesses
`u_r,u_s`, the set

\[
X\cup J\cup\{u_r,u_s\}
\]

is independent: `J` misses `X` by the definition of `B_X`; the two witnesses
miss `J` and the closed neighbourhood of `X`; and distinct private regions
are anticomplete.  It has order `(p-3)+alpha(G[B_X])+2`.  Therefore

\[
\alpha(G[B_X])\leq\alpha(G)-p+1.
\]

A maximum independent set dominates its induced graph; with the conventions
`alpha(empty)=gamma(empty)=0`, this also covers an empty bad set.  Combining
the last inequality with (BM) yields

\[
\gamma_s(G)\leq p+\gamma(G[B_X])
\leq p+\alpha(G[B_X])\leq\alpha(G)+1. \tag{2}
\]

This proof is all-orders and has no computational dependency.

## Dominating-triangle theorem

> **Theorem.**  Let `G` be a connected induced-`P5`-free graph with
> `alpha(G)>=3`.  If `G` has a dominating triangle, then
> \[
> \gamma_s(G)\leq\alpha(G)+1.
> \]

Fix a dominating triangle `K`.  If some private region `P_i` is empty, the
other two hubs form a dominating pair, so the already proved dominating-pair
theorem applies.  If two distinct nonempty private regions have a cross edge,
the private-cross-edge theorem supplies a dominating induced `P3`, so the
dominating-path theorem applies.  Otherwise the private regions are nonempty
and pairwise anticomplete, and (2) proves the result.  The cases are
exhaustive.

## A discarded global packing shortcut

The direct attempt to pay for all of `gamma(M)` with an arbitrary independent
subset is false.  The graph6 instance

```text
I{OeEAg}?
```

has dominating triangle `K={0,1,2}`, pairwise-anticomplete singleton private
regions `{3},{4},{5}`, and multi-neighbour region `{6,7,8,9}`.  Exact checking
gives

\[
\alpha(G)=5,\quad \gamma_s(G)=4,\quad \gamma(G[M])=4,
\]

but the proposed packing value is only five instead of the required six.
This refutes the proof strategy, not the candidate bound.  Its outside graph
is `C5`-free, so the one-hub route gives a secure set of size six even though
the graph itself has a secure four-set.  The independent checker and retained
certificate make this failed route reproducible.

## Exact remaining global branch

Together with the Bacsó--Tuza dominating-clique-or-`P3` theorem and the
already solved dominating-pair and dominating-path cases, the result removes
every dominating clique of order at most three.  Any counterexample to the
global `alpha+1` candidate must now have an inclusion-minimal dominating
clique of order at least four.  This note does not claim that larger-clique
branch is solved.

## Reproduce and audit

- `../referees/triangle-bad-m-audit.md` is the independent line-by-line
  referee report.
- `../referees/triangle-global-common-two-audit.md` independently audits the
  all-orders common-two proof and theorem scope.
- `../referees/verify_triangle_bad_m.py` independently checks 11,473 residual
  constructions and includes explicit nonvacuous tight examples.
- `../referees/verify_triangle_global_common_two.py` checks the path templates,
  legacy finite abstraction, and 1,523 independent incidence instances.
- `../referees/verify_triangle_packing_obstruction.py` checks the discarded
  packing inequality witness by the definitions.
- The retained machine-readable outputs are in `../computation/results/`.

## Primary source

- S. Degawa and A. Saito,
  [*A note on secure domination in \(C_5\)-free graphs*](https://doi.org/10.1016/j.dam.2023.03.016),
  *Discrete Applied Mathematics* 333 (2023), 82--83.
