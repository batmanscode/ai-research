# Clean-room referee report: component gluing across a dominating clique

## Verdict

**PASS, with three presentation-level clarifications.**

I reconstructed Theorems A and B directly from the definition of secure
domination and from the rooted-completion construction in
`structure/cut-vertices.md`.  I found no mathematical gap in either theorem.
In particular, the hypotheses that may initially look technical are exactly
the ones needed when a retained clique root moves:

- `|R| >= 2` leaves a clique guard after a root moves;
- every local completion `D_i` dominates `C_i` without its root, so a root
  may be shared among components safely;
- in Theorem B, roots for the nondesignated components must lie in
  `R-{r}`, because `X_0=I_0-{x}` need not dominate `C_0` if the reserved
  complete root `r` moves elsewhere; and
- an omitted clique attack in Theorem B must be defended by a member of
  `R-{r}`, not by the reserved root.

The scratch verifier independently checked the final sets by the definition
of secure domination.  It passed 21,942 basic and 25,495 saving constructions
in the complete NetworkX Graph Atlas, plus 49,368 basic and 49,583 saving
constructions in the accepted randomized instances.  These computations are
supporting validation, not part of the proof.

## Reconstruction of the imported rooted lemma

Let `C` be connected, let `k` be outside `C` with a neighbor in `C`, and
assume there is no induced path `k-a-b-c`.  Put

\[
L=N_C(k),\qquad Z=C\setminus L.
\]

For each component `Q` of `G[Z]`, every member of `L` is complete or
anticomplete to `Q`; otherwise an edge at the first change along a path in
`Q` produces a rooted induced `P4`.  Connectedness gives each `Q` a complete
neighbor in `L`.  The anchor-group construction from the cut-vertex note
therefore applies verbatim: it produces `D subseteq C` with

1. `D` dominating `C` without `k`;
2. `{k} union D` secure in `G[C union {k}]`; and
3. `|D| <= alpha(C)`.

Thus the gluing draft uses no unspoken cut-vertex property.  If a root `k`
has neighbors in two components `C_i,C_j` of `H=G-K`, any rooted path
`k-a-b-c` in `C_i union {k}`, together with a neighbor `y in C_j`, gives the
induced path `y-k-a-b-c`.  This proves the rooted hypothesis used in both
theorems.

## Audit of Theorem A

For every component choose the rooted set `D_i` and put

\[
S=R\cup\bigcup_i D_i.
\]

Domination is immediate: `R` dominates `K`, and each `D_i` dominates its
component independently of its root.  The attacks are exhaustive as follows.

### Attack in `K-R`

Move any `r in R` to the attacked vertex `v`.  Since `v in K`, it dominates
all of `K`, including the vacated root.  Each outside component remains
dominated by its rootless `D_i`.  No attachment assumption beyond those
already used to construct the `D_i` is needed here.

### Attack in `C_i-D_i`, defender in `D_i`

The local secure exchange dominates `C_i union {f(i)}`.  Every root remains,
so `K` remains dominated.  Every other component is unchanged and is
dominated by its own `D_j`.

### Attack in `C_i-D_i`, defender `f(i)`

The local secure exchange dominates `C_i` and the vacated root.  Since
`|R|>=2`, another member of `R` remains and dominates the whole clique.
Every other component is still dominated by `D_j`, even if its assigned
root was the same moved vertex `f(i)`.  This is precisely where rootless
domination prevents a shared-root failure.

These cases prove security.  The component additivity of independence gives

\[
|S|\le |R|+\sum_i\alpha(C_i)=|R|+\alpha(H).
\]

The budget consequence is correct: when `Delta=1` and `|R|=2`, the right
side is `alpha(G)+1`.

## Audit of Theorem B

Let `I_0` be a maximum independent set of the designated component, choose
`x in I_0`, and put `X_0=I_0-{x}`.  Because `r` is complete to `C_0`, the
singleton `{r}` dominates `G[C_0 union {r}]`.  The general residual
completion theorem therefore proves that `{r} union X_0` is secure locally,
including the edge case `alpha(C_0)=1`, when `X_0` is empty.

For `i ne 0`, take the rooted completion `D_i` for a root
`f(i) in R-{r}` and set

\[
S=R\cup X_0\cup\bigcup_{i\ne0}D_i.
\]

The attack audit is:

### Attack in `K-R`

