# The sharp four-thirds theorem

## Main result

> **Theorem.**  If (G) is a connected induced-(P_5)-free graph with
> (alpha(G)\geq3), then
>
> \[
> \boxed{\gamma_s(G)\leq\alpha(G)+1.}
> \tag{1}
> \]

Consequently the smallest universal coefficient (c) satisfying
(gamma_s(G)\leq c\alpha(G)) on this class is exactly

\[
\boxed{c_{\mathrm{opt}}=\frac43.}
\tag{2}
\]

This improves the published (3\alpha/2) coefficient and answers its open
improvement question.  It does not contradict the published theorem.

The proof assembles the previously proved dominating-pair,
dominating-induced-(P_3), dominating-triangle, pairwise-private, and global
cross-partition theorems.  The only new ingredient needed for the last branch
is the cross-edge closure below.

## 1. Setup for the last clique branch

Let

\[
K=\{k_1,\ldots,k_t\},\qquad t\geq4,
\]

be an inclusion-minimal dominating clique.  For every hub, define its
singleton-private region

\[
P_i=\{v\notin K:N(v)\cap K=\{k_i\}\}.
\]

Every (P_i) is nonempty by inclusion-minimality.  Let (M) be the outside
vertices with at least two neighbours in (K).

The global cross-partition theorem defines a graph (Q) on
(P=\bigcup_iP_i): two vertices in distinct private regions are adjacent in
(Q) exactly when they are nonadjacent in (G).  The connected components
of (Q) are the global cross parts, and for
(u\in P_i,v\in P_j), (i\ne j),

\[
uv\in E(G)
\quad\Longleftrightarrow\quad
u,v\text{ lie in different global cross parts}.
\tag{3}
\]

Edges inside one private region remain unrestricted.

## 2. A private cross edge is seen twice from every third region

Let (x\in P_i,y\in P_j), (i\ne j), and suppose (xy\in E(G)).  Every
(z\in P_\ell), with (ell\notin\{i,j\}), is adjacent to both (x) and
(y).

The private-transversal rule first says that (z) sees at least one endpoint:
otherwise (xy) would be the sole edge on three distinct private types and
(z-k_\ell-k_i-x-y) would be an induced (P_5).  If, say,
(zy\in E(G)) but (zx\notin E(G)), choose a fourth hub
(k_h), with (h\notin\{i,j,\ell\}).  Then

\[
k_h-k_i-x-y-z
\]

is induced.  The exact private types remove all hub/private chords and the
selected nonedge removes (xz).  The symmetric one-sided case is identical.
Thus every third private region is complete to both endpoints.

## 3. The endpoint parts avoid the opposite endpoint regions

Let (A) and (B) be the global cross parts of (x) and (y).  Since
(xy\in E(G)), equation (3) gives (A\ne B).  Then

\[
A\cap P_j=\varnothing,
\qquad
B\cap P_i=\varnothing.
\tag{4}
\]

Suppose (z\in A\cap P_j).  Choose a third private region (P_\ell) and
(w\in P_\ell).  Section 2 applied to (xy) makes (w) adjacent to both
(x) and (y), so the part of (w) differs from both (A) and (B).
Equation (3) therefore makes (zw) an edge.  Apply Section 2 again, now to
the cross edge (zw) with (x\in P_i) as the third-private vertex.  It
forces (xz\in E(G)), contradicting equation (3) because (x,z) lie in
the same part (A) and in distinct private regions.  This proves the first
claim; the second is symmetric.

## 4. Multi-neighbours are also covered

Every (m\in M) that misses (k_i) sees at least one of (x,y).

Otherwise (m) misses all of (k_i,x,y).  Since (m) has at least two
neighbours in (K), choose
(k_a\in N_K(m)-\{k_j\}).  Because (m) misses (k_i), the hub (k_a)
differs from both (k_i,k_j).  Then

\[
m-k_a-k_i-x-y
\]

is induced.  Privacy removes (k_ax,k_ay,k_iy), and the assumed misses
remove (mk_i,mx,my), a contradiction.

## 5. Cross-edge closure

The three vertices

\[
D=\{k_i,x,y\}
\]

induce the path (k_i-x-y), since the private vertex (y\in P_j) misses
(k_i).  They dominate all of (G):

- (k_i) dominates (K\cup P_i);
- equation (4) and the global partition make (x) adjacent to every vertex
  of (P_j);
- Section 2 covers every (P_\ell) with (ell\notin\{i,j\}); and
- a member of (M) either sees (k_i) or is covered by Section 4.

Thus every cross edge between distinct private regions forces a dominating
induced (P_3).

## 6. Assembly of the global theorem

The Bacsó--Tuza structure theorem says that every connected induced-(P_5)-
free graph has a dominating clique or a dominating induced (P_3).

- A dominating induced (P_3) is handled by the previously proved
  dominating-path theorem.
- If there is a dominating clique, choose an inclusion-minimal one (K).
  A clique of order at most two is handled by the dominating-set residual
  bound; order three is handled by the full dominating-triangle theorem.
- Let (|K|\geq4).  If no edge joins two distinct private regions, the
  pairwise-private higher-order theorem gives (1).  If such an edge exists,
  Section 5 supplies a dominating induced (P_3), and the dominating-path
  theorem again gives (1).

These cases are exhaustive, proving the sharp bound
(gamma_s(G)\leq\alpha(G)+1).

Finally, for (alpha(G)\geq3),

\[
\alpha(G)+1\leq\frac43\alpha(G).
\]

The complement of the icosahedral graph is connected and induced-(P_5)-free
with ((\alpha,\gamma_s)=(3,4)), so no coefficient below (4/3) is possible.
This proves (2).

## Scope and dependencies

The hand proof is all-orders.  Finite Graph Atlas and SAT checks corroborate
the lemmas but are not logical dependencies.  The theorem assumes
connectivity and (alpha\geq3), exactly matching the coefficient question.
The graph construction establishing sharpness was known previously in another
context; its secure-domination calculation and the sharp coefficient are the
relevant contributions here.
