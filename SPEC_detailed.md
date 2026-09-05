# Detailed specification

Last updated: 5 September 2026

This is the current product, research, and technical truth for `ai-research`,
published under the Silly Goose Research Labs umbrella brand.

## Purpose

The repository is an extensible public home for small, independently auditable
AI-assisted research results. Its first release contains one exact graph-
theory result and one exploratory biological machine-learning result, plus one
independently deployable, lay-facing visual paper for each result.

## Repository structure

- `graph/` — category index; each named project owns its theorem, evidence,
  verifier, design contract, and visual paper.
- `biology/` — category index; each named project owns its analysis, results,
  preregistration, design contract, and visual paper.
- `decision-theory/` — category index; each project owns its model, proof,
  reproducible checks, citation, and beginner-facing interactive.
- `site/` — compatibility copy of the original two-page static explainer.
- `findings/` — Markdown source for external finding submissions.
- Root documents — project routing, owner intent, current truth, shared design,
  validation, deployment, repository-level citation, licensing, and file
  integrity. `public-sites.json` is the small allowlist of deployable visual
  paper roots. Each named project also owns its result-specific citation.

## Graph result

For graph6 `KtiSYtlXqwmT`, the complement of the icosahedral graph:

- order 12, size 36, connected, degree sequence `6^12`;
- no induced `P5` among all 792 five-subsets;
- independence number `alpha = 3`;
- zero secure triples among all 220 triples;
- 435 secure four-sets, including `{0,1,2,3}`;
- secure domination number `gamma_s = 4`.

Therefore the proposed coefficient-one strengthening is false.  The
continuation project now proves that the best universal coefficient for the
published connected class with `alpha>=3` is exactly `4/3`. The graph
construction itself is not
claimed as new. The published `3alpha/2` theorem remains valid because the
example satisfies `4 <= 4.5`; only the stronger coefficient-one candidate is
refuted.

The separate `graph/secure-domination-optimal-coefficient/` continuation now
records the next rigorous boundary:

- the extremal secure-domination value at `alpha=3` is exactly four;
- the ratio `4/3` occurs in the infinite connected family `B[K_t]`;
- no `alpha=4` graph without a secure five-set was found through order 17;
- no `alpha=5` graph without a secure six-set was found through order 16;
- with minimum dominating-clique size at least three, no `gamma_s > alpha`
  graph was found through order 15 at `alpha=4` or order 14 at `alpha=5`;
- both order-12 UNSAT formulas have retained CNF/DRUP traces independently
  checked through the empty clause;
- the cut-vertex, dominating-pair, dominating-induced-`P3`, and full
  dominating-triangle branches satisfy `gamma_s <= alpha+1` by all-orders
  proofs;
- by the Bacsó--Tuza split, only inclusion-minimal dominating cliques of order
  at least four remain;
- a connected residual behind a smallest counterexample satisfies
  `alpha(G-K)=alpha(G)` and `gamma_s(G-K)=alpha(G-K)+1`;
- the pairwise-anticomplete private-region branch is solved for every
  dominating-clique order: active missed-hub sets are nested, have order at
  most two, and the two-hub case yields the final saving;
- for clique order at least four, one global cross partition determines every
  edge and nonedge between distinct private regions; within-region edges
  remain unrestricted; and
- every private-cross-edge branch at a larger dominating clique collapses to
  a dominating induced `P3`; and
- the exhaustive Bacsó--Tuza assembly proves `gamma_s <= alpha+1` and the
  exact optimum coefficient `4/3`.

The continuation is now a solved theorem package with its own noob-first
interactive visual paper at
`graph/secure-domination-optimal-coefficient/website/`. The planned combined
route is `/secure-domination-optimal-coefficient/`; production deployment
remains owner-managed.

Status boundary: the existence and secure-domination calculation for this
12-vertex graph are an exact theorem/counterexample, not a conjecture. The
stronger statement that order 12 is globally minimum remains finite SAT
evidence in this repository because no checkable unsatisfiability trace is
included. The exact optimum coefficient is now proved to be `4/3` in the
continuation project.

## Biology result

The FLIP2 Hydro analysis uses correct native cores `FLFFIIV`, `VIVVVFV`, and
`VIIVLVI`. Within each official held-backbone fold, feature family and ridge
penalty are chosen using training-side validation. Primary and secondary
validation scores within `1e-5` are numerical ties; the stronger ridge penalty
wins so the recorded choice is stable across linear-algebra builds.

