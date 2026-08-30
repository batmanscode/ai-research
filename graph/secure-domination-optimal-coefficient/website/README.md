# Deploy the sharp-coefficient visual paper

This directory is a self-contained static root and rollback build context. The
canonical Coolify release uses the repository-root Dockerfile and serves this
paper at `/secure-domination-optimal-coefficient/`. Use this directory's
Dockerfile on port `3000` only for a standalone or rollback deployment.

```text
index.html
favicon.png
css/site.css
js/proof-map.js
Dockerfile
nginx.conf
```

The six-step map is a schematic of the all-orders proof, not a finite graph or
a solver trace. Formal statements, audits, and the independent checker live
one directory above. No build command, environment variable, database, or
sibling website is required.
