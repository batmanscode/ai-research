# Referee report on the dominating-induced-\(P_3\) theorem

## Verdict

**PASS.** I find no mathematical gap in the proposed theorem or in the equality lemma that supplies its only nonroutine case. In particular, the failed-exchange witnesses exist with all the asserted properties; witnesses attached to different path vertices are distinct; the minimum-weight comparison remains valid even when a witness is one of the two omitted vertices of the original independent set; every displayed five-vertex path is induced; and both final enlargement arguments contradict \(\alpha(G)=q\) exactly as claimed.

The proof is suitable for publication after ordinary editorial polishing and after the general completion lemma and the standard dominating-clique/dominating-\(P_3\) structure theorem are cited or stated in the surrounding paper. The clarifications suggested at the end of this report are expository only.

## Statement audited

Let \(G\) be a connected induced-\(P_5\)-free graph with \(\alpha(G)\ge 3\), and suppose that \(D=\{a,b,c\}\) is a dominating induced path \(a-b-c\). The claim is

\[
\gamma_s(G)\le \alpha(G)+1.
\]

Write \(H=G-D\). The general completion lemma proves the claim when \(\alpha(H)\le \alpha(G)-1\). The new equality lemma treats \(\alpha(H)=\alpha(G)=q\ge3\).

## Audit of the equality lemma

Choose a maximum independent set \(I\) of \(H\) minimizing

\[
w_D(I)=\sum_{u\in I}|N(u)\cap D|.
\]

Choose \(x,y\in I\) maximizing \(\delta_D(x)+\delta_D(y)\), put \(X=I\setminus\{x,y\}\), and set \(S=D\cup X\). Then \(|S|=q+1\), and \(S\) dominates because it contains \(D\).

### 1. Reduction to attacks anticomplete to \(X\)

If an attacked vertex \(v\notin S\) has a neighbor \(z\in X\), then \(z\) defends \(v\): after replacing \(z\) by \(v\), the untouched set \(D\) still dominates every vertex, including \(z\). Hence a failed attack must satisfy \(N(v)\cap X=\varnothing\).

Let \(r=|N(v)\cap D|\). Since \(D\) dominates, \(r\ge1\). If the attack is not defendable, then for every \(d\in N(v)\cap D\), the set

\[
S_d=(S\setminus\{d\})\cup\{v\}
\]

fails to dominate.

### 2. Existence, location, and distinctness of the witnesses

Fix \(d\in N(v)\cap D\). Because \(S_d\) is not dominating, some vertex is undominated by it. This vertex cannot be the removed vertex \(d\): in the path \(a-b-c\), every vertex has a path neighbor in \(D\setminus\{d\}\). Every member of \(S\setminus\{d\}\) lies in \(S_d\), so the undominated vertex lies outside \(S\). Call it \(p_d\).

Since \(p_d\) is undominated by \(S_d\), it is distinct from and nonadjacent to \(v\), and it has no neighbor in \(S\setminus\{d\}\). On the other hand, the original set \(S\) dominates \(p_d\), so necessarily

\[
N(p_d)\cap S=\{d\}.
\]

Thus \(p_d\in H\), \(p_dv\notin E(G)\), \(p_d\) is anticomplete to \(X\), and \(\delta_D(p_d)=1\).

For different path vertices \(d\ne e\), the witnesses are automatically distinct: equality \(p_d=p_e\) would give both \(N(p_d)\cap S=\{d\}\) and \(N(p_d)\cap S=\{e\}\), which is impossible. This justifies all later cardinalities involving two witnesses.

The set

\[
J_d=X\cup\{v,p_d\}
\]

is therefore independent in \(H\) and has order \(|X|+2=q\). This remains true if \(v\) or \(p_d\) happens to equal \(x\) or \(y\): both are outside \(X\), and \(v\ne p_d\).

### 3. The minimum-weight inequality

Put \(m=\delta_D(x)+\delta_D(y)\). Since \(J_d\) is a maximum independent set of \(H\), the choice of \(I\) gives

\[
w_D(I)\le w_D(J_d).
\]

After cancelling the common contribution from \(X\), this is

\[
m\le \delta_D(v)+\delta_D(p_d)=r+1. \tag{1}
\]

No disjointness between \(J_d\) and \(I\) beyond their common set \(X\) is needed for this comparison; it is an inequality between the weights of two maximum independent sets.

### 4. Incidence with the path and the top-pair deduction

