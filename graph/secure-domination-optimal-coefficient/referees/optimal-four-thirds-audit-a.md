# Independent final-theorem referee report

## Verdict

**PASS.**  The proposed cross-edge closure for minimum dominating cliques of
order at least four is correct.  Combined with the independently audited
pairwise-private closure, dominating-pair theorem, dominating-triangle
theorem, dominating-`P3` theorem, and the Bacsó--Tuza structure theorem, it
proves the all-orders result

\[
\boxed{\gamma_s(G)\leq\alpha(G)+1}
\]

for every connected induced-`P5`-free graph with `alpha(G)>=3`.

The independently verified complement-of-the-icosahedron witness has
`alpha=3` and `gamma_s=4`.  Therefore, on this stated `alpha>=3` domain,

\[
\boxed{c_{\rm opt}=4/3}.
\]

I reconstructed the proof from the definitions and the previously audited
lemmas.  Every defender dependency, component quantifier, and proposed
induced-path chord was checked below.

## 1. Exact setup and dependencies

Let `K` be an inclusion-minimal dominating clique of order `t>=4` in an
induced-`P5`-free graph.  For each `i in K`, its exact private region is

```text
P_i={v outside K : N(v) intersect K={i}}.
```

Every `P_i` is nonempty.  Indeed, if `P_i` were empty, deleting `i` would
leave a smaller dominating clique.  This use is valid for `t>=2`: a private
witness cannot be the clique vertex itself because it has other selected
clique neighbours.

The following two previously audited results are assumed.

1. If the private regions are pairwise anticomplete, the higher-order
   bad-`M` argument proves `gamma_s(G)<=alpha(G)+1`.
2. In the general branch, define the cross-nonedge graph `Q` on
   `U=union_i P_i`: vertices from distinct private regions are adjacent in
   `Q` exactly when they are nonadjacent in `G`; no within-region pair is a
   `Q`-edge.  Every `Q`-component is cross-complete.  Hence, for vertices
   from distinct private regions,

   ```text
   xy is an edge of G  iff  x and y lie in different Q-components.
   ```

The second statement controls cross-region pairs only; no within-region
adjacency is inferred.

It remains to close the branch containing a cross edge.

## 2. A cross edge is complete to every third private region

Fix a cross edge

```text
xy,    x in P_i,    y in P_j,
```

and let `A,B` be the respective `Q`-components of `x,y`.  Since `x,y` lie
in distinct private regions and are adjacent in `G`, the global `Q`
partition gives `A!=B`.

Let `z in P_l` for any third label `l` distinct from `i,j`.  The
per-transversal edge-dominating lemma says that `z` sees at least one of
`x,y`; otherwise the edge `xy` would fail to dominate a transversal
containing these three vertices.

Suppose `z` sees `y` but misses `x`.  Because `t>=4`, choose a fourth hub
`k_h` with `h` distinct from `i,j,l`.  Then

```text
k_h-k_i-x-y-z
```

is an induced `P5`.  Its path edges are the clique edge `k_h k_i`, the
private edge `k_i x`, the fixed cross edge `xy`, and the assumed edge `yz`.
Its six chords are:

| chord | reason |
| --- | --- |
| `k_h x` | `x` is private to `k_i`, with `h!=i` |
| `k_h y` | `y` is private to `k_j`, with `h!=j` |
| `k_h z` | `z` is private to `k_l`, with `h!=l` |
| `k_i y` | `y` is private to `k_j`, with `i!=j` |
| `k_i z` | `z` is private to `k_l`, with `i!=l` |
| `xz` | the assumed miss |

The case in which `z` sees only `x` is symmetric, using
`k_h-k_j-y-x-z`.  Consequently

\[
\boxed{z\text{ is adjacent to both }x\text{ and }y}
\tag{1}
\]

for every vertex in every third private region.  The quantifier is over all
vertices, not merely one selected transversal witness.

## 3. The endpoint components avoid the opposite private regions

We prove

\[
A\cap P_j=\varnothing,
\qquad
B\cap P_i=\varnothing.
\tag{2}
\]

Suppose instead that `z in A intersect P_j`.  Choose any `w in P_l` from a
third nonempty private region.  By (1), `w` is adjacent to both `x` and `y`.
Because these are cross-region edges, the `Q` partition puts `w` in a
component `C` distinct from both `A` and `B`.

Now `z in A` and `w in C` lie in distinct private regions and different
`Q`-components, so `zw` is a cross edge of `G`.  Apply (1) to this cross
edge, using `x in P_i` as the third-region vertex.  It forces `xz` to be an
edge.  But `x,z` lie in distinct private regions and the same `Q`-component
`A`, so the global partition says `xz` is a nonedge.  This contradiction
proves `A intersect P_j` empty.  Exchanging `x,y` proves the other half.

