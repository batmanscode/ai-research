# Silly Goose Research Labs · AI research

An extensible home for auditable, AI-assisted research. The first two tracks
developed from public open problems: an exact counterexample in secure
domination and a corrected exploratory experiment on protein-fitness transfer.

**Independent visual papers:**
[graph counterexample](graph/secure-domination-p5-free/website/index.html) ·
[protein transfer](biology/aggregate-chemistry-transfer/website/index.html)

## Results at a glance

| track | result | status | start here |
|---|---|---|---|
| Graph theory | For the complement \(G\) of the icosahedral graph, \(\gamma_s(G)=4>3=\alpha(G)\). Thus the proposed coefficient-one strengthening is false and the best universal coefficient lies in \([4/3,3/2]\). | The 12-vertex example and its \(4/3\) lower bound are exact theorem/counterexample results—not conjectures. Minimum order is finite computational evidence; the optimum coefficient remains open. | [`graph/secure-domination-p5-free/`](graph/secure-domination-p5-free/) |
| Graph coefficient continuation | The extremal value is exactly four when `alpha=3`, including an infinite connected family at ratio `4/3`. Exact SAT finds no counterexample to `gamma_s <= alpha+1` through order 17 for `alpha=4` and order 16 for `alpha=5`; order-12 instances carry independently checked DRUP proofs. | Active research, not a claimed all-orders solution. A stronger dominating-clique subclaim also survives exact finite search, and the precise collective-exchange bottleneck is documented. | [`graph/secure-domination-optimal-coefficient/`](graph/secure-domination-optimal-coefficient/) |
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

Both visual papers are dependency-free. The root Dockerfile serves them from one
small static deployment at `/secure-domination-p5-free/` and
`/aggregate-chemistry-transfer/`. Their project-owned `website/` directories
remain independently usable as static roots. The original `site/` paths remain
compatibility copies for previously shared or cached links.

## Published findings

- [Secure-domination counterexample](https://www.emergentmind.com/open-problems/improve-secure-domination-bound-connected-p5-free-graphs#research-findings)
- [Aggregate-chemistry transfer experiment](https://www.emergentmind.com/open-problems/mechanisms-one-hot-protein-representation-performance#research-findings)

Publication IDs, canonical source links, and status are recorded in
[`findings/README.md`](findings/README.md). The sibling Markdown files are the
finding bodies submitted to Emergent Mind; they are not dumps of the complete
API payload, whose IDs and public URLs are tracked in that index.

Open-problem discovery, literature navigation, and finding publication used
the wonderful [Emergent Mind skills and API](https://www.emergentmind.com/skills).
Those tools helped organize and publish the work; the repository's code,
certificates, results, and scoped claims remain the auditable evidence.

## Citation

Use the root [`CITATION.cff`](CITATION.cff) when citing the repository as a
collection. For a specific result, use that project's more precise citation
instead:

- [`graph/secure-domination-p5-free/CITATION.cff`](graph/secure-domination-p5-free/CITATION.cff)
- [`graph/secure-domination-optimal-coefficient/CITATION.cff`](graph/secure-domination-optimal-coefficient/CITATION.cff)
- [`biology/aggregate-chemistry-transfer/CITATION.cff`](biology/aggregate-chemistry-transfer/CITATION.cff)

When a project receives a preprint or archive DOI, its project citation should
be updated to prefer that permanent scholarly record.

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

- The release-wide [`CHECKSUMS.sha256`](CHECKSUMS.sha256) detects accidental
  changes or corruption when the repository is exported outside Git. It is an
  integrity manifest, not a signature or a deployment requirement.
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
