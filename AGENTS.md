# Contributor guide

This repository publishes auditable research. Keep claims precise, evidence
reproducible, and exploratory results visibly exploratory.

## Read the right truth

1. `SPEC_detailed.md` — current repository, result, and interaction truth.
2. `graph/README.md` and `biology/README.md` — domain methods and claim scope.
3. `DESIGN.md` — visual, interaction, and public-voice rules.
4. `PLAYTEST.md` — evergreen verification contract and open gates.
5. `playtest/RESULTS.md` — durable evidence and unresolved gates.
6. `SPEC_rough.md` — append-only owner intent and decision history.

`README.md` is the short entry point. `findings/` contains publication source
drafts, not a second source of scientific truth.

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

