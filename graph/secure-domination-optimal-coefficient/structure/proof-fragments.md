# Proof fragments toward the connected `P5`-free coefficient

These notes are independent scratch work.  They do **not** claim the full
`gamma_s <= alpha + 1` theorem.

## Definitions used below

For a dominating set `S` and `u in S`, write

`epn(u,S) = {x outside S : N(x) intersect S = {u}}`.

An outside vertex `v` is defended by `u in S` exactly when `uv` is an edge
and every vertex of `epn(u,S)` is adjacent to `v`.

## Lemma 1: the bad-cycle lemma

Let `G` be `P5`-free, let `I` be a maximum independent set, let `q` be a
vertex outside `I`, and put `S = I union {q}`.  If `S` is not secure, then
there is an induced 5-cycle `C` such that

1. `q` is anticomplete to `C`;
2. `I` meets `C` in two nonadjacent vertices; and
3. `I \ C` is anticomplete to `C`.

### Proof

Because `I` is dominating, `epn(q,S)` is empty.  Hence every outside
neighbor of `q` is defended by `q`.  Choose a vertex `v` not defended by
`S`; necessarily `qv` is not an edge.

The standard maximum-independent-set lemma used in the published
`3 alpha / 2` proof says that `v` has at least two neighbors in `I`.  Choose
two, called `i,j`.  Since neither can defend `v`, choose

- `x in epn(i,S) \ N(v)`, and
- `y in epn(j,S) \ N(v)`.

All chords of the path `x-i-v-j-y` are absent except possibly `xy`.
Consequently `xy` must be an edge, or those five vertices induce a `P5`.
Thus

`C = x-i-v-j-y-x`

is an induced 5-cycle.

Let `d in I \ {i,j}`.  The definition of the two private neighbors makes
`d` nonadjacent to `x,y`, and independence makes it nonadjacent to `i,j`.
If `dv` were an edge, then `d-v-i-x-y` would be an induced `P5`.  Therefore
`d` is anticomplete to `C`, proving (2) and (3).

We already know that `q` is nonadjacent to `x,v,y`.  It cannot be adjacent
to exactly one of `i,j`: for example, if it sees `i` but not `j`, then
`q-i-v-j-y` is an induced `P5`.  Suppose it sees both.  If it also sees some
`d in I \ {i,j}`, then `d-q-i-x-y` is an induced `P5`.  Hence in this case
`q` is anticomplete to `I \ {i,j}`.  But then

`(I \ {i,j}) union {q,x,v}`

is an independent set of size `|I|+1`, a contradiction.  Thus `q` sees
neither `i` nor `j`, and is anticomplete to all of `C`.  This proves (1).

## Lemma 2: a dominating induced 5-cycle is secure

If an induced 5-cycle `C` dominates a `P5`-free graph, then `C` is a secure
dominating set.  In particular, `gamma_s(G) <= 5`.

### Proof

An outside vertex cannot have exactly one neighbor on `C`: if its unique
cycle neighbor is `c_0`, then it followed by four consecutive cycle vertices
`v-c_0-c_1-c_2-c_3` induces a `P5`.  Since `C` dominates, every outside
vertex therefore has at least two neighbors in `C`.  Hence every cycle guard
has empty external private neighborhood relative to `C`, so every outside
vertex is defended.

## Lemma 3: the favorable dominating-path branch

Suppose `G` is `P5`-free, `alpha(G) >= 3`, and `a-b-c` is a dominating
induced `P3`.  If some maximum independent set `I` contains the two endpoints
`a,c`, then `I union {b}` is secure.  Hence `gamma_s(G) <= alpha(G)+1`.

### Proof

Apply Lemma 1 with `q=b`.  If `I union {b}` is not secure, obtain its bad
cycle `C`.  Since `a-b-c` dominates `G` and `b` is anticomplete to `C`, the
two endpoints `a,c` dominate `C`.  Lemma 1 says that every member of `I`
outside the distinguished independent pair on `C` is anticomplete to `C`.
It follows that `a,c` must be exactly that pair. But `b` is adjacent to both
`a` and `c`, contradicting Lemma 1's conclusion that `b` is anticomplete to
the bad cycle. Therefore no bad cycle exists and `I union {b}` is secure.

## Lemma 4: exact obstruction for a maximum independent set

Let `I` be a maximum independent set in a `P5`-free graph.  Then `I` is not
secure if and only if there is an induced cycle

`C = x-i-v-j-y-x`

such that `I intersect C={i,j}` and `I\{i,j}` is anticomplete to `C`.

### Proof

The forward implication is the proof of Lemma 1 with no added vertex `q`:
an undefended attack `v`, two neighboring guards `i,j`, and witnesses
`x in epn(i,I)\N(v)` and `y in epn(j,I)\N(v)` force `xy` and hence the
displayed induced cycle.  Every other member of `I` is anticomplete to the
cycle, or it completes an induced `P5`.

Conversely, in the displayed configuration, `v` has exactly the two guards
`i,j` as neighbors.  The vertex `x` is an external private neighbor of `i`
missed by `v`, and `y` is an external private neighbor of `j` missed by `v`.
Thus neither `i` nor `j` defends the attack at `v`, so `I` is not secure.

This identifies the obstruction exactly: an *`I`-isolated 5-cycle*.

## Lemma 5: exact reduction inside a dominating clique

Let `K` be a dominating clique of a `P5`-free graph, with `|K|>=2`.  For
`k in K`, put

`P_k={z outside K : N(z) intersect K={k}}`.

Then each `G[P_k]` is a disjoint union of cliques.

For any `X subseteq V(G)\K`, put `S=K union X` and

