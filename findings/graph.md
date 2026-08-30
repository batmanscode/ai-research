# The sharp secure-domination coefficient for connected P5-free graphs

Let \(I\) be the icosahedral graph and \(G=\overline I\). Exact exhaustive
verification gives

\[
G\text{ connected and induced-}P_5\text{-free},\qquad
\alpha(G)=3,\qquad \gamma_s(G)=4.
\]

Therefore the natural strengthening \(\gamma_s(G)\leq\alpha(G)\) is false for
connected induced-\(P_5\)-free graphs with \(\alpha\geq3\).  The continuation
now proves the sharp all-orders bound

\[
\gamma_s(G)\leq\alpha(G)+1,
\qquad
c_{\mathrm{opt}}=\frac43.
\]

The published \(3\alpha/2\) theorem remains valid: this example satisfies
\(4\leq(3/2)\cdot3=4.5\). The counterexample rules out only the stronger
coefficient-one candidate.

The graph is encoded by graph6 string `KtiSYtlXqwmT`. A standard-library
verifier checks all 792 five-vertex subsets, all 220 triples, and all 495
four-sets. It finds no induced \(P_5\), no secure triple, and 435 secure
four-sets. It also emits a machine-readable failure witness for every triple
and a defense map for the secure set \(\{0,1,2,3\}\).

This 12-vertex existence result is an exact counterexample theorem, not a
conjecture. The separate claim that 12 is the smallest possible order is not
needed for the result and is not asserted as a theorem here: searches exclude
smaller orders, but the repository does not include a formally checkable SAT
unsatisfiability trace.

The graph construction itself is not new: Bonamy et al. use the complement of
the icosahedron in work on induced saturation. The contribution here is the
secure-domination calculation, the structural proof, and the resulting sharp
coefficient.  The published \(3\alpha/2\) theorem remains valid but is not
optimal on the connected \(\alpha\geq3\) class.

## Structural progress after the counterexample

The follow-up project now proves several all-orders bounds and reductions
relevant to the
stronger candidate

\[
\gamma_s(G)\leq\alpha(G)+1.
\]

First, for every dominating set \(D\) with nonempty outside graph,

\[
\gamma_s(G)\leq |D|+
\min\{\gamma(G-D),\alpha(G-D)-1\}.
\]

In particular, every graph with a dominating pair satisfies the candidate
bound, without any \(P_5\)-free assumption.

Second, every connected induced-\(P_5\)-free graph with a cut vertex satisfies
\(\gamma_s(G)\leq\alpha(G)+1\). The proof is constructive: it decomposes the
unique possible deep articulation component into boundary modules, completes
them within the independence budget, and glues maximum independent sets from
the shallow components. An independent implementation exhaustively checked
all 5,001 proof-permitted choices over 2,196 rooted Atlas instances.

Third, every connected induced-\(P_5\)-free graph with \(\alpha\geq3\) and a
dominating induced \(P_3\) satisfies the same bound. In the only tight residual
case, a minimum-weight maximum independent set is modified by omitting its two
highest-attachment vertices. Two clean-room proof referees passed the
argument; direct checks covered 1,991 Atlas constructions, 240 choices on the
tight icosahedral complement, and 366,730 non-Atlas constructions.

The Bacsó–Tuza structure theorem says that every connected induced-\(P_5\)-free
graph has a dominating clique or a dominating induced \(P_3\). Consequently,
the dominating-path theorem and the clique results below exhaust the class.

Inside that clique core, two further reductions are now proof-grade.  Rooted
secure completions can be glued across disconnected components of `G-K`, with
one guard saved for every component assigned a disjoint reserved root block.
For a dominating triangle, any edge between two distinct singleton-private
regions forces a dominating induced \(P_3\).  In the complementary
pairwise-anticomplete branch, the global common-two lemma bounds the exact bad
multi-neighbour set within the remaining independence budget.  These cases,
together with the dominating-pair branch, prove
\(\gamma_s(G)\leq\alpha(G)+1\) for every dominating triangle.

A one-hub lift combined with Degawa--Saito separately removes every case in
which `G-K` is induced-`C5`-free.  The stronger common-two proof needs no such
case split and closes every private-budget gap.  Two clean-room referees
passed the hand proof; its computation is corroborating rather than a logical
dependency.

For the remaining larger-clique core, a smallest counterexample with
connected residual `H=G-K` must satisfy
`alpha(H)=alpha(G)` and `gamma_s(H)=alpha(H)+1`.  The pairwise-anticomplete
private-region subbranch is now completely solved: active missed-hub sets are
nested, have order at most two, and the two-hub case supplies one extra common
hub saving, proving `gamma_s(G)<=alpha(G)+1` for every clique order.  When
`|K|>=4`, the private cross-edge geometry also has one globally compatible
partition: between distinct private regions, adjacency is exactly membership
in different global cross parts.  A final cross-edge lemma closes that core:
every third private region sees both endpoints; the endpoint part cannot meet
the opposite private region; and all multi-hub neighbours are covered.
Therefore one endpoint hub together with the cross edge is a dominating
induced `P3`.  The no-cross-edge alternative is exactly the solved pairwise-
private branch.

Combining these cases with Bacsó--Tuza proves
`gamma_s(G)<=alpha(G)+1` for every connected induced-`P5`-free graph with
`alpha>=3`.  Since `alpha+1<=4alpha/3` and the icosahedral complement attains
`4/3`, the coefficient is exactly `4/3`.  Multiple independent referees
passed the all-orders proof; finite audits are corroborating only.

- [Interactive visual paper](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-p5-free/website/index.html)
- [Proof and precise scope](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-p5-free/README.md)
- [Independent exhaustive verifier](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-p5-free/verify_counterexample.py)
- [Machine-readable certificate](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-p5-free/data/counterexample_certificate.json)
- [Optimal-coefficient continuation](https://github.com/batmanscode/ai-research/tree/main/graph/secure-domination-optimal-coefficient)
- [Cut-vertex theorem and constructive proof](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-optimal-coefficient/structure/cut-vertices.md)
- [Independent cut-vertex audit](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-optimal-coefficient/referees/cut-vertex-audit.md)
- [Dominating-path theorem and proof](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-optimal-coefficient/structure/dominating-p3.md)
- [Two independent dominating-path audits](https://github.com/batmanscode/ai-research/tree/main/graph/secure-domination-optimal-coefficient/referees)
- [Clique-component gluing theorems](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-optimal-coefficient/structure/clique-component-gluing.md)
- [Triangle private-cross-edge theorem](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-optimal-coefficient/structure/triangle-private-cross-edge.md)
- [Triangle multi-region absorption lemma](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-optimal-coefficient/structure/triangle-multi-absorption.md)
- [Full dominating-triangle theorem](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-optimal-coefficient/structure/triangle-bad-m.md)
- [Connected residual and higher-order clique reductions](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-optimal-coefficient/structure/connected-clique-residual.md)
- [Pairwise-private closure and global cross-partition theorem](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-optimal-coefficient/structure/larger-clique-private-geometry.md)
- [Sharp four-thirds theorem](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-optimal-coefficient/structure/optimal-four-thirds-theorem.md)
- [Noob-first visual proof map](https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-optimal-coefficient/website/index.html)
- [Bacsó–Tuza structural theorem](https://doi.org/10.1007/BF02352694)
