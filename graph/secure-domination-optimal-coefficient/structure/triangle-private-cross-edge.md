# The triangle-core cross-edge branch

## Outcome

The whole dominating-clique problem is not closed here.  The following
subbranch is closed by forcing the already solved dominating-path outcome.

> **Triangle cross-edge theorem.**  Let `G` be an induced-`P5`-free graph and let
> `K={a,b,c}` be a dominating triangle.  For `k in K`, put
> \[
> P_k=\{v\notin K:N(v)\cap K=\{k\}\}.
> \]
> If there is an edge between two distinct singleton-private regions, then
> `G` has a dominating induced `P3`.

Consequently, the cross-edge subbranch satisfies

\[
\gamma_s(G)\leq\alpha(G)+1
\]

for every connected induced-`P5`-free `G` with `alpha(G)>=3`, directly by the
dominating-`P3` theorem already proved in the project.

Equivalently, in any still-unresolved graph with a dominating triangle, the
three regions `P_a,P_b,P_c` are pairwise anticomplete.  This moves all
remaining cross-region coupling into the multi-neighbour region

\[
M=\{v\notin K:|N(v)\cap K|\ge2\}.
\]

## Proof of the triangle cross-edge theorem

Assume for a contradiction that `G` has no dominating induced `P3`.  By
symmetry, let

\[
x\in P_a,\qquad y\in P_b,\qquad xy\in E(G).
\]

We repeatedly use this elementary cross-edge fact.  The pair `{x,y}`
dominates `P_c`: otherwise, for `z in P_c` missed by both, the sequence

\[
z-c-a-x-y
\]

would be an induced `P5`.  All its nonconsecutive pairs are nonedges by the
three private-region definitions and the assumption that `z` misses `x,y`.

The induced path `x-a-b` dominates `K`, `P_a`, `P_b`, and `M`.  Indeed,
every member of `M` sees at least one of `a,b`, because `K` is a triangle and
it has at least two neighbours in `K`.  Since this `P3` is not dominating,
there is a vertex

\[
z\in P_c\setminus N(x).
\]

The cross-edge fact forces `zy in E(G)`.  Symmetrically, the nondominating
path `y-b-a` supplies

\[
w\in P_c\setminus N(y),\qquad wx\in E(G).
\]

Now

\[
C_a=a-x-y-z-c-a
\]

is an induced `C5`.  Its five possible chords are absent as follows:
`ay,yc` are excluded by `y in P_b`; `az,xc` by the private types of `z,x`;
and `xz` by the choice of `z`.

The cycle `C_a` cannot dominate `G`.  Indeed, if it did, the induced path
`x-y-z` would dominate `K` (one selected vertex sees each private hub),
`P_c` by the edge `xy`, and `P_a` by the edge `yz`.  It would also dominate
`P_b`: because `C_a` dominates and members of `P_b` miss `a,c`, each must
see at least one of `x,y,z`.  The only possible missed vertices would lie in
`M`.  If `m in M` missed `x,y,z` and saw `a`, then

\[
z-y-x-a-m
\]

would be an induced `P5`.  If it missed `a`, then it would see both `b,c`,
and

\[
x-y-z-c-m
\]

would be an induced `P5`.  Thus no such `m` exists, making `x-y-z` a
dominating induced `P3`, contrary to the assumption.

Therefore choose a vertex `u` anticomplete to `C_a`.  The cycle contains
both `a` and `c`.  Every vertex outside `K` has a neighbour in `K`, while
`b` itself sees `a,c`.
Thus the only possible type of `u` is

\[
u\in P_b.
\]

In particular, `u` is nonadjacent to `x,y,z`.

The symmetric cycle

\[
C_b=b-y-x-w-c-b
\]

is also induced and nondominating.  The nondomination follows by the same
argument with the labels interchanged: if `C_b` dominated, then `y-x-w`
would dominate all three private regions and `K`; a missed member of `M`
would create `w-x-y-b-m` when it sees `b`, or `y-x-w-c-m` when it misses
`b`.  An anticomplete witness for `C_b` must be a vertex

\[
v\in P_a,
\]

and `v` is nonadjacent to `y,x,w`.

Induced-`P5`-freeness now forces two new cross edges.  If `uw` were absent,
then

\[
u-b-a-x-w
\]

