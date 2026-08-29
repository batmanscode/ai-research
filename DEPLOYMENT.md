# Deployment

Deployment is intentionally owner-managed. No GitHub Actions deployment
workflow is included.

## Deployable source

Use `site/` as the static publish directory. It contains:

- `index.html` — graph explainer;
- `biology.html` — biology report;
- `css/site.css` and `js/graph-story.js`;
- `assets/biology_comparison.png`.

All first-party links are relative, so the site works at a domain root or a
subpath. No build step, server runtime, secret, database, or environment
variable is required.

## Host contract

- Serve `index.html` for the publish root.
- Preserve `biology.html`, `css/`, `js/`, and `assets/` paths.
- Serve UTF-8 HTML/CSS/JS and `image/png` with correct content types.
- HTTPS is recommended for public deployment.
- Do not inject analytics, cookies, runtime model calls, or user tracking as
  part of the default research release.

## Release check

After deployment, run the complete website scenario in `PLAYTEST.md` against
the production URL. Verify desktop and mobile states, all four graph steps,
console and first-party requests, external repository/source links, and the
biology caveat. Only then add the production URL to repository metadata or
external finding submissions.