Use a defender `s in R-{r}`.  This set is nonempty because `|R|>=2`.
After the swap, the attacked clique vertex dominates `K`; more importantly,
the reserved root remains and dominates `C_0`.  Every other component is
dominated by its rootless `D_i` even if `s` rooted one or several of them.
Using `r` as defender here would not be justified in general, and the draft
correctly avoids doing so.

### Attack in `C_0-X_0`

Use the local defender from the secure set `{r} union X_0`.  If that defender
is in `X_0`, `r` remains.  If it is `r`, the local exchange dominates
`C_0 union {r}`, another member of `R` remains to dominate the clique, and
all other components remain dominated by their `D_i` sets.  There is no
need for `X_0` alone to dominate `C_0` after this particular move: local
security supplies the stronger exchanged-set statement.

### Attack in `C_i-D_i`, `i ne 0`

Use the local rooted defender.  If it lies in `D_i`, all clique roots remain.
If it is `f(i)`, the hypothesis `f(i) in R-{r}` ensures that reserved `r`
still dominates `C_0` and `K`; the local exchange dominates `C_i`, and every
other component is dominated by its rootless completion.  This verifies that
the exclusion of `r` from all nondesignated root assignments is essential
and sufficient.

The count is exact up to the rooted budgets:

\[
|S|\le |R|+\alpha(C_0)-1+
\sum_{i\ne0}\alpha(C_i)=\alpha(H)+|R|-1.
\]

Since `alpha(G)=alpha(H)+Delta`, this is at most `alpha(G)+1` exactly when
`|R|<=Delta+2`.  The stated two-root consequence for `Delta=0` and
three-root consequence for `Delta=1` are correct.

## Edge cases and structural consequences

- `q>=2` is used to turn a root attached to two outside components into a
  rooted-`P4` exclusion.
- Components are nonempty, so `alpha(C_0)>=1` and the omitted vertex exists.
- `|R|>=2` is necessary in both security proofs whenever a root moves.
- A root may serve arbitrarily many components in Theorem A because every
  local `D_i` dominates without it.
- In Theorem B, the second attachment witnessing rooted-`P4`-freeness for
  `f(i)` may be `C_0`; it need not be another nondesignated component.
- If a component of `H` had exactly one attachment in `K`, that attachment
  would be a cut vertex because `q>=2`.  Therefore every counterexample in
  this setup, not merely every minimum counterexample, has at least two
  attachments per component by the existing cut-vertex theorem.

## Minimal recommended edits

1. After equation (1), define `H-N_H(k)` explicitly as the induced subgraph
   on the vertices of `H` not adjacent to `k`; this prevents ambiguity about
   open versus closed neighborhood deletion.
2. The authoritative cut-vertex note states its rooted lemma contextually as
   “`H` as above.”  For a standalone publication, include the short
   reconstruction above or extract the rooted-`P4`-free formulation as a
   separately stated corollary.  The generalization is valid, but should not
   be left solely to the reader to infer from the old proof.
3. In Section 5, strengthen/clarify “a minimum counterexample is
   2-connected” to “every counterexample is 2-connected”; the proved
   cut-vertex theorem is global.

No hypothesis or conclusion needs mathematical repair.

## Addendum: Theorem C (multi-saving root cover)

**Verdict: PASS.**  I audited the subsequently added multi-saving theorem
independently.  Its injective matching, mobility restriction, omitted-clique
condition, and count are all necessary and sufficient for the stated
construction.

Write `R=B dotcup Q`, with every reserved root `b in B` injectively matched
to a distinct component `C_b` to which it is complete.  In `C_b`, retain
`I_b-{x_b}` from a maximum independent set.  Every remaining component uses
a rooted completion `D_i` whose assigned root is mobile, in `Q`.  The global
set is

\[
S=R\cup\bigcup_{b\in B}(I_b-\{x_b\})
\cup\bigcup_{i:C_i\notin\{C_b:b\in B\}}D_i.
\]

The attack cases are exhaustive:

- In a saved component `C_b`, its local residual-completion defender works.
  If `b` moves, another root remains because `|R|>=2`; injectivity ensures
  no other saved component depends on `b`, and every regular component is
  rootless-dominated.
- In a regular component, its local rooted defender works.  If the assigned
  mobile root moves, all other regular components remain dominated by their
  `D_i`, while every reserved root remains in place for its saved component.
  A different member of `R` remains to dominate `K`.
