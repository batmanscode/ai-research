# Composition operations for secure domination in induced-`P5`-free graphs

## Scope and notation

For a graph `G`, write `alpha(G)` for its independence number and
`gamma_s(G)` for its secure domination number. A secure dominating set `D`
is a dominating set such that every `x` outside `D` has a neighboring
defender `d` in `D` for which `(D - {d}) union {x}` is still dominating.

For nonempty graphs `H_v` indexed by `v in V(Q)`, write
`Q[H_v : v in V(Q)]` for substitution: replace `v` by `H_v`, make two bags
complete to one another when their quotient vertices are adjacent, and make
them anticomplete otherwise. The uniform case is the lexicographic product
`Q[H]`.

The graph `B` below is graph6 `KtiSYtlXqwmT`, the complement of the
icosahedral graph. Its established exact parameters are

`alpha(B) = 3` and `gamma_s(B) = 4`.

## 1. Disjoint union: exact and ratio-preserving

**Lemma 1.** For vertex-disjoint graphs `G_1,...,G_k`,

`alpha(disjoint_union_i G_i) = sum_i alpha(G_i)`

and

`gamma_s(disjoint_union_i G_i) = sum_i gamma_s(G_i)`.

**Proof.** Independence is componentwise. If `D` securely dominates the
union, then `D intersect V(G_i)` dominates `G_i`; every attack and every
possible defender also lie in `G_i`, so the intersection securely dominates
`G_i`. Conversely, the union of secure dominating sets of the components is
secure, since every attack and exchange occurs in one component. QED.

Consequently the ratio of a disjoint union is the `alpha`-weighted average
of the component ratios. It can preserve a ratio but cannot increase the
largest component ratio. It also cannot produce a connected example from
more than one nonempty component.

Induced-`P5`-freeness is componentwise. In particular, `k C5` has
`alpha=2k` and `gamma_s=3k`, but is disconnected for `k>1`.

## 2. General substitution: exact independence and `P5` closure

**Lemma 2 (weighted independence formula).** If
`F = Q[H_v : v in V(Q)]`, then

`alpha(F) = max { sum_(v in I) alpha(H_v) : I is independent in Q }`.

**Proof.** The bags met by an independent set in `F` form an independent set
of `Q`, and its intersection with bag `H_v` has size at most `alpha(H_v)`.
Conversely, choose a maximum independent set inside every bag indexed by an
independent set of `Q`. QED.

**Lemma 3 (`P5` substitution closure).** `F` is induced-`P5`-free if and
only if `Q` and every `H_v` are induced-`P5`-free.

**Proof.** The reverse implication is the only point requiring argument.
Every bag is a module of `F`. The path `P5` is prime: it has no nontrivial
proper module. Thus an induced `P5` in `F` either lies in one bag or meets
every bag in at most one vertex. The first option gives an induced `P5` in a
factor; the second projects to an induced `P5` in `Q`. QED.

This proves that substitution is a legitimate construction operation inside
the target hereditary class, but it does not make secure domination
multiplicative. The later exact examples show substantial collapse.

## 3. Complete join: exact formula and a no-amplification theorem

For nonempty `A subseteq V(G)`, define property `P_G(A)` by

`for every x notin A: N_G(x) intersects A is nonempty, or A union {x} dominates G`.

For nonempty `G,H`, define

`m(G,H) = min |A|+|C|`,

where the minimum is over nonempty `A subseteq V(G)` and nonempty
`C subseteq V(H)` satisfying

- `|C| >= 2` or `P_G(A)`; and
- `|A| >= 2` or `P_H(C)`.

Also define

- `s_2(G) = max(2,gamma_s(G))` when `|V(G)|>=2`;
- `s_2(G) = infinity` when `|V(G)|=1`; and
- `epsilon(G,H)=1` when both factors are complete, and infinity otherwise.

**Theorem 4 (exact join formula).**

`gamma_s(G join H) = min { m(G,H), s_2(G), s_2(H), epsilon(G,H) }`.

**Proof.** Let a secure set `S` have traces `A=S intersect V(G)` and
`C=S intersect V(H)`.

If one trace is empty and `|S|>=2`, security in the join is equivalent to
security of the nonempty trace in its factor: exchanges against vertices in
the other factor automatically leave a mixed dominating set. A singleton is
secure precisely when the whole join is complete. These are the last three
terms.

