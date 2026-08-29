# Deployment

Deployment is intentionally owner-managed. No GitHub Actions deployment
workflow is included. The canonical visual papers are served together from one
small Coolify application; the portfolio owns the separate research index.

## Public route contract

The root Dockerfile publishes only the two paper directories:

| Paper | Route |
|---|---|
| Secure domination | `/secure-domination-p5-free/` |
| Protein transfer | `/aggregate-chemistry-transfer/` |

### Deriving a URL before deployment

The host comes from the domain attached in Coolify. The path comes directly
from the destination directory in the root Dockerfile:

```text
COPY ... /usr/share/nginx/html/<paper-slug>/
                                  ↓
https://<coolify-domain>/<paper-slug>/
```

For example, copying the graph paper into
`/usr/share/nginx/html/secure-domination-p5-free/` fixes its path as
`/secure-domination-p5-free/`. With `research.sillygoose.fyi` attached, its
planned URL is therefore
`https://research.sillygoose.fyi/secure-domination-p5-free/` before the first
deployment occurs.

The route is explicit; nginx does not derive it from the source project folder
or paper title. For a new paper, choose a stable lowercase slug, copy its public
files into the matching destination directory, and add that route to the table
above. The trailing slash remains canonical because the route names a directory
whose entry point is `index.html`.

The deployment has no root homepage. The base nginx image handles static files,
directory indexes, and missing paths with its default behavior; this repository
does not carry a root `nginx.conf`, application health endpoint, or Docker
`HEALTHCHECK`.

Each paper keeps relative first-party asset paths, so the trailing slash is part
of its canonical URL. A request without it is normalized to the directory URL
by nginx.

## Coolify contract

Create one GitHub-App application with these settings:

| Setting | Value |
|---|---|
| Repository | `https://github.com/batmanscode/ai-research` |
| Branch | `main` |
| Build pack | Dockerfile |
| Base Directory | `/` |
| Dockerfile | `/Dockerfile` |
| Port Exposes | `8080` |
| Port Mappings | empty |
| Environment variables | none |
| Persistent storage | none |

Attach the research subdomain to that resource. For
`research.sillygoose.fyi`, the intended paper URLs are:

- `https://research.sillygoose.fyi/secure-domination-p5-free/`
- `https://research.sillygoose.fyi/aggregate-chemistry-transfer/`

Do not publish those URLs as live until both production routes and their assets
have been checked. Auto Deploy is optional: leave it off for manual releases,
or enable it when every push to `main` should refresh the paper collection.

## Image contract

The root image uses the same unprivileged nginx family as the portfolio, but it
does not need the portfolio's host routing, SPA fallback, or cache rules. The
Dockerfile therefore uses the base image's default static configuration and
copies only each paper's public HTML, CSS, JavaScript, and images.

The papers have no application build, runtime model call, secret, database, or
environment variable. `site/` remains a compatibility source for previously
shared or cached links and is not copied into the canonical deployment image.

The Dockerfiles inside the individual `website/` directories remain temporary
rollback options for the first combined release. They are not the canonical
Coolify path and are not runtime redundancy. Remove them after the combined
production deployment is verified unless standalone paper domains are still
useful.

## Release check

After deployment, run the hosted website scenario in `PLAYTEST.md` against both
paper URLs. Verify desktop and mobile states, graph steps where applicable,
console and first-party requests, external source links, and the biology caveat.
Only then add the production URLs to the portfolio or repository metadata.

When a local Docker runtime is available:

```bash
docker build -t silly-goose-research .
docker run --rm -p 8080:8080 silly-goose-research
```

In another terminal, open both canonical paths or check them directly:

```bash
curl -I http://127.0.0.1:8080/secure-domination-p5-free/
curl -I http://127.0.0.1:8080/aggregate-chemistry-transfer/
curl -I http://127.0.0.1:8080/not-a-paper
```

The paper routes and first-party assets should return `200`; the unknown path
should return `404`.
