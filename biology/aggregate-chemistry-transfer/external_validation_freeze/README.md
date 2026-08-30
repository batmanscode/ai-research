# Prospective label-escrow freeze

This package keeps a future fourth-backbone test genuinely prospective. It
contains no phenotype values. A data steward retains the sealed phenotype file
until `freeze.py` has written `manifest.lock.json`.

## Files locked before reveal

- `candidate_design.tsv` — one row per assayed observation, with sequence,
  construct, library, batch, and native-count stratum metadata;
- `predictions.tsv` — one label-free score per variant from every prespecified
  model;
- `structures.lock.json` — structure versions, chains, site mapping, descriptor
  formulas, and deterministic tie rules;
- `protocol.lock.json` — model columns, metrics, thresholds, random seeds, and
  resampling procedures; and
- the current `native_core_transfer.py`, `freeze.py`, and
  `reveal_evaluate.py` source files.

The schema guard rejects phenotype-like columns from both pre-reveal TSV files.
The manifest hashes every locked input and refuses to overwrite an existing
freeze.

## Freeze workflow

1. Copy the two TSV templates to `candidate_design.tsv` and `predictions.tsv`.
2. Copy `structures.lock.template.json` to `structures.lock.json` and replace
   every placeholder before labels are available.
3. Generate every model prediction without opening the phenotype file.
4. Run:

   ```bash
   python3 freeze.py
   ```

5. Give `manifest.lock.json` to the data steward. Only after that manifest is
   timestamped and independently archived may the steward provide
   `phenotypes.tsv`.
6. Evaluate once, with no model-selection branch:

   ```bash
   python3 reveal_evaluate.py \
     --phenotypes phenotypes.tsv \
     --output prospective_results.json
   ```

The evaluator verifies every frozen hash before reading labels, emits every
prespecified comparator regardless of sign, and reports the replication
criterion exactly as locked. It cannot turn a negative result into a different
model-selection exercise.

## Revealed phenotype schema

The steward-supplied file is not committed. It has exactly:

```text
observation_id	phenotype
```

`observation_id` must match the pre-reveal design. Larger phenotype means
better performance. Replicate/library/batch metadata remain in the already
frozen design file.

## Claim boundary

This package is infrastructure and preregistration—not evidence from a fourth
protein. No eligible public fourth matched backbone was found, and no candidate
phenotype file was inspected while creating it.
