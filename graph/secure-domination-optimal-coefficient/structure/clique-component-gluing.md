# Component induction across a dominating clique

## Status

This note proves three clique-separator gluing theorems for the remaining
dominating-clique branch.  They are structural reductions, not a proof of the
full `gamma_s(G) <= alpha(G)+1` statement.

Throughout, `G` is a connected induced-`P5`-free graph, `K` is a dominating
clique, and

\[
H=G-K=C_1\dot\cup\cdots\dot\cup C_q,
\qquad q\ge2.
\]

For a component `C_i`, write

\[
A_i=\{k\in K:N_G(k)\cap C_i\ne\varnothing\}
\]

for its attachment set in the clique.

## 1. Exact independence bookkeeping

Put `a_H=alpha(H)`.  Since `K` is a clique, an independent set of `G`
contains at most one vertex of `K`.  Consequently

\[
\alpha(G)=\max\left\{
\alpha(H),\ 1+\max_{k\in K}\alpha(H-N_H(k))
\right\}.
\tag{1}
\]

Here `H-N_H(k)` means the subgraph induced by the vertices of `H` that are
nonadjacent to `k` (the vertex `k` itself is not in `H`).

In particular,

\[
\Delta:=\alpha(G)-\alpha(H)\in\{0,1\}.
\tag{2}
\]

This is the correct budget variable for component gluing.  A construction of
order `alpha(H)+c` proves the target precisely when `c<=Delta+1`.

## 2. Rooted completion imported from the cut-vertex proof

The following form is exactly what the gluing arguments use.

**Rooted-completion lemma.**  Let `C` be connected, let `k` be a vertex
outside `C` with a neighbour in `C`, and suppose `G[C union {k}]` has no
induced path `k-a-b-c` starting at `k`.  Then there is `D subseteq C` such
that

1. `D` dominates `C` without help from `k`;
2. `{k} union D` is secure in `G[C union {k}]`; and
3. `|D|<=alpha(C)`.

This is the rooted-completion lemma proved constructively in
`structure/cut-vertices.md`.  Although that note introduces it in a
cut-vertex context, inspection of the construction shows that its only
inputs are connectedness of `C` and absence of the displayed rooted `P4`:
put `L=N_C(k)`, take the components of `C-L`, use the rooted-`P4` exclusion
to prove that every vertex of `L` is complete or anticomplete to each such
component, group the nonclique components by complete anchors in `L`, omit
one maximum-independent-set representative per anchor group, and finish the
undominated part of `L` with a maximal independent set.  The count,
rootless domination, and attack-by-attack security proof in that lemma then
apply verbatim.  No separation property of `k` is used in the construction.

The clique separator makes the hypothesis automatic in an important case.

**Observation.**  If `k` has a neighbour in `C_i` and also a neighbour in a
different component `C_j`, then `G[C_i union {k}]` has no induced rooted
`P4`.

**Proof.**  Choose `y in C_j cap N(k)`.  If `k-a-b-c` were an induced path
inside `C_i union {k}`, then

\[
y-k-a-b-c
\]

would be an induced `P5`: distinct components of `H` have no edges between
them.  This contradicts the hypothesis on `G`.  `square`

There is also only one possible exceptional component per root.

**One-deep-component lemma.**  For every `k in K`, among the components to
which `k` attaches, at most one is not complete to `k`.

**Proof.**  Suppose two attached components `C_i,C_j` both contain a
nonneighbor of `k`.  In each component choose a nonneighbor at minimum
distance from `k`.  The first two vertices of corresponding shortest paths
give induced paths `k-a-b` and `k-c-d`, where `a,c` see `k` and `b,d` do
not.  Then

\[
b-a-k-c-d
\]

is an induced `P5`: shortestness deletes the two root chords and distinct
components of `H` delete every cross edge.  `square`

Thus every root is complete to all but at most one of the outside components
it meets.  This supplies many candidate reserved blocks for Theorems B and C;
the unresolved issue is the global matching/covering of components, not a
local shortage of complete attachments.

## 3. Root-cover gluing theorem

**Theorem A (root-cover gluing).**  Let `R subseteq K` with `|R|>=2`.
Suppose there is an assignment

\[
f:\{1,\ldots,q\}\longrightarrow R
\]

such that, for every `i`,

1. `f(i) in A_i`; and
2. `f(i) in A_j` for at least one `j ne i`.

Then

\[
\gamma_s(G)\le \alpha(H)+|R|.
\tag{3}
\]

**Proof.**  By the observation and the rooted-completion lemma, for every
`i` choose `D_i subseteq C_i` such that

\[
|D_i|\le\alpha(C_i),\qquad
D_i\text{ dominates }C_i,qquad
\{f(i)\}\cup D_i\text{ is secure on }C_i\cup\{f(i)\}.
\]

Set

