# Independent audit: connected residual and higher-order clique reductions

## Verdict

**PASS.**  The connected-residual equality theorem, the generalized
seen-region and missed-region lemmas, the nested missed-hub lemma, the
parameterized \(\alpha+f\) accounting, and the arbitrary-private-transversal
lemma all survive a line-by-line chord and quantifier check.

The audit rejected an earlier typed-cycle argument that used a dense-cycle
attachment lemma without first proving that the relevant clique hub touched
the cycle.  Every consequence of that gap, including a claimed
\(n\geq18\) lower bound, has been withdrawn and is absent from the theorem
chain.

## Connected-residual equality

For \(H=G-K\), where \(K\) is a dominating clique and \(H\) is connected,

\[
\alpha(G)=\max\{\alpha(H),1+\max_{k\in K}\alpha(H-N_H(k))\}
\]

is exact.  It gives \(\alpha(G)-\alpha(H)\in\{0,1\}\).  A secure set of
\(H\) plus one clique hub securely dominates \(G\).  Combining that lift
with smallest-counterexample minimality (or the published bound when
\(\alpha(H)=2\)) forces

\[
\alpha(H)=\alpha(G),\qquad
\gamma_s(H)=\alpha(H)+1.
\]

No hidden assumption about a selected maximum independent set is used.

## Higher-order path checks

For a bad vertex \(m\) with both a neighbour and a non-neighbour in a
residual private clique \(U_i\):

- if \(m\) misses a hub \(k_h\), the path
  \(u-v-m-k_j-k_h\) is induced for a second seen hub \(k_j\);
- if \(m\) sees every hub, badness at another hub supplies
  \(u-v-m-k_j-w\).

Thus \(m\) is anticomplete to every \(U_i\) whose hub it sees.

If active \(m\) has an edge into \(U_i\) and misses another hub \(k_h\), a
nonedge from \(m\) into \(U_h\) would create
\(u-m-k_j-k_h-v\).  Therefore \(m\) is complete to every other residual
private clique at a missed hub.

For independent active bad vertices \(m,n\) with incomparable missed sets,
choose \(k_r\in F(m)-F(n)\) and \(k_s\in F(n)-F(m)\).  The preceding lemma
supplies the endpoint edges and seen-region anticompleteness removes the
crossed edges, making

\[
u_r-m-k_s-u_s-n
\]

induced.  Hence the missed sets are nested.

## Accounting

Let \(F\) be the largest active missed set in a maximum independent set
\(J\subseteq B_X\), and let \(f=|F|\).  Each \(U_i\) outside \(F\) is
anticomplete to \(J\).  Adding one vertex from each such \(U_i\) to
\(X\cup J\) gives an independent set of exact order \(p+|J|-f\).  Therefore

\[
\gamma(G[B_X])\leq |J|\leq\alpha(G)-p+f
\]

and the previously audited completion gives

\[
\gamma_s(G)\leq\alpha(G)+f.
\]

The bounds \(0\leq f\leq |K|-2\) include the empty and inactive cases.

## Private transversals

If a chosen private transversal contains an edge whose endpoints are both
missed by a third chosen witness, then
\(w_h-k_h-k_i-w_i-w_j\) is induced.  Hence every edge dominates the
transversal.  Equivalently, its complement is \(P_3\)-free, so each
transversal is complete multipartite.

The conclusion is deliberately scoped per arbitrary transversal.  It does
not assert a single global multipartite partition of the union of all
private regions.

## Remaining gap

The audited statements do not close the \(|K|\geq4\) branch.  In the
pairwise-anticomplete case, a live obstruction still may have a largest
active missed set of size at least two.  In the cross-edge case, compatibility
between the multipartite partitions arising from different transversals has
not been proved.
