# Bad multi-neighbours at a dominating triangle

This note continues the dominating-triangle branch after the
[private-cross-edge theorem](triangle-private-cross-edge.md).  It proves two
all-orders reductions:

1. if the outside graph of any nonempty clique is induced-`C5`-free, the
   `alpha+1` bound follows by a one-hub lift; and
2. in the unresolved triangle branch, the case in which the three private
   regions already account for all of `alpha(G)` satisfies the bound.

Neither statement solves the remaining loose-budget, `C5`-bearing residue.

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

## Exact remaining triangle residue

After these results, a counterexample in the dominating-triangle branch must
satisfy all of the following:

- the singleton-private regions are nonempty and pairwise anticomplete;
- `H=G-K` contains an induced `C5`;
- `p<=alpha(G)-1`; and
- for every permitted choice of the `I_k,x_k`, inequality (1) fails.

The live question is therefore no longer arbitrary coupling through all of
`M`: it is whether the independence gain outside the private regions can pay
for the domination number of the much smaller bad set `B_X`, in a residual
that necessarily contains an induced `C5`.

## Reproduce and audit

- `../referees/triangle-bad-m-audit.md` is the independent line-by-line
  referee report.
- `../referees/verify_triangle_bad_m.py` independently checks 11,473 residual
  constructions and includes explicit nonvacuous tight examples.
- `../referees/verify_triangle_packing_obstruction.py` checks the discarded
  packing inequality witness by the definitions.
- The retained machine-readable outputs are in `../computation/results/`.

## Primary source

- S. Degawa and A. Saito,
  [*A note on secure domination in \(C_5\)-free graphs*](https://doi.org/10.1016/j.dam.2023.03.016),
  *Discrete Applied Mathematics* 333 (2023), 82--83.
