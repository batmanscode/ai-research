# Larger dominating cliques: a solved branch and a global cross partition

Let (G) be induced-(P_5)-free and let

\[
K=\{k_1,\ldots,k_t\},\qquad t\geq3,
\]

be an inclusion-minimal dominating clique.  Its singleton-private regions

\[
P_i=\{v\notin K:N(v)\cap K=\{k_i\}\}
\]

are nonempty.  This note proves two all-orders results.

1. If the (P_i) are pairwise anticomplete, then
   (gamma_s(G)\leq\alpha(G)+1), for every (t\geq3).
2. If (t\geq4), all private-region cross edges and nonedges admit one
   globally compatible partition.  The subsequent
   [cross-edge closure](optimal-four-thirds-theorem.md) uses that partition
   to finish the multi-part branch and prove the sharp global theorem.

## 1. The bad multi-neighbour completion

Assume first that the (P_i) are pairwise anticomplete.  Let (M) be the
outside vertices with at least two neighbours in (K).  For every (i),
choose a maximum independent set (I_i) of (P_i), choose (x_i\in I_i),
and put

\[
X=\bigcup_i(I_i-\{x_i\}),\qquad
U_i=P_i-N[X],\qquad
p=\sum_i\alpha(P_i).
\tag{1}
\]

Every (U_i) is a nonempty clique: it contains (x_i), and two nonadjacent
members together with (I_i-\{x_i\}) would exceed (alpha(P_i)).  The
pairwise anticompleteness also makes (igcup_i I_i) independent, so

\[
p\leq\alpha(G).
\tag{2}
\]

Define

\[
B_X=\{m\in M:N(m)\cap X=\varnothing\text{ and, for every }k_i\in N_K(m),
U_i\nsubseteq N(m)\}.
\tag{3}
\]

The previously proved bad-multi-neighbour completion works for arbitrary
(t): if (Y) dominates (G[B_X]), then (K\cup X\cup Y) is secure.
Since (|K|=t) and (|X|=p-t),

\[
\gamma_s(G)\leq p+\gamma(G[B_X]).
\tag{4}
\]

For (m\in B_X), write (F(m)=K-N_K(m)) for its missed-hub set, and call
(m) *active* if it has a neighbour in some (U_i).

## 2. Local path restrictions

**Seen-region anticompleteness.**  If (m\in B_X) sees (k_i), then (m)
is anticomplete to (U_i).

Badness gives (u\in U_i-N(m)).  If (m) also saw (v\in U_i), then
(uv\in E(G)).  If (m) misses a hub (k_h), choose a second seen hub
(k_j\ne k_i); then

\[
u-v-m-k_j-k_h
\]

is induced.  If (m) sees every hub, badness at another hub (k_j) gives
(w\in U_j-N(m)), and (u-v-m-k_j-w) is induced.

**Missed-region completeness.**  Suppose active (m) sees (u\in U_i).
Then (m) is complete to every (U_r) with
(k_r\in F(m)-\{k_i\}).  Otherwise, a missed (v\in U_r) and any seen hub
(k_j) yield the induced path

\[
u-m-k_j-k_r-v.
\]

**Nested missed-hub lemma.**  If (J\subseteq B_X) is independent, the sets
(F(m)) over its active members form an inclusion chain.

Indeed, incomparable active (m,n\in J) provide
(k_r\in F(m)-F(n)) and (k_s\in F(n)-F(m)).  Activity plus missed-region
completeness supplies (u_r\in U_r) adjacent to (m) and
(u_s\in U_s) adjacent to (n).  Seen-region anticompleteness removes the
crossed edges, so

\[
u_r-m-k_s-u_s-n
\]

is an induced (P_5).

## 3. An active bad vertex misses at most two hubs

If active (m) has (|F(m)|\geq2), then (m) is complete to every (U_r)
with (k_r\in F(m)).  Start with an active edge into (U_i).  Missed-region
completeness makes (m) complete to every other missed region.  Using an
edge into one of those regions as the new source and applying the same lemma
again also makes (m) complete to (U_i).

Consequently,

\[
\boxed{|F(m)|\leq2\text{ for every active }m\in B_X.}
\tag{5}
\]

Otherwise choose three missed hubs (k_h,k_r,k_s).  For arbitrary
(u_r\in U_r,u_s\in U_s), the path

\[
k_h-k_r-u_r-m-u_s
\]

is induced: privacy removes the hub/private chords, membership in (F(m))
removes (k_hm,k_rm), and pairwise private anticompleteness removes
(u_ru_s).

## 4. The two-missed-hub case saves one more guard

Let (J) be a maximum independent set of (G[B_X]).  If its active missed
sets have maximum (F), put (f=|F|); if no member is active, put (f=0).
For every (i\notin F), (U_i) is anticomplete to (J).  Thus one vertex
from each such (U_i), together with (X\cup J), is an independent set of
order

\[
(p-t)+|J|+(t-f)=p+|J|-f.
\tag{6}
\]

For (f\leq1), equation (6) gives

\[
|J|\leq\alpha(G)-p+1.
\tag{7}
\]

It remains to treat (f=2).  Write (F=\{k_r,k_s\}) and choose active
(m\in J) with (F(m)=F).  The preceding completeness result makes (m)
complete to (U_r,U_s).  If (z\in X\cap P_r), then for any
(u_s\in U_s),