\[
S=R\cup\bigcup_iD_i.
\]

The set dominates `G`: `R` dominates the clique `K`, and each `D_i`
dominates its own outside component.

Consider an attack outside `S`.

- If `v in K-R`, choose any `r in R` as defender.  After replacing `r` by
  `v`, the new clique guard `v` dominates all of `K`, while every `D_i`
  still dominates `C_i` without its root.
- Suppose `v in C_i-D_i`.  Security of `{f(i)} union D_i` supplies a local
  defender.  If that defender belongs to `D_i`, all roots in `R` remain and
  the exchange changes nothing outside `C_i`.  If the defender is `f(i)`,
  the local exchanged set dominates `C_i union {f(i)}`.  Since `|R|>=2`, a
  different member of `R` remains and dominates the whole clique `K`.
  Every other component remains dominated by its rootless set `D_j`, even
  when it was also assigned to `f(i)`.

Thus every attack is defended.  Finally,

\[
|S|\le |R|+\sum_i\alpha(C_i)=|R|+\alpha(H).
\]

This proves (3). `square`

**Budget consequence.**  In the independence-gain branch `Delta=1`, a
two-vertex root cover satisfying Theorem A proves

\[
\gamma_s(G)\le\alpha(H)+2=\alpha(G)+1.
\tag{4}
\]

The rootless-domination clause in the rooted lemma is essential twice: when
an omitted clique vertex is attacked, and when one root serves several
components but moves into just one of them.

## 4. A one-guard saving from a complete attachment

The preceding construction costs one retained guard per member of `R`.  The
next theorem saves one guard in a designated outside component.

**Theorem B (reserved-root saving).**  Let `R subseteq K`, `|R|>=2`, fix a
reserved root `r in R`, and fix a component `C_0`.  Assume:

1. `r` is complete to `C_0`;
2. for every `i ne 0`, there is a root
   `f(i) in (R-{r}) cap A_i`; and
3. every such `f(i)` also belongs to `A_j` for some `j ne i`.

Then

\[
\gamma_s(G)\le\alpha(H)+|R|-1.
\tag{5}
\]

**Proof.**  Let `I_0` be a maximum independent set of `C_0`, choose any
`x in I_0`, and put `X_0=I_0-{x}`.  Because `r` is complete to `C_0`, the
general dominating-set residual-completion theorem, applied inside
`G[C_0 union {r}]` with dominating set `{r}`, says that

\[
\{r\}\cup X_0
\]

is secure on `C_0 union {r}`.  Notice that `X_0` is not asserted to dominate
`C_0` after `r` leaves; this is why `r` is reserved and never assigned as a
root to another component.

For every `i ne 0`, choose the rooted-completion set `D_i subseteq C_i` for
root `f(i)` as in Theorem A.  Thus `D_i` dominates `C_i` without its root,
`{f(i)} union D_i` is locally secure, and `|D_i|<=alpha(C_i)`.  Set

\[
S=R\cup X_0\cup\bigcup_{i\ne0}D_i.
\]

Again inspect every kind of attack.

- If `v in K-R`, choose a defender `s in R-{r}`, which exists because
  `|R|>=2`.  The reserved root `r` stays, so it continues to dominate both
  `C_0` and all of `K`; each `D_i` dominates its component without `s`.
- If `v in C_0-X_0`, use the defender supplied by security of
  `{r} union X_0`.  If `r` moves, another member of `R` remains to dominate
  `K`; all other components are still dominated by their rootless `D_i`.
  The local exchange dominates `C_0 union {r}`.
- If `v in C_i-D_i` for `i ne 0`, use the local rooted defender.  It cannot
  be `r` because all these roots lie in `R-{r}`.  Hence `r` remains and
  continues to dominate `C_0` and `K`.  Every component other than `C_i`
  remains dominated by its rootless completion.

This proves security.  Its order is at most

\[
|R|+(\alpha(C_0)-1)+\sum_{i\ne0}\alpha(C_i)
=\alpha(H)+|R|-1.
\]

`square`

**Budget consequences.**  By (2), Theorem B proves the desired bound whenever

