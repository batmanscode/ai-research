# Deploy the graph visual paper

This directory is a self-contained Coolify build context. Use Dockerfile build
pack, Base Directory `/graph/secure-domination-p5-free/website`, Dockerfile
`/Dockerfile`, internal port `3000`, empty Port Mappings, and health path `/`.
It needs no build command, environment variable, database, or sibling website.

```text
index.html
css/site.css
js/graph-story.js
Dockerfile
nginx.conf
```

The animation uses exact graph data rather than a decorative approximation.
The formal proof and verifier live one directory above.
