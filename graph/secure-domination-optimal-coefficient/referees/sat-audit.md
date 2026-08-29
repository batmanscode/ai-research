# Independent referee report: extremal secure-domination SAT search

Date: 2026-08-29 UTC

## Verdict

**PASS, with publication-wording corrections.** I found no semantic error in
the unconditional SAT encoding. The order-12 UNSAT claims for both targets
have valid, reproducible clausal certificates. The larger frontiers are
internally consistent and reproducible CDCL-solver results, but they are not
proof-trace-certified and therefore must not be described as formal
certificates.

The two finite claims encoded are exactly:

1. For each `7 <= n <= 17`, there is no connected simple induced-`P5`-free
   graph on `n` vertices with `alpha = 4` and no secure dominating set of size
   five. Equivalently, the search reports no such graph with `gamma_s >= 6`.
   Combined with the published `gamma_s <= 3 alpha / 2` theorem, this says no
   such graph in the searched orders attains `gamma_s = 6`.
2. For each `8 <= n <= 16`, there is no connected simple induced-`P5`-free
   graph on `n` vertices with `alpha = 5` and no secure dominating set of size
   six. Equivalently, the search reports `gamma_s <= 6 = alpha + 1` throughout
   this finite range.

These are bounded results. Neither proves an all-orders upper bound, nor does
the alpha-four frontier show that the published coefficient `3/2` is not
optimal at larger independence number.

## Encoding audit

I inspected `search_extremal.py` line by line and checked the following.

### Exact independence number

- Vertices `0,...,alpha-1` are forced independent.
- Every `(alpha+1)`-subset is forced to contain an edge.
- Thus `alpha(G)` is exactly the requested value.
- Fixing one maximum independent set at those labels is lossless under graph
  relabeling.

### Induced-`P5` exclusion

For every five-vertex subset, all 60 undirected path orderings are forbidden.
Each clause is false exactly when the four path edges are present and the
other six pairs are absent. This is an exact induced-`P5` encoding.

### Connectivity

The final-layer reachability claims are recursively supported either by the
previous layer or by a witness that itself requires previous-layer
reachability and a real incident edge. Because layer zero contains only
vertex zero, every forced final claim yields an actual path to zero. The
one-way auxiliary implications are sufficient for this existential
certificate.

### Domination and failed security

- `q[S,y]` is equivalent to `y` having no neighbor in `S`.
- `d[S]` is equivalent to every outside vertex being dominated by `S`.
- When `d[S]` holds, an outside attack vertex is selected for which every
  adjacent member of `S` yields a non-dominating swap.
- Hence every target-size set is either non-dominating or not secure.

Secure domination is upward-closed: if `S` is secure, adding vertices keeps it
secure, since every former valid swap remains a dominating superset. Because
the instances have more than the target number of vertices, excluding every
target-size secure set also excludes every smaller secure set.

### Outside-type symmetry break

Every vertex outside the fixed maximum independent set must have a nonempty
neighborhood in that set; otherwise it enlarges the independent set. The
encoding sorts these nonzero bit-vectors in nondecreasing numerical order.
Outside vertices are otherwise unlabeled and can always be permuted into that
order, while all substantive constraints are graph-isomorphism invariant.
The symmetry break is therefore lossless.

I exhaustively checked the mask-order truth table for alpha four and five: it
accepts every and only nondecreasing adjacent pair. I also canonically
relabelled the known icosahedral-complement positive fixture (`alpha=3`, no
secure triple) and fixed all its edges; both the symmetry-free and sorted
encodings returned SAT.

### Optional reductions

The `--minimal-reductions` constraints are not used in the two unconditional
frontiers. I did not rely on their external minimum-counterexample theorem.
The reachability encodings for vertex deletion and complement connectivity
are structurally sound; the adjacent-true-twin constraint also has the needed
direction. Results using those flags must continue to be labeled conditional.

## Executable checks performed

1. `sha256sum -c agent-sat-extremal/SHA256SUMS`: all five listed artifacts
   passed.
2. The stored DIMACS headers and bodies agree exactly:
   - alpha four: 13,542 variables and 120,233 clauses;
   - alpha five: 13,674 variables and 133,775 clauses.
3. Regenerating both order-12 formulas and proofs produced **byte-identical**
   CNF and DRUP files (matching SHA-256 hashes).
4. Rechecking every retained proof addition by MapleSAT unit propagation,
   while soundly ignoring deletion lines, gave:
   - alpha four: 5,375 RUP additions, 23,105 ignored deletions, no failed
     additions, empty clause at addition 5,374;
   - alpha five: 12,449 RUP additions, 19,995 ignored deletions, no failed
     additions, empty clause at addition 12,448.
5. `test_encoding.py` passed all 20,000 bundled randomized fixed-edge checks.
6. I added an exhaustive fixed-edge comparison between the SAT formula and
   independent direct predicates:
   - `(n, alpha, target)=(6,4,5)`: all 512 assignments;
   - `(7,4,5)`: all 32,768 assignments;
   - `(7,5,6)`: all 2,048 assignments.
   There were no mismatches.
7. For every frontier JSON, independently computed combinatorial clause-family
   totals agree with the recorded clause total. Older alpha-four JSON uses the
   previous family names `fixed_independent_four` and `no_independent_five`,
   but its counts are the same constraints.

## Evidence levels

| Result | Referee status |
|---|---|
| alpha four, order 12 | Formally trace-checked UNSAT for the emitted CNF; exactly reproduced |
| alpha five, order 12 | Formally trace-checked UNSAT for the emitted CNF; exactly reproduced |
| alpha four, orders 7--17 | Coherent contiguous CDCL UNSAT portfolio; order 12 certified, larger boundary untraced |
| alpha five, orders 8--16 | Coherent contiguous CDCL UNSAT portfolio; order 12 certified, order 16 from Glucose and untraced |
| order-18 reduced alpha-four run | Conditional on external reductions; correctly excluded from unconditional frontier |

## Corrections recommended before publication

1. Change “CaDiCaL 1.9.5 produced the contiguous UNSAT portfolios” to the
   precise statement: CaDiCaL produced alpha-four through order 17 and
   alpha-five through order 15; Glucose 4.2 closed alpha-five order 16.
2. Keep the existing distinction between order-12 clausal certificates and
   untraced higher-order CDCL evidence. Do not call the full frontiers
   formally certified unless DRAT/LRAT proofs are generated and checked.
3. Add the icosahedral-complement SAT fixture to `test_encoding.py`. The two
   current randomized suites report zero qualifying graphs, so they exercise
   rejection paths but no positive model. The independently run positive
   fixture passed both sorted and unsorted encodings.
4. Update `generate_check_drup.py`'s stale docstring (“producer is CaDiCaL”):
   the checked successful artifacts are produced by Glucose 4.2. The code and
   JSON already identify the actual producer correctly.
5. Normalize or document the two historical clause-family key names in older
   alpha-four JSON. This is metadata/schema drift, not a logical discrepancy.
6. `SHA256SUMS` paths are rooted one directory above `agent-sat-extremal`, so
   document that the checksum command is run from the parent directory (or
   rewrite paths relative to the checksum file).

No correction is required to the mathematical semantics of the generic
alpha-four or alpha-five encodings.
