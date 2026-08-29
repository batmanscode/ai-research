# Cut vertices in the `gamma_s <= alpha + 1` problem

## Conclusion

The cut-vertex reduction is valid, in a stronger form than a
minimum-counterexample argument.

> **Theorem.** If `G` is a connected induced-`P5`-free graph with a cut
> vertex, then
>
> \[
> \gamma_s(G)\leq\alpha(G)+1.
> \]

Consequently, if the candidate inequality fails anywhere, **every**
counterexample is 2-connected. In particular, a minimum counterexample can
be assumed 2-connected. The proof does not assume that smaller graphs satisfy
the candidate inequality.

The construction below is explicit. The key point missing from naive gluing
is that one boundary guard can serve several deep residual components, as long
as exactly one of those components omits one independent-set vertex. The full
independent set in every other component keeps it dominated when the shared
boundary guard moves.

## Definitions

A set `S` is a secure dominating set if it dominates `G` and, for every
`v` outside `S`, some neighbor `u` of `v` in `S` can move to `v` while the
resulting set remains dominating. Its minimum order is `gamma_s(G)`.

Fix a cut vertex `x`, and let the components of `G-x` be called **shallow**
if every one of their vertices is adjacent to `x`, and **deep** otherwise.

## Structural facts at a cut vertex

### At most one component is deep

Suppose two components are deep. In each, take the first two vertices after
`x` on a shortest path from `x` to a nonneighbor of `x`. Calling these
vertices `a,b` and `c,d`, respectively,

\[
b-a-x-c-d
\]

is an induced `P5`: shortestness excludes `xb` and `xd`, and distinct
components of `G-x` have no cross edges. This is impossible.

### The deep side has no rooted induced `P4`

Assume a deep component `C` exists. There is also at least one shallow
component; choose a vertex `y` in it. If `x-a-b-c` were an induced `P4` in
`G[C union {x}]`, then

\[
y-x-a-b-c
\]

would be an induced `P5`, because `y` has no neighbor in `C`. Hence no such
rooted `P4` exists.

Put

\[
L=N_C(x),\qquad R=C\setminus L.
\]

For every component `Q` of `G[R]`, each vertex of `L` is either complete or
anticomplete to `Q`. Indeed, if `a in L` distinguishes adjacent vertices
`b,c` of `Q`, then `x-a-b-c` is a rooted induced `P4`. Connectedness of `Q`
propagates this all-or-nothing adjacency along its edges. Every `Q` has at
least one complete neighbor in `L`, because `C` is connected.

## Rooted completion lemma

The following lemma contains the real gluing work.

> **Lemma.** Let `H=G[C union {x}]` be as above. There is a set `D` contained
> in `C` such that:
>
> 1. `D` dominates `C`;
> 2. `{x} union D` is secure in `H`; and
> 3. `|D| <= alpha(C)`.

### Construction

For every component `Q` of `G[R]`, fix a maximum independent set `I_Q`.

1. If `Q` is a clique, put one arbitrary vertex of `Q` into `D_0`.
2. If `Q` is not a clique, choose a vertex `a(Q) in L` complete to `Q`.
   Group the nonclique components that chose the same anchor `a`.
3. In every nonempty anchor group, choose one designated component `Q_a`.
   Put `a` in `D_0`, put `I_Q` in `D_0` for every nondesignated component
   of the group, and put `I_{Q_a}-{r_a}` in `D_0`, where `r_a` is any member
   of `I_{Q_a}`.

For a group anchored at `a`, the count is exactly

\[
1+(|I_{Q_a}|-1)+\sum_{Q\ne Q_a}|I_Q|
=\sum_Q\alpha(Q).
\]

The clique components also cost exactly their independence number, namely
one. Thus

\[
|D_0|=\sum_{Q\in\mathcal Q}\alpha(Q).
\]

Let `U` be the vertices of `L` not dominated by `D_0`, choose a maximal
independent set `J` of `G[U]`, and set

\[
D=D_0\cup J.
\]

The set `D` dominates `C`: the local selections dominate every component of
`R`, `D_0` dominates `L-U`, and `J` dominates `U`.

Moreover, `U` is anticomplete to `R`. For a clique component, its selected
representative would dominate any boundary neighbor. For a nondesignated
nonclique component, its full `I_Q` is nonempty. For a designated nonclique
component, `I_Q-{r_a}` is still nonempty because `alpha(Q)>=2`. Since boundary
adjacency to `Q` is all-or-nothing, a vertex of `U` cannot touch any such
`Q`.

It follows that

\[
J\cup\bigcup_Q I_Q
\]

is independent in `C`. Therefore

\[
|D|=|J|+\sum_Q\alpha(Q)\leq\alpha(C).
\]

### Security proof

Let `S_0={x} union D`.

- An attack at `v in L-D` is defended by `x`. After `x` moves to `v`, the
  set `D` still dominates `C`, and `v` dominates `x`.
- In a clique component `Q`, its selected representative defends every
  unselected vertex of `Q`.
