# Connected residuals and higher-order clique reductions

This note records the proof-grade information now available for the only
remaining Bacsó--Tuza core: an inclusion-minimal dominating clique of order at
least four.  Throughout, graphs are finite and simple, and \(\gamma_s\) is the
secure domination number.

## 1. Exact equality behind a connected residual

Let \(G\) be a smallest counterexample to

\[
\gamma_s(G)\leq\alpha(G)+1
\]

among connected induced-\(P_5\)-free graphs with \(\alpha(G)\geq3\).  Let
\(K\) be a dominating clique, put \(H=G-K\), and assume that \(H\) is
connected.  Write

\[
a=\alpha(G),\qquad a_H=\alpha(H),\qquad \Delta=a-a_H.
\]

Because \(K\) is a clique, an independent set uses either no vertex of
\(K\), or one vertex \(k\in K\) followed by vertices of \(H\) nonadjacent to
\(k\).  Hence

\[
\alpha(G)=\max\left\{\alpha(H),
1+\max_{k\in K}\alpha(H-N_H(k))\right\},
\tag{1}
\]

so \(\Delta\in\{0,1\}\).

**Connected-residual equality theorem.**  Under these hypotheses,

\[
\boxed{\alpha(H)=\alpha(G)=a,\qquad \gamma_s(H)=a+1.}
\tag{2}
\]

**Proof.**  If \(T\) securely dominates \(H\), then
\(T\cup\{k\}\) securely dominates \(G\) for any \(k\in K\).  An attack in
\(H\) uses its old defender while \(k\) continues to dominate \(K\); an
attack in \(K-\{k\}\) is defended by \(k\), after which the attacker
dominates the clique and \(T\) still dominates \(H\).  Thus

\[
\gamma_s(G)\leq1+\gamma_s(H).
\tag{3}
\]

If \(a_H\geq3\), counterexample minimality gives
\(\gamma_s(H)\leq a_H+1\).  If \(a_H=2\), the published
\(3\alpha/2\) theorem gives the same upper bound.  Equation (1) excludes
\(a_H\leq1\).  Since \(G\) is a counterexample,

\[
a_H+\Delta+2\leq\gamma_s(G)
\leq1+\gamma_s(H)\leq a_H+2.
\]

Therefore \(\Delta=0\) and every inequality is tight, proving (2).
\(\square\)

Two useful consequences are immediate.

1. The residual \(H\) contains an induced \(C_5\); otherwise the
   Degawa--Saito theorem would give \(\gamma_s(H)\leq\alpha(H)\).
2. Every maximum independent set of \(H\) is maximum in \(G\) and dominates
   every vertex of \(K\), by (1).

The previously audited maximum-independent-set bad-cycle lemma can therefore
be applied to every pair consisting of a maximum independent set of \(H\) and
a clique guard.  This supplies an isolated induced \(C_5\) missed by that
guard.  If a second adjacent clique guard touches such a cycle, its missed
cycle vertices are independent and it sees at least three cycle vertices;
otherwise an induced \(P_5\) is exposed.

The touch hypothesis in the last sentence is essential.  An earlier draft
omitted it and claimed typed-cycle counts and an \(n\geq18\) consequence.
Those claims were withdrawn after an explicit 13-vertex obstruction exposed
the gap; they are not used here or elsewhere in the project.

## 2. A parameterized bound for larger dominating cliques

Let \(G\) be induced-\(P_5\)-free, and let
\(K=\{k_1,\ldots,k_t\}\) be an inclusion-minimal dominating clique,
where \(t\geq3\).  Its singleton-private regions

\[
P_i=\{v\notin K:N(v)\cap K=\{k_i\}\}
\]

are nonempty.  In this section assume that the \(P_i\) are pairwise
anticomplete.  Let \(M\) be the vertices outside \(K\) with at least two
neighbours in \(K\).

For each \(i\), choose a maximum independent set \(I_i\) of \(P_i\), choose
\(x_i\in I_i\), and define

\[
X=\bigcup_i(I_i-\{x_i\}),\qquad
U_i=P_i-N[X],\qquad
p=\sum_i\alpha(P_i).
\]

Every \(U_i\) is a nonempty clique, and pairwise anticompleteness gives
\(p\leq\alpha(G)\).  Define the exact bad multi-neighbour set

\[
B_X=\{m\in M:N(m)\cap X=\varnothing\text{ and, for every }k_i\in N_K(m),
U_i\nsubseteq N(m)\}.
\tag{4}
\]

