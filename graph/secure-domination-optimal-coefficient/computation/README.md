# Exact extremal search for secure domination in connected P5-free graphs

This directory is an isolated computational audit of two possible sharp
bounds for connected induced-P5-free graphs:

1. whether the published `3 alpha / 2` coefficient is attained when
   `alpha = 4`, which requires `gamma_s = 6`; and
2. whether the stronger global candidate `gamma_s <= alpha + 1` survives its
   next case, `alpha = 5`.

No graph meeting either obstruction was found.  These are finite SAT results,
not all-orders theorems.

## Exact status

| Target | Orders solved UNSAT | Meaning |
|---|---:|---|
| `alpha = 4`, no secure 5-set | 7 through 17 | no connected induced-P5-free graph of these orders has `gamma_s = 6` |
| `alpha = 5`, no secure 6-set | 8 through 16 | no graph of these orders refutes `gamma_s <= alpha + 1` |

A secondary hypothesis-mining portfolio tested the still stronger statement
`gamma_s <= alpha` away from the known `alpha=3` obstruction.  It found no
`alpha=4, gamma_s>=5` graph through order 14, and no
`alpha=5, gamma_s>=6` graph through order 13.  These finite UNSAT runs have no
proof traces and are reported only as a guide for the proof search: so far the
12-vertex icosahedral-complement obstruction is isolated to `alpha=3`.

### Dominating-clique branch

An exact existential selector also tests graphs that have a dominating
clique. The general `gamma_s <= alpha+1` candidate automatically survives the
larger generic frontiers above, which impose no clique assumption.

For the stronger subclaim `gamma_s <= alpha` when the *minimum* dominating
clique has size at least three, the model exactly excludes universal vertices
and dominating edges. It found no counterexample through:

- order 15 for `alpha=4` (Glucose 4.2; 36,255 variables, 346,640 clauses); and
- order 14 for `alpha=5` (Glucose 4.2; 41,979 variables, 354,782 clauses).

These are untraced finite results, not a structural theorem. As a positive
control, the unrestricted dominating-clique model at `alpha=3,n=12` found
graph6 `KCV@|Xtyne^_`; the plain verifier independently gives `gamma_s=4`,
and direct enumeration gives minimum dominating-clique size two. The selector
therefore recovers the known obstruction type while the size-three clauses
remove precisely that branch.

The lower starting orders are lossless.  In every connected graph on at least
two vertices, `V - {v}` is secure for any vertex `v`: the omitted vertex can
be defended by a neighbor, and the swap omits only that neighbor.  Hence
`gamma_s >= 6` requires at least seven vertices and `gamma_s >= 7` requires at
least eight.

CaDiCaL 1.9.5 produced the `alpha=4` portfolio through order 17 and the
`alpha=5` portfolio through order 15. Glucose 4.2 closed the `alpha=5`,
order-16 case. At order 12, MapleSAT and Glucose 4.2 independently agreed for
`alpha = 4`, and Glucose 4.2 independently agreed for `alpha = 5`. The largest
completed generic instances were:

- `alpha=4`, `n=17`: 159,477 variables, 1,291,205 clauses, 367.7 solver seconds;
- `alpha=5`, `n=16`: 172,144 variables, 1,419,367 clauses, 521.7 solver seconds
  with Glucose 4.2 (the first 360-second CaDiCaL attempt timed out).

The JSON result files contain exact clause-family counts and solver statistics.
At order 12 for each target, Glucose 4.2 emitted a DRUP trace and a separate
MapleSAT propagation pass checked every retained addition as RUP and confirmed
derivation of the empty clause.  Deletion lines were conservatively ignored.
The larger-order instances have no DRAT/LRAT proof trace.  Accordingly, the
order-12 cases have checkable clausal certificates, while the higher-order
boundary remains reproducible exact CDCL-solver evidence rather than formally
certified unsatisfiability.

## Encoding

`search_extremal.py` uses edge variables for a labeled simple graph and adds:

- a fixed independent set on vertices `0,...,alpha-1`, plus a clause requiring
  an edge in every `(alpha+1)`-set (exact independence number after lossless
  relabeling);
- all 60 undirected path orderings on every 5-set, forbidding every induced
  P5;
- layered reachability from vertex 0, giving an explicit connectivity
  certificate;