\[
z-k_r-k_s-u_s-m
\]

is induced.  Hence (X\cap P_r=\varnothing), and symmetrically
(X\cap P_s=\varnothing).  Therefore

\[
\alpha(P_r)=\alpha(P_s)=1.
\tag{8}
\]

The nonempty active missed sets form a finite inclusion chain with largest
member ({k_r,k_s}); choose a hub (k_q) in its smallest member.  Every
active member of (J) misses (k_q).  Every inactive member misses both
(k_r,k_s): if inactive (n\in J) saw (k_r), arbitrary
(u_r\in U_r,u_s\in U_s) would make

\[
n-k_r-u_r-m-u_s
\]

an induced (P_5).  Thus every member of (J) misses (k_q).

Choose one (u_i\in U_i) for every (i\notin F).  Then

\[
X\cup J\cup\{u_i:i\notin F\}\cup\{k_q\}
\tag{9}
\]

is independent.  Equation (8) removes the only possible edge from (k_q)
to (X); the common missed hub removes its edges to (J); and the chosen
(U_i) have indices outside (F).  The set in (9) has order

\[
(p-t)+|J|+(t-2)+1=p+|J|-1.
\]

So (7) also holds when (f=2).  A maximum independent set dominates its
induced graph, and (4) now yields

\[
\gamma_s(G)\leq p+\gamma(G[B_X])
\leq p+|J|\leq\alpha(G)+1.
\]

> **Pairwise-private higher-order theorem.**  If an inclusion-minimal
> dominating clique in an induced-(P_5)-free graph has pairwise-anticomplete
> singleton-private regions, then
> 
> \[
> \boxed{\gamma_s(G)\leq\alpha(G)+1.}
> \]

The proof uses neither connectedness of (G-K), smallest-counterexample
minimality, finite computation, nor the connected-residual equality.

## 5. One global partition of all cross-region pairs

Now drop pairwise anticompleteness and assume (t\geq4).  Put
(P=\bigcup_iP_i).  For vertices in three distinct private regions, their
induced graph cannot have exactly one edge: if (xy) were the sole edge,
then

\[
z-k_h-k_i-x-y
\]

would be an induced (P_5).  Equivalently, if (x\in P_i,y\in P_j) are
nonadjacent and (z) lies in a third region, then

\[
zx\in E(G)\quad\Longleftrightarrow\quad zy\in E(G).
\tag{10}
\]

Define the *cross-nonedge graph* (Q) on (P) by

\[
uv\in E(Q)
\quad\Longleftrightarrow\quad
u\in P_i, v\in P_j, i\ne j, uv\notin E(G).
\tag{11}
\]

There are no (Q)-edges within a private region, irrespective of adjacency
in (G).

> **Global cross-partition theorem.**  If (u,v) lie in the same connected
> component of (Q) and belong to distinct private regions, then
> (uv\in E(Q)).

Suppose instead that cross-region vertices (z_0,z_\ell) in one
(Q)-component are adjacent in (G), and take a shortest (Q)-path
(z_0-z_1-\cdots-z_\ell).  Its length is at least three.  Equation (10)
shortcuts any three consecutive path vertices in distinct private regions,
so the first four region labels alternate:

\[
z_0,z_2\in P_i,\qquad z_1,z_3\in P_j.
\tag{12}
\]

Shortestness removes the (Q)-edge (z_0z_3); since the endpoints have
distinct private types, (z_0z_3\in E(G)).

Choose (w) in a third nonempty region (P_k).  Along each of the first
three (Q)-edges, equation (10) forces (w) to have the same (G)-adjacency
to both endpoints.  Since (z_0z_3\in E(G)), the three-region rule forces
(w) to see at least one endpoint, and hence to see all four path vertices.
Choose a fourth hub (k_h), with (h\notin\{i,j,k\}).  Then

\[
k_h-k_i-z_0-w-z_1
\]

is induced: the private types remove the five hub/private chords and
(z_0z_1) is a (Q)-edge, hence a (G)-nonedge.  This contradiction proves
the theorem.

Call the connected components of (Q) the *global cross parts*.  For every
(u\in P_i,v\in P_j) with (i\ne j),

\[
\boxed{uv\in E(G)
\quad\Longleftrightarrow\quad
u,v\text{ lie in different global cross parts}.}
\tag{13}
\]

The qualifier *cross* is essential.  Edges within one private region are
unrestricted, even between vertices assigned to the same global cross part.
Equation (13) is not a claim that the whole induced graph (G[P]) is an
ordinary complete multipartite graph.

## 6. Cross-edge branch and subsequent closure

The pairwise-anticomplete private branch is solved for every clique order.
For (t\geq4), the only private-region geometry left has at least two global
cross parts.  Every cross-region pair in different parts is an edge, while
every cross-region pair in one part is a nonedge.

The [sharp four-thirds theorem](optimal-four-thirds-theorem.md) closes this
branch.  A cross edge (xy), together with one endpoint hub, forms a
dominating induced (P_3): the global partition forces every third private
region to see both endpoints and excludes the endpoint part from the opposite
private region, while a separate induced-path argument covers (M).