Suppose both traces are nonempty. The set is automatically dominating. For
`x in V(G)-A`, an internal neighbor in `A` can defend `x`, because the
exchange leaves vertices on both sides. If `x` has no internal neighbor in
`A`, a defender must lie in `C`. Removing it still leaves a mixed set when
`|C|>=2`; when `|C|=1`, the exchange is entirely inside `G` and succeeds
exactly when `A union {x}` dominates `G`. This is precisely the first
condition defining `m(G,H)`. The second is symmetric. Thus every candidate
in the displayed minimum is secure and every secure set belongs to one of
the listed cases. QED.

Useful consequences are

- `alpha(G join H)=max(alpha(G),alpha(H))`;
- if both factors have at least two vertices, `m(G,H)<=4`;
- a complete join cannot increase the ratio `gamma_s/alpha`.

For the last statement, choose a factor `J` of maximum independence number.
If `gamma_s(J)>=2`, the pure-factor candidate gives
`gamma_s(G join H)<=gamma_s(J)` while
`alpha(G join H)=alpha(J)`. If `gamma_s(J)=1`, then `J` is complete and has
independence number one; maximality forces the other factor to be complete,
so the join itself is complete. Therefore

`gamma_s(G join H)/alpha(G join H) <= max(gamma_s(G)/alpha(G), gamma_s(H)/alpha(H))`.

The formula was checked with zero failures on every ordered pair of nonempty
Graph Atlas graphs of order at most five (all pairs whose join has order at
most ten).

Exact examples:

- `gamma_s(C5 join C5)=2`, `alpha=2`;
- `gamma_s(B join B)=3`, `alpha=3`.

Thus complete joining destroys, rather than connects while preserving, the
`3/2` ratio of two copies of `C5`.

## 4. True-twin blow-ups: weak Roman domination

Let `G[K_t]` replace every vertex of `G` by a clique of size `t`.

For a graph with no isolated vertex and `t>=2`, the known lexicographic-product
formula is

`gamma_s(G[K_t]) = gamma_r(G)`,

where `gamma_r` is the weak Roman domination number. This is Theorem 3.4(i)
of Cabrera Martínez, Estrada-Moreno, and Rodríguez-Velázquez, *From (secure)
w-domination in graphs to protection of lexicographic product graphs*
(arXiv:2105.05199).

The formula also follows directly by recording how many selected vertices a
secure set has in each clique bag. Counts above two are unnecessary. Empty
bags require exactly the weak-Roman transfer condition, while an unselected
clone in a nonempty clique bag is defended by a selected clone in its own
bag.

Moreover,

`alpha(G[K_t])=alpha(G)` and `gamma_r(G)<=gamma_s(G)`.

Hence true-twin blow-up cannot increase `gamma_s/alpha`.

For `B`, exact enumeration of all `{0,1,2}` weight vectors gives
`gamma_r(B)=4`: there are no valid weak Roman functions at weights 1, 2, or
3, while weight 4 has witnesses. In graph6 label order, one witness is

`(0,0,0,0,0,0,1,0,0,1,0,2)`.

The low-weight audit is:

| weight | bounded vectors | dominating supports | weak Roman functions |
|---:|---:|---:|---:|
| 1 | 12 | 0 | 0 |
| 2 | 78 | 6 | 0 |
| 3 | 352 | 112 | 0 |
| 4 | 1,221 | 741 | 501 |

**Corollary 5 (infinite counterexample family).** For every `t>=1`,

`B[K_t]` is connected and induced-`P5`-free, with
`alpha(B[K_t])=3` and `gamma_s(B[K_t])=4`.

For `t=1` this is the original exact counterexample; for `t>=2` it follows
from the weak Roman formula. This is a useful strengthening from one graph to
an infinite true-twin family, but it does not improve the lower-bound ratio
beyond `4/3`.

As an independent finite cross-check of the product formula, direct secure-set
enumeration gives `gamma_s(B[K_2])=gamma_s(B[K_3])=4`, with no secure set of
size at most three in either graph.

## 5. False-twin blow-ups: a universal ratio collapse

Let `G[I_t]` replace every vertex by an independent set of `t>=2` false
twins.

**Lemma 6.**

`alpha(G[I_t]) = t alpha(G)`

and

`gamma_s(G[I_t]) <= t gamma(G) <= t alpha(G)`.

