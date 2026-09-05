# Interactive research note

Self-contained static root for **Who gets the Infinity Stones?**

- `index.html` — the scenario, controls, theorem, limitations, and citations.
- `css/site.css` — responsive page and accessible controls.
- `js/model.js` — independent JavaScript implementation of the mathematics.
- `js/explorer.js` — presentation only; recomputes on local input changes.
- `favicon.png` — the existing repository-family icon.

No build, runtime dependency, API key, external model, network request, or
remote font is needed. Open through a static HTTP server to inspect it.
`public-sites.json` maps this directory to `/infinity-stones/`; production
requires the separately reviewed Portfolio submodule update.

The default example is pre-rendered for readers without JavaScript. Controls
require JavaScript, and the page says so. The diagrams show model values, not
empirical forecasts or confidence intervals.
