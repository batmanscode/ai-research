# Design system

Last updated: 30 August 2026

## Direction

Silly Goose Research Labs is the umbrella brand; each visual paper keeps its
precise scientific title. The family should feel like a careful research
exhibit, not a generic AI dashboard: warm paper, deep ink, restrained botanical
and mineral accents, large editorial type, and evidence that becomes more
concrete as the reader moves down the page.

This root contract stays deliberately broad. It defines the family resemblance
and review standard; each project-owned `DESIGN.md` is authoritative for that
paper's reader promise, narrative, evidence boundary, and interactions.

## Voice

- Lead with the result in ordinary language.
- Introduce the problem before asking the reader to carry specialist terms.
- Write for a curious adult: plain without becoming cute, vague, or patronizing.
- Use short declarative headings and explain symbols nearby.
- Separate what is proved, what is finite evidence, and what remains open.
- Keep corrections and post-hoc caveats prominent rather than defensive.
- Never convert exploratory evidence into mechanism, causality, or SOTA copy.

## Visual tokens

- Background `#f9f8f4`; panels `#fffdf8`; primary text `#1e201d`.
- Forest `#2a5438` marks conclusions and selected guards.
- Madder `#9e3a2b` marks attacks, warnings, and the key matching.
- Powder blue `#dce9ef` with slate-blue ink `#3d6277` marks exploratory
  context, dataset metadata, and baseline comparisons.
- Violet `#65569c` marks comparison/exposure states.
- Manrope carries UI and body copy; Newsreader italic adds editorial emphasis;
  DM Mono carries numbers, labels, and exact quantities.

Typography may fall back to system sans, Georgia, and monospace if remote font
loading is unavailable. Information must remain legible without the web fonts.

## Layout and interaction

- Each named project owns a `DESIGN.md` that defines its paper-specific
  narrative, visual semantics, interactions, evidence hierarchy, and claim
  boundaries. This root file defines the shared family resemblance.
- Each paper is a complete problem-to-result reading experience and must not
  depend on its sibling site being deployed beside it.
- The opening order is result hook, problem, minimum vocabulary, visual
  argument, evidence boundary, and what remains unknown.
- Maximum content width is 1160 px with generous vertical rhythm.
- The graph story is a two-column stage/panel above 900 px and a single column
  below it.
- Proof steps are directly selectable. Timed playback is optional and must be
  pausable; `prefers-reduced-motion` suppresses transition duration.
- Guard, attack, and exposed states use both color and accompanying legend/copy.
- Evidence counts appear as exact, visually grouped quantities.
- On phone widths, navigation remains compact, charts stack, and no control may
  require horizontal scrolling.
- Navigation labels stay short and on one line at the supported narrow width;
  prefer a few direct links over a disclosure menu.
- Goose illustrations are optional colophon or marginal details, never the
  hero subject. They must not compete with a paper's result, problem, or
  evidence; the compact `SG` mark is sufficient when a mascot adds no meaning.

## Review standard

For material visual changes, inspect representative desktop (1440×900), compact
(1024×768), phone (390×844), and narrow (320×568) states. Exercise all four
graph steps and the biology page, check console and first-party requests, then
review representative captures directly. Gemini Flash may critique final
captures; accept only substantiated suggestions.
