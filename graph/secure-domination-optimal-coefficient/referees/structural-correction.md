# Structural correction: singleton private regions need not be clusters

Date: 29 August 2026

## Correction

An earlier draft claimed that, for a dominating clique `K` and

`P_k = {z outside K : N(z) intersect K = {k}}`,

every induced subgraph `G[P_k]` is a cluster graph. This is false. The
proposed path `ell-k-a-b-c` for an induced `P3=a-b-c` inside `P_k` has the
chords `kb` and `kc`, because every member of `P_k` is adjacent to `k`.

The already verified cone-`C5` family is an exact counterexample: its hubs
form a dominating clique and every `P_k` is an induced `C5`. The false
cluster sublemma and the component-representative consequence derived from
it have therefore been removed.

## Surviving exact criterion

For any dominating clique `K`, any `X` outside `K`, and `S=K union X`, put

`U_k = P_k minus N[X]`.

Then `S` is secure exactly when every attack `v` outside `S` with no neighbor
in `X` has a neighboring `k in K` such that

`U_k minus {v} is a subset of N(v)`.

This equivalence follows directly from external private neighborhoods and
does not require `P_k` to have any particular internal structure.

## Dependency audit

The correction does **not** affect:

- the complement-of-the-icosahedron counterexample;
- the exact `alpha=3` extremal value four;
- the infinite `B[K_t]` family;
- the coefficient interval `4/3 <= c_opt <= 3/2`;
- any SAT encoding, finite frontier, CNF, or DRUP trace;
- the private-representative complete-multipartite lemma; or
- the operation formulas and their independent audit.

It removes one proposed route toward `gamma_s <= alpha+1`. That global
candidate remains open, as it did before the correction.

## Executable verification

`structure/verify_obstructions.py` checks that all three private regions in
the three-cone instance are induced `C5`s and compares the residual criterion
with direct secure-domination predicates for all 1,024 choices of `X` in the
two-cone instance.

`referees/verify_residual_atlas.py` is independent code using NetworkX. It
checks every dominating clique of size at least two and every outside subset
in every Graph Atlas graph: 170,824 comparisons, with zero mismatches.
