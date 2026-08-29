# Design contract: optimal secure-domination coefficient

## Status

This is an active research package, not yet a finished visual paper. A public
website should not imply that the exact coefficient has been solved. The
project becomes a separately deployable paper site only after a global upper
bound or exact counterexample survives independent audit.

## Future noob-first story

1. Introduce guards, attacks, and one-for-one swaps with a tiny interactive
   graph before showing notation.
2. Explain the known interval `4/3 <= c_opt <= 3/2` as a gap between one exact
   connected family and one published universal theorem.
3. Let the reader move from `alpha=3` to the unresolved `alpha=4` slice; show
   why a hypothetical `(4,6)` graph would settle sharpness.
4. Separate theorem, proof-certified finite search, untraced solver evidence,
   and conjecture through persistent labels—not color alone.
5. Turn failed proof routes into a short “why the obvious ideas break” gallery,
   using the exact graph6 witnesses and the collective cone-`C5` family.
6. Finish at the precise collective-selection condition, making the open step
   visible rather than hiding it behind “future work.”

## Visual language

- Reuse the dark Silly Goose Research Labs paper shell and graph colors from the sibling
  counterexample site so the projects read as one research family.
- Reserve red for a failed defense or disproved shortcut, green for a verified
  defense, and amber for finite evidence. Every state also gets a text label.
- Prefer SVG/Canvas for exact graphs and proof states; do not use generated art
  for mathematical diagrams.
- Animations must be optional, pauseable, deterministic, and disabled by
  `prefers-reduced-motion`.
- The narrowest phone layout must preserve equations, evidence labels, and
  graph controls without horizontal page scrolling.

## Review gate

Before deployment, inspect desktop and mobile screenshots directly, verify all
displayed numbers against the machine-readable results, then use Gemini Flash
as a secondary visual/communication review. The working researcher makes the
final judgment.
