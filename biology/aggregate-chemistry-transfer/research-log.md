# Research log: corrections, useful failures, and current hypothesis

This is a concise audit trail, not a transcript of private model reasoning.

## 1. Initial signal

Small physicochemical summaries appeared to transfer across the three Hydro
backbones better than a full-sequence one-hot ridge baseline. Mutation burden
was then added as a deliberately hard control.

## 2. A serious reference-state bug

The first audit counted residues different from valine, effectively assuming
an all-valine wild type. That assumption was false. Canonical sequence mapping
showed that `VVVVVVV` is an engineered anchor and recovered the correct native
cores `FLFFIIV`, `VIIVLVI`, and `VIVVVFV`.

The earlier numerical interpretation was retracted rather than patched. Every
result was recomputed using native Hamming distance.

## 3. Chemistry beyond mutation count

The corrected experiment separated two effects:

- a strong, backbone-dependent relationship between mutation burden and
  fitness; and
- a reproducible within-burden ranking signal carried by aggregate chemistry.

Stratified bootstrap intervals kept the full-rank improvement above zero on
all three backbones. Within-count permutations gave no null replicate as large
as the observed statistic in 1,000 runs for any backbone.

## 4. Structural follow-up that failed

The randomized sites were mapped at 100% identity to FYN 1A0N-B, CI-2A
3CI2-A, and CspA 1MJC-A. Adding raw position-specific 3D features looked useful
on training-side validation but generalized poorly to every held fold.

That failure was informative: the seven selected sites are not homologous
ordinal coordinates across unrelated folds. The successful model's
permutation invariance is likely a feature, not a compromise.

## 5. Reconstruction after workspace maintenance

Workspace maintenance removed the earlier local artifacts. The present code
was rebuilt from the public FLIP2 files and the recorded corrected protocol.
The reconstructed model adds signed and absolute property-change aggregates
and gives stronger held-backbone correlations (0.411, 0.246, 0.476). Because
the public test labels had already influenced the broader research path, these
remain exploratory results even though per-fold hyperparameters are selected
using training-side validation only.

## 6. Numerical tie-breaking

A cross-platform rerun found that the two best CI-2A ridge penalties can swap
order when validation scores move by less than `1e-5` across linear-algebra
builds. The selection rule now treats both primary and secondary validation
scores inside that tolerance as tied, then prefers the stronger ridge penalty.
This makes the recorded choice reproducible without changing any displayed
result or claim.

## 7. Next decisive experiment

Freeze the current representation and evaluation code, then run it once on a
new protein before inspecting labels. That experiment—not another bootstrap on
the same three backbones—is the clean evidence boundary.
