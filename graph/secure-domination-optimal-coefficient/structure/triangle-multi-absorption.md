# Triangle-clique multi-region absorption

## Setting

Let `K={k_i,k_j,k_l}` be a dominating triangle in an induced-`P5`-free
graph.  For a hub `k_r`, let

\[
P_r=\{v\notin K:N(v)\cap K=\{k_r\}\}.
\]

For a two-element subset of the hubs, let `M_{rs}` be the vertices outside
`K` whose `K`-neighbourhood is exactly `{k_r,k_s}`; vertices complete to `K`
form `M_{ijl}`.  This notation is a refinement of the multi-region `M` in
the main clique-branch report.

## Proof-grade lemma: a multi/private edge nearly yields a dominating P3

**Triangle multi-region absorption lemma.**  Suppose

\[
m\in M_{ij},\qquad y\in P_i\cap N(m).
\]

Then `D={y,m,k_j}` is an induced `P3`, and every vertex outside `P_i` is
dominated by `D`.  Equivalently,

\[
V(G)\setminus N[D]\subseteq P_i.
\tag{A}
\]

The symmetric statement holds after exchanging `i` and `j`.

**Proof.**  Since `y` is private to `k_i`, it is nonadjacent to `k_j`.
Thus `y-m-k_j` is an induced path on three vertices.  The vertex `k_j`
dominates all of `K` and `P_j`, and it dominates every vertex in `M_{ij}`,
`M_{jl}`, or `M_{ijl}`.

It remains to cover `P_l` and `M_{il}`.  If `z in P_l` were anticomplete to
both `m` and `y`, then

\[
z-k_l-k_j-m-y
\]

would be an induced `P5`: the two assumed nonedges remove the only
nontrivial outside chords; privacy removes `z k_j`, `k_l y`, and `k_j y`;
and `m` misses `k_l` because `m in M_{ij}`.  This is impossible.  Hence
every `P_l` vertex is adjacent to `m` or `y`.

The same displayed path proves the statement for `z in M_{il}`: now
`z k_l` is an edge, while membership in `M_{il}` removes `z k_j`; if `z`
misses `m,y`, every nonconsecutive pair is again nonadjacent.  Thus every
`M_{il}` vertex is also adjacent to `m` or `y`.  All possible regions have
now been covered except `P_i`, proving (A). `square`

**No-dominating-`P3` consequence.**  In the unresolved branch where a
dominating induced `P3` has already been excluded, (A) forces a vertex

\[
x\in P_i\setminus N[\{y,m\}].
\tag{B}
\]

In particular, every edge from `M_{ij}` to `P_i` certifies a specific
non-neighbour pair in `P_i`; hence `alpha(G[P_i])>=2`.  This is a genuine
exchange/packing constraint, rather than the incorrect claim that different
private regions are anticomplete.

## Why the earlier cross-edge shortcut does not work

For `x in P_i`, `y in P_j`, and `xy in E(G)`, induced-`P5`-freeness does imply
that `{x,y}` dominates `P_l`.  It does **not** imply that `x` alone dominates
`P_l`: a third-region vertex may see only `y`.  Consequently, the path
`x-k_i-k_j` need not be a dominating `P3`.  This correction matters and is
explicitly preserved here so it does not leak into a proof.

## Independent checks

`audit_triangle_multi_absorption.py` applies the definitions directly to
every triangle of every induced-`P5`-free Graph Atlas graph.  It verifies the
two `P5` cover implications and the exact residual statement (A):

```text
PASS
p5free_graphs=873
dominating_triangles=3022
relevant (m,y) tuples=1277
third-private cover checks=228
multi cover checks=366
exact-residual checks=1277
```

The audit is an implementation check, not evidence in place of the proof.

## Next proof direction

The lemma makes an explicit charging strategy plausible.  Each multi/private
edge consumes an independent witness in the source private region by (B).
The open task is to select these witnesses globally, allowing overlap, and
show that either their aggregate independence pays for `gamma(M)` in the
local completion or the residual outside graph obtains a small secure set for
the one-hub lift.  Any proof must retain the two-vertex nature of the
cross-region collapse; replacing it by a one-vertex claim is invalid.

