# Deploy the graph visual paper

This directory remains a self-contained static root and rollback build context.
The canonical Coolify release now uses the repository-root Dockerfile and serves
this paper at `/secure-domination-p5-free/`. Use this directory's Dockerfile on
port `3000` only for a standalone or rollback deployment. It needs no build
command, environment variable, database, or sibling website.

```text
index.html
favicon.png
css/site.css
js/graph-story.js
Dockerfile
nginx.conf
```

The animation uses exact graph data rather than a decorative approximation.
The formal proof and verifier live one directory above. The companion sharp-
coefficient paper is deployed at `/secure-domination-optimal-coefficient/`.
