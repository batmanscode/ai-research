# Independent referee report: triangle bad-`M` residual and tight budget

## Verdict

**PASS.**  Two precision edits requested during review are applied in the
repository proof note.

I reconstructed the definitions and checked every defender swap, both proofs
of the tight-budget bad-set lemma, and the separate `C5`-free residual
corollary.  I found no mathematical gap in the bad-`M` completion lemma or in
the conclusion that `B_X` is a clique when `p=alpha(G)`.  The repository note
uses the shorter uniform-attachment/common-two proof recommended during
review in place of the earlier same-type case split.

The applied precision edits are:

1. The note now states the contextual hypotheses at the start of the bad-`M`
   section.  The construction of `X` requires every `P_k` to be nonempty.  The completion
   lemma itself needs only a dominating triangle and nonempty private regions;
   the inequality `p<=alpha(G)` needs pairwise anticompleteness of the three
   private regions; the tight bad-set clique theorem additionally needs
   induced-`P5`-freeness.  In the intended unresolved branch these hypotheses
   are available.  The note states them through an inclusion-minimal
   dominating triangle with pairwise-anticomplete private regions.
2. The note now explicitly defines `N[X]` as the closed neighborhood and uses
   the convention `gamma(empty graph)=0`.  These are standard conventions,
   but both matter in the displayed count and in the empty-`B_X` corollary.

The existing Atlas output is correctly reported, but it does **not** audit the
tight structural claim: it has 11 tight-budget choices and zero tight bad
vertices (`tight_budget_restriction_checks=0`).  The proof, rather than that
finite run, establishes the tight theorem.  A targeted nonvacuous audit is
reported below.

## 1. Definitions reconstructed

Let `K={a,b,c}` be a dominating triangle.  For each hub `k`, let

`P_k={v outside K : N(v) intersect K={k}}`,

and let `M` consist of the outside vertices with at least two neighbors in
`K`.  In the residual branch the `P_k` are nonempty and pairwise
anticomplete.  Choose a maximum independent set `I_k` in each `P_k`, omit one
vertex `x_k`, and put

`X = union_k (I_k-{x_k})` and `U_k=P_k-N[X]`.

Here `N[X]` must be closed.  Since `x_k` has no neighbor in
`I_k-{x_k}`, every `U_k` is nonempty.  It is a clique: if two vertices of
`U_k` were nonadjacent, adding both to `I_k-{x_k}` would exceed
`alpha(P_k)`.

For

`S=K union X union Y`,

the only possible external private neighbors of a hub `k` are in `P_k`.
More precisely,

`epn(k,S) subseteq P_k-N[X]=U_k`.

Vertices in another private region see another selected hub, and vertices in
`M` see at least two selected hubs.  Adding `Y` can only shrink this external
private neighborhood.

## 2. Bad-`M` completion lemma

Define `B_X` to consist of the vertices `v` in `M` that

- have no neighbor in `X`; and
- for every adjacent hub `k`, miss at least one member of `U_k`.

Let `Y` dominate the induced graph `G[B_X]`.  I checked all attack classes
for `S=K union X union Y`.

### Attack with an outside-guard neighbor

If an attacker `v` has a neighbor `g` in `X union Y`, use `g` as defender.
After replacing `g` by `v`, all three vertices of the dominating triangle
remain.  Therefore the new set still dominates the entire graph.  This
argument is valid for guards in `Y` as well as guards in `X`; no guard attack
is omitted.

### Attack in a private region

Suppose `v in P_k` has no neighbor in `X union Y`.  Then `v in U_k`.
Replace hub `k` by `v`.  The removed hub is dominated by the attacker, all
other vertices not external-private to `k` remain dominated, and every other
member of the actual external-private neighborhood of `k` lies in the clique
`U_k` and is adjacent to `v`.  Thus `k` is a valid defender.  The attacked
vertex itself need not be adjacent to itself; the swap condition only asks it
to dominate the other exposed vertices.

### Attack in `M`

Suppose `v in M` has no neighbor in `X union Y`.  Because `v` is outside
`S`, domination of `G[B_X]` by `Y` implies `v` cannot lie in `B_X`.
Therefore an adjacent hub `k` satisfies `U_k subseteq N(v)`.  Replacing that
hub by `v` dominates the removed hub and the whole actual external-private
neighborhood of the hub, which is a subset of `U_k`.

These cases exhaust `V(G)-S`; vertices of `K`, `X`, and `Y` are selected.
Hence the security proof passes.

Since each nonempty `I_k` loses one vertex,

`|K|+|X|=3+(p-3)=p`,

and a minimum dominating set of `G[B_X]` gives

`gamma_s(G) <= p+gamma(G[B_X])`.

No induced-`P5` hypothesis is used in this completion lemma.

## 3. Empty/clique corollary

Pairwise anticompleteness of the private regions makes the union of the three
`I_k` independent, so `p<=alpha(G)`.  If `B_X` is empty then its domination
number is zero; if it is a nonempty clique then its domination number is one.
Consequently

`gamma_s(G) <= p+1 <= alpha(G)+1`.

This corollary passes exactly as stated once the empty-graph convention is
made explicit.

## 4. Tight structural restrictions

Assume `p=alpha(G)` and `v in B_X`.

- If `v` sees all three hubs, badness supplies `u_k in U_k-N(v)` for all
  three hubs.  The set `X union {v,u_a,u_b,u_c}` is independent and has
  order `(p-3)+4=p+1`, a contradiction.
- Hence every bad vertex has exactly two hub neighbors.  If its type is
  `{a,b}` and it misses some `u_c in U_c`, badness also supplies missed
  vertices `u_a in U_a` and `u_b in U_b`; the same independent-set count is
  a contradiction.  Therefore a type-`{a,b}` bad vertex is complete to
  `U_c`.

