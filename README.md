# Verified open-problem results

Two auditable research tracks developed from public open problems: an exact
counterexample in secure domination and a corrected exploratory experiment on
protein-fitness transfer.

**Independent visual papers:**
[graph counterexample](graph/secure-domination-p5-free/website/index.html) ·
[protein transfer](biology/aggregate-chemistry-transfer/website/index.html)

## Results at a glance

| track | result | status | start here |
|---|---|---|---|
| Graph theory | For the complement \(G\) of the icosahedral graph, \(\gamma_s(G)=4>3=\alpha(G)\). Thus the proposed coefficient-one strengthening is false and the best universal coefficient lies in \([4/3,3/2]\). | Exact, exhaustively certified theorem/counterexample. The optimum coefficient remains open. | [`graph/secure-domination-p5-free/`](graph/secure-domination-p5-free/) |
| Protein fitness | A validation-selected 11–16 feature aggregate-chemistry ridge improves on native mutation count in all three FLIP2 Hydro held-backbone folds; within-count signal is positive in each. | Exploratory reconstruction, not untouched confirmation. A fourth backbone is preregistered. | [`biology/aggregate-chemistry-transfer/`](biology/aggregate-chemistry-transfer/) |

## Reproduce

The graph result needs only Python's standard library:

```bash
cd graph/secure-domination-p5-free
python3 verify_counterexample.py
```

The biology pipeline downloads the public FLIP2 Hydro data and recreates the
statistics and figure:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd biology/aggregate-chemistry-transfer
python3 native_core_transfer.py
```

Both visual papers are dependency-free. Deploy
`graph/secure-domination-p5-free/website/` and
`biology/aggregate-chemistry-transfer/website/` independently with any static
host. The original `site/` paths remain as compatibility copies for published
or cached links; canonical links use the named project directories.

## Published findings

- [Secure-domination counterexample](https://www.emergentmind.com/open-problems/improve-secure-domination-bound-connected-p5-free-graphs#research-findings)
- [Aggregate-chemistry transfer experiment](https://www.emergentmind.com/open-problems/mechanisms-one-hot-protein-representation-performance#research-findings)

Publication IDs, canonical source links, and status are recorded in
[`findings/README.md`](findings/README.md).

## Repository map

```text
graph/      category index and named graph-theory projects
biology/    category index and named biological projects
site/       compatibility copy of the original combined explainer
findings/   publication index and source bodies for the Emergent Mind reports
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
- Each project's `research-log.md` records corrections and failed approaches
  because negative information is part of the useful result.

## Sources and licenses

The graph question comes from Gupta, Henning, Maniya, and Pradhan,
[*Secure domination in \(P_5\)-free graphs*](https://arxiv.org/abs/2503.08088).
The protein experiment uses the [FLIP2 Hydro benchmark](https://flip.protein.properties/)
and its [CC-BY 4.0 data](https://zenodo.org/records/18433203).

Repository code and original prose are MIT-licensed. Upstream datasets retain
their own licenses and are downloaded rather than redistributed.
