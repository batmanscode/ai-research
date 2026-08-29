# Dominating-set residual completion

This note records a general secure-domination lemma obtained while repairing
the dominating-clique branch. It does not use induced-`P5`-freeness.

## Theorem

Let `D` be a dominating set of a graph `G`, and suppose `G-D` is nonempty.
Then

\[
\gamma_s(G)\leq |D|+\alpha(G-D)-1.
\]

More explicitly, if `I` is any maximum independent set of `G-D` and
`x` is any member of `I`, then

\[
S=D\cup(I\setminus\{x\})
\]

is a secure dominating set of `G`.

### Proof

Put `X=I\setminus\{x\}` and

\[
R=V(G-D)\setminus N_{G-D}[X].
\]

The set `R` is a clique. Otherwise two distinct nonadjacent vertices `v,w`
of `R` would make `X\cup\{v,w\}` an independent set of `G-D` larger than
`I`.

The set `S` dominates because it contains `D`. Consider an attack at a
vertex `v` outside `S`.

- If `v` has a neighbor `y` in `X`, then `y` defends `v`. Every vertex of
  `G` already has a neighbor in `D`, so `y` has no external private neighbor
  relative to `S`; after the swap, `y` itself is dominated by `v`.
- Otherwise `v` lies in `R`. Choose a neighbor `d` of `v` in `D`. Every
  external private neighbor of `d` relative to `S` has no neighbor in `X`,
  and therefore lies in `R`. Since `R` is a clique, `v` is adjacent to all
  of those vertices other than possibly itself. Thus replacing `d` by `v`
  preserves domination.

Every outside attack has a valid defender, so `S` is secure. Its order is
`|D|+|I|-1`, proving the bound. \(\square\)

## Consequences for the open problem

1. If `G` has domination number at most two, then

   \[
   \gamma_s(G)\leq\alpha(G)+1.
   \]

   In particular, the entire dominating-edge branch is solved. This is a
   theorem for arbitrary graphs, not merely induced-`P5`-free graphs.
2. If `D` is a dominating set of order three and
   `alpha(G-D)<=alpha(G)-1`, the same candidate bound follows.
3. The icosahedral-complement witness has a dominating edge and
   `(alpha,gamma_s)=(3,4)`, so the corollary is tight.

The theorem is not the full solution. A connected induced-`P5`-free graph
may have no dominating pair, and a dominating clique supplied by the usual
structure theorem may have more than two vertices. The remaining proof must
either control the residual independence number more sharply or replace
several core guards collectively.

## A dominating-clique refinement

Let `K` be an inclusion-minimal dominating clique with `|K|>=2`. Define

\[
P_k=\{v\notin K:N(v)\cap K=\{k\}\}
\]

and let `M` contain the outside vertices with at least two neighbors in `K`.
Then

\[
\gamma_s(G)\leq
\sum_{k\in K}\alpha(G[P_k])+\gamma(G[M]).
\]

Indeed, every `P_k` is nonempty by inclusion-minimality. In each region take
a maximum independent set and omit one member; its closed-neighborhood
residual is a clique by the same argument as above. Add a minimum dominating
set of `G[M]`. Added guards have empty external private neighborhoods because
`K` already dominates. An attack with an added neighbor is therefore safe;
an attack without one lies in a unique `P_k`, whose residual clique makes
`k` a valid defender. Counting cancels the `|K|` clique guards against the
one omitted vertex in every nonempty private region.

This refinement also needs no `P5`-free assumption. It recovers the optimum
`gamma_s=alpha` construction for the clique-of-hubs with one private induced
`C5` at each hub.

### A failed accounting shortcut

The right-hand side cannot be bounded by `alpha+1` region by region. For
`m>=3`, let `K={a,b}`, let `A` and `B` be independent `m`-sets, and add the
edges `ab`, all edges from `a` to `A`, all edges from `b` to `B`, and every
edge between `A` and `B`. This graph is connected and induced-`P5`-free,
`K` is an inclusion-minimal dominating clique, and

\[
\alpha(G)=m+1,
\qquad
\alpha(G[P_a])+\alpha(G[P_b])=2m.
\]

Thus the separate-region excess over `alpha+1` is unbounded. The candidate
bound itself is not threatened: for `x in A` and `y in B`, the four-set
`{a,b,x,y}` is secure. Cross-region edges create the guard saving that
independent local accounting misses.

## Verification

[`../referees/verify_dominating_set_residual.py`](../referees/verify_dominating_set_residual.py)
checks the displayed construction directly for every dominating set, every
maximum independent set of its outside graph, and every omitted independent
vertex in the complete NetworkX Graph Atlas. It also checks all 5,830 local
choices produced by the clique refinement over 2,425 inclusion-minimal
dominating cliques. It does not call either residual argument when testing
security.

The maximum-independent residual observation is closely related to standard
external-private-neighborhood lemmas in secure-domination theory. No novelty
claim is made here without a broader literature review; the theorem is used
as a verified reduction for this project.