No within-region relation is used here: `z,y` both lie in `P_j`, but the
argument never assumes anything about their adjacency.

Equation (2) has the exact completeness consequence needed later.  Every
vertex of `P_j` belongs to a `Q`-component different from `A`, so it is
adjacent to `x`.  Similarly, `y` is complete to `P_i`:

\[
x\text{ is complete to }P_j,
\qquad
y\text{ is complete to }P_i.
\tag{3}
\]

## 4. The cross edge produces a dominating induced path

Put

```text
D={k_i,x,y}.
```

This is an induced `P3` in the order `k_i-x-y`: the two displayed edges
exist, while `k_i y` is absent because `y` is private to `k_j`.

The set `D` dominates:

- all of `K`, through the clique vertex `k_i`;
- `P_i`, through `y`, by (3);
- `P_j`, through `x`, by (3); and
- every `P_l` with `l` distinct from `i,j`, through both `x,y`, by (1).

It remains only to audit the multi-neighbour region.

Let `m` be a multi-neighbour and suppose, for contradiction, that it misses
all of `D`; thus

```text
m k_i,   mx,   my
```

are nonedges.  The vertex `m` has at least two clique neighbours.  Since it
misses `k_i`, choose

```text
k_a in N_K(m)-{k_j}.
```

This set is nonempty: even if `k_j` is one clique neighbour, there is a
second one; and the selected `k_a` is automatically distinct from `k_i`.
Then

```text
m-k_a-k_i-x-y
```

is an induced `P5`.  The path edges are respectively the selected
multi/hub edge, a clique edge, the private edge `k_i x`, and the fixed
cross edge `xy`.  Its six chords are:

| chord | reason |
| --- | --- |
| `m k_i` | `m` was assumed to miss `D` |
| `mx` | `m` was assumed to miss `D` |
| `my` | `m` was assumed to miss `D` |
| `k_a x` | `x` is private to `k_i`, with `a!=i` |
| `k_a y` | `y` is private to `k_j`, with `a!=j` |
| `k_i y` | `y` is private to `k_j`, with `i!=j` |

This contradiction proves that every multi-neighbour is dominated by `D`.
The clique, private, and multi-neighbour cases partition the whole graph,
so `D` is a dominating induced `P3`.

The independently audited dominating-`P3` theorem now gives

\[
\gamma_s(G)\leq\alpha(G)+1
\]

for the cross-edge branch.

## 5. Exhaustive global case split

Let `G` be connected, induced-`P5`-free, and satisfy `alpha(G)>=3`.
Bacsó--Tuza supplies either a dominating induced `P3` or a dominating
clique.

- A dominating induced `P3` is handled by the audited dominating-`P3`
  theorem.
- In the clique case, take an inclusion-minimal dominating subclique `K`.
  - If `|K|<=2`, the audited dominating-pair theorem applies.
  - If `|K|=3`, the audited dominating-triangle theorem applies.
  - If `|K|>=4`, every private region is nonempty.  If they are pairwise
    anticomplete, the audited higher-order bad-`M` theorem applies.  If not,
    they contain a cross edge, and Sections 2--4 above supply a dominating
    induced `P3`.

These alternatives exhaust every connected induced-`P5`-free graph in the
stated independence range.  Thus the `alpha+1` theorem is proved for all
orders; none of the steps is a bounded enumeration or an asymptotic
argument.

## 6. Optimal coefficient

For `alpha(G)>=3`, the theorem implies

\[
\frac{\gamma_s(G)}{\alpha(G)}
\leq 1+\frac1{\alpha(G)}
\leq \frac43.
\]

The previously verified complement of the icosahedral graph is connected
and induced-`P5`-free with

\[
\alpha=3,
\qquad
\gamma_s=4.
\]

It attains ratio `4/3`, so the coefficient is exactly `4/3` on the
`alpha>=3` domain.  This coefficient statement should retain that domain
explicitly; extending the quantifier to smaller independence numbers would
be a different claim and is not needed for the original problem.

## Final assessment

I actively tested the places most likely to hide a failure:

- the fourth hub is always distinct from all three private-region labels in
  the double-adjacency path;
- the `Q`-component argument never treats same-region vertices as governed
  by the partition theorem;
- the second use of double adjacency has three genuinely distinct private
  regions;
- the multi-neighbour path always has an available hub outside
  `{k_i,k_j}`; and
- the Bacsó--Tuza clique can be reduced to an inclusion-minimal subclique
  without losing domination or clique structure.

No counterexample or missing case survives these checks.  The theorem is
proof-grade, subject to the already completed independent audits of its
named dependencies.
