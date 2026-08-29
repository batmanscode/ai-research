# Rough specification

This file preserves owner intent and major decisions. It is append-only.

## Initial brief — August 2026

- Continue two research tracks: a secure-domination open problem and an
  exploratory protein-fitness transfer experiment.
- Preserve exact proofs, computation, useful failures, and reproducible code.
- Make the graph result understandable to a lay reader through a beautiful
  interactive explanation, with animation where it genuinely helps.
- Keep graph and biology work together if an umbrella repository makes future
  research easier to add; separate them clearly inside it.
- Use Gemini Flash as an optional visual reviewer, while the working agent's
  judgment remains primary.
- Send meaningful progress and finished artifacts to the owner's private
  Telegram bot without persisting credentials.
- Use Emergent Mind's finding-publication workflow for one graph report and one
  biology report, after stable repository links exist.
- Preserve corrections honestly, especially the retracted all-valine biology
  interpretation.

## Changes 29/08/2026

- Use one extensible public umbrella repository named `ai-research`.
- Follow the documentation and verification conventions in the owner's
  `project-bootstrap` repository and its cross-repository review.
- The owner will deploy the website. Do not add GitHub Pages automation.
- Emergent Mind publication remains the last step after repository work.
- Give every paper its own descriptively named project folder, project-level
  `DESIGN.md`, and independently deployable noob-first visual website. Use the
  portfolio as a research index linking to the complete paper sites.
- Both Emergent Mind findings were published after the repository links became
  stable, then updated to the final named project paths.
- Use “Silly Goose Labs” as the public umbrella brand while retaining precise
  scientific titles and descriptively named project folders.
- Keep one global repository citation and one result-specific citation inside
  each project; prefer a project DOI later when a formal archive exists.
- Deploy the two visual papers as separate Coolify applications from their own
  `website/` Base Directories and Dockerfiles. Do not publish them through
  GitHub Pages or ChatGPT Sites.
- Perform final desktop/mobile screenshot review against the public deployment,
  with direct inspection first and Gemini 3.7 Flash as a second opinion; send
  useful captures and results to Telegram.

## Changes 30/08/2026

- Rename the public umbrella brand to “Silly Goose Research Labs”; keep the
  shorter `SG` mark as the compact visual signature.
- Keep the root citation for the repository as a collection and one precise
  citation inside each project. A reader citing one result should use its
  project citation rather than being asked to cite both levels by default.
- Keep goose illustrations optional and subordinate to the research. Prefer a
  small colophon or marginal mark over a mascot competing with a paper's title,
  problem, or evidence.

## Changes 29/08/2026 — optimal-coefficient continuation

- Keep the proved 12-vertex counterexample in its finished named project.
- Continue the all-orders connected coefficient question in the separate
  `graph/secure-domination-optimal-coefficient/` project and branch.
- Treat `gamma_s <= alpha + 1` as a high-value theorem/counterexample fork:
  proving it makes the sharp multiplicative coefficient `4/3`, while a
  certified counterexample redirects the bound.
- Do not merge or externally publish a claimed global solution until its proof
  or counterexample certificate survives an independent audit.

## Changes 30/08/2026 — unified deployment

- Replace the two canonical Coolify applications with one lightweight root
  Docker image that serves every paper beneath its own stable path on the
  research subdomain. The portfolio will own the separate research index, so
  this deployment needs no root homepage.
- Keep the combined image minimal: use the unprivileged nginx image's default
  static configuration, do not add a root `nginx.conf`, custom health endpoint,
  or Docker `HEALTHCHECK`, and let unknown static paths fail normally.
- Retain the individual paper Dockerfiles only as temporary rollback options
  through the first combined production release; remove them afterward unless
  standalone paper domains remain useful.
