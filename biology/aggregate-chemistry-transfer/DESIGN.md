---
version: 1
name: Aggregate Chemistry Across Protein Backbones
description: A visual exploratory paper about transferable protein-fitness signal, its correction, and its evidence boundary.
colors:
  background: "#0B0F10"
  panel: "#121718"
  text: "#F4F1EA"
  model: "#74E8DC"
  caveat: "#FF826E"
  comparison: "#AE9CFF"
typography:
  display: "Newsreader, Georgia, serif"
  body: "Manrope, system-ui, sans-serif"
  data: "DM Mono, ui-monospace, monospace"
---

# Design contract

## Reader promise

A reader without protein-ML background should understand the prediction task,
why mutation count is the necessary baseline, what the aggregate model adds,
why an earlier analysis was corrected, and why a fourth backbone is still
required.

## Narrative

1. Explain a protein backbone as a different structural context, not merely a
   new row from the same distribution.
2. Compare native mutation count with the small aggregate-chemistry model on
   all three held backbones.
3. Interrupt the success story with the native-core correction.
4. Show within-count ranking to separate chemistry signal from mutation burden.
5. Explain why position-invariant aggregation may transfer when naive site
   correspondence does not.
6. Finish with the prospective fourth-backbone test and publication boundary.

## Visual language

- Cyan identifies the aggregate model.
- Violet identifies published comparators, always named in surrounding copy.
- Coral marks corrections and post-hoc limitations, never buried footnotes.
- Values appear as text as well as bar length; bars are descriptive, not a
  claim of an official leaderboard win.

## Evidence hierarchy

The exploratory label appears before the first chart. Point estimates,
bootstrap intervals, permutation tests, native cores, method code, and the
preregistration remain reachable in one reading path. Provenance data are not
described as independent replication.

## Interaction

This paper is intentionally reading-first. Static comparisons are preferred to
animation unless an interaction materially clarifies backbone shift or feature
aggregation. Any future control must work with keyboard and touch, retain text
equivalents, and respect reduced motion.

## Do / do not

Do make the correction conspicuous, label the public-test feedback, and explain
the distinction between association, predictive utility, and mechanism.

Do not call the result untouched confirmation, causal biology, a universal
mechanism, or an official leaderboard submission. Do not imply bootstrap
resampling creates a fourth independent protein.
