# Aggregate chemistry provides a small cross-backbone signal on FLIP2 Hydro

This exploratory reconstruction tests a narrow mechanism for why small protein
representations can remain competitive under backbone shift: permutation-
invariant summaries may avoid transferring false positional correspondences.

For each official FLIP2 Hydro held-backbone fold, a ridge model uses 11 or 16
features describing native mutation count plus aggregate final, signed-change,
and absolute-change physicochemical properties. Feature family and penalty are
selected only on the fold's training-side validation data.

| held backbone | native-count \(\rho\) | aggregate model \(\rho\) | within-count \(\rho\) |
|---|---:|---:|---:|
| FYN-SH3 / P06241 | 0.253 | **0.411** | 0.389 |
| CspA / P0A9X9 | 0.056 | **0.246** | 0.272 |
| CI-2A / P01053 | 0.293 | **0.476** | 0.395 |

All three stratified paired-bootstrap intervals for improvement exclude zero.
All within-native-count permutation tests give \(p=1/1001\), showing that the
signal is not only mutation burden. A previous structure-conditioned model
that transferred ordinal site labels failed on every held backbone, which is
consistent with—but does not prove—the invariance hypothesis.

One correction is central. An earlier analysis treated `VVVVVVV` as the wild
type. Canonical mapping showed that it is an engineered anchor. All current
metrics use the correct native cores `FLFFIIV`, `VIIVLVI`, and `VIVVVFV`.

This is partial empirical evidence about representation behavior, not a
universal biological mechanism or an untouched leaderboard claim. Public test
landscapes influenced the broader research path. The decisive next experiment
is a frozen, prospective evaluation on a fourth backbone; a preregistration is
included. An official-source audit found no eligible public fourth matched
backbone: the FLIP2 and source GEO core files cover the same three proteins,
while additional public assays remain FYN-only with changed designs or
readouts. No candidate phenotype file was opened. A label-escrow package now
locks candidate metadata, predictions, structural rules, protocol, and
evaluator hashes before a steward reveals any future labels.

- [Interactive visual paper](https://github.com/batmanscode/ai-research/blob/main/biology/aggregate-chemistry-transfer/website/index.html)
- [Full methods and limitations](https://github.com/batmanscode/ai-research/blob/main/biology/aggregate-chemistry-transfer/README.md)
- [Reproducible pipeline](https://github.com/batmanscode/ai-research/blob/main/biology/aggregate-chemistry-transfer/native_core_transfer.py)
- [Fourth-backbone preregistration](https://github.com/batmanscode/ai-research/blob/main/biology/aggregate-chemistry-transfer/fourth_backbone_preregistration.md)
- [Fourth-backbone feasibility audit](https://github.com/batmanscode/ai-research/blob/main/biology/aggregate-chemistry-transfer/external_validation_feasibility.md)
- [Prospective label-escrow package](https://github.com/batmanscode/ai-research/tree/main/biology/aggregate-chemistry-transfer/external_validation_freeze)
