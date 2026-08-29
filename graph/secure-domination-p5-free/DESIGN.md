---
version: 1
name: A 4/3 Lower Bound for Secure Domination in Connected P5-Free Graphs
description: A visual paper that turns an exact secure-domination counterexample into a four-step guard story.
colors:
  background: "#F9F8F4"
  panel: "#FFFDF8"
  text: "#1E201D"
  proof: "#2A5438"
  failure: "#9E3A2B"
  construction: "#65569C"
typography:
  display: "Newsreader, Georgia, serif"
  body: "Manrope, system-ui, sans-serif"
  data: "DM Mono, ui-monospace, monospace"
---

# Design contract

## Reader promise

A reader who has never studied domination should understand the guard rule,
see the exact counterexample, and know precisely what was disproved—and what
remains open—without reading the formal certificate first.

## Narrative

1. Lead with the theorem-level contribution: the universal coefficient is at
   least `4/3`.
2. Introduce ordinary domination as placing guards.
3. Add the secure-exchange rule: a guard may move only if coverage survives.
4. Start with the familiar icosahedron and flip edges to form its complement.
5. Show one certified attack that defeats three guards.
6. Show a secure four-guard set and the exact `4 > 3` conclusion.
7. Separate the theorem from finite minimality evidence and the open
   coefficient interval.

## Visual language

- Forest green identifies successful guards and proved conclusions.
- Madder red identifies an attack, exposed vertex, or failed exchange.
- Violet distinguishes construction/complement states.
- Every state has a text legend; color never carries the proof alone.
- The graph visualization is generated from exact adjacency data. Decorative
  simplification may not change vertices, edges, guard sets, or witnesses.

## Interaction

- The four proof steps are directly selectable and keyboard reachable.
- Timed playback is optional, pausable, and never the only reading route.
- Selecting a step during playback takes control immediately.
- Reduced-motion preference removes nonessential transition duration.

## Evidence hierarchy

The page leads with ordinary language, then exposes exact counts, the proof
note, verifier, certificate, and research log. “No secure triple” is exhaustive;
“minimum order” remains finite SAT evidence unless a checked proof trace is
published.

## Do / do not

Do keep the `4/3`–`3/2` gap visible and explain every symbol nearby. Do record
failed proof routes because they explain why the counterexample was sought.

Do not call the icosahedral construction new, imply the original `3/2` theorem
is false, or animate an aesthetically improved graph that is not the certified
object.