\[
|R|\le\Delta+2.
\tag{6}

In particular, the hard `Delta=0` case is closed whenever there are two
roots `{r,s}` such that

- `r` is complete to one component `C_0`; and
- every other component is attached to `s`, with `s` attached to at least
  one component besides each component it roots (the second component may
  be `C_0`).

For `Delta=1`, the same construction permits three roots.

## 5. Several simultaneous savings

The reserved-root idea extends to disjoint blocks of roots.  A component can
be cheap even when no single root is complete to it, provided a reserved
root block dominates it collectively.

**Theorem C (disjoint-block multi-saving).**  Let `R subseteq K`,
`|R|>=2`.  Choose distinct designated components

\[
C_{j_1},\ldots,C_{j_m}
\]

and pairwise disjoint nonempty root blocks

\[
B_1,\ldots,B_m\subseteq R
\]

such that `B_l` dominates `C_{j_l}` for every `l`.  Put

\[
Q=R-\bigcup_{l=1}^m B_l,
\]

and call the roots of `Q` mobile.  Suppose:

1. every nondesignated component `C_i` is assigned a root `f(i) in Q`
   which attaches both to `C_i` and to some different outside component;
2. no reserved root in any `B_l` is used for a nondesignated component; and
3. if `R ne K`, then `Q` is nonempty.

Then

\[
\gamma_s(G)\le\alpha(H)+|R|-m.
\tag{7}
\]

**Proof.**  For every designated component `C_{j_l}`, take a maximum
independent set `I_l`, omit one member, and put
`X_l=I_l-{x_l}`.  Since `B_l` dominates `C_{j_l}` and is a clique, it is a
dominating set of `G[C_{j_l} union B_l]`.  The general residual-completion
theorem therefore says that

\[
B_l\cup X_l
\]

is secure on `C_{j_l} union B_l`.  Its outside cost is
`alpha(C_{j_l})-1`.  For every nondesignated component, take the rootless
rooted completion belonging to its assigned mobile root; its cost is at most
that component's independence number.  Retain all of `R`.

For an attack in a designated component, use its local residual-completion
defender.  If a reserved root moves, another member of `R` remains to
dominate `K` because `|R|>=2`; pairwise disjointness means no other
designated component loses a root from its own block.  For an attack in a
nondesignated component, use its rooted defender.  If the mobile root moves,
all other nondesignated components assigned to it remain dominated by their
rootless sets, while every reserved block remains in place.  If `R ne K`
and an omitted clique vertex is attacked, use any mobile root as defender:
all nondesignated components are rootless-dominated and every reserved block
remains in place.  If `R=K`, this last attack type does not exist.

The count is

\[
|R|+\sum_{l=1}^m(\alpha(C_{j_l})-1)
+\sum_{i\notin\{j_1,\ldots,j_m\}}\alpha(C_i)
=\alpha(H)+|R|-m.
\]

`square`

The target follows whenever

\[
|R|-m\le\Delta+1.
\tag{8}

The singleton-block special case takes `B_l={b_l}`; its domination condition
is exactly that `b_l` be complete to its designated component.  Thus in the
hard `Delta=0` branch, one mobile root plus any number of injectively matched
complete reserved roots costs only `alpha(H)+1`.  If `R=K`, every component
is assigned to a disjoint dominating root block, and `m>=|K|-Delta-1`, the
same bound follows with no mobile root.  The cone-with-private-`C5` family is
the extremal singleton-block case `R=K` and `m=|K|`, giving
`gamma_s(G)<=alpha(H)`.

## 6. What a disconnected counterexample must avoid

The already proved cut-vertex theorem implies that every counterexample is
2-connected.  Hence every component `C_i` has at least two attachment
vertices in `K`; otherwise its unique attachment would be a cut vertex.

Combining this with Theorems A--C gives concrete necessary conditions for
any remaining counterexample with disconnected `H`:

1. if `Delta=1`, no two roots can cover the components in the rooted sense
   of Theorem A;
2. if `Delta=0`, no reserved complete root plus one other rooted cover can
   satisfy Theorem B;
3. more generally, no reserved-root configuration of size at most
   `Delta+2` can satisfy Theorem B.
4. more generally still, every disjoint-block cover from Theorem C must
   satisfy `|R|-m>=Delta+2`.

Thus disconnectedness is not itself eliminated, but it is reduced to an
attachment-hypergraph obstruction: every component has at least two clique
attachments, yet all low-order root covers and every low-order
complete-attachment saving must fail.

## 7. Verification

The checker `referees/verify_clique_component_gluing.py` independently
searches for the rooted sets by brute force and directly tests the final set against the
definition of secure domination.  It audits every applicable dominating
clique and component/root assignment in the complete NetworkX Graph Atlas,
plus randomized fixed clique-separator attachments.  The checker does not
use the proof's attack classification when testing the final set.

The completed run returned `PASS`.  In the complete Atlas it checked 2,220
clique separators, 21,942 Theorem-A constructions, 25,495 Theorem-B
constructions, 37,947 singleton-block multi-saving constructions, and 57,722
general disjoint-block constructions.  On 6,455 randomized induced-`P5`-free
fixed-separator graphs it checked a further 49,368, 49,583, 72,895, and
95,846 constructions of those four respective types, with zero failures.
For the general block count, every root was exhaustively labeled as mobile
or reserved to one designated component for each fixed root set; hence
nonsingleton reserved blocks were included rather than inferred from the
singleton special case.

The results should be treated as adversarial finite validation of the three
proofs, not as evidence that their hypotheses always occur.