All cross-region and `X` nonedges used here follow respectively from
pairwise anticompleteness and the definition of `U_k`; the bad vertex misses
`X` by definition.  The restriction is valid.

## 5. Recommended tight-clique proof

I recommend replacing the longer same-type split in
`clique_branch_proof_2.md` with the uniform-attachment/common-two proof in
`clique_structure_miner_2/findings.md`.

### Uniform attachment

Let bad vertex `m` have type `{a,b}`.  Badness gives
`u in U_a-N(m)`.  If `m` had a neighbor `v in U_a`, then `uv` is an edge
because `U_a` is a clique, and

`u-v-m-b-c`

is an induced `P5`.  Its path edges are `uv,vm,mb,bc`; its six required
nonedges are

`um, ub, uc, vb, vc, mc`.

They follow from the chosen miss, the private type of `u,v`, and the hub
type of `m`.  Thus `m` is anticomplete to `U_a`, and symmetrically to
`U_b`.  The tight independence argument above makes it complete to `U_c`.

### Different bad types

Let `m` have type `{a,b}` and `n` type `{a,c}`.  If `mn` were absent, choose
arbitrary `u in U_b` and `v in U_c`.  Uniform attachment gives the four path
edges in

`u-n-a-m-v`.

The six nonconsecutive pairs are absent:

`ua` and `av` by private types; `um` and `nv` by uniform attachment;
`uv` by cross-private anticompleteness; and `nm` by assumption.

Thus distinct hub types are adjacent in `B_X`.

### Same bad type

Every independent set in `B_X` therefore consists of one common hub type,
say `{a,b}`.  Uniform attachment makes it anticomplete to all of `U_a` and
`U_b`.  If it contained independent vertices `m,n`, then

`X union {m,n,u_a,u_b}`

would be independent for arbitrary `u_a in U_a,u_b in U_b`, and would have
order `(p-3)+4=p+1`.  This contradicts `p=alpha(G)`.  Therefore `B_X` has no
independent pair and is a clique.

This proof is shorter, makes every chord source transparent, and eliminates
the current proof's secondary common-nonneighbor subcases.  The current proof
also appears valid: I separately verified the paths
`y-w-c-z-v`, `y-b-v-x'-x`, and `x-w-y-y'-v` and all their chords.  The
uniform proof is nevertheless preferable for publication.

Combining the clique conclusion with the completion lemma proves

`gamma_s(G)<=p+1=alpha(G)+1`

for the tight private-budget triangle branch.

## 6. `C5`-free residual corollary

This corollary also passes, but the one-hub lift should be stated explicitly:

> If `K` is any nonempty clique of a graph `G`, `H=G-K` is nonempty, and
> `T` is a secure dominating set of `H`, then `T union {k}` is secure in
> `G` for every `k in K`.

No domination, minimality, connectivity, or induced-`P5` assumption on `K`
or `G` is needed.  For an attack in `H-T`, use its defender in `T`; after
the swap, `H` remains dominated and `k` dominates all of `K`.  For an attack
in `K-{k}`, use `k`; after the swap, the attacker dominates the clique and
`T` still dominates `H`.

Degawa--Saito's theorem is stated for every induced-`C5`-free graph, not
only connected graphs.  Hence, when nonempty `H` is induced-`C5`-free,

`gamma_s(G) <= 1+gamma_s(H) <= 1+alpha(H) <= 1+alpha(G)`.

If `H` is empty, then `G=K` is a nonempty clique and a single vertex is a
secure dominating set.  Here `alpha(H)=0` under the standard convention,
but no secure set of the empty graph need be invoked.  This handles the
only zero-independence case cleanly.

Therefore the corollary is an all-orders theorem for arbitrary `G`, not
merely the present induced-`P5`-free branch.  Its use here losslessly reduces
the live one-hub residual to cases in which `G-K` contains an induced `C5`.

## 7. Independent computation

I reran the supplied checker with its vendored NetworkX dependency:

`PYTHONPATH=agent-sat-extremal/vendor python triangle_bad_m_verify.py`

It reproduced:

- 1,253 Atlas graphs;
- 13 eligible triangle cores;
- 15 residual choices and 15 secure constructions;
- zero failures;
- 11 tight choices, but zero tight bad-vertex restriction checks.

I also wrote a self-contained independent bit-mask checker,
`bad_m_residual_independent_audit.py`, which does not import the author's
checker.  It generated arbitrary dominating-triangle partitions with
nonempty pairwise-anticomplete private regions (the completion lemma itself
does not require `P5`-freeness), computed all relevant maximum independent
sets and minimum bad-set dominating sets exactly, and checked security by
the definition.  Fixed seed `20260830` produced:

- 2,500 random graphs;
- 11,473 residual choices;
- 11,473 secure constructions;
- 7,645 tight choices;
- 332 nonvacuous tight bad-vertex restriction checks;
- 1,198 induced-`P5`-free tight choices;
- zero failures.

The random sample did not contain a `P5`-free tight bad set of order two, so
I added three explicit induced-`P5`-free, order-10/11 tight examples: one bad
vertex, an adjacent same-type bad pair, and an adjacent different-type bad
pair.  In all three, `p=alpha=6`, the computed `B_X` is a clique, a one-vertex
`Y` dominates it, and the constructed set is secure.  Four non-`P5`-free
random tight choices had nonclique bad sets, confirming that the
induced-`P5` hypothesis in the clique theorem is doing real work.

These computations audit the definitions and exercise the previously
vacuous tight cases; the all-orders conclusions rest on the proofs above.
