# Independent referee report: full dominating-triangle theorem

## Verdict

**PASS, conditional only on the three cited project dependencies.**

I independently reconstructed the all-orders argument in
`../structure/triangle-bad-m.md`, including every required path edge,
every forbidden chord, the quantifiers in the failed-witness step, the
independence-number accounting, and the reduction from an arbitrary
dominating triangle.  The pure new argument is correct.

The exact result established is:

> If `G` is a connected induced-`P5`-free graph with `alpha(G)>=3` and `G`
> has a dominating triangle, then
> `gamma_s(G)<=alpha(G)+1`.

The proof is conditional on already accepting the repository's separately
proved results:

1. the bad-`M` completion lemma;
2. a private cross edge at a dominating triangle forces a dominating induced
   `P3`; and
3. the dominating-pair and dominating-induced-`P3` branches satisfy the
   `alpha+1` bound.

I did not discover a use of the connected-residual typed-`C5` claims, any
bounded SAT frontier, the older finite triple common-two certificate, or the
tight-budget equality theorem.  None of those is a dependency of the new
proof.

## 1. Setup reconstructed

Let `K={a,b,c}` be a dominating triangle.  In the only branch needing the
new argument, the exact singleton-private regions

`P_i={v outside K : N(v) intersect K={i}}`

are nonempty and pairwise anticomplete.  For each `i`, choose a maximum
independent set `I_i` of `G[P_i]`, omit `x_i in I_i`, and define

`X = union_i (I_i-{x_i})`,

`U_i = P_i-N[X]`,

where `N[X]` is closed.  Put

`p=sum_i alpha(P_i)`.

Every `U_i` is nonempty because it contains `x_i`.  Every `U_i` is a clique:
two nonadjacent vertices in it, together with `I_i-{x_i}`, would exceed
`alpha(P_i)`.  Also `X` is independent, and the pairwise anticompleteness of
the private regions gives `p<=alpha(G)`.

The bad set `B_X` consists of those multi-neighbour vertices `m` which miss
`X` and, at every hub `i` they see, fail to cover all of `U_i`.

## 2. Seen-region anticompleteness

The key first lemma says that every `m in B_X` is anticomplete to `U_i` for
every hub `i` seen by `m`.

Fix such an `i`.  Badness supplies `u in U_i` missed by `m`.  If `m` also
sees `v in U_i`, then `uv` is an edge because `U_i` is a clique.

### 2.1 Two-hub bad vertex

Suppose `N_K(m)={i,j}`, with `k` the missed hub.  Then

`u-v-m-j-k`

has the four path edges `uv,vm,mj,jk`.  Its six nonconsecutive pairs are

`um, uj, uk, vj, vk, mk`.

The first and last are the chosen miss and the hub type of `m`; the other
four are absent because `u,v` are private to `i`.  This is an induced `P5`,
a contradiction.

### 2.2 Three-hub bad vertex

Suppose `m` sees all three hubs.  Choose a different hub `j`; badness at `j`
supplies `w in U_j` missed by `m`.  Then

`u-v-m-j-w`

has path edges `uv,vm,mj,jw`.  Its six nonconsecutive pairs are

`um, uj, uw, vj, vw, mw`.

The first and last are chosen misses; `uj,vj` are absent by privacy; and
`uw,vw` are absent because different private regions are anticomplete.
Again this is an induced `P5`.

Thus both possible multi-neighbour types satisfy the asserted uniform
anticompleteness.  The three-hub case is essential: without it, the global
argument would not characterize a failed residual clique correctly.

## 3. Global common-two lemma

Let `J` be an arbitrary independent set of `G[B_X]`.  Call `U_i` failed if
it contains no vertex anticomplete to all of `J`.

If `U_i` fails, then every vertex of `U_i` has a neighbour in `J`.  Choose
one edge `u_i m_i` with `u_i in U_i` and `m_i in J`.  Seen-region
anticompleteness shows that `m_i` cannot see hub `i`.  Since `m_i` is a
multi-neighbour of a three-vertex clique, its type is therefore exactly

`N_K(m_i)=K-{i}`.

This is the correct one-way implication.  The proof does **not** need, and
the source does not claim, the false converse that every vertex of type
`K-{i}` makes `U_i` fail.

Suppose two distinct residual cliques `U_i,U_j` fail.  Let `k` be the third
hub and choose the corresponding edges `u_i m_i` and `u_j m_j`.  The two
bad vertices are distinct because their exact hub types differ.  Then

`u_i-m_i-k-m_j-u_j`

has the four path edges.  Its six nonconsecutive pairs are absent for the
following exact reasons:

- `u_i k` and `k u_j`: privacy;
- `u_i m_j`: `m_j` sees `i`, so seen-region anticompleteness applies;
- `m_i u_j`: `m_i` sees `j`, by the same lemma;
- `u_i u_j`: pairwise anticompleteness of the private regions;
- `m_i m_j`: independence of `J`.

