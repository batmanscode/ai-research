# Clean-room referee report: triangle cross-edge and multi/private absorption lemmas

## Verdict

**PASS.**  An intermediate version of the `C_2`-domination paragraph used a
cross edge whose second endpoint was not in the proposed dominating path.
The current draft now repairs that inference with the required additional
induced-`P5` argument.  I found no remaining mathematical gap in either
handwritten lemma.

The strengthened cross-edge theorem is valid:

> If an induced-`P5`-free graph has a dominating triangle
> `K={a,b,c}` and an edge between two distinct singleton-private regions,
> then it has a dominating induced `P3`.

The cited consequence `gamma_s(G) <= alpha(G)+1` is also valid for the stated
connected, induced-`P5`-free scope with `alpha(G)>=3`.  The triangle
multi-region absorption lemma in `clique_structure_miner_2/findings.md` is
valid as well.

## 1. Triangle cross-edge theorem: line-by-line reconstruction

Fix the dominating triangle `K={a,b,c}` and an edge `xy` with
`x in P_a`, `y in P_b`.  Assume that there is no dominating induced `P3`.

### 1.1 The cross-edge cover

The pair `{x,y}` dominates `P_c`.  If `z in P_c` missed both endpoints, then

`z-c-a-x-y`

has the four required edges.  Its six nonconsecutive pairs are nonedges:
`za, zx, zy, cx, cy, ay`.  The first, fourth, fifth, and sixth follow from
the private-region definitions; `zx,zy` are the assumed misses.  Hence this
would be an induced `P5`.

This argument is symmetric in the three regions and can therefore be reused
for any private cross edge.

### 1.2 The first two witnesses

`x-a-b` is an induced `P3`: `xa,ab` are edges and `xb` is not.  It dominates
all of `K`, `P_a`, `P_b`, and `M`.  In particular, every vertex of `M` sees
`a` or `b`, since any two-element subset of a three-element set intersects
`{a,b}`.  Since the path is not dominating, a missed vertex must therefore
be some `z in P_c` with `zx` absent.  The cross-edge cover forces `zy`.

Symmetrically, non-domination of `y-b-a` gives `w in P_c` with `wy` absent,
and the cover forces `wx`.  Necessarily `z != w`, since `zx` is absent while
`wx` is present.

### 1.3 The first two induced cycles

The cycle

`C_a = a-x-y-z-c-a`

is induced.  Its five chords are exactly `ay,yc,az,xc,xz`; the first four
are forbidden by private types and the last by the choice of `z`.

If `C_a` dominated, the induced path `x-y-z` would dominate `K`, `P_c` by
the cross edge `xy`, and `P_a` by the cross edge `yz`.  It would dominate
`P_b` as well: every `P_b` vertex misses the other cycle vertices `a,c`, so
domination by `C_a` makes it see one of `x,y,z` (with `y` itself already on
the path).  If a remaining `m in M` missed `x,y,z`, then:

- when `ma` is present, `z-y-x-a-m` is induced; its six nonconsecutive
  pairs are `zx,za,zm,ya,ym,xm`;
- when `ma` is absent, `m` sees `b,c`, and `x-y-z-c-m` is induced; its six
  nonconsecutive pairs are `xz,xc,xm,yc,ym,zm`.

Every listed pair is absent by the chosen misses or private types.  Thus
`x-y-z` would be a dominating induced `P3`, a contradiction.  Therefore
`C_a` is not dominating, and we may choose a vertex `u` anticomplete to it.  It
misses `a,c`.  It cannot be the remaining hub `b`, because `b` sees both,
and domination by `K` forces any outside vertex missing `a,c` to have
`K`-neighborhood exactly `{b}`.  Thus `u in P_b`; in particular it misses
`x,y,z` because it is anticomplete to the cycle.

Likewise,

`C_b = b-y-x-w-c-b`

