# Verified open-problem results

Two auditable research tracks developed from public open problems: an exact
counterexample in secure domination and a corrected exploratory experiment on
protein-fitness transfer.

**Interactive explainer source:** [`site/index.html`](site/index.html)

## Results at a glance

| track | result | status | start here |
|---|---|---|---|
| Graph theory | For the complement \(G\) of the icosahedral graph, \(\gamma_s(G)=4>3=\alpha(G)\). Thus the proposed coefficient-one strengthening is false and the best universal coefficient lies in \([4/3,3/2]\). | Exact, exhaustively certified theorem/counterexample. The optimum coefficient remains open. | [`graph/README.md`](graph/README.md) |
| Protein fitness | A validation-selected 11–16 feature aggregate-chemistry ridge improves on native mutation count in all three FLIP2 Hydro held-backbone folds; within-count signal is positive in each. | Exploratory reconstruction, not untouched confirmation. A fourth backbone is preregistered. | [`biology/README.md`](biology/README.md) |

## Reproduce

The graph result needs only Python's standard library:

```bash
cd graph
python3 verify_counterexample.py
```

The biology pipeline downloads the public FLIP2 Hydro data and recreates the
statistics and figure:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd biology
python3 native_core_transfer.py
```

The website is dependency-free. Open `site/index.html`, or deploy the `site/`
directory with any static host.

## Repository map

```text
graph/      proof, standard-library verifier, exact certificate, research log
biology/    corrected pipeline, results, preregistration, research log
site/       lay explanation and interactive graph story
findings/   source drafts for the two Emergent Mind reports
```

Project truth and verification are routed through [`AGENTS.md`](AGENTS.md),
[`SPEC_detailed.md`](SPEC_detailed.md), [`DESIGN.md`](DESIGN.md), and
[`PLAYTEST.md`](PLAYTEST.md). Deployment is owner-managed; see
[`DEPLOYMENT.md`](DEPLOYMENT.md).

## Integrity and scope

- Generated outputs are recorded in [`CHECKSUMS.sha256`](CHECKSUMS.sha256).
- The graph construction was already known in another context; its
  secure-domination calculation and resulting lower bound are the contribution
  described here.
- The biology test landscapes had influenced the broader research path before
  this reconstruction. The per-fold hyperparameters are selected on
  training-side validation, but the result remains exploratory.
- `graph/research-log.md` and `biology/research-log.md` record corrections and
  failed approaches because negative information is part of the useful result.

## Sources and licenses

The graph question comes from Gupta, Henning, Maniya, and Pradhan,
[*Secure domination in \(P_5\)-free graphs*](https://arxiv.org/abs/2503.08088).
The protein experiment uses the [FLIP2 Hydro benchmark](https://flip.protein.properties/)
and its [CC-BY 4.0 data](https://zenodo.org/records/18433203).

Repository code and original prose are MIT-licensed. Upstream datasets retain
their own licenses and are downloaded rather than redistributed.