`U_k=P_k\N[X]`.

The set `S` is secure if and only if, for every vertex `v outside S` with no
neighbor in `X`, there is some `k in N(v) intersect K` such that

`U_k\{v} subseteq N(v)`.

### Proof

If `a-b-c` were an induced `P3` in some `P_k`, choose
`ell in K\{k}`.  Then `ell-k-a-b-c` is an induced `P5`.  Hence every
`P_k` is `P3`-free, equivalently a cluster graph.

Since `K` dominates, every newly added guard in `X` has empty external
private neighborhood relative to `S`.  Therefore any outside vertex with a
neighbor in `X` is defended.  Now let `v` have no neighbor in `X`.  Its only
possible defenders lie in `K`.  For `k in N(v) intersect K`, direct use of
the definitions gives

`epn(k,S)=P_k\N[X]=U_k`.

Thus swapping `k` for `v` preserves domination exactly when every member of
`U_k` other than the attacked vertex itself is adjacent to `v`.  This is the
displayed condition.

### Collective selection consequence

If `P_k` has `a_k` clique components, selecting one vertex from all but one
component makes `U_k` a clique.  Doing this for every `k` automatically
settles every attack belonging to a singleton-`K` region.  What remains is
the precise bottleneck for the dominating-clique branch:

> select the component representatives so that every undominated vertex
> with at least two neighbors in `K` is complete to `U_k` for at least one
> of its neighboring clique guards, while keeping
> `|K|+|X| <= alpha+1`.

The multi-`K` condition cannot be omitted.  In graph6 `Jhf]gF]@?@?`, the
minimum dominating clique `K={1,5,6,8}` has four singleton private regions,
but `K` is not secure: attack `0` defeats swaps of `1,5,6,8` by exposing
`2,9,7,10`, respectively.  Adding vertex `3` repairs the set.

## Consequence already sufficient for one structural branch

The Liu--Zhou characterization says that every connected induced subgraph of
a `P5`-free graph has either a dominating induced 5-cycle or a dominating
clique.  Lemma 2 completely handles the dominating-cycle branch for the
desired `alpha+1` bound whenever `alpha >= 4`; the published
`3 alpha / 2` theorem handles `alpha=3`.

The remaining bottleneck is therefore the dominating-clique branch and,
specifically, the collective representative-selection condition in Lemma 5.
The tempting stronger claim that one can always add a single clique vertex to
a fixed maximum independent set is false; the exact biconnected witness
`LkdB{DEaseKoWg` is documented and independently checked in
`private-clique-obstructions.md`.

Lemma 1 still sharply describes each local obstruction: every failed choice
of an added vertex creates an induced 5-cycle anticomplete to it, with all but
two vertices of `I` anticomplete to that cycle. Multiple such cycles must be
handled collectively.

## Candidate statements explicitly falsified during the proof search

- A dominating `P3` need not have its endpoints in a maximum independent
  set.  A triangle with a pendant leaf on two different triangle vertices is
  `P5`-free and gives a five-vertex counterexample.
- Replacing "maximum" by "maximal" in Lemma 3 is false.  The path
  `a-b-c` with two additional leaves at `c` has the maximal independent set
  `{a,c}`, but `{a,b,c}` is not secure.

- It is false that a connected `P5`-free graph containing an induced `C5`
  has domination number at most three.  A smallest SAT witness found by the
  fixed-cycle encoding has graph6 string `Jhf]gF]@?@?` and edge set

  ```text
  01 04 05 06 08 12 15 16 18 23 34 35 36 38 45 48
  56 58 59 67 68 8(10)
  ```

  (vertices are `0,...,10`).  Independent plain-set checks give: connected,
  no induced `P5`, exactly one induced `C5` (on `0,1,2,3,4`),
  `alpha=5`, `gamma=4`, and `gamma_s=5`.  Thus the weaker proposed route
  "non-dominating `C5` implies domination number at most three" also fails,
  although this witness is harmless for the secure bound because it already
  has a secure maximum independent set.

- Even in the dominating-clique branch, not every clique guard works.  Start
  with an induced cycle `x-i-v-j-y-x`, add a vertex `d` anticomplete to the
  cycle, and add an edge `qr`, where `q` sees only `d` outside that edge and
  `r` is complete to the cycle and misses `d`.  The graph is connected and
  `P5`-free, `I={i,j,d}` is a maximum independent set, and `I union {q}` is
  not secure (the attack at `v` is undefended).  Hence a clique-branch proof
  must choose the added guard globally; it cannot assert that an arbitrary
  member of a dominating clique suffices.

- A minimum dominating clique of size at least three does **not** force a
  secure maximum independent set.  For `k>=2`, take disjoint induced cycles
  `C_1,...,C_k`, add a clique `Q={q_1,...,q_k}`, and make `q_i` complete to
  `C_i` and anticomplete to every other cycle.  This graph is connected and
  `P5`-free.  It has `alpha=2k`; every alpha-set consists of an independent
  pair from each cycle and is insecure.  For `k>=3`, `Q` is a minimum
  dominating clique of size `k`.  Nevertheless, the set consisting of all
  of `Q` plus one vertex from each cycle is secure, so `gamma_s=alpha=2k`.
  The family shows that the useful operation is a *collective* exchange of
  all isolated-cycle pairs, not selection of a better alpha-set.

- For the same reason, repairing one bad cycle by replacing its independent
  pair `{i,j}` with the complementary triple `{x,v,y}` need not make the set
  secure, even in a connected graph.  In the preceding family with `k>=2`,
  every untouched cycle remains an independent obstruction.
