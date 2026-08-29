# Aggregate chemistry transfers across FLIP2 Hydro backbones

**Visual paper:** [`website/index.html`](website/index.html)

**Design contract:** [`DESIGN.md`](DESIGN.md)

## Status

This is a **reconstructed exploratory analysis**, not an untouched external
validation. The representation choices were influenced by earlier inspection
of the public FLIP2 test landscapes. The code now selects model details using
training-side validation only, but that does not erase study-level test
feedback.

## Corrected result

The FLIP2 Hydro task holds out an entire protein backbone. The baseline ranks
variants only by their Hamming distance from the correct native seven-residue
core. The model is ridge regression on 11 or 16 aggregate, position-invariant
features describing mutation burden, final physicochemical totals, signed
changes, and absolute changes.

| held backbone | test variants | native-count baseline | aggregate model | paired improvement, 95% bootstrap CI | within-count \(\rho\) |
|---|---:|---:|---:|---:|---:|
| FYN-SH3 / P06241 | 9,972 | 0.253 | **0.411** | +0.158 [0.132, 0.178] | 0.389 |
| CspA / P0A9X9 | 8,500 | 0.056 | **0.246** | +0.189 [0.170, 0.208] | 0.272 |
| CI-2A / P01053 | 6,463 | 0.293 | **0.476** | +0.182 [0.158, 0.208] | 0.395 |

All three within-native-count permutation tests have Monte Carlo
\(p=1/1001\). The result therefore is not just “more mutations are worse”:
simple aggregate chemistry also ranks variants within a fixed mutation burden.

## Native-reference correction

An earlier analysis incorrectly treated `VVVVVVV` as the native core. It is an
engineered anchor, not the wild type for these proteins. The corrected cores
are:

| protein | accession | native core |
|---|---|---|
| FYN-SH3 | P06241 | `FLFFIIV` |
| CI-2A | P01053 | `VIIVLVI` |
| CspA | P0A9X9 | `VIVVVFV` |

Every current metric uses Hamming distance from those native cores.

## Comparison with published FLIP2 values

The reconstructed model is below the best reported comparator on FYN-SH3 but
above the published table value on the other two held backbones:

| held backbone | this analysis | published best | difference |
|---|---:|---:|---:|
| FYN-SH3 | 0.411 | 0.444 (SaProt-650M likelihood) | −0.033 |
| CspA | 0.246 | 0.151 (Dayhoff likelihood) | +0.095 |
| CI-2A | 0.476 | 0.394 (ESMC-300M LoRA) | +0.082 |

This is a descriptive, post-hoc public-test comparison—not an official
leaderboard submission or a new-SOTA claim.

## Why invariance appears to matter

The seven randomized residues occupy unrelated positions in three unrelated
folds. A prior structure-conditioned experiment mapped every site to an
experimental structure, then added position-specific 3D descriptors. It
failed on every held backbone (Spearman 0.221, −0.016, and −0.150). Contact-
graph matching also left dozens of equally optimal site correspondences.

The aggregate model avoids inventing a false position 1-to-1 correspondence.
That negative result supports a narrow mechanism hypothesis: for this domain
shift, the useful inductive bias is permutation invariance over a small set of
buried hydrophobic substitutions, not naive transfer of ordinal site labels.

## Reproduce

The script downloads the public CC-BY 4.0 Hydro split files from FLIP2's
Zenodo record, performs training-side model selection, refits, evaluates, and
regenerates the figure and machine-readable results:

```bash
python3 native_core_transfer.py
```

Dependencies are listed in the repository-level `requirements.txt`. The exact
output used here is `results/analysis.json`.

## Publication boundary

The evidence supports a concise exploratory benchmark or methods note. It does
not establish a universal biological mechanism, because there are only three
backbones and the public test landscapes influenced the research path. A
confirmatory paper needs the now-frozen protocol evaluated once on an untouched
fourth randomized-core landscape. `fourth_backbone_preregistration.md` gives a
concrete prospective design.

## Sources

- [FLIP2 project and benchmark](https://flip.protein.properties/)
- [FLIP2 data, Zenodo record 18433203](https://zenodo.org/records/18433203)
- Escobedo et al., *Science* (2025),
  [source analyses](https://github.com/lehner-lab/combinatorialcores)