is induced: its chords `bx,bw,yw,yc,xc` are absent.  It is nondominating by
the exact symmetric argument.  More explicitly, if it dominated, then
`y-x-w` would dominate `K`, `P_c` through `yx`, `P_b` through `xw`, and
`P_a` because members of `P_a` miss `b,c`.  A missed `m in M` gives
`w-x-y-b-m` when `mb` is present and `y-x-w-c-m` otherwise.  The latter
case uses that a multi-neighbour vertex missing `b` sees `a,c`; all chords
are again absent by the path misses and private types.  Hence an
anticomplete witness `v` for `C_b` exists, must lie in `P_a`, and misses
`y,x,w`.

All forced types are distinct when they need to be: `u` cannot be `y`
because `y` is on `C_a`; `v` cannot be `x` because `x` is on `C_b`; and the
private-region types separate `u,v` from `z,w`.

### 1.4 The two forced cross edges

If `uw` were absent, then

`u-b-a-x-w`

would be induced.  Besides the assumed `uw` nonedge, its nonconsecutive
pairs are `ua,ux,bx,bw,aw`, all absent by `u` being private/anticomplete and
`x,w` having private types `P_a,P_c`.  Hence `uw` is forced.

Similarly, absence of `vz` makes

`v-a-b-y-z`

an induced `P5`; its nonconsecutive pairs `vb,vy,vz,ay,az,bz` are all
excluded by the same data.  Thus `vz` is forced.

### 1.5 The final cycle and contradiction

Now

`C_2 = x-y-z-v-a-x`

is an induced `C5`.  Its chords are exactly `xz,xv,yv,ya,za`: `xz` was
chosen absent; `xv,yv` are absent because `v` is anticomplete to `C_b`; and
`ya,za` are absent by private type.

If `C_2` dominated, the induced path `x-y-z` would dominate `K`, `P_c`
through `xy`, and `P_a` through `yz`.  The draft's statement that the edge
`zv` directly makes this path dominate `P_b` is not literally valid because
`v` is not on the path.  The required conclusion nevertheless follows: if
some `q in P_b - {y}` were not dominated by `x-y-z`, domination by
`C_2={x,y,z,v,a}` and the private nonedge `qa` would force `qv`; then

`q-v-z-y-x`

would be an induced `P5`.  Its nonconsecutive pairs are `qz,qy,qx,vy,vx,zx`:
the first three are the assumed misses, the next two follow because `v` is
anticomplete to `C_b`, and `zx` was chosen absent.  Thus `x-y-z` also
dominates `P_b`.

A missed member of `M` now gives `z-y-x-a-m` when it sees `a`, or
`x-y-z-c-m` when it misses `a`; these are the same already-audited induced
paths.  Hence `x-y-z` would be a dominating induced `P3`, a contradiction.
Therefore `C_2` is not dominating, and we may choose `m` anticomplete to it.
Then:

1. `m` misses `a`, so it is neither a hub nor in `P_a`.
2. The edge `xy` between `P_a,P_b` dominates `P_c` by the cross-edge cover.
3. The edge `zv` between `P_c,P_a` dominates `P_b` by the same cover.

Thus `m` lies in the multi-neighbour region `M`.  It misses `a`, so its at
least two neighbors on `K` must be exactly `b,c`.  Finally,

`m-b-a-v-z`

is induced.  Its nonconsecutive pairs are `ma,mv,mz,bv,bz,az`; the first
three are absent because `m` is anticomplete to `C_2`, and the last three
are absent by the private types of `v,z`.  This is the required
contradiction.

There is no hidden coincidence in this endgame.  For example, the earlier
vertex `u in P_b` could be anticomplete to `C_2` only if it also missed `v`,
but the cross edge `zv` must dominate `P_b`, and `u` already misses `z`.
Hence `uv` is forced and `u` cannot serve as `m`.

## 2. Consequence and audited local repair

The dominating-`P3` outcome is covered by the project's separately proved
dominating-`P3` theorem for connected induced-`P5`-free graphs with
`alpha>=3`.

Therefore the strengthened cross-edge theorem implies
`gamma_s(G)<=alpha(G)+1` directly throughout the stated `alpha>=3` scope;
there is no longer a separate `C5` or `alpha=3` branch.  A dominating
triangle makes `G` connected automatically, although connectedness is not
needed for the structural theorem itself.

The strengthened draft correctly replaces the invalid shortcut

> the three cross edges `xy`, `yz`, and `zv` would make [the path] dominate
> `P_c`, `P_a`, and `P_b`

