# Independent audit: the failed private/M packing lemma

## Verdict

The graph6 certificate `I{OeEAg}?` is correct.  A fresh
standard-library-only implementation (`independent_packing_counterexample.py`)
reconstructs the graph and verifies every claimed value below.  No research
module or NetworkX is imported.

## The graph

The graph has 10 vertices and edge list

```text
01 02 03 06 07 08 09 12 14 16 17 19 25 28 29 39 48 49
```

Take `K={0,1,2}`, `P={3,4,5}`, and `M={6,7,8,9}`.  The outside
K-neighborhoods are

```text
3:{0}   4:{1}   5:{2}
6:{0,1} 7:{0,1} 8:{0,2} 9:{0,1,2}
```

Thus `K` is a dominating triangle, each private region is a singleton,
the three private vertices are pairwise nonadjacent, and `M` is independent.
The graph is connected and induced-​`P5`-free.

## Exact quantities

Exhaustive subset enumeration gives:

| quantity | value | certificate |
|---|---:|---|
| independence number `alpha(G)` | 5 | `{3,4,5,6,7}` |
| domination number of `G[M]` | 4 | `M` itself (it is independent) |
| secure domination number `gamma_s(G)` | 4 | `{0,1,2,3}` is secure; no set of size ≤3 is secure |
| secure domination number `gamma_s(G-K)` | 5 | e.g. `{3,4,5,6,7}`; no set of size ≤4 is secure |
| local completion `|P|+gamma(M)` | 7 | `3+4` |
| one-hub-lift value `1+gamma_s(G-K)` | 6 | adding any one of `0,1,2` to the displayed 5-set is secure |

There is no dominating pair and no dominating induced `P3` (all pairs and all
3-subsets were checked directly).  The graph therefore sits in the intended
hard branch even though its actual secure domination number is only 4.

## Failure of the proposed packing inequality

For `R` contained in `P`, define

\[
B(G)=\max_R\left(|R|+\alpha(G[M-N(R)])\right).
\]

The complete calculation is

| `R` | `M-N(R)` | `alpha` | total |
|---|---|---:|---:|
| `∅` | `{6,7,8,9}` | 4 | 4 |
| `{3}` | `{6,7,8}` | 3 | 4 |
| `{4}` | `{6,7}` | 2 | 3 |
| `{5}` | `{6,7,8,9}` | 4 | 5 |
| `{3,4}` | `{6,7}` | 2 | 4 |
| `{3,5}` | `{6,7,8}` | 3 | 5 |
| `{4,5}` | `{6,7}` | 2 | 4 |
| `{3,4,5}` | `{6,7}` | 2 | 5 |

Consequently

\[
B(G)=5 < 6=\gamma(G[M])+2.
\]

This refutes the proposed *packing strategy*, not the secure-domination
conjecture.  It shows that the local completion and one-hub-lift routes must
be coupled; an independent-set charge in `M` cannot by itself pay for the
local bound.

## Reproduction

```bash
python independent_packing_counterexample.py
```

The command emits the full machine-readable certificate as JSON and asserts
all headline claims before exiting successfully.