The bad-multi-neighbour completion from the dominating-triangle proof works
without change for arbitrary \(t\): if \(Y\) dominates \(G[B_X]\), then
\(K\cup X\cup Y\) is secure.  Consequently,

\[
\gamma_s(G)\leq p+\gamma(G[B_X]).
\tag{5}
\]

Fix an independent set \(J\subseteq B_X\).  Call \(m\in J\) *active* if it
has a neighbour in some \(U_i\), and let

\[
F(m)=K-N_K(m)
\]

be its missed-hub set.

**Seen-region anticompleteness.**  If \(m\in B_X\) sees \(k_i\), then
\(m\) is anticomplete to \(U_i\).

Indeed, badness supplies \(u\in U_i-N(m)\).  If \(m\) also saw
\(v\in U_i\), then \(uv\) is an edge.  If \(m\) misses a hub \(k_h\), a
second seen hub \(k_j\) gives the induced path
\(u-v-m-k_j-k_h\).  If \(m\) sees all hubs, badness at another hub
\(k_j\) gives \(w\in U_j-N(m)\), and
\(u-v-m-k_j-w\) is induced.

**Missed-region completeness.**  Suppose active \(m\) sees
\(u\in U_i\).  Then \(m\) is complete to every \(U_h\) with
\(k_h\in F(m)-\{k_i\}\).  Otherwise, for a missed
\(v\in U_h\) and any seen hub \(k_j\),

\[
u-m-k_j-k_h-v
\]

is an induced \(P_5\).

**Nested missed-hub lemma.**  The sets \(F(m)\) over the active members of
\(J\) are linearly ordered by inclusion.

If active \(m,n\in J\) had incomparable missed sets, choose
\(k_r\in F(m)-F(n)\) and \(k_s\in F(n)-F(m)\).  Activity together with
missed-region completeness supplies \(u_r\in U_r\) adjacent to \(m\) and
\(u_s\in U_s\) adjacent to \(n\).  Seen-region anticompleteness removes the
crossed edges, so

\[
u_r-m-k_s-u_s-n
\]

is an induced \(P_5\), a contradiction.

Let \(F\) be the largest active missed set, or the empty set if \(J\) has no
active member, and put \(f=|F|\).  Every \(U_i\) with \(k_i\notin F\) is
anticomplete to \(J\).  One vertex from each of those \(t-f\) residual
cliques extends \(X\cup J\) to an independent set of order

\[
(p-t)+|J|+(t-f)=p+|J|-f.
\]

Taking \(J\) maximum in \(G[B_X]\) and using (5) gives the all-orders bound

\[
\boxed{\gamma_s(G)\leq\alpha(G)+f,
\qquad 0\leq f\leq t-2.}
\tag{6}
\]

For \(t=3\), (6) recovers the full dominating-triangle theorem.  For every
larger clique, it closes the pairwise-private branch whenever the largest
active bad vertex misses at most one hub.  Thus a live obstruction in this
branch must have \(t\geq4\) and an active bad vertex missing at least two
clique hubs.  Saving one additional hub in that nested missed set is the
sharply isolated exchange problem.

## 3. Every private transversal is complete multipartite

The cross-edge branch is also rigid.  Choose one private witness
\(w_i\in P_i\) for every hub and put \(W=\{w_i:k_i\in K\}\).

Every edge of \(G[W]\) dominates \(G[W]\).  Otherwise, if \(w_iw_j\) is an
edge and a third witness \(w_h\) misses both endpoints, then

\[
w_h-k_h-k_i-w_i-w_j
\]

is an induced \(P_5\).  Equivalently, the complement of \(G[W]\) contains
no induced \(P_3\), and is therefore a disjoint union of cliques.  Hence

\[
\boxed{G[W]\text{ is complete multipartite}.}
\tag{7}
\]

The conclusion holds for every arbitrary choice of one witness per private
region.  It is a per-transversal statement; it does not yet imply one global
multipartite partition of all private-region vertices.  Establishing such a
compatibility theorem, or finding the exact replacement for it, is the other
precise route into the remaining \(|K|\geq4\) core.

## Scope

Equations (2), (6), and (7) are all-orders theorems.  They do not prove the
global \(\alpha+1\) candidate: the remaining cases are inclusion-minimal
dominating cliques of order at least four, with either a nontrivial private
cross-edge geometry or a nested active missed set of size at least two.
Bounded SAT searches are maintained separately as corroborating evidence and
are not a logical dependency of these statements.