This induced `P5` is impossible.  Hence at most one of the three `U_i`
fails, proving that two residual cliques have respective vertices
anticomplete to all of the *entire* set `J`.  The quantifier is global, not
merely pairwise in members of `J`.

## 4. Independence and domination accounting

Take `J` to be a maximum independent set of `G[B_X]`, and choose common
witnesses `u_r in U_r`, `u_s in U_s` from the global lemma.  The set

`X union J union {u_r,u_s}`

is independent:

- `X` is independent;
- `J` is independent;
- every bad vertex misses `X` by definition of `B_X`;
- every `U_i` misses `X` by the definition `U_i=P_i-N[X]`;
- `u_r,u_s` miss all of `J` by their choice; and
- the two witnesses lie in distinct anticomplete private regions.

Its order is

`(p-3)+|J|+2 = p+|J|-1`.

Therefore

`alpha(B_X)=|J| <= alpha(G)-p+1`.

A maximum independent set is maximal, and every maximal independent set
dominates its graph.  With the standard empty-graph convention this gives

`gamma(G[B_X]) <= alpha(G[B_X]) <= alpha(G)-p+1`.

The bad-`M` completion lemma now yields

`gamma_s(G) <= p+gamma(G[B_X]) <= alpha(G)+1`.

This is a pure all-orders conclusion.  It does not use equality
`p=alpha(G)` and supersedes the older computer-assisted independent-triple
step.

## 5. Empty and boundary cases

The source handles the boundary cases correctly.

- If `B_X` is empty, take `J=empty`; every nonempty `U_i` is automatically a
  common-witness clique, `alpha(B_X)=gamma(B_X)=0`, and the calculation still
  holds.
- If some `P_i` is empty, the other two hubs form a dominating pair.  Any
  outside vertex has a nonempty neighbourhood in `K`; it cannot have the
  singleton type `{i}`, and every other possible type meets the other two
  hubs.  The omitted hub of the triangle is also adjacent to that pair.
- If all `P_i` are nonempty but two private regions have a cross edge, the
  separately proved private-cross-edge theorem supplies a dominating induced
  `P3`.
- Otherwise all three `P_i` are nonempty and pairwise anticomplete, exactly
  the hypotheses used by the new bad-set argument.

Thus the three cases in the final theorem are exhaustive.  They also give
the advertised reduction from an arbitrary dominating triangle to either a
dominating pair, a dominating `P3`, or the inclusion-minimal
pairwise-anticomplete residual.

Connectivity and `alpha(G)>=3` are used through the cited dominating-`P3`
theorem.  A dominating triangle itself already forces connectivity, but
retaining it in the stated scope is harmless and matches the surrounding
open problem.

## 6. Dependency boundary

I treated the following as dependencies rather than silently reproving them
inside this audit:

- The bad-`M` completion lemma converts any dominating set of `G[B_X]` into
  the secure set `K union X union Y` of order `p+|Y|`.
- The private-cross-edge theorem forces a dominating induced `P3`.
- The general dominating-set completion closes a dominating pair, and the
  project's dominating-`P3` theorem closes that branch for connected
  induced-`P5`-free graphs with independence number at least three.

Each is stated and independently audited elsewhere in the repository.  If
any were later withdrawn, only the corresponding dependency arrow—not the
new seen-region/common-two proof—would need reassessment.

The final sentence reducing the larger Bacsó--Tuza scope to an
inclusion-minimal dominating clique of order at least four is correct once
the standard dominating-clique-or-`P3` theorem is invoked: clique sizes one
and two are covered by the dominating-pair branch, and size three is the
theorem audited here.

## 7. Independent computational stress audit

`verify_full_triangle.py` does not import the author's checker.  It
reimplements induced-`P5`-freeness, domination, secure domination,
independence, the triangle partition, `U_i`, and `B_X` from definitions.  It
checks every independent subset of each bad set, not only maximum ones, and
checks every constructed secure set directly by all defender swaps.

Its fixed run returned:

```text
PASS
atlas_graphs=1253
dominating_triangles=9014
empty_private_cases=6809
private_cross_edge_cases=106
bad_m_cases=2099
residual_choices=12848
nonempty_bad_choices=136
seen_region_checks=314
three_hub_bad_vertices=8
common_two_sets=13016
direct_full_graph_checks=2403
random_p5free=2000 (from 7205 attempts)
```

The complete Graph Atlas is combined with 2,000 larger fixed-seed random
induced-`P5`-free triangle cores.  The eight observed three-hub bad vertices
make the all-three-hub anticompleteness test nonvacuous.  There were zero
failures.

These finite checks are supporting validation only.  The general theorem
rests on the induced-path and counting proofs in Sections 2--5.

## Final assessment

The global common-two step is a valid hand proof, not a finite extrapolation.
It closes the entire dominating-triangle branch at `alpha+1`, with the exact
scope stated in the source.  No mathematical correction is required.  For
publication clarity only, the author may optionally expand the one sentence
asserting that `X union J union {u_r,u_s}` is independent by listing the six
nonedge sources recorded in Section 4 above.
