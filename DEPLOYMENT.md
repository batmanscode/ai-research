# Deployment

Deployment is owner-managed. The canonical production image is built by the
private `batmanscode/portfolio` repository, which pins this public repository
as a Git submodule and copies only the declared visual-paper roots into its
static `dist/` output. Research code, datasets, proof material, logs, and
project documents remain public here and do not enter the website image.

## Public-site manifest

[`public-sites.json`](public-sites.json) is the deployment boundary. It maps
each stable URL slug to one project-owned static root:

| Paper | Source | Route |
|---|---|---|
| Secure domination | `graph/secure-domination-p5-free/website` | `/secure-domination-p5-free/` |
| Sharp secure-domination coefficient | `graph/secure-domination-optimal-coefficient/website` | `/secure-domination-optimal-coefficient/` |
| Protein transfer | `biology/aggregate-chemistry-transfer/website` | `/aggregate-chemistry-transfer/` |

Every declared source must stay inside this repository, contain `index.html`,
and use relative first-party asset paths. A new visual paper chooses one stable
lowercase slug and adds one manifest entry. The Portfolio build validates the
manifest and refuses traversal, duplicate slugs, missing roots, or missing
entry points before copying anything.

## Portfolio release contract

Portfolio checks out this repository at `vendor/ai-research`. Its production
build reads the pinned manifest and stages each declared source at
`dist/<slug>/`. The final nginx image contains the hub plus those static paper
folders only; it does not contain the Git checkout or the rest of this
repository.

Advancing `ai-research` does not silently change production. The submodule pin
must move in a reviewed Portfolio commit. Portfolio may use Dependabot's
`gitsubmodule` ecosystem to propose that pin update automatically.

## Coolify

In steady state, only the Portfolio Coolify application owns
`research.sillygoose.fyi`; no per-paper path domains are required. Git
submodules must be enabled for that resource. Coolify supports submodule cloning
and currently enables it by default.

For the migration:

1. deploy a Portfolio revision that contains the pinned submodule and exported
   paper folders;
2. verify the research root, all three paper URLs, their first-party assets, and
   an unknown path;
3. only then remove `research.sillygoose.fyi` and its path rules from the old
   `ai-research` resource; and
4. stop that resource, retaining it briefly for rollback before deletion.

The root `Dockerfile` remains a local-preview and short rollback option. It
serves the same three paper routes on port `8080`, deliberately without a root
homepage. It should not keep the production research hostname after the
Portfolio deployment is verified.

Reference: [Coolify application Git settings](https://coolify.io/docs/applications).

## URL, attribution, and analytics contract

The canonical paper URLs do not change, so portfolio cards, sitemap entries,
source links, and Emergent Mind attribution/UTM parameters need no migration.
The existing Research Labs Umami property remains attached to
`research.sillygoose.fyi`; moving static files between build sources does not
change that hostname or website ID. The visual papers themselves gain no new
tracker as part of this deployment change.

## Local image verification

The independent paper-only preview remains available:

```bash
docker build -t silly-goose-research .
docker run --rm -p 8080:8080 silly-goose-research
```

Then check the three routes and one miss:

```bash
curl -I http://127.0.0.1:8080/secure-domination-p5-free/
curl -I http://127.0.0.1:8080/secure-domination-optimal-coefficient/
curl -I http://127.0.0.1:8080/aggregate-chemistry-transfer/
curl -I http://127.0.0.1:8080/not-a-paper
```

The paper routes and first-party assets should return `200`; the unknown path
should return `404`.
