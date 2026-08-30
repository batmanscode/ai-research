# Fourth-backbone feasibility audit

**Decision:** no eligible public fourth matched backbone was found. No
candidate score, phenotype, count, or label file was downloaded or opened
during this audit. This is a source-and-metadata result, not a new numerical
experiment.

## Why the public confirmation cannot be done honestly

The current FLIP2 Hydro release contains exactly three wild-type proteins, all
already used in the exploratory analysis. The source GEO study contains extra
public libraries, but they are FYN-SH3 experiments with different randomized
sites or readouts—not an unrelated fourth backbone. FLIP2 Hydro and the GEO
core-score files are representations of the same source study, so comparing
against both would test provenance, not replication.

| source | checked fact | reuse boundary |
|---|---|---|
| [FLIP2 Hydro](https://flip.protein.properties/) | 24,935 variants from three wild types; seven core sites use the F/I/L/M/V alphabet; the held-backbone splits are `to_P06241`, `to_P0A9X9`, and `to_P01053`. | Hydro is CC-BY 4.0. |
| [FLIP2 Zenodo v3](https://zenodo.org/records/18433203) | The 30 January 2026 record contains the same three held-backbone files and no fourth Hydro library or baseline predictions. | Pin the record version and checksums. |
| [GEO GSE266299](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE266299) | The sparse core experiment uses FYN-SH3, CI-2A, and CspA. Extra assays are FYN-only and change the design or readout. | Public availability is not a redistribution license; do not vendor score files without a confirmed license. |
| [Source analysis repository](https://github.com/lehner-lab/combinatorialcores) and [Zenodo 11175469](https://zenodo.org/records/11175469) | These establish the raw/processed provenance behind Hydro. | The repository root showed no license; cite it and use independent code. |
| RCSB [1A0N](https://www.rcsb.org/structure/1A0N), [1MJC](https://www.rcsb.org/structure/1MJC), [3CI2](https://www.rcsb.org/structure/3CI2) | Experimental structures can support label-free mappings for the three current proteins. | PDB archive/API data are CC0; attribute depositions and RCSB. |

## Candidate decisions

| candidate | unrelated backbone? | matched design/readout? | blind confirmation? | decision |
|---|---:|---:|---:|---|
| Existing three FLIP2 `to_*` splits | No | Yes | No | Duplicate exploratory tests. |
| GEO sparse core scores | No | Yes | No | Duplicate provenance. |
| GEO FYN buried/exposed library | No | No: 36 sites and site-specific alphabets | No | At most a labelled exploratory sensitivity study; scores remain unopened. |
| GEO FYN binding/permissivity libraries | No | No: altered readout or added mutations | No | Not confirmation. |
| Other FLIP2 tasks such as TrpB | Yes | No: different assay and mutational design | Only as out-of-domain stress tests | Do not relabel as replication. |

## Accession correction

The FLIP2 webpage's visible Hydro button parentheticals appear accession-
swapped. Primary UniProt/RCSB records support the mapping used by this project:

| accession | protein | structure |
|---|---|---|
| `P06241` | FYN-SH3 | 1A0N chain B |
| `P0A9X9` | CspA | 1MJC chain A |
| `P01053` | CI-2A | 3CI2 chain A |

Future documentation should anchor names to accessions and primary records,
not copy the webpage parentheticals.

## What remains publishable before wet lab

The strongest honest computational paper is an explicitly exploratory
leave-one-backbone-out methods/screening study with:

1. the current aggregate model frozen as primary;
2. a partial-pooling sensitivity model, labelled prior-sensitive because each
   fold has only two source backbones;
3. structural mapping fixed before any future phenotype reveal;
4. an applied `precision@5%` endpoint plus predeclared 1% and 10% secondary
   thresholds;
5. native-count, additive-position, one-hot, fixed pLM-likelihood, one-hot+pLM,
   and structure-invariant comparators; and
6. a prospective label-escrow package that locks candidate metadata,
   predictions, structure rules, model configuration, and evaluation code.

The package in [`external_validation_freeze/`](external_validation_freeze/)
implements that final item without including phenotype values.

## Eligibility for genuine confirmation

A future confirmatory experiment still needs an unrelated protein with seven
buried F/I/L/M/V sites—or a justified closest match—1,000–2,000 quality-
controlled variants across native-count strata, at least three independently
prepared biological libraries, and a stability/abundance-linked assay with
batch metadata. A data steward or collaborating lab must keep phenotypes
unavailable until the freeze manifest exists.

That experiment is technically straightforward but requires new experimental
access. It cannot be manufactured by downloading another public FLIP2 or GEO
file.