Every maximum independent set of \(H\), and hence \(I\), contains a neighbor in \(H\) of each of \(a,b,c\). Otherwise the missed path vertex could be added to it, producing an independent set of \(G\) of order \(q+1\).

Also, \(I\) cannot contain both an \(a\)-only vertex \(u\) and a \(c\)-only vertex \(w\). If it did, then

\[
u-a-b-c-w
\]

would be induced: \(uw\notin E(G)\) because \(I\) is independent; \(ac\notin E(G)\) because \(a-b-c\) is induced; and the singleton attachment types exclude all remaining chords.

All vertices of \(I\) have positive \(D\)-degree because \(D\) dominates. If all had degree one, meeting all three path neighborhoods would force both an \(a\)-only and a \(c\)-only vertex, contrary to the preceding paragraph. Hence some vertex of \(I\) has \(D\)-degree at least two. The two largest degrees therefore have sum

\[
m\ge 2+1=3. \tag{2}
\]

Since \(r\le3\), (1) and (2) imply \(r\ge2\) and \(m\le4\).

### 5. Exclusion of \(r=3\)

Suppose \(r=3\). The witnesses \(p_b\) and \(p_c\) are distinct. If they were nonadjacent, then

\[
X\cup\{v,p_b,p_c\}
\]

would be an independent set in \(H\) of order \(q+1\), contradicting \(\alpha(H)=q\). Thus \(p_bp_c\in E(G)\). Now

\[
a-v-c-p_c-p_b
\]

is an induced \(P_5\). Its nonconsecutive pairs are nonedges for the following exhaustive reasons:

- \(ac\notin E(G)\) because the core path is induced;
- \(ap_c,ap_b,cp_b\notin E(G)\) because each witness has its named vertex as its unique neighbor in \(D\);
- \(vp_c,vp_b\notin E(G)\) by the witness construction.

This contradicts induced-\(P_5\)-freeness, so \(r\ne3\). Equations (1) and (2) now force

\[
r=2,\qquad m=3. \tag{3}
\]

Because \(x,y\) realize the two largest positive \(D\)-degrees in \(I\), a top-pair sum of three means the two largest degrees are \(2\) and \(1\). Therefore exactly one vertex of \(I\) has degree two, none has degree three, and every other vertex has degree one. In particular, every vertex of \(X\) has a singleton attachment to \(D\), and \(X\ne\varnothing\) because \(q\ge3\).

### 6. Exhaustion of the three two-neighbor types of \(v\)

#### Type \(N(v)\cap D=\{a,c\}\)

The distinct witnesses \(p_a,p_c\) must be adjacent; otherwise \(X\cup\{v,p_a,p_c\}\) is an independent \((q+1)\)-set in \(H\). Choose \(z\in X\). According to the singleton attachment of \(z\), one obtains one of the following paths:

| Type of \(z\) | Five-vertex path | Complete chord check |
|---|---|---|
| \(a\)-only | \(c-p_c-p_a-a-z\) | \(cp_a,ca,cz,p_ca,p_cz,p_az\) are absent: singleton witness types exclude the first and fourth, the induced core excludes \(ca\), the type of \(z\) excludes \(cz\), and witnesses are anticomplete to \(X\). |
| \(b\)-only | \(z-b-a-p_a-p_c\) | \(za,zp_a,zp_c,bp_a,bp_c,ap_c\) are absent by, respectively, the type of \(z\), witness anticompleteness to \(X\), and the singleton witness types. |
| \(c\)-only | \(a-p_a-p_c-c-z\) | \(ap_c,ac,az,p_ac,p_az,p_cz\) are absent by the singleton witness types, the induced core, the type of \(z\), and witness anticompleteness to \(X\). |

In every row the four consecutive edges are present by construction, so each row is an induced \(P_5\), a contradiction.

#### Type \(N(v)\cap D=\{a,b\}\)

If some \(z\in X\) is \(c\)-only, then

\[
z-c-b-a-p_a
\]

is an induced \(P_5\). The nonconsecutive pairs \(zb,za,zp_a,ca,cp_a,bp_a\) are nonedges: the first two follow from the type of \(z\), \(zp_a\notin E(G)\) from witness anticompleteness to \(X\), \(ca\notin E(G)\) from the induced core, and the last two from the \(a\)-only witness type.

Consequently every member of \(X\) is \(a\)-only or \(b\)-only. The independent \(q\)-set

\[
J_a=X\cup\{v,p_a\}
\]

