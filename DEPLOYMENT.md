# Deployment

Deployment is intentionally owner-managed. No GitHub Actions deployment
workflow is included.

## Deployable sources

Each paper is an independent static website:

| Paper | Publish directory | Entry point |
|---|---|---|
| Secure domination | `graph/secure-domination-p5-free/website/` | `index.html` |
| Protein transfer | `biology/aggregate-chemistry-transfer/website/` | `index.html` |

Each directory contains its own first-party styles, scripts, or images. Point
a static host at either directory without copying files between them. Both work
at a domain root or a subpath and require no build step, server runtime, secret,
database, or environment variable.

`site/` is the original combined explainer and remains only as a compatibility
source for already-published links. New deployments should use the paper-owned
directories above.

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
metadata, or external finding submissions.
