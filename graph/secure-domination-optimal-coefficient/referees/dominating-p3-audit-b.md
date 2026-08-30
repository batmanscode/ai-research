# Referee B audit: dominating induced `P3`

## Verdict

**PASS.** I find the theorem and the equality lemma mathematically sound. In
particular, the proof remains valid for every minimum-weight maximum independent
set `I`, every maximizing tied choice of the omitted pair `x,y`, attacks equal
to `x` or `y`, and witnesses equal to an omitted member of `I`.

## Clean-room derivation

Let `D={a,b,c}` induce `a-b-c`, let `H=G-D`, and assume
`alpha(H)=alpha(G)=q>=3`. Choose a maximum independent set `I` of `H` of
minimum `D`-weight, then choose `x,y in I` with maximum degree-sum into `D`.
Write `X=I-{x,y}` and `S=D union X`.

The set `S` dominates. Any outside vertex adjacent to `X` is securely defended
by that neighbor, since the exchange leaves all of `D` untouched. Consider an
undefendable attack `v` anticomplete to `X`. For each `d in N_D(v)`, failure of
the exchange `d -> v` produces an undominated vertex `p_d`. The removed vertex
`d` itself cannot be that vertex, because another path vertex still dominates
it. Thus

- `p_d in H-S`, `p_d != v`, and `p_d v` is a nonedge;
- `N(p_d) intersection S={d}`; hence `p_d` is anticomplete to `X` and has
  `D`-degree one.

Consequently `X union {v,p_d}` is an independent `q`-set in `H`. This is true
even when `v` or `p_d` is one of `x,y`. If `r=delta_D(v)` and
`m=delta_D(x)+delta_D(y)`, minimum weight gives

`m <= r+1`.                                                     (1)

Every maximum independent set of `H` meets each of `N(a),N(b),N(c)`, since a
missed path vertex could otherwise be added to form an independent
`(q+1)`-set in `G`. If every member of `I` had `D`-degree one, meeting both
`N(a)` and `N(c)` would give an `a`-only vertex and a `c`-only vertex; together
with `a-b-c` they induce a `P5`. Hence some member of `I` has `D`-degree at
least two, all have positive `D`-degree, and

`m >= 3`.                                                       (2)

Since `r<=3`, (1)--(2) first leave `r=2` or `3`. If `r=3`, the distinct
witnesses `p_b,p_c` must be adjacent, or `X union {v,p_b,p_c}` is an
independent `(q+1)`-set. Their adjacency makes
`a-v-c-p_c-p_b` an induced `P5`; all possible chords are excluded by the
witness properties and the induced path `a-b-c`. Thus `r!=3`, so `r=2` and
`m=3`.

The maximizing-pair choice now implies that `I` has exactly one vertex of
`D`-degree two and every other vertex has degree one. Every maximizing pair
contains the unique degree-two vertex, regardless of ties, so every vertex of
the nonempty set `X` is a singleton-attachment vertex.

The three possible two-element neighborhoods of `v` close as follows.

- If `N_D(v)={a,c}`, then `p_a p_c` is forced, or again there is an independent
  `(q+1)`-set. For any `z in X`, according as its singleton attachment is `a`,
  `b`, or `c`, respectively, one obtains the induced path
  `c-p_c-p_a-a-z`, `z-b-a-p_a-p_c`, or `a-p_a-p_c-c-z`.
- If `N_D(v)={a,b}`, a `c`-only `z in X` gives the induced path
  `z-c-b-a-p_a`. If no such `z` exists, the independent `q`-set
  `X union {v,p_a}` is anticomplete to `c`, so adding `c` contradicts
  `alpha(G)=q`.
- The neighborhood `{b,c}` is symmetric, using `z-a-b-c-p_c` or adding `a`
  to `X union {v,p_c}`.

I checked every displayed path chord-by-chord. Witnesses for different path
vertices are necessarily distinct because each has a different unique
neighbor in `D`; witnesses also cannot lie in `X` because `X subset S`.
Thus none of the paths or enlargement arguments has a hidden vertex-coincidence
problem. The assumed failed attack is impossible, proving that `S` is secure
and has size `q+1`.

## Completion of the theorem

I also independently re-derived the imported completion lemma. For any
dominating set `D` with nonempty `H=G-D`, take a maximum independent set `I`
of `H`, omit any `x in I`, and put `T=D union (I-{x})`. Attacks adjacent to an
unomitted member of `I` are defended while retaining `D`. For an attack `v`
with no such neighbor, choose `d in D intersection N(v)`. If exchanging `d`
for `v` failed, an undominated witness `p` would be outside the exchanged set,
anticomplete to `I-{x}` and to `v`; hence
`(I-{x}) union {v,p}` would be an independent set of `H` larger than `I`.
Therefore `gamma_s(G)<=|D|+alpha(H)-1`.

For the dominating path, `H` is nonempty because `alpha(G)>=3`. If
`alpha(H)<=alpha(G)-1`, this lemma gives the desired `alpha(G)+1` bound; the
equality case is exactly the lemma audited above.

## Independent computational attempts to falsify

I wrote predicates independent of the proof criterion and checked security
directly from its definition.

- Random/non-Atlas stress: 6,000 generated graphs of orders 8--20, consisting
  of fixed-dominating-path rejection samples, random connected split graphs,
  and random connected cographs. There were 1,377 induced-`P5`-free samples,
  1,309 with independence number at least three, 97,767 dominating induced
  paths, 34,369 equality-case paths, and 366,730 permitted constructions after
  quantifying over every minimum-weight maximum `I` and every maximizing pair.
  All 366,730 constructed sets were secure.
- Exact SAT stress: fixing only labels for `D`, a selected minimum-weight
  maximum `I`, and a selected maximizing pair (which loses no generality), I
  encoded domination by `D`, the induced path, `P5`-freeness,
  `alpha(H)=alpha(G)=q`, minimum weight, the maximizing-pair inequalities, and
  exact insecurity of the constructed set. All 42 cases
  `8<=n<=14`, `3<=q<=n-3`, were UNSAT. These runs have no retained proof traces
  and are corroboration, not part of the mathematical proof.
- As a separate check, the complement of the icosahedral graph has 60
  equality-case dominating paths and 240 allowed constructions when all ties
  are retained; all 240 passed.

No counterexample or proof defect was found.
