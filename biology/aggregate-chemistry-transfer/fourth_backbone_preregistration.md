# Draft preregistration: fourth-backbone confirmation

**Current status:** protocol/template ready; no eligible public fourth matched
backbone was found, and no candidate phenotype file has been opened. See the
[feasibility audit](external_validation_feasibility.md) and the executable
[label-escrow freeze](external_validation_freeze/).

## Objective

Test whether a frozen, position-invariant aggregate chemistry representation
improves variant ranking over native mutation count on a previously unseen
randomized hydrophobic-core landscape.

## Freeze before labels

- The five amino-acid property columns and all feature formulas in
  `native_core_transfer.py`.
- Candidate feature sets and ridge penalty grid.
- Training-side selection order: macro within-count Spearman, then macro full
  Spearman.
- Primary and secondary metrics, bootstrap, permutation procedure, and random
  seed policy.
- The new protein's native core and randomized positions from sequence and
  design records, before phenotype inspection.
- Candidate metadata, all prespecified model predictions, structure mappings,
  protocol configuration, and evaluator source hashes in
  `external_validation_freeze/manifest.lock.json`.

## Dataset

- One unrelated protein with seven buried positions randomized over
  `F/I/L/M/V`, or the closest experimentally defensible matching design.
- Target 1,000–2,000 quality-controlled variants sampled across native
  mutation-count strata.
- At least three independently prepared biological replicate libraries so the
  uncertainty is not only variant-sampling uncertainty.
- A folding/stability-linked readout comparable to abundancePCA, with batch and
  replicate metadata retained.

Earlier subsampling of the three public landscapes suggested that 500 variants
were sufficient for positive variant-sampling lower bounds on all three, while
250 was not sufficient for FYN-SH3. The larger target above allows for batch
and new-protein uncertainty that simple subsampling cannot estimate.

## Primary endpoint

The difference in held-backbone Spearman rank correlation between the frozen
aggregate model and native-mutation-count baseline. Report a block-bootstrap
95% confidence interval with blocks defined by biological replicate and
mutation-count stratum.

## Co-primary mechanism check

Within-native-count Spearman correlation after residualizing prediction and
phenotype within mutation-count stratum and batch. Use a one-sided permutation
test that shuffles phenotype only within those blocks.

## Applied endpoint

Difference in `precision@5%` between the frozen aggregate model and native-
count baseline. The selected and true top sets use larger-is-better ranking and
deterministic SHA-256 variant-ID tie-breaking. Report 1% and 10% as locked
secondary thresholds; do not choose a threshold after reveal.

## Comparators

- native mutation count;
- additive per-position ridge;
- official one-hot ridge;
- one fixed protein-language-model likelihood baseline; and
- one-hot plus that fixed likelihood baseline; and
- one permutation-invariant structural baseline, if its descriptors can be
  fixed without phenotype feedback.

## Success criterion

Claim replication only if the primary bootstrap interval excludes zero and the
co-primary permutation test is significant under the preregistered threshold.
Report all metrics and all comparators regardless of outcome.

## Label escrow

A data steward or collaborating lab keeps the exact two-column phenotype file
unavailable until the manifest exists. `freeze.py` rejects phenotype-like
columns, validates the seven-site F/I/L/M/V design and library assignments,
hashes all label-free inputs and evaluator code, and refuses to overwrite a
freeze. `reveal_evaluate.py` verifies every frozen hash before opening labels,
then runs only the locked models, bootstrap, permutation, and top-k endpoints.

Any changed design, candidate, model, structure rule, or evaluator requires a
new freeze before reveal. A failed or negative prospective test is still the
result and should be published.

## Interpretation

A positive result supports a cheap cross-backbone ranking method and the value
of a permutation-invariant inductive bias. It still would not prove a causal
biophysical mechanism. A negative result falsifies the current transfer claim
cleanly and should be published.
