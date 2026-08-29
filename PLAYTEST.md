# Playtest and verification contract

Last reviewed: 29 August 2026

This is the evergreen release contract. Durable baselines and unresolved gates
live in `playtest/RESULTS.md`.

## Evidence labels

- **Automated** — repeatable command or exact assertion.
- **Scenario** — realistic flow through the repository or website.
- **Manual** — human visual, interaction, accessibility, or scientific review.
- **External** — hosted environment, upstream provider, Telegram, or second
  reviewer.

An easier evidence class never proves a stronger one. Static parsing does not
prove responsive layout; an AI review does not replace primary judgment.

## Proportional release matrix

| Change | Required evidence |
|---|---|
| Documentation only | Markdown/link review, checksum refresh, secret scan, commit diff review. |
| Graph code or claim | Documentation gate plus exact verifier, regenerated certificate comparison, and claim-scope review. |
| Biology code or claim | Documentation gate plus selected-model/point-estimate reproduction; use the full bootstrap/permutation run for published statistics or figures. |
| Public UI or visual | Relevant computation gate plus desktop/compact/phone/narrow browser journeys, all changed states, console/asset review, and direct screenshot review. |
| External publication | All affected gates plus stable public source links, duplicate-finding check, and final attribution/scope review. |

## Automated commands

From the repository root:

```bash
(cd graph/secure-domination-p5-free && python3 verify_counterexample.py --output /tmp/certificate.json)
cmp graph/secure-domination-p5-free/data/counterexample_certificate.json /tmp/certificate.json

python3 biology/aggregate-chemistry-transfer/native_core_transfer.py \
  --data-dir .cache/hydro \
  --output /tmp/biology.json \
  --figure /tmp/biology.png \
  --bootstrap 50 --permutations 100

node --check graph/secure-domination-p5-free/website/js/graph-story.js
sha256sum -c CHECKSUMS.sha256
```

The reduced biology run must reproduce selected feature families, penalties,
and point estimates. It intentionally does not reproduce the checked-in
`1/1001` permutation p-values; use the script defaults for that publication
gate.

Run a credential-pattern scan over the commit candidate. Never print matching
credential values; report only pass/fail or filenames needing inspection.

## Website scenario

Run the graph scenario with `graph/secure-domination-p5-free/website/` as the
static root and the biology scenario with
`biology/aggregate-chemistry-transfer/website/` as the static root. Neither may
rely on its sibling site being mounted beside it.

1. Confirm the hero states `gamma_s = 4 > 3 = alpha` and the coefficient gap.
2. Select Shape, Flip, Three, and Four. Confirm edge counts 30, 36, 36, 36;
   state copy and legends change; the failed exchange names vertices 1, 7, and
   10; the secure set is `{0,1,2,3}`.
3. Play, pause, and directly select a step during playback.
4. Follow proof, certificate, research-log, repository, and source links.
5. Separately open the biology website and verify all nine comparison values,
   all three within-count values, native cores, and the exploratory warning.
6. On both websites, confirm no unexpected console errors, broken first-party requests, clipped
   text, or horizontal document overflow.

Repeat at approximately 1440×900, 1024×768, 390×844, and 320×568. At 200%
zoom, verify usable reflow. Keyboard through skip link, tabs, play control, and
links. Confirm visible focus and that reduced-motion preference removes
nonessential transition duration.

Browser emulation does not complete human screen-reader or physical-device
testing.

## Visual review

Capture representative graph steps and the complete biology comparison after
the scenario. Inspect hierarchy, graph legibility, text collisions, clipping,
bar accuracy, caveat visibility, color-plus-text state, and mobile reading
order. Ask Gemini Flash for a sanitized second opinion only after direct
inspection. Record durable failures or open gates, not ceremonial approvals.

## External publication

Immediately before publishing an Emergent Mind finding:

- retrieve existing findings again and stop on substantive duplication;
- use the exact matching open-problem slug;
- label partial evidence and open questions plainly;
- include stable repository, method, and certificate/preregistration links;
- use the agreed attribution; and
- read the returned finding object back before claiming success.
