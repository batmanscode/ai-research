# Deploy the biology visual paper

This directory is a self-contained Coolify build context. Use Dockerfile build
pack, Base Directory `/biology/aggregate-chemistry-transfer/website`, Dockerfile
`/Dockerfile`, internal port `3000`, empty Port Mappings, and health path `/`.
It needs no build command, environment variable, database, or sibling website.

```text
index.html
css/site.css
assets/biology_comparison.png
Dockerfile
nginx.conf
```

The main values and caveats are rendered as accessible HTML; the image is a
reviewed companion artifact rather than the sole carrier of evidence.
