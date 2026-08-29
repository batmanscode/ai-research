# Independent referee report: cut-vertex theorem

## Verdict

**PASS.** I found no mathematical gap in the claimed theorem, rooted
completion lemma, or global gluing argument.

> If `G` is a connected induced-`P5`-free graph with a cut vertex, then
> `gamma_s(G) <= alpha(G) + 1`.

The proof is direct and does not use a minimal-counterexample or induction
hypothesis.  Consequently every counterexample to the candidate inequality,
if one exists, is 2-connected.

## Line-by-line structural audit

1. **Unique deep component.**  In a deep component, a shortest path from
   `x` to a nonneighbor of `x` supplies an induced two-edge prefix `x-a-b`.
   Prefixes from two distinct components of `G-x` give the induced path
   `b-a-x-c-d`.  Cross edges are absent by component separation, and the two
   possible chords incident with `x` are absent by shortestness.  Thus there
   is at most one deep component.

2. **No rooted induced `P4`.**  Since `x` is a cut vertex, a unique deep
   component implies at least one shallow component.  A vertex `y` in a
   shallow component is adjacent to `x` and anticomplete to the deep
   component.  Therefore any induced `x-a-b-c` would extend to the induced
   `y-x-a-b-c`, a contradiction.

3. **Boundary-module property.**  For `L=N_C(x)` and `R=C-L`, if a boundary
   vertex in `L` has mixed adjacency on a connected component `Q` of `G[R]`,
   some edge of `Q` crosses from a neighbor to a nonneighbor.  That edge,
   together with `x` and the boundary vertex, is a rooted induced `P4`.
   Hence each boundary vertex is complete or anticomplete to `Q`.  Since `C`
   is connected, every `Q` has at least one complete boundary neighbor.

## Rooted completion audit

The count of `D_0` is exact.  A clique residual component costs one, equal to
its independence number.  In each anchor group, one boundary anchor replaces
exactly one omitted member of the designated component's maximum independent
set; all nondesignated components retain their full maximum independent sets.
Thus the group costs exactly the sum of the component independence numbers.

If `U` is the undominated part of `L`, then `U` is anticomplete to every
residual component: each residual component contains a selected vertex, and
boundary adjacency to it is all-or-nothing.  Consequently a maximal
independent set `J` of `G[U]` is independent from the union of all chosen
maximum independent sets in the residual components.  This proves

`|D| = |J| + sum_Q alpha(Q) <= alpha(C)`.

The domination assertion is also exact: local selections or their anchors
dominate every residual component, `D_0` dominates `L-U`, and maximality of
`J` makes it dominate `U`.

All defender swaps are valid:

- For an attack in `L-D`, `x` moves; `D` dominates `C`, and the attacked
  vertex (which is adjacent to `x`) dominates the vacated root.
- In a clique residual component, its representative moves to the attack;
  the attacked vertex then dominates that clique.
- In a nondesignated nonclique component, a neighboring independent-set
  guard moves while the complete anchor remains and dominates the whole
  component.
- In the designated component, if an `X=I_Q-{r}` guard can move, the complete
  anchor remains.  Otherwise the anchor moves.  The residual
  `Q-N_Q[X]` is a clique, because two nonadjacent residual vertices together
  with `X` would form an independent set larger than `I_Q`.  The attacked
  vertex belongs to this residual and therefore dominates it after the move.
  Every other component in the same anchor group retains a full maximum
  independent set and remains dominated.

When a boundary or independent-set guard moves, the root `x` remains and
dominates all of `L`; when `x` itself moves, `D` dominates all of `C`.  Hence
`{x} union D` is secure, and deleting `x` leaves a dominating set of `C`, as
required for gluing.

## Global gluing and accounting

For a deep attack, the rooted defender works.  If it is not `x`, `x` remains
and dominates every shallow component.  If it is `x`, the rootless set `D`
dominates the deep component and each shallow maximum independent set
dominates its own component.  For a shallow attack, `x` moves; `D` and all
shallow maximum independent sets preserve domination everywhere.  In each
move by `x`, the attacked vertex is adjacent to and hence dominates the
vacated root.

Writing `a=alpha(C)` and `q=sum_i alpha(A_i)`, maximum independent sets in
the components of `G-x` show `alpha(G) >= a+q`.  Any independent set avoiding
`x` has size at most `a+q`.  An independent set containing `x` contains no
shallow vertex and has size at most `a+1 <= a+q`, because at least one shallow
component exists and hence `q>=1`.  Therefore `alpha(G)=a+q`, and the
constructed set has size at most `1+a+q=alpha(G)+1`.

If there is no deep component, `x` is universal.  A maximum independent set
of `G-x` is maximal and hence dominating; adding `x` gives a secure set.
Since a cut-vertex graph has more than one vertex and `x` is universal,
`alpha(G)=alpha(G-x)`, so its size is exactly `alpha(G)+1`.

## Independent computation

The supplied constructive verifier passed all 268 connected induced-`P5`-free
Atlas graphs with a cut vertex, covering 349 articulation choices and 285
choices with a genuine deep side.

I also wrote `independent_referee.py` without importing any supplied proof
code.  It checked every rooted Graph Atlas instance through order seven
satisfying the exact local rooted hypothesis.  It deliberately did **not**
assume the rooted graph itself was `P5`-free, so this tests the rooted lemma
under a stronger domain.  It exhaustively enumerated all choices permitted by
the proof: maximum independent sets, clique representatives, complete
anchors, designated components, omitted representatives, and maximal
independent boundary completions.

Result:

```text
PASS rooted_instances=2196 allowed_constructions=5001 largest_order=7
```

## Recommended wording corrections before publication

These are precision edits, not repairs to the argument:

1. After the sentence "When the anchor `a` moves ...", explicitly add:
   "The root `x` remains in the set and dominates every vertex of `L`; the
   attacked vertex dominates the vacated anchor because `a` is complete to
   `Q_a`."
2. In the no-deep case, explicitly add:
   "Because `x` is universal and the graph has at least two vertices,
   `alpha(G)=alpha(G-x)`."
3. Replace the audit phrase "no failure of the rooted size bound" by
   "no failure of `|{x} union D| <= alpha(C)+1`, equivalently
   `|D| <= alpha(C)`" to avoid ambiguity about whether the root is counted.
4. Use "a maximal independent set of `G[U]`" consistently.  The construction
   needs maximality for domination and independence for the size bound; it
   does not need this set to be maximum.

Subject to those wording clarifications, the proof is publication-ready from
the standpoint of internal correctness.  Novelty and venue suitability are
separate questions outside this referee audit.
