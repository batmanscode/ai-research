# Contributor guide

This repository publishes auditable research. Keep claims precise, evidence
reproducible, and exploratory results visibly exploratory.

Silly Goose Labs is the umbrella brand. Keep each project's scientific title
precise in reports, citations, and deployment metadata; do not replace result
names with the umbrella label.

## Read the right truth

1. `SPEC_detailed.md` — current repository, result, and interaction truth.
2. Each named project's `README.md` — domain methods and claim scope; category
   `README.md` files route to the current projects.
3. `DESIGN.md` — visual, interaction, and public-voice rules.
4. `PLAYTEST.md` — evergreen verification contract and open gates.
5. `playtest/RESULTS.md` — durable evidence and unresolved gates.
6. `SPEC_rough.md` — append-only owner intent and decision history.

`README.md` is the short entry point. `findings/README.md` records publication
status and IDs; the sibling finding bodies are submission sources, not a second
source of scientific truth.

## Boundaries

- Never commit credentials, sessions, raw private conversations, or external-
  model payloads.
- Do not strengthen the graph result beyond the exact certified theorem. The
  coefficient-one strengthening is false; the optimum in `[4/3, 3/2]` remains
  open.
- Do not describe the biology analysis as untouched confirmation, a causal
  mechanism, or an official leaderboard result.
- Keep `SPEC_rough.md` append-only. Update live documents only when their truth
  changes.
- Deployment is owner-managed. Do not add or run automatic deployment unless
  the owner explicitly requests it.
- Treat `graph/<project>/` and `biology/<project>/` as independent projects.
  Each owns its scientific report, evidence, `CITATION.cff`, `DESIGN.md`, and
  `website/`.
- Keep `site/` as a compatibility copy for previously shared or cached paths;
  canonical links belong to the named project directories.
- Publish external findings only after the corresponding source tree and links
  are stable.

## Normal validation

Run the exact graph verifier, the proportional biology rerun, checksum and
secret checks, and the affected browser journeys from `PLAYTEST.md`. For visual
work, inspect desktop and mobile yourself; an external model is a second
opinion, not the decision-maker.

Before major commits, check whether the relevant README, specs, design,
playtest, and domain reports still agree. Commit coherent milestones with clear
messages.
