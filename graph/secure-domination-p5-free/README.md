# A 12-vertex counterexample in secure domination

**Visual paper:** [`website/index.html`](website/index.html)

**Design contract:** [`DESIGN.md`](DESIGN.md)

**Published finding:** [Emergent Mind research findings](https://www.emergentmind.com/open-problems/improve-secure-domination-bound-connected-p5-free-graphs#research-findings)

## Result

Let \(I\) be the icosahedral graph and let \(G=\overline I\). Then

\[
G\text{ is connected and induced-}P_5\text{-free},\qquad
\alpha(G)=3,\qquad \gamma_s(G)=4.
\]

Consequently the natural coefficient-one strengthening
\(\gamma_s(G)\leq\alpha(G)\) is false for connected induced-\(P_5\)-free
graphs with \(\alpha\geq3\). If \(c_{\rm opt}\) denotes the best universal
coefficient in \(\gamma_s(G)\leq c\alpha(G)\) for that class, this example and
the published upper bound give

\[
\boxed{\frac43\leq c_{\rm opt}\leq\frac32}.
\]

The example is encoded by graph6 string `KtiSYtlXqwmT`.

## Definitions

A set \(S\) dominates a graph when every vertex outside \(S\) has a neighbor
in \(S\). It is *secure* when every outside vertex \(v\) can be exchanged for
some adjacent guard \(u\in S\), leaving
\((S\setminus\{u\})\cup\{v\}\) dominating. The minimum size of such a set is
\(\gamma_s\). The independence number \(\alpha\) is the largest size of a
pairwise nonadjacent vertex set.

## Exact proof certificate

`verify_counterexample.py` uses only the Python standard library for the core
checks. It exhaustively verifies:

- 12 vertices, 36 edges, degree sequence \(6^{12}\), and connectivity;
- no induced \(P_5\) among all \(\binom{12}{5}=792\) five-vertex subsets;
- 20 independent triples and no independent four-set, hence \(\alpha=3\);
- no secure triple among all \(\binom{12}{3}=220\) triples;
- 435 secure four-sets, including \(\{0,1,2,3\}\), with a defense map;
- recognition as the complement of an icosahedron;
- automorphism-group order 120 and five triple orbits.

The 220 triple failures split into 120 non-dominating triples and 100
dominating triples with a certified bad attack. Thus no set of size three is
secure, while the explicit secure four-set proves \(\gamma_s=4\).

Run from this directory:

```bash
python3 verify_counterexample.py --output data/counterexample_certificate.json
```

## What this answers

Gupta, Henning, Maniya, and Pradhan proved
\(\gamma_s(G)\leq3\alpha(G)/2\) for every induced-\(P_5\)-free graph and asked
whether connectivity together with \(\alpha\geq3\) permits a better bound.
This example answers one important subquestion: the coefficient cannot be
reduced all the way to 1. It does **not** decide whether the published
coefficient \(3/2\) can be improved to a value strictly between \(4/3\) and
\(3/2\).

The graph construction itself is not claimed as new. Bonamy et al. previously
used the complement of the icosahedron as a \(P_5\)-induced-saturated graph.
The contribution here is its secure-domination calculation and the resulting
coefficient lower bound.

## Finite minimality evidence

Earlier exact graph-catalog enumeration found no counterexample through order
10. A separate, symmetry-broken SAT encoding found every order-11 instance
unsatisfiable for \(\alpha=3,\ldots,10\) with two CDCL solvers and recovered
the icosahedral complement at order 12. That supports the statement that this
is minimum-order, but the current reconstructed repository does not include a
formally checked DRAT proof trace. The theorem above does not depend on the
minimality claim.

## Sources

- U. K. Gupta, M. A. Henning, P. V. Maniya, and D. Pradhan,
  [*Secure domination in \(P_5\)-free graphs*](https://arxiv.org/abs/2503.08088),
  *Discrete Mathematics* (2026).
- M. Bonamy, C. Groenland, T. Johnston, N. Morrison, and A. Scott,
  [*Infinite induced-saturated graphs*](https://arxiv.org/abs/2506.08810).
