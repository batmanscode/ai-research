# Independent referee report: operation route

## Verdict

The central operation lemmas are correct.  I found no mathematical
counterexample to the disjoint-union, substitution, join, twin-expansion,
one-hub, dominating-`C5`, or favorable dominating-`P3` statements.  The exact
finite counts that I reran also agree.

The material is **not yet a proof of** `gamma_s <= alpha + 1` or of an optimal
connected coefficient.  Two statements need qualification before they are
presented as theorem-level consequences, and some finite table rows need a
saved one-command reproducer.

## Claim-by-claim disposition

| Claim | Referee status | Comment |
|---|---|---|
| Additivity on disjoint unions | **Theorem; pass** | Both domination and every legal exchange are confined to one component. |
| Weighted independence under substitution | **Theorem; pass** | Standard projection/lifting proof is complete. |
| `P5`-freeness iff quotient and all nonempty bags are `P5`-free | **Theorem; pass** | Intersections of a substitution bag with an induced subgraph are modules, and `P5` is prime. |
| Exact complete-join trace formula | **Theorem; pass** | The four trace cases are exhaustive.  The pure-factor and mixed-trace arguments handle singleton traces correctly. |
| Complete joins do not amplify `gamma_s/alpha` | **Theorem; pass** | Choosing a maximum-alpha factor gives the claimed inequality.  The `gamma_s=1` exception is safe because a graph with secure domination number one is complete. |
| Dominating-edge quotient four-set | **Theorem with an essential hypothesis** | Correct only as stated in the lemma: **both endpoint bags must contain at least two vertices**.  Do not shorten this to “a quotient with a dominating edge collapses.” |
| One-vertex clique/true-twin expansion does not increase `gamma_s` | **Theorem; pass** | A selected original vertex lifts to one clone; an attack on another clone is handled inside the bag.  Equality is not claimed and is false in general. |
| `gamma_s(G[K_t]) = gamma_r(G)` | **Published theorem; pass for the application** | The cited theorem assumes `G` has no isolated vertex and `K_t` is nontrivial.  These hypotheses hold for the connected graph `B` and `t>=2`; retain them when stating the general formula. |
| `B[K_t]` has `(alpha,gamma_s)=(3,4)` | **Theorem; pass** | The source product formula plus the exact weak-Roman audit gives the result for `t>=2`; `t=1` is the original exact witness. |
| Single false-twin expansion bound | **Theorem; pass** | The two cases (`v` selected or not selected in the old SDS) lift correctly and give `gamma_s(new)<=gamma_s(G)+t-1`. |
| Uniform false-twin blow-up ratio at most one | **Theorem; pass** | Selecting all `t` clones over an ordinary dominating set gives a secure set of size `t gamma(G)`. |
| `B[I_t]` has `gamma_s=4`, `alpha=3t` | **Theorem conditional on the supplied finite bag-vector audit; pass** | The weight-four construction is explicit.  The lower bound checks `t=2,3,4`; for total weight at most three all `t>=4` predicates coincide with `t=4`, so the finite audit closes every `t`. |
| One hub partially meeting two anticomplete `C5`s creates a `P5` | **Theorem; pass** | Boundary edges give the induced path `a0-a1-z-c1-c0`; all possible chords are excluded by construction. |
| The remaining one-hub census has 21 cases, all `(4,4)` | **Exact finite computation; pass** | Independent enumeration of all `31*31=961` labeled nonempty neighborhood pairs gives exactly 21 `P5`-free pairs (three orbits), all with `alpha=gamma_s=4`. |
| Universal hub plus `k C5`, checked for `k=2..5` | **Finite claim as written; true, and strengthen-able** | I reran `k=2,3,4`.  In fact a short direct proof gives `gamma_s=alpha=2k` for every `k>=2`; see below. |
| A dominating induced `C5` is secure | **Theorem; pass** | Every outside vertex has at least two cycle neighbors, since exactly one would yield an induced `P5`; deleting any cycle guard therefore preserves domination. |
| Favorable dominating-`P3` branch | **Theorem; pass with presentation repair** | In the active context `alpha>=3`, if `a-b-c` dominates and a maximum independent set contains `a,c`, then `I union {b}` is secure.  Keep the `alpha>=3` hypothesis unless a standalone stronger proof is supplied. |

## Required wording corrections

1. **Dominating-edge substitutions.**  In `operation_report.md`, the first
   paragraph of the lemma is correct.  The following sentence beginning
   “Thus any alpha-4 equality construction ...” is too easy to read as a
   claim about every dominating-edge quotient.  Replace it by “any such
   construction in which both endpoint bags have order at least two.”

