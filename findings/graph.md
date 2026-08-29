# A 12-vertex counterexample raises the coefficient floor to 4/3

Let \(I\) be the icosahedral graph and \(G=\overline I\). Exact exhaustive
verification gives

\[
G\text{ connected and induced-}P_5\text{-free},\qquad
\alpha(G)=3,\qquad \gamma_s(G)=4.
\]

Therefore the natural strengthening \(\gamma_s(G)\leq\alpha(G)\) is false for
connected induced-\(P_5\)-free graphs with \(\alpha\geq3\). Together with the
published \(3\alpha/2\) upper bound, the best universal coefficient \(c\)
now satisfies

\[
\frac43\leq c\leq\frac32.
\]

The graph is encoded by graph6 string `KtiSYtlXqwmT`. A standard-library
verifier checks all 792 five-vertex subsets, all 220 triples, and all 495
four-sets. It finds no induced \(P_5\), no secure triple, and 435 secure
four-sets. It also emits a machine-readable failure witness for every triple
and a defense map for the secure set \(\{0,1,2,3\}\).

The graph construction itself is not new: Bonamy et al. use the complement of
the icosahedron in work on induced saturation. The contribution here is the
secure-domination calculation and its coefficient lower bound. The exact
coefficient between \(4/3\) and \(3/2\) remains open.

- [Interactive visual paper](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-p5-free/website/index.html)
- [Proof and precise scope](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-p5-free/README.md)
- [Independent exhaustive verifier](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-p5-free/verify_counterexample.py)
- [Machine-readable certificate](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-p5-free/data/counterexample_certificate.json)