| Held backbone | Native-count rho | Aggregate model rho | Within-count rho |
|---|---:|---:|---:|
| FYN-SH3 / P06241 | 0.253 | 0.411 | 0.389 |
| CspA / P0A9X9 | 0.056 | 0.246 | 0.272 |
| CI-2A / P01053 | 0.293 | 0.476 | 0.395 |

All three full-rank paired-bootstrap improvement intervals exclude zero; all
three within-count permutation tests report `p = 1/1001`. These are exploratory
public-test results. The broader representation path was influenced by prior
test inspection. Confirmation requires the frozen prospective fourth-backbone
study. An official-source audit found no eligible public matched candidate;
the new label-escrow package freezes candidate metadata, model predictions,
structure rules, protocol, and evaluator code before a steward reveals labels.

## Recurring disarmament result

`decision-theory/infinity-stones/` develops CYBRDELIC's Infinity Stones
scenario into a stationary model with fresh handover risk, temporary safety,
and returning production. The proof gives an exact decision threshold, sharp
bounds given a mean and time limits, a zero mean-only robust threshold, and
noncommuting patience/uncertainty limits. These are conditional mathematical
results using established renewal and convexity tools; global novelty and
external peer review remain unconfirmed. A permanently trustworthy custodian
is explicitly shown to change the result.

## Visual papers

`graph/secure-domination-p5-free/website/index.html` introduces secure
domination in plain language and contains
a four-step SVG story: icosahedron, complement, failed triple, secure four-set.
Tabs and an optional timed playback control change the exact graph state.

`graph/secure-domination-optimal-coefficient/website/index.html` explains the
sharp `4/3` theorem with a deterministic six-step proof map: the Bacsó--Tuza
split, path theorem, small and triangular cliques, larger pairwise-private
cliques, and the cross-edge return to a dominating path.

`biology/aggregate-chemistry-transfer/website/index.html` explains the corrected
reference state, three held-backbone comparisons, within-count signal,
invariance hypothesis, failed position-specific structural transfer, and
evidence boundary.

`decision-theory/infinity-stones/website/index.html` introduces the scenario
without requiring maths, compares three equal-average comeback patterns, and
lets readers test which time limits make a decision possible. The decision
equation and same-average arithmetic are visible with ordinary explanations; the time-weight definition and secondary settings are optional.
Scores, assumptions, and CYBRDELIC attribution remain visible.
Before the experiments, a visible setup box distinguishes permanent prevention
from surviving production and links the one-off calculation in the proof.

Each paper owns its first-party assets and can be deployed without the other.
All four pages use relative first-party assets, semantic headings, a skip link,
responsive layouts, visible text labels in addition to color, and reduced-
motion handling. External links point to stable repository or source URLs.

## Deployment

Deployment is owner-managed. `public-sites.json` maps stable path slugs to the
four project-owned `website/` sources. The private Portfolio repository pins
this repository as a Git submodule, validates that manifest, and copies only
those static roots into the production research-host image. Advancing this
repository cannot change production until the reviewed submodule pin advances.
The root Dockerfile remains a paper-only local preview and rollback path on port
8080. See `DEPLOYMENT.md`.

## Known limitations and open gates

- The sharp graph coefficient theorem has not yet undergone conventional
  external peer review, despite multiple independent proof audits.
- The proof-carrying finite coefficient searches do not imply an all-orders
  theorem; higher-order frontier runs beyond order 12 retain solver results
  but not proof traces.
- Minimum-order SAT evidence is described honestly but no formally checked DRAT
  trace is included in this reconstruction.
- The biology result has no untouched fourth backbone or wet-lab confirmation;
  the public-source audit found no eligible fourth matched landscape.
- The new Infinity Stones route requires a reviewed Portfolio pin update
  before production-host verification; this source change does not deploy it.
- Human screen-reader and device testing are not claimed.

## Acceptance criteria

- Infinity Stones evidence regenerates, agrees with the browser calculator,
  and keeps model assumptions and novelty limits visible.
- Exact graph certificate regenerates and matches the checked-in file.
- Biology point estimates and selections regenerate from public data.
- Claims and caveats agree across root, domain, site, and finding documents.
- All tracked artifact checksums pass and no credentials appear in the commit.
- All four visual papers work at desktop, compact, phone, and narrow widths
  once hosted, with no broken first-party assets or critical console errors.
