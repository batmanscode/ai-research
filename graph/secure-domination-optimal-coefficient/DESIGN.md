# Design contract: optimal secure-domination coefficient

## Status

This is a finished visual paper for the independently audited all-orders
theorem `gamma_s(G) <= alpha(G)+1`, hence `c_opt=4/3`, on connected
induced-`P5`-free graphs with `alpha>=3`. The published `3alpha/2` theorem
remains correct but nonoptimal. Conventional external peer review remains
pending and must stay visible.

## Noob-first story

1. Lead with the closed gap and define secure guarding in ordinary language.
2. State the additive theorem and the `alpha>=3` arithmetic that yields `4/3`.
3. Use a deterministic six-step proof map: Bacsó--Tuza split; path; small
   cliques; triangles; larger no-cross-edge cliques; cross-edge back to path.
4. Pair the universal upper proof with the exact 12-vertex lower witness.
5. Keep failed routes short and useful: they explain why the final structural
   split was needed, without making obsolete searches look like dependencies.
6. End with exact scope: the coefficient is solved; equality classification,
   minimum witness order, and conventional peer review are not.

## Visual language

- Reuse the warm-paper Silly Goose Research Labs shell and graph colors from
  the sibling counterexample site so the projects read as one research family.
- Reserve red for a failed defense or disproved shortcut, green for a verified
  defense, and amber for finite evidence. Every state also gets a text label.
- Prefer SVG/Canvas for exact graphs and proof states; do not use generated art
  for mathematical diagrams.
- Animations must be optional, pauseable, deterministic, and disabled by
  `prefers-reduced-motion`.
- The narrowest phone layout must preserve equations, evidence labels, and
  graph controls without horizontal page scrolling.

## Review gate

Before deployment, inspect desktop and mobile screenshots directly, exercise
all six proof-map states, verify every displayed number against the checked
results, then use Gemini Flash as a secondary visual/communication review. The
working researcher makes the final judgment.
