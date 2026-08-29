# Independent attack on `gamma_s <= alpha + 1`

## Bottom line

I did not close the all-orders conjecture.  I found no counterexample to it.
The strongest exact negative results here concern proof shortcuts, not the
conjecture itself.  The work isolates the remaining issue as a genuinely
collective absorption problem for several induced-`C5` obstruction cores.

All finite claims below are independently reproduced by
`verify_obstructions.py`, which uses only plain Python sets/bitsets and checks
every 5-vertex subset and every candidate secure set at the relevant sizes.

## 1. A rigorous private-witness lemma

Let `K={k_1,...,k_t}` be an inclusion-minimal dominating clique of a
`P5`-free graph.  For each `i`, choose an external private neighbour
`p_i` of `k_i` relative to `K`; such a vertex exists by minimality.  Then the
graph induced by `{p_1,...,p_t}` is `P1 union P2`-free, equivalently it is a
complete multipartite graph.

Proof.  Suppose distinct representatives `p_i,p_j,p_l` satisfy
`p_i p_j` in `E` while `p_l` is adjacent to neither endpoint.  Then

`p_l - k_l - k_i - p_i - p_j`

is an induced `P5`.  Indeed, the three `k` vertices belong to a clique, but
only `k_l,k_i` occur in the displayed path; the definition of external
private neighbour removes every nonconsecutive edge from a representative to
the wrong clique vertex, and the assumed isolated-edge pattern removes the
remaining chords.  This is impossible.  The complement is therefore
`P3`-free, hence a disjoint union of cliques, proving the equivalent complete
multipartite description.

This is a real structural restriction, but it does not alone give a large
enough independent transversal or a secure set.

## 2. The proposed non-dominating-cycle shortcut is false

The statement

> If a connected `P5`-free graph contains an induced `C5` but no dominating
> induced `C5`, then it has a dominating vertex or edge

is false already at order 9.  An exact counterexample is graph6
`HhfUgCC`, with edges

```
01 04 05 06 12 15 16 23 34 35 36 56 58 67.
```

It is connected and induced-`P5`-free, has one induced `C5` (vertices
`0,1,2,3,4`), that cycle is not dominating, and it has no dominating vertex
or pair.  Its parameters are `alpha=4` and `gamma_s=4`, so it is benign for
the main conjecture.

## 3. Adding one vertex of a dominating clique is not enough

The attractive statement

> For a maximum independent set `I` and a dominating clique `K`, some
> `q in K\I` makes `I union {q}` secure

is false, even after requiring 2-connectivity and a minimum dominating clique
of order two.  Graph6 `LkdB{DEaseKoWg` is an exact 13-vertex witness.  It is
2-connected and induced-`P5`-free, `alpha=4`, and edge `01` dominates.  The
maximum independent set `I={9,10,11,12}` has neither `I+0` nor `I+1` secure.
The graph itself is easy (`gamma_s=3`, witness `{0,1,6}`), so this again kills
only the fixed-choice proof.

The bad-cycle complementary-triple reconfiguration also need not fix all
obstructions.  If failure of `I+q` yields

`C=x-i-v-j-y-x`,

then replacing `i,j` by `x,v,y` repairs this `C5` at net cost one, but another
anticomplete obstruction core can remain insecure.

## 4. An exact infinite collective-obstruction family

For `t>=2`, define `F_t` as follows.  Take a clique of hubs
`K={q_1,...,q_t}`.  For every `i`, attach a private induced cycle `C_i=C5`
complete to `q_i`, anticomplete to the other hubs, and anticomplete to every
other cycle.

Then

`F_t` is connected and `P5`-free, and

`alpha(F_t)=gamma_s(F_t)=2t`.

Proof of `P5`-freeness.  A path contained in one cone is not an induced
`P5`: the rim is a `C5`, while a path using its universal hub acquires a
chord as soon as it uses two rim vertices on the same side.  A path meeting
two modules must use their adjacent hubs.  It can use at most one rim vertex
beyond each hub, since each hub is complete to its own rim.  It therefore has
at most four vertices.  Three hubs create clique chords.  Hence no induced
`P5` exists.

For independence, omitting all hubs permits two rim vertices per cycle,
giving `2t`.  An independent set containing a hub loses its entire rim and
all other hubs, and has size at most `1+2(t-1)=2t-1`.

For secure domination, every secure set needs at least two vertices from
each block `{q_i} union C_i`.  Zero fails domination.  A lone rim vertex does
not dominate its `C5`.  A lone hub dominates the rim, but after an attack by
a rim vertex and removal of the hub, a distance-two rim vertex is
undominated.  Thus `gamma_s>=2t`.  Conversely, take all hubs and one arbitrary
rim vertex from every cycle.  A rim attacker adjacent to the chosen rim guard
is defended by that guard (it has no external private neighbour).  A rim
attacker not adjacent to it is defended by its hub: the two rim vertices not
seen by the chosen guard are adjacent, so the swap still dominates the block.
Other blocks are unaffected.  This is a secure `2t`-set.

For `t=3`, every maximum independent set takes two vertices per rim.  Adding
any one hub repairs at most its own cycle, so every single-hub attempt fails.
This is the cleanest reason a proof must absorb obstruction cycles
collectively.  It also shows that the collective phenomenon itself tends
toward coefficient one, not toward a counterexample.

## 5. What remains

The known bad-cycle lemma says that whenever `I+q` fails, it exposes an
induced `C5` anticomplete to `q` and to all but two vertices of `I`.  The
experiments and `F_t` show the next lemma cannot be a one-cycle or one-clique-
vertex statement.  A successful proof needs a global packing/exchange lemma,
roughly:

1. pack the bad cycles according to the two independent guards they consume;
2. use connectivity/dominating-clique attachments to replace every packed
   pair by at most two guards on average; and
3. pay at most one additional guard for all residual, overlapping cycles.

The exact SAT searches already in the project find no violation for
`alpha=4` through order 17 or `alpha=5` through order 16.  That remains finite
evidence only.  The private-witness lemma above and the exact family identify
the combinatorial bottleneck but do not yet supply the required global
exchange theorem.