would be an induced `P5`: `u` is private to `b` and misses `x`; `w` is
private to `c`; and `uw` is the only remaining possible chord.  Therefore
`uw` is an edge.  Symmetrically, absence of `vz` would make

\[
v-a-b-y-z
\]

an induced `P5`, so `vz` is an edge.

It follows that

\[
C_2=x-y-z-v-a-x
\]

is an induced `C5`.  Its consecutive edges are `xy,yz,zv,va,ax`; its five
chords are absent because `xz` was chosen absent, `v` is anticomplete to
`C_b` (giving `vx,vy`), and the private types give `ya,za` absent.

The cycle `C_2` cannot dominate.  If it did, the induced path `x-y-z` would
dominate `K`, while the first two cross edges `xy` and `yz` would make it
dominate `P_c` and `P_a`.  It also dominates `P_b`: if some `q in P_b`
missed `x,y,z`, domination by `C_2` would force `qv`, and then

\[
q-v-z-y-x
\]

would be an induced `P5`.  Indeed, `q` misses `z,y,x` by choice, `v` misses
`y,x` because it is anticomplete to `C_b`, and `zx` is absent.  Finally, a
missed member of `M` creates `z-y-x-a-m` if it sees `a`, and
`x-y-z-c-m` otherwise.  Thus `x-y-z` would be a dominating induced `P3`,
contrary to the assumption.

Let `m` be anticomplete to `C_2`.  We can identify `m` exactly:

- it misses `a`, so it is not in `K` or `P_a`;
- the cross edge `xy` dominates all of `P_c`;
- the cross edge `zv`, between `P_c` and `P_a`, dominates all of `P_b`.

Hence `m` lies in `M` and misses `a`.  Since `K` has three vertices and `m`
has at least two neighbours there, it sees both `b` and `c`.  But then

\[
m-b-a-v-z
\]

is an induced `P5`.  The four path edges are present; `m` misses `a,v,z`
because it is anticomplete to `C_2`; `b` misses `v,z` by their private
types; and `a` misses `z`.  This final contradiction proves the theorem.

## Exact scope of the advance

For a dominating triangle, the proof closes every case with an edge between
two of `P_a,P_b,P_c`.  In the remaining case those three regions are
pairwise anticomplete.  The old clique-local construction immediately also
closes the following subcases:

1. `M` is empty, when
   \[
   \gamma_s(G)\le \sum_{k\in K}\alpha(P_k)\le\alpha(G);
   \]
2. more generally,
   \[
   \sum_{k\in K}\alpha(P_k)+\gamma(G[M])\le\alpha(G)+1.
   \]

The genuinely live triangle-core residue therefore has pairwise
anticomplete singleton-private regions, nontrivial `M`, failure of the last
displayed numerical inequality, and failure of the one-hub lift.  No claim
that this final `M`-coupling case is solved is made here.

## Audit notes

The most tempting shorter argument was rejected: from a cross edge `xy`, the
path `x-a-b` does **not** automatically dominate `P_c`; the cross-edge lemma
only says every vertex of `P_c` sees `x` *or* `y`, and `y` is not on that
path.  The witnesses `z,w` above are necessary.

The theorem has also been checked directly on every applicable Graph
Atlas graph.  A stronger bounded SAT check fixes a dominating triangle and
a private cross edge, imposes induced-`P5`-freeness, and forbids every
dominating induced `P3`; it is UNSAT through order 14.
Those finite checks are corroboration only; the proof above is independent
of them, and the UNSAT runs have no retained proof traces.

The direct Atlas checker and its retained machine-readable output are
`../referees/verify_triangle_private_cross_edge.py` and
`../computation/results/triangle_private_cross_edge_atlas.json`.  They examine 1,253 Atlas graphs,
873 of them induced-`P5`-free, and find zero failures among 521 private
cross-edge instances over 3,022 dominating triangles.
The bounded model and its retained results are
`../computation/triangle_private_cross_edge_sat.py` and `../computation/results/triangle_private_cross_edge_sat.json`.

## Source and dependency scope

- The dominating-induced-`P3` implication is the project theorem in
  `structure/dominating-p3.md`, whose structural starting point is
  Bacsó--Tuza,
  [*Dominating cliques in P5-free graphs*](https://doi.org/10.1007/BF02352694).