with the `q-v-z-y-x` argument above.  That insertion makes the strengthened
proof complete.  As an optional wording cleanup, its preceding phrase should
say that the **first two** cross edges `xy,yz` cover `P_c,P_a`; the third
edge `zv` is used only inside the separate `P_b` argument.

## 3. Triangle multi-region absorption lemma

Let `K={k_i,k_j,k_l}`, `m in M_{ij}`, and `y in P_i cap N(m)`.

The set `{y,m,k_j}` induces the path `y-m-k_j`: the two path edges hold by
hypothesis/type and `yk_j` is absent because `y` is private to `k_i`.
The guard `k_j` dominates `K`, `P_j`, `M_{ij}`, `M_{jl}`, and `M_{ijl}`.
This leaves only `P_i`, `P_l`, and `M_{il}` to consider.

For either `z in P_l` or `z in M_{il}`, if `z` missed both `m,y`, then

`z-k_l-k_j-m-y`

would be induced.  Its nonconsecutive pairs are `zk_j,zm,zy,k_lm,k_ly,k_jy`.
The first is absent for both relevant types; the next two are the assumed
misses; and the final three are excluded by the exact types of `m,y`.
Hence every such `z` sees `m` or `y`.  This proves

`V(G) - N[{y,m,k_j}] subseteq P_i`.

If dominating induced `P3`s have already been excluded, the displayed path
must miss some `x`.  The residual inclusion forces `x in P_i`, and vertices
of `P_i` already miss `k_j`, so `x` must miss both `y,m`.  Thus
`x in P_i - N[{y,m}]`, and `x,y` are an independent pair in `G[P_i]`.
The stated conclusion `alpha(G[P_i])>=2` follows.

No region is omitted: the seven outside attachment classes are the three
private classes, the three exact two-hub classes, and the class complete to
the triangle.

## 4. Independent computational checks

These checks corroborate the proofs; none is used as a substitute for them.

### Triangle cross-edge theorem

- Direct Graph Atlas audit: all 1,253 Atlas graphs, including 873
  induced-`P5`-free graphs and 3,022 dominating triangles.  There were 521
  applicable private cross-edge instances, and every one had a dominating
  induced `P3`.
- Independent random audit: 30,000 fixed-dominating-triangle graphs on
  7--13 vertices.  Of these, 8,464 were induced-`P5`-free, yielding 33,842
  applicable triangle/cross-edge cases and zero failures of the strengthened
  dominating-`P3` conclusion.
- Independent exact CNF: fixed dominating triangle, fixed edge between
  `P_a,P_b`, induced-`P5`-freeness, and no dominating induced `P3`.  Every
  order 5--14 was UNSAT independently in
  CaDiCaL 1.9.5 and Kissat 4.0.4.  These are solver results without proof
  traces and are therefore finite evidence only.

The independent scripts used for this audit are
`triangle_referee_checks.py` and `triangle_referee_sat.py` in the scratch
workspace; no repository file was edited.

### Multi/private absorption lemma and finite slices

- The direct Atlas audit reports PASS for 1,277 relevant `(m,y)` tuples over
  3,022 dominating triangles, including 228 third-private cover checks, 366
  `M_{il}` cover checks, and 1,277 exact-residual checks.
- The retained one-multi SAT outputs contain 28/28 UNSAT cases in each of
  CaDiCaL and Kissat.
- The retained two-multi SAT outputs contain 190/190 UNSAT cases in each
  solver.
- The direct-predicate versus CNF unit test independently passes on all 88
  fixed graphs.

The two structured SAT slices concern only the specific bounded shapes
encoded by their scripts.  Their presentation as finite evidence—not as a
proof of the remaining triangle branch—is correct.

## Final assessment

Both lemmas pass as proof-grade results with the local `q-v-z-y-x` repair
now present in the draft.  The strengthened cross-edge theorem closes
exactly the branch with an edge between two singleton-private regions; it does not
close the remaining pairwise-anticomplete-private, nontrivial-`M` branch.
The absorption lemma is a sound local packing constraint for that residue,
but its witnesses have not yet been globally combined into the full
`gamma_s<=alpha+1` theorem.

