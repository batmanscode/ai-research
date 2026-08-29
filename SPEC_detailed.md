# Detailed specification

Last updated: 29 August 2026

This is the current product, research, and technical truth for `ai-research`.

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
- `site/` — compatibility copy of the original two-page static explainer.
- `findings/` — Markdown source for external finding submissions.
- Root documents — project routing, owner intent, current truth, design,
  validation, deployment, citation, licensing, and file integrity.

## Graph result

For graph6 `KtiSYtlXqwmT`, the complement of the icosahedral graph:

- order 12, size 36, connected, degree sequence `6^12`;
- no induced `P5` among all 792 five-subsets;
- independence number `alpha = 3`;
- zero secure triples among all 220 triples;
- 435 secure four-sets, including `{0,1,2,3}`;
- secure domination number `gamma_s = 4`.

Therefore the proposed coefficient-one strengthening is false, and the best
universal coefficient for the published connected class lies in `[4/3, 3/2]`.
The exact coefficient remains open. The graph construction itself is not
claimed as new.

## Biology result

The FLIP2 Hydro analysis uses correct native cores `FLFFIIV`, `VIVVVFV`, and
`VIIVLVI`. Within each official held-backbone fold, feature family and ridge
penalty are chosen using training-side validation.

| Held backbone | Native-count rho | Aggregate model rho | Within-count rho |
|---|---:|---:|---:|
| FYN-SH3 / P06241 | 0.253 | 0.411 | 0.389 |
| CspA / P0A9X9 | 0.056 | 0.246 | 0.272 |
| CI-2A / P01053 | 0.293 | 0.476 | 0.395 |

All three full-rank paired-bootstrap improvement intervals exclude zero; all
three within-count permutation tests report `p = 1/1001`. These are exploratory
public-test results. The broader representation path was influenced by prior
test inspection. Confirmation requires the frozen prospective fourth-backbone
study.

## Visual papers

`graph/secure-domination-p5-free/website/index.html` introduces secure
domination in plain language and contains
a four-step SVG story: icosahedron, complement, failed triple, secure four-set.
Tabs and an optional timed playback control change the exact graph state.

`biology/aggregate-chemistry-transfer/website/index.html` explains the corrected
reference state, three held-backbone comparisons, within-count signal,
invariance hypothesis, failed position-specific structural transfer, and
evidence boundary.

Each paper owns its first-party assets and can be deployed without the other.
Both pages use relative first-party assets, semantic headings, a skip link,
responsive layouts, visible text labels in addition to color, and reduced-
motion handling. External links point to stable repository or source URLs.

## Deployment

Deployment is owner-managed. The canonical deploy roots are the two project
`website/` directories; the repository contains no automatic deployment
workflow. See `DEPLOYMENT.md`.

## Known limitations and open gates

- The graph coefficient between `4/3` and `3/2` is unresolved.
- Minimum-order SAT evidence is described honestly but no formally checked DRAT
  trace is included in this reconstruction.
- The biology result has no untouched fourth backbone or wet-lab confirmation.
- Production-host browser passes remain pending until the owner deploys both
  visual papers.
- Human screen-reader and device testing are not claimed.

## Acceptance criteria

- Exact graph certificate regenerates and matches the checked-in file.
- Biology point estimates and selections regenerate from public data.
- Claims and caveats agree across root, domain, site, and finding documents.
- All tracked artifact checksums pass and no credentials appear in the commit.
- Both visual papers work at desktop, compact, phone, and narrow widths once
  hosted, with no broken first-party assets or critical console errors.
