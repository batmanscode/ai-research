# Independent referee report: global common-two triangle argument

## Verdict

**PASS.**  The upgraded argument is a pure all-orders proof.  It removes the
finite three-member certificate from the logical dependency chain and closes
the entire pairwise-anticomplete private-region branch for a dominating
triangle, for every value of the private budget `p` and every size/structure
of the multi-neighbour region.

The author corrected the one quantifier issue I found during the audit:
failure of `U_i` **implies** the existence of a `K-{i}`-type member adjacent
to some vertex of `U_i`; the existence of one such edge is not, by itself,
equivalent to failure.  The stable draft uses the correct implication.

Together with the previously proved dominating-pair, dominating-induced-`P3`,
and triangle-private-cross-edge theorems, the argument proves:

> If a connected induced-`P5`-free graph `G` with `alpha(G)>=3` has a
> dominating triangle, then `gamma_s(G)<=alpha(G)+1`.

It does **not** settle the whole conjectured `alpha+1` bound.  In the
Bacsó--Tuza/minimum-connected-dominating-set reduction, an unresolved
counterexample must now have an inclusion-minimal dominating clique of order
at least four.

## Setup and elementary prerequisites

Let `K={a,b,c}` be a dominating triangle.  The exact private regions `P_i`
are assumed nonempty and pairwise anticomplete in the live branch.  For each
`i`, take a maximum independent set `I_i`, omit `x_i`, and write

```text
X = union_i (I_i-{x_i}),        U_i = P_i-N[X].
```

The following facts used by the proof are sound.

1. `X` is independent and has order `p-3`, where
   `p=sum_i alpha(P_i)`.  Pairwise anticompleteness of the private regions is
   exactly what permits the three independent sets to be combined.
2. `U_i` is nonempty: `x_i` itself lies in it.
3. `U_i` is a clique.  If two vertices of `U_i` were nonadjacent, adjoining
   both to `I_i-{x_i}` would create an independent set of order
   `alpha(P_i)+1` in `P_i`.
4. Every `m in B_X` lies in the multi-neighbour region, is anticomplete to
   `X`, and misses at least one member of `U_i` for every hub `i` it sees.
5. `p<=alpha(G)`, again because the three maximum independent sets combine.

No connectedness assumption on `G-K` enters any of the new arguments.

## Seen-region anticompleteness: full chord audit

The claim is that every `m in B_X` is anticomplete to `U_i` whenever it sees
hub `i`.  Badness supplies `u in U_i` missed by `m`.  Suppose for contradiction
that `m` sees `v in U_i`; then `uv` is an edge because `U_i` is a clique.

### Two-hub type

Suppose `N_K(m)={i,j}` and let `k` be the missed hub.  The claimed path is

```text
u - v - m - j - k.
```

Its four path edges are respectively the clique edge in `U_i`, the assumed
edge to `m`, the type edge `mj`, and the triangle edge `jk`.  Its six chords
are all absent:

| chord | reason |
| --- | --- |
| `um` | `u` was chosen as a badness witness |
| `uj`, `uk` | `u` is private to `i` |
| `vj`, `vk` | `v` is private to `i` |
| `mk` | `m` has exactly the hub type `{i,j}` |

Thus the path is induced.

### Three-hub type

Suppose `m` sees all three hubs.  Choose any `j!=i`.  Badness at `j` supplies
`w in U_j` missed by `m`.  The claimed path is

```text
u - v - m - j - w.
```

The path edges are `uv`, `vm`, `mj`, and `jw`.  The six chords are absent:

| chord | reason |
| --- | --- |
| `um` | badness witness at `i` |
| `uj`, `vj` | `u,v` are private to `i` and `j!=i` |
| `uw`, `vw` | distinct private regions are anticomplete |
| `mw` | badness witness at `j` |

This is again an induced `P5`.  The argument works for arbitrarily large
`U_i`; it uses only two selected vertices from it.

## Global common-two lemma: quantifiers and chord audit

For an independent `J subseteq B_X`, call `U_i` failed if it has no vertex
anticomplete to all of `J`.

If `U_i` fails, choose any `u_i in U_i`.  Since `u_i` is not anticomplete to
`J`, it has a neighbour `m_i in J`.  Seen-region anticompleteness shows that
`m_i` cannot see hub `i`.  Because every member of `B_X` has at least two
hub neighbours and `K` has order three, necessarily

```text
N_K(m_i) = K-{i}.
```

This is the precise implication the proof needs.  There is no converse
claim: one edge from such an `m_i` need not cover the whole of `U_i`.

Suppose different `U_i,U_j` both fail and let `k` be the third hub.  Select
the witnesses above.  The path

```text
u_i - m_i - k - m_j - u_j
```

has its four edges by selection and by the two forced hub types.  Its six
chords are absent as follows:

| chord | reason |
| --- | --- |
| `u_i k` | `u_i` is private to `i` |
| `u_i m_j` | `m_j` sees `i`, so seen-region anticompleteness applies |
| `u_i u_j` | pairwise anticompleteness of private regions |
| `m_i m_j` | `J` is independent |
| `m_i u_j` | `m_i` sees `j`, so seen-region anticompleteness applies |
| `k u_j` | `u_j` is private to `j` |

Also `m_i!=m_j`, because their hub types omit different hubs.  Hence the
five displayed vertices are distinct and induce a `P5`, a contradiction.
At most one `U_i` fails, which proves that two residual cliques contain
simultaneous witnesses for the entire `J`.  This proof is independent of
`|J|`; the empty set is harmless because all three nonempty `U_i` then work.

## Independence and domination bookkeeping

Let `J` be a maximum independent set of `G[B_X]`.  The set

```text
X union J union {u_r,u_s}
```

is independent:

- `X` is independent;
- `B_X` is anticomplete to `X` by definition;
- `u_r,u_s` lie outside `N[X]`;
- they are anticomplete to `J` by the common-two lemma; and
- they lie in distinct pairwise-anticomplete private regions.

It has order `(p-3)+alpha(B_X)+2`, and therefore

```text
alpha(B_X) <= alpha(G)-p+1.
```

For nonempty `B_X`, a maximum independent set is maximal and hence a
dominating set, so `gamma(B_X)<=alpha(B_X)`.  If `B_X` is empty, the same
inequality holds under the convention `alpha(empty)=gamma(empty)=0`, already
used by the bad-`M` completion lemma.  Thus

```text
gamma_s(G) <= p+gamma(B_X)
           <= p+alpha(B_X)
           <= alpha(G)+1.
```

The conclusion is valid for every `0<=alpha(G)-p`; it is not limited to
`p=alpha(G)` or `p=alpha(G)-1`.

## Scope and relationship to the connected-residual reduction

The earlier connected-residual analysis forced the two numerical cases
`p in {alpha(G)-1,alpha(G)}` for a minimum counterexample with connected
`G-K`.  The pure common-two proof strictly supersedes that use: it handles
all private-budget gaps and does not assume `G-K` connected.  The old
finite triple certificate remains a valid corroborating artifact, but is no
longer needed to close the one-unit-slack case.

For the stated dominating-triangle theorem, the three outer cases are
exhaustive:

1. If some `P_i` is empty, the other two triangle vertices dominate: any
   outside vertex either is private to one of those two or sees at least two
   triangle vertices.  The prior dominating-pair theorem applies.
2. If two distinct private regions have a cross edge, the prior triangle
   cross-edge theorem supplies a dominating induced `P3`, and the prior
   dominating-`P3` theorem applies.
3. Otherwise all three private regions are nonempty and pairwise
   anticomplete, exactly the branch closed above.

The common-two proof itself needs neither connectedness nor `alpha>=3` once
its three nonempty private regions are present.  Those hypotheses enter the
packaged theorem through the surrounding prior results.

## Secondary audit of the old finite triple certificate

The retained certificate is also internally correct.

- A failed residual clique has no all-zero neighbourhood pattern on the
  labelled triple.  Every vertex therefore has one of seven nonzero patterns.
  Multiplicity is irrelevant to badness and to existence of a crossed
  miss/see orientation, so a profile is exactly a nonempty subset of those
  seven patterns: `2^7-1=127` possibilities.
- Each of three labelled members has one of four hub types.  Relabelling the
  independent triple sorts the type list, leaving
  `C(4+3-1,3)=20` multisets.  Every one of the `4^3` ordered lists maps to one
  of those 20 cases.
- For fixed failed `U_0,U_1`, an ordered pair `m,n` can form the crossed path
  `u-n-k_2-m-v` exactly when both see the third hub, `U_0` realizes a pattern
  missed by `m` and seen by `n`, and `U_1` realizes the reverse orientation.
  The certificate forbids every such ordered pair.  Other possible induced
  paths are not encoded, but that only weakens the necessary system; UNSAT
  under the weaker system is sufficient.
- The unused third residual clique can be represented locally by one empty
  pattern.  It satisfies badness for every hub seen by a triple member and
  introduces no crossed orientation.  No hidden bound on its actual order is
  being assumed, because only realized pattern types matter.

My independent implementation reproduces all 20 retained rows exactly and
again finds no survivor.

## Independent computation

`verify_triangle_global_common_two.py` imports none of the author's proof or
enumeration code.  It reports `PASS` and performs:

- 18 mechanical five-vertex chord-template checks;
- an independent reproduction of all 20 legacy profile rows, byte-for-value
  equal to the retained JSON row data; and
- a direct singleton-representative abstraction for independent sets
  `|J|=1,...,5`, checking 1,523 incidence instances, of which 893 are
  induced-`P5`-free, with zero common-two failures.

The author's separate direct Graph Atlas audit was also rerun.  It found four
nonempty bad vertices, nine seen-region attachment checks, four independent
bad sets, and zero failures.  These finite checks are corroboration only;
the proof above has no order bound and no computational dependency.