- If `v in K-R`, a mobile root defends it.  This is why `Q` must be nonempty
  when `R ne K`: moving a reserved root could expose its saved component.
  The new guard `v` dominates `K`, all regular components are
  rootless-dominated, and all saved roots remain.
- If `R=K`, there is no omitted-clique attack, so `Q` may be empty.  When it
  is empty, hypothesis 2 forces every outside component to be among the
  injectively designated components; hence no uncovered regular component
  is hidden in this edge case.

Injectivity is exactly what permits one independent-set omission per
reserved root without attempting to save twice in the same component.  By
component additivity,

\[
|S|\le |R|+
\sum_{b\in B}(\alpha(C_b)-1)+
\sum_{i:C_i\notin\{C_b\}}\alpha(C_i)
=\alpha(H)+|R|-|B|=\alpha(H)+|Q|.
\]

Thus `|Q|<=Delta+1` gives `|S|<=alpha(G)+1`, as claimed.

I reran the expanded exact verifier.  It directly tested 37,947 applicable
Atlas and 72,895 randomized Theorem-C constructions; every constructed set
was secure.  The earlier Theorem-A and Theorem-B totals also remained
unchanged and passing.

### Strengthened disjoint-block form

The strengthened Theorem C, in which each saved component `C_{j_l}` is
dominated by a pairwise-disjoint nonempty reserved block `B_l subseteq R`,
also **passes**.  The singleton-root version audited above is its special
case.

For each designated component, `B_l` is a dominating set of the induced
graph on `C_{j_l} union B_l`: it dominates `C_{j_l}` by hypothesis and it
dominates itself because it lies in the clique `K`.  The general residual
completion theorem therefore makes

\[
B_l\cup(I_l-\{x_l\})
\]

secure locally, at an outside cost of `alpha(C_{j_l})-1`.  An individual
root in `B_l` need not itself be complete to, or even attach to, the
component: residual completion selects an actually adjacent defender and
uses the whole dominating set `B_l`.

If a block root moves under an attack in its designated component, local
security preserves that component, another member of `R` remains to
dominate `K`, every other designated block remains intact by pairwise
disjointness, and every nondesignated component has a rootless completion.
If a mobile root moves under an attack in a nondesignated component, all
reserved blocks remain and every other regular component is independently
dominated.  An attack in `K-R` is defended by a mobile root, whose existence
is correctly required when `R ne K`; no saved block is disturbed.  When
`R=K`, that attack class is empty.  In the extreme `Q=empty` case,
hypothesis 1 forces all outside components to be designated, so no component
is silently left without a completion.

Distinct designated components avoid duplicate savings, and disjoint blocks
avoid making two saved components depend on one movable root.  Consequently

\[
|S|\le |R|+
\sum_{l=1}^m(\alpha(C_{j_l})-1)+
\sum_{i\notin\{j_1,\ldots,j_m\}}\alpha(C_i)
=\alpha(H)+|R|-m.
\]

The budget test `|R|-m<=Delta+1` is therefore correct.  No mathematical
repair is needed.  I independently reran the expanded direct checker: it
passed 57,722 general disjoint-block constructions in the Graph Atlas and
95,846 in the randomized induced-`P5`-free separators, with zero failures.

## Addendum: one exceptional attachment component per root

The proposed short structural lemma is also **correct**:

> For a fixed `k in K`, among the components of `H=G-K` to which `k`
> attaches, at most one is not complete to `k`.

Indeed, suppose two distinct components `C,D` are attached to `k` but each
contains a nonneighbor of `k`.  In `C`, take a shortest path from `k` to a
nonneighbor and let `b` be the first nonneighbor on it.  Its predecessor
`a` is adjacent to `k`; moreover `b` occurs at distance exactly two from
`k`, since if the predecessor path contained another vertex, that vertex
would already be the first nonneighbor.  Thus `k-a-b` is an induced path.
Equivalently, one may choose an edge crossing from `N_C(k)` to
`C-N_C(k)`, which exists by connectedness.  Obtain `k-c-d` similarly in
`D`.

Now

\[
b-a-k-c-d
\]

is an induced `P5`: `bk` and `dk` are absent by construction, and every
other nonconsecutive pair lies in the two distinct components `C,D` of
`H`, so has no edge.  This contradicts induced-`P5`-freeness.  The lemma
needs only that `C,D` are distinct connected components of `H`, that `k`
has a neighbor and a nonneighbor in each, and that `G` is induced-`P5`-free;
neither domination nor minimality of `K` is otherwise used.
