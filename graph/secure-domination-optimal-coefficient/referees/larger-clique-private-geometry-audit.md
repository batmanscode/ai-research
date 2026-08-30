# Independent audit: larger-clique private geometry

## Verdict

**PASS.**  Both all-orders claims were reconstructed independently.

1. Pairwise-anticomplete singleton-private regions imply
   (gamma_s(G)\leq\alpha(G)+1) for every inclusion-minimal dominating
   clique order (t\geq3).
2. For (t\geq4), components of the cross-nonedge graph give one globally
   compatible partition of all cross-region pairs.  Edges inside one private
   region remain unrestricted.

Neither theorem depends on bounded SAT.

## Pairwise-private closure

The previously audited seen-region, missed-region, and nested missed-set
lemmas are used with matching hypotheses.  Switching the active source shows
that an active vertex missing at least two hubs is complete to every residual
private clique at a missed hub.  Three missed hubs then give the chordless
path

\[
k_h-k_r-u_r-m-u_s,
\]

so an active missed set has order at most two.

For a maximal missed set ({k_r,k_s}), the path

\[
z-k_r-k_s-u_s-m
\]

forces (X\cap P_r=X\cap P_s=\varnothing).  Active members of an independent
bad set form a chain and therefore share one of these hubs.  If an inactive
member (n) saw (k_r), then

\[
n-k_r-u_r-m-u_s
\]

would be induced; hence inactive members miss both.  Adding the common hub
to the earlier independent-set construction gives exact order
(p+|J|-1), and therefore

\[
\alpha(B_X)\leq\alpha(G)-p+1.
\]

The bad-multi-neighbour completion then proves the claimed
(alpha+1) bound.  Empty bad sets and independent bad sets without active
members are covered by the (f=0) accounting.

## Global cross partition

Let (Q) join vertices in distinct private regions exactly when they are
nonadjacent in (G).  The three-region rule makes cross nonadjacency
transitive whenever three private types are distinct.

If one (Q)-component contained (G)-adjacent vertices of distinct private
types, a shortest (Q)-path between such a pair would have length at least
three.  Transitivity forces its first four private labels to alternate
(i,j,i,j); shortestness makes the first and fourth vertices adjacent in
(G).  A vertex in a third private region has uniform adjacency along the
three (Q)-edges, and the endpoint edge makes it complete to the four path
vertices.  A fourth hub then gives the chordless path

\[
k_h-k_i-z_0-w-z_1.
\]

Thus each (Q)-component is complete in (Q) across the private regions it
meets.  Between different components every cross-region pair is an edge of
(G) by definition.

## Finite stress check

As corroboration, the smallest nontrivial region profile of sizes
((2,2,1,1)) has 183 assignments satisfying every per-transversal rule.
Eight are abstractly incompatible with a single global cross partition; all
eight create an induced (P_5) after adding the (K_4) private-hub
structure, matching the shortest-path proof.

## Scope

The audit does not promote the remaining multi-part cross-edge branch to a
theorem.  The global parts control only pairs from different private regions;
within-region adjacency is arbitrary, and multi-neighbour vertices are not
classified by the partition theorem.
