# Deployment

Deployment is intentionally owner-managed. No GitHub Actions deployment
workflow is included. The canonical papers are not published through GitHub
Pages or ChatGPT Sites; the owner deploys them as Coolify applications.

## Coolify contract

Deploy the same GitHub repository twice as two independent Coolify resources.
Each resource uses the Dockerfile inside its own website folder, following the
same unprivileged-nginx contract as the portfolio repository.

| Setting | Secure-domination paper | Protein-transfer paper |
|---|---|---|
| Repository | `https://github.com/batmanscode/ai-research` | same |
| Branch | `main` | `main` |
| Build pack | Dockerfile | Dockerfile |
| Base Directory | `/graph/secure-domination-p5-free/website` | `/biology/aggregate-chemistry-transfer/website` |
| Dockerfile | `/Dockerfile` | `/Dockerfile` |
| Port Exposes | `3000` | `3000` |
| Port Mappings | empty | empty |
| Health-check path | `/` | `/` |
| Environment variables | none | none |
| Persistent storage | none | none |

The Dockerfile path is relative to the selected Base Directory. Do not point
both domains at one resource: each paper is a complete domain-root website with
its own `index.html` and first-party assets.

In Coolify:

1. Create a GitHub-App application from `batmanscode/ai-research`.
2. Select **Dockerfile** and enter the first Base Directory from the table.
3. Keep Dockerfile Location as `/Dockerfile`, expose `3000`, leave host port
   mappings empty, set the paper's domain, and deploy.
4. Repeat as a second application with the other Base Directory and domain.

Auto Deploy is optional. Leave it off for manual releases, or enable it on both
GitHub-App resources when every push to `main` should redeploy both papers.
The images deliberately have no Dockerfile `HEALTHCHECK`; Coolify owns the
deployment health check, as it does for the portfolio.

## Deployable sources

Each paper is also an ordinary independent static website:

| Paper | Publish directory | Entry point |
|---|---|---|
| Secure domination | `graph/secure-domination-p5-free/website/` | `index.html` |
| Protein transfer | `biology/aggregate-chemistry-transfer/website/` | `index.html` |

Each directory contains its own first-party styles, scripts, or images. The
checked-in Dockerfile adds only the nginx serving layer; the papers themselves
have no application build, runtime model call, secret, database, or environment
variable.

`site/` is the original combined explainer and remains only as a compatibility
source for previously shared or cached links. Canonical and new deployment
links should use the paper-owned directories above.

## Host contract

- Serve `index.html` for the publish root.
- Preserve the selected paper directory's `css/`, `js/`, or `assets/` paths.
- Serve UTF-8 HTML/CSS/JS and `image/png` with correct content types.
- HTTPS is recommended for public deployment.
- Do not inject analytics, cookies, runtime model calls, or user tracking as
  part of the default research release.

## Release check

After deployment, run the relevant website scenario in `PLAYTEST.md` against
each production URL. Verify desktop and mobile states, graph steps where
applicable, console and first-party requests, external source links, and the
biology caveat. Only then add production URLs to the portfolio, repository
metadata, or the already-published external findings.

Local container checks:

```bash
docker build -t silly-goose-graph graph/secure-domination-p5-free/website
docker run --rm -p 3000:3000 silly-goose-graph

docker build -t silly-goose-biology biology/aggregate-chemistry-transfer/website
docker run --rm -p 3001:3000 silly-goose-biology
```

The second command in each pair is foregrounded; stop it with Ctrl+C before
reusing the terminal. In another terminal, check `http://127.0.0.1:3000/` or
`http://127.0.0.1:3001/` respectively.