- In a nondesignated nonclique component, the full maximum independent set
  `I_Q` dominates `Q`. A neighbor of the attacked vertex in `I_Q` can move;
  the anchor remains and is complete to `Q`.
- In a designated component `Q_a`, put `X=I_{Q_a}-{r_a}`. If the attacked
  vertex has a neighbor in `X`, that neighbor moves and anchor `a` remains.
  Otherwise the anchor moves. The residual

  \[
  Q_a-N_{Q_a}[X]
  \]

  is a clique: two nonadjacent residual vertices together with `X` would be
  an independent set larger than `I_{Q_a}`. Hence `X` together with the
  attacked vertex dominates `Q_a`. When anchor `a` moves, every other
  component assigned to `a` remains dominated by its full `I_Q`; the root
  `x` remains and dominates `L`, while the attacked vertex dominates the
  vacated anchor because `a` is complete to `Q_a`.

In every deep attack, `x` remains unless it is itself the stated defender;
when `x` moves, `D` dominates all of `C`. Thus `S_0` is secure and is also
stable in the precise sense needed for gluing: `S_0-{x}=D` dominates `C`.

## Completing the whole graph

If no deep component exists, `x` is universal. Let `I` be a maximum
independent set of `G-x`. Then `{x} union I` is secure: `x` defends every
outside attack, while `I` continues to dominate `G-x`; the attacked vertex
dominates the vacated root. Because `x` is universal and a cut-vertex graph
has more than one vertex, `alpha(G)=alpha(G-x)`. The set therefore has order
`alpha(G)+1`.

Now suppose `C` is the unique deep component and `A_1,...,A_t` are the
shallow components. Let `I_i` be a maximum independent set of `A_i`, and use
the rooted set from the lemma:

\[
S=\{x\}\cup D\cup\bigcup_{i=1}^t I_i.
\]

Deep attacks use their defender from the rooted lemma. If that defender is
not `x`, then `x` continues to dominate every shallow component. If it is
`x`, the sets `D` and `I_i` dominate all components after the move. Every
shallow attack is defended by `x`, because `D` dominates `C` and every `I_i`
dominates its own component after `x` moves.

Finally, write `a=alpha(C)` and `q=sum_i alpha(A_i)`. An independent set not
containing `x` has maximum size `a+q`. An independent set containing `x`
uses no shallow vertex and has size at most `a+1`, which is at most `a+q`
because `q>=1`. Hence

\[
\alpha(G)=a+q
\]

and

\[
|S|\leq 1+a+q=\alpha(G)+1.
\]

This proves the theorem.

## Why the obvious shortcut is not a proof

It is not enough to take `x` together with an arbitrary maximum independent
set of the deep component. There are induced-`P5`-free articulation graphs
where such a set is insecure. One 8-vertex example has vertices

`x,p,u1,u2,v,w1,w2,y`

and edges

- `xp, xy`;
- `p` joined to each of `u1,u2,v,w1,w2`;
- `u1v, u2v, u1w1, u2w2, w1w2`.

The set `{u1,u2}` is a maximum independent set of the deep component, but an
attack at `v` defeats `{x,u1,u2,y}`: moving `u1` leaves `w1` undominated and
moving `u2` leaves `w2` undominated. The anchor-group construction instead
uses `p` and avoids this failure. Thus the reduction is valid, but the
defender bookkeeping is essential.

## Independent finite audit

Two executable checks accompany this report.

- `../referees/verify_cut_vertex.py` constructs the proof set directly for every cut
  vertex of every connected induced-`P5`-free graph in the complete NetworkX
  Graph Atlas (all unlabeled graphs through order 7). It checked 268 graphs,
  349 articulation choices, and 285 choices with a genuine deep side. Every
  constructed set was secure, every independence identity held, and every
  size was at most `alpha+1`.
- `../referees/analyze_cut_vertex_atlas.py` independently enumerates all vertex subsets to compute
  `alpha` and `gamma_s`. It found no violation of `gamma_s<=alpha+1` among
  the same 268 articulation graphs (indeed, all happened to satisfy the
  stronger `gamma_s<=alpha` at these small orders). It also found no failure
  of `|{x} union D|<=alpha(C)+1`, equivalently `|D|<=alpha(C)`.
- `../referees/stress_cut_vertex.py` independently generated 10,000 rooted module graphs
  through deep-side order 10. Of these, 6,498 were connected and induced-
  `P5`-free; exact subset enumeration found a rooted set within the claimed
  budget in every case, and the explicit anchor-group construction also
  passed after a shallow leaf was attached.

These computations test the construction and formulas; the theorem itself
is established by the proof above.

Run from this project directory after installing
`computation/requirements.txt`:

```bash
python referees/verify_cut_vertex.py
python referees/verify_cut_vertex_independent.py
python referees/analyze_cut_vertex_atlas.py
python referees/stress_cut_vertex.py --trials 10000 --max-n 10
```