2. **Minimum-order equality structure.**  The equality accounting proves
   even `alpha`, exact two-for-one repairs, and `n >= 5 alpha/2`.  It does not
   by itself prove that a minimum-order equality graph partitions or
   decomposes into induced `C5` gadgets.  “`C5`-like obstruction cores” is a
   useful search heuristic; it must remain labeled as such unless a separate
   classification proof is included.

3. **Dominating-path proof prose.**  The scratch proof in
   `../structure/proof-fragments.md` reaches the correct lemma, but its
   last paragraph says that `b` is anticomplete to the bad cycle “except” for
   `bc`, after the preceding lemma asserted that it is anticomplete.  The
   repair is simpler: the dominating endpoints must be the bad cycle's two
   `I`-vertices, immediately contradicting `b` being anticomplete to the bad
   cycle.  The project should include that corrected proof or cite a proof
   note, rather than only state the result.

4. **Product-formula scope.**  State the source hypothesis “`G` has no
   isolated vertex and `t>=2`” with the uniform true-twin formula.  The
   application to `B` is unaffected.

## A proof upgrading the universal-hub experiment

Let `H_k = K_1 join (k C5)` with universal vertex `z` and `k>=2`.

For the upper bound, select `z`, one cycle vertex in one distinguished cycle,
and a dominating nonadjacent pair in every other cycle.  This has size `2k`.
An attack in a two-guard cycle is handled by a local guard while `z` remains.
In the one-guard cycle, a nonneighbor of its guard is handled by moving `z`;
the resulting two nonadjacent cycle vertices dominate that `C5`, while every
other cycle remains locally dominated.  Hence the set is secure.

For the lower bound, if an SDS omits `z`, its trace on every cycle must itself
securely dominate that cycle, costing at least three per cycle.  If it
contains `z`, every cycle trace is nonempty.  Two different cycle traces
cannot both have size one: attack a nonneighbor of the sole guard in one
cycle and move `z`; the other one-guard cycle is then undominated.  Thus at
most one trace has size one and every other trace has size at least two, so
the total size is at least `1+1+2(k-1)=2k`.  Therefore

`gamma_s(H_k)=alpha(H_k)=2k` for every `k>=2`.

## Independent computation performed

- Exact join formula: 2,704 ordered pairs of nonempty Graph Atlas graphs of
  order at most five and total join order at most ten; zero failures.
- One-hub census: all 961 labeled neighborhood pairs; 21 `P5`-free cases,
  all `(alpha,gamma_s)=(4,4)`.
- Dominating induced `C5`: 109 applicable Graph Atlas occurrences through
  order seven; zero failures.
- Favorable dominating `P3`: 10,720 ordered path/maximum-independent-set
  cases through order seven; zero failures.
- One-vertex true/false clone bounds: 1,167 vertex expansions of Graph Atlas
  graphs through order six; zero failures.
- Two-`C5` substitution table: 1,666 weighted-alpha-four cases; distribution
  `gamma_s=2:526`, `3:915`, `4:225`, matching the report.
- Singleton/`C5` table through quotient order six: 6,586 assignments; no
  positive gap, matching the report.
- Uniform `C5` and `B` attachments to `B`: 42 and 18 admissible cases,
  respectively; every case has a secure set of size at most five.
- The supplied weak-Roman, false-twin bag-count, lexicographic-product, and
  true-twin audits reran without assertion failures.

The independent test driver is `verify_operations_audit.py` in this directory.

## Reproducibility note

The report's named scripts reproduce most rows.  Before publication, add a
small saved driver (and machine-readable output) for the 21-case one-hub
census and for the table rows “one `B` bag plus singletons” and “two `B` bags
plus singletons.”  At present those numbers are plausible and consistent
with the broader substitution search, but they are not exposed by a clearly
named one-command reproducer in the original operation-search workspace.

## Final classification

- **Rigorous theorems:** the operation lemmas listed above, after retaining
  their hypotheses; the exact `alpha=3` slice; the explicit `B[K_t]` family.
- **Exact finite computation:** the atlas/substitution/product censuses and
  SAT bounds through fixed order.
- **Open:** `gamma_s <= alpha+1` for all connected induced-`P5`-free graphs,
  `c_opt=4/3`, and existence of a connected `3/2` equality graph.
- **Unsupported as currently worded:** a full minimum-order decomposition
  into paired induced `C5` gadgets.
