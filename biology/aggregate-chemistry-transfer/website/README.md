# Deploy the biology visual paper

This directory remains a self-contained static root and rollback build context.
The canonical Coolify release now uses the repository-root Dockerfile and serves
this paper at `/aggregate-chemistry-transfer/`. Use this directory's Dockerfile
on port `3000` only for a standalone or rollback deployment. It needs no build
command, environment variable, database, or sibling website.

```text
index.html
favicon.png
css/site.css
assets/biology_comparison.png
Dockerfile
nginx.conf
```

The main values and caveats are rendered as accessible HTML; the image is a
reviewed companion artifact rather than the sole carrier of evidence.