is then anticomplete to \(c\): this holds for \(X\) by its remaining types, for \(v\) because \(N(v)\cap D=\{a,b\}\), and for \(p_a\) because its unique neighbor in \(D\) is \(a\). Hence \(J_a\cup\{c\}\) is an independent set in \(G\) of order \(q+1\), contradicting \(\alpha(G)=q\).

#### Type \(N(v)\cap D=\{b,c\}\)

This is the exact reversal of the preceding case. If an \(a\)-only \(z\in X\) exists, then \(z-a-b-c-p_c\) is induced. Its nonconsecutive pairs \(zb,zc,zp_c,ac,ap_c,bp_c\) are excluded by the same three sources: the type of \(z\), witness anticompleteness to \(X\), the induced core, and the \(c\)-only witness type. If no such \(z\) exists, then \(J_c=X\cup\{v,p_c\}\) is anticomplete to \(a\), so adding \(a\) gives an independent \((q+1)\)-set in \(G\).

All possibilities for a failed attack lead to a contradiction. Thus \(S\) is secure.

## Audit of the passage to the branch theorem

For completeness, I also checked the general completion lemma used for the strict residual case. If \(D\) is any dominating set, \(H=G-D\ne\varnothing\), \(I\) is a maximum independent set in \(H\), \(x\in I\), and \(X=I\setminus\{x\}\), then

\[
R=V(H)\setminus N_H[X]
\]

is a clique: two nonadjacent vertices in \(R\), together with \(X\), would form an independent set larger than \(I\). For \(S=D\cup X\), an attack adjacent to \(X\) is defended from \(X\). An attack \(v\in R\) is defended by any adjacent \(d\in D\): the removed \(d\) is dominated by \(v\), while every external private neighbor of \(d\) relative to \(S\) lies in \(R\) and is therefore adjacent to \(v\) unless it is \(v\) itself, in which case it belongs to the exchanged set. Hence

\[
\gamma_s(G)\le |D|+\alpha(H)-1.
\]

For the dominating path, if \(\alpha(H)\le\alpha(G)-1\), this gives

\[
\gamma_s(G)\le3+\alpha(H)-1\le\alpha(G)+1.
\]

If \(\alpha(H)=\alpha(G)\), the equality lemma gives a secure set of order \(q+1\). These cases are exhaustive because \(H\) is an induced subgraph of \(G\). Also, \(H\ne\varnothing\) automatically here: an induced \(P_3\) alone has independence number two, whereas \(\alpha(G)\ge3\).

## Independent finite counterexample search

I rebuilt the relevant predicates directly and did not call the proof criterion to test security. The check enumerated vertex subsets for independence, all five-vertex subsets for induced \(P_5\)'s, all three-vertex subsets for dominating induced paths, all maximum independent sets of \(H\), every minimum-weight choice of \(I\), every top-degree pair \(x,y\), and every legal defender exchange in the definition of secure domination.

On the complete NetworkX Graph Atlas (all unlabeled graphs through order seven), the results were:

| Audit population | Count | Failures |
|---|---:|---:|
| Connected induced-\(P_5\)-free, \(\alpha\ge3\), dominating induced-\(P_3\) core instances | 5,152 | 0 violations of \(\gamma_s\le\alpha+1\) |
| Strict residual instances \(\alpha(H)<\alpha(G)\) | 4,081 | 0 |
| Completion sets over every maximum \(I\) and every omitted \(x\) in the strict instances | 16,590 | 0 insecure sets |
| Equality instances \(\alpha(H)=\alpha(G)\) | 1,071 | 0 |
| Allowed minimum-weight/top-pair equality constructions | 1,991 | 0 insecure sets |

As a separate larger stress test, the complement of the icosahedral graph has 60 equality-case dominating-\(P_3\) cores. They yield 240 allowed minimum-weight/top-pair constructions, all secure.

These finite checks are not used in the proof, but they independently support the exact points where a missing distinctness condition, a wrong cardinality, or a missed chord would most readily create a small counterexample.

## Editorial recommendations

I recommend adding three short clarifications to the proof before publication:

1. State explicitly that \(p_d\ne p_e\) for \(d\ne e\), since their neighborhoods in \(S\) are the different singletons \(\{d\}\) and \(\{e\}\).
2. When saying that \(I\) meets each of \(N(a),N(b),N(c)\), specify that the relevant neighbors lie in \(H\), as \(I\subseteq V(H)\).
3. After \(r=2,m=3\), spell out that all \(D\)-degrees in \(I\) are positive; this makes the conclusion \(2,1,1,\ldots,1\) immediate.

None of these points requires a change to the argument.