- exact variables `d[S]` saying a target-size set `S` dominates; and
- for every dominating `S`, an outside attack `x` such that each adjacent
  defender produces a non-dominating swap.

Thus every target-size set fails secure domination.  Secure domination is
upward-closed: if `S` is secure, every superset is secure.  Therefore ruling
out a secure 5-set rules out every smaller secure set, and likewise at size 6.

Outside vertices are sorted by their nonempty bit-vector of neighbors in the
fixed independent set.  This is a lossless symmetry break because those
vertices may be permuted arbitrarily.  Small no-symmetry runs agree.

The optional `--minimal-reductions` model additionally encodes
2-connectivity, complement-connectivity, and absence of adjacent true twins.
Its negative results are conditional on the separate theorem that a minimum
counterexample has these properties; the generic portfolios do not use it.
At order 18 this reduced model is UNSAT (Glucose 4.2, 328,527 variables,
2,066,498 clauses, 615.5 seconds), while the generic model reached its
910-second wall limit without a result.  Thus order 18 is deliberately not
included in the unconditional table above.

## Independent checks

`test_encoding.py` fixes 10,000 random edge assignments compatible with the
distinguished independent set for each of `(alpha, target size) = (4,5)` and
`(5,6)`.  For every assignment, SAT satisfiability agrees with separate direct
set predicates for connectivity, independence, induced P5s, domination, and
secure exchange. It also checks the known icosahedral-complement positive
fixture with and without the outside-type symmetry break, so the suite covers
both acceptance and rejection paths.

`verify_candidate.py` shares neither SAT clauses nor auxiliary variables.  If
a model is ever found, it exhaustively emits:

- graph6 and an edge list;
- maximum independent sets and every induced P5 (if any);
- a failure witness for every target-size set; and
- an explicit secure set at the next size with a complete defense map.

No candidate currently exists to certify.

`generate_check_drup.py` reproduces the order-12 clausal certificates. The
files under `proofs/` include lossless `.xz` streams of the original DIMACS
formula and DRUP trace, split into GitHub-friendly 128 KiB parts, plus the
machine-readable independent audit. Reconstruct a raw artifact with, for
example:

```bash
cat proofs/a4_n12_glucose.cnf.xz.part-* | xz -dc > a4_n12_glucose.cnf
```

The raw CNF/DRUP hashes printed in the referee report match the reconstructed
files byte for byte. Only artifacts whose audit status is `PASS` are evidence;
the valid prefixes are `a4_n12_glucose` and `a5_n12_glucose`.

## Composition searches

Two non-SAT searches attacked natural infinite-family constructions:

- All 1,199,511 independent-set substitutions of sizes 1--3 over every
  connected induced-P5-free graph-atlas skeleton of order 2--7.  Among 69,769
  outputs with weighted independence number four, every graph had a secure
  5-set.
- All 1,199,511 substitutions over the same 637 skeletons using modules
  `K1`, `C5`, or the icosahedral complement.  Among 68,486 alpha-four outputs
  of order at most 50, every graph had a secure 5-set.

Substitution is a particularly natural route because induced P5-freeness is
preserved when substituting into a P5-free skeleton (P5 is prime).  The
negative result explains why combining the known tight disconnected `C5`
gadgets, or inflating the 12-vertex `4/3` example, does not automatically
approach `3/2` in the connected class.  It is still only a bounded family
search.

## Reproduction

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

python test_encoding.py
python generate_check_drup.py --n 12 --alpha 4 --secure-size 5 \
  --producer glucose42 --checker maplesat --prefix reproduced-a4-n12
python search_extremal.py --n 17 --alpha 4 --secure-size 5 \
  --solver cadical195 --output reproduced-a4-n17.json
python search_extremal.py --n 16 --alpha 5 --secure-size 6 \
  --solver glucose42 --output reproduced-a5-n16.json
python search_extremal.py --n 15 --alpha 4 --secure-size 4 \
  --dominating-clique --min-dominating-clique-size 3 \
  --solver glucose42 --output reproduced-domclique3-a4-n15.json
python atlas_substitution_search.py
python module_composition_search.py
```

The largest SAT runs require several minutes and substantial transient memory.
The checked-in JSON outputs are under `results/`; the two composition scripts
write fresh JSON beside themselves so a reproduction cannot silently overwrite
the retained results.