**Proof.** The independence formula is Lemma 2. Let `D` be a minimum ordinary
dominating set of `G`, and select every clone in every bag indexed by `D`.
For an outside clone in bag `v`, choose a neighboring bag `u in D` and move
one of its selected clones. Because `t>=2`, another selected clone remains in
bag `u`, so every bag that was dominated before remains dominated; it also
dominates the unselected clones in the newly occupied bag, and the moved
guard dominates the vacated clone. Thus the lifted set of size `t gamma(G)`
is secure. Finally `gamma(G)<=alpha(G)` because a maximal independent set is
dominating. QED.

Therefore every false-twin blow-up has `gamma_s/alpha<=1`, no matter how
large the ratio of the original graph was.

For `B` there is a sharper exact formula:

**Proposition 7.** For every `t>=2`,

`gamma_s(B[I_t])=4` and `alpha(B[I_t])=3t`.

**Certificate.** Vertices 6 and 11 in graph6 label order form a dominating
edge of `B`. Selecting two clones in each of these bags is secure for every
`t>=2`: after any defense move, at least one clone remains in the defending
bag, so the same dominating edge support persists.

For the lower bound, a secure set is represented exactly by its bag-count
vector `f in {0,...,t}^12`. The script checks domination and every legal
one-unit transfer on the quotient. No vector of total weight at most three
works for `t=2`, `t=3`, or `t=4`. For `t>=4`, every vector of total weight at
most three leaves every bag non-full, so the predicate is identical to the
`t=4` predicate. This closes all `t>=2`.

Thus the ratio is `4/(3t)` and tends to zero.

## 6. Lexicographic products: exact examples and finite search

Secure domination is not multiplicative under lexicographic product. Direct
bit-set enumeration gives:

| product | alpha | gamma_s | ratio |
|---|---:|---:|---:|
| `C5[C5]` | 4 | 4 | 1 |
| `B[C5]` | 6 | 4 | 2/3 |
| `C5[B]` | 6 | 5 | 5/6 |

For `C5[C5]`, the displayed four-guard witness uses one vertex in each of
four consecutive quotient bags; all 2,625 subsets of size at most three fail.
For the two 60-vertex products, exhaustive search through the first secure
cardinality gives witnesses `(0,1,5,6)` for `B[C5]` and
`(0,1,12,24,25)` for `C5[B]` in lexicographic node order. These values are
independently recomputed by `gamma_s_bit`; no product formula is assumed.

As a finite diagnostic, all 165 ordered lexicographic products `G[H]` with
connected induced-`P5`-free Graph Atlas factors of orders 2 through 5 and
product order at most 15 were evaluated exactly. None had ratio greater than
the larger factor ratio. The only products attaining `3/2` were `C5[K2]`
and `C5[K3]`, which merely preserve the already-known `C5` equality while
keeping `alpha=2`. This search is evidence, not a general theorem.

## 7. Consequence for the connected `3/2` question

The standard modular operations do not turn the disconnected equality
family `k C5` into a connected equality family:

- disjoint union preserves `3/2` but is disconnected;
- complete join cannot increase the factor ratio and sends `C5 join C5` to
  ratio 1;
- true-twin blow-up cannot increase the ratio and cannot raise `alpha`;
- false-twin blow-up forces ratio at most 1;
- representative lexicographic products collapse sharply.

Therefore an `alpha=4, gamma_s=6` connected induced-`P5`-free graph, if it
exists, is unlikely to be a routine modular composition of `C5` or of the
icosahedral-complement counterexample. The next search should emphasize
prime or near-prime graphs with induced `C4` and claw structure, rather than
joins or twin expansions.

## Reproduction

From this directory, install the project requirements and run:

```bash
python verify_operations.py
```

The script contains independent exact predicates for domination, secure
domination, weak Roman domination, false-twin bag-count transfers, weighted
domination, substitution examples, and the join formula audit.

## Source used

- A. Cabrera Martínez, A. Estrada-Moreno, J. A. Rodríguez-Velázquez,
  *From (secure) w-domination in graphs to protection of lexicographic
  product graphs*, arXiv:2105.05199.
- P. V. Maniya, U. K. Gupta, M. A. Henning, D. Pradhan,
  *Secure domination in P5-free graphs*, arXiv:2503.08088.
