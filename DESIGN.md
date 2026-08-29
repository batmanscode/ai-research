# Design system

Last updated: 29 August 2026

## Direction

The explainer should feel like a careful research exhibit, not a generic AI
dashboard: dark paper, restrained fluorescent accents, large editorial type,
and evidence that becomes more concrete as the reader moves down the page.

## Voice

- Lead with the result in ordinary language.
- Use short declarative headings and explain symbols nearby.
- Separate what is proved, what is finite evidence, and what remains open.
- Keep corrections and post-hoc caveats prominent rather than defensive.
- Never convert exploratory evidence into mechanism, causality, or SOTA copy.

## Visual tokens

- Background `#0b0f10`; panels `#121718`; primary text `#f4f1ea`.
- Acid `#d9ff6f` marks conclusions and selected guards.
- Coral `#ff826e` marks attacks, warnings, and the key matching.
- Cyan `#74e8dc` marks the aggregate biology model.
- Violet `#ae9cff` marks comparison/exposure states.
- Manrope carries UI and body copy; Newsreader italic adds editorial emphasis;
  DM Mono carries numbers, labels, and exact quantities.

Typography may fall back to system sans, Georgia, and monospace if remote font
loading is unavailable. Information must remain legible without the web fonts.

## Layout and interaction

- Maximum content width is 1160 px with generous vertical rhythm.
- The graph story is a two-column stage/panel above 900 px and a single column
  below it.
- Proof steps are directly selectable. Timed playback is optional and must be
  pausable; `prefers-reduced-motion` suppresses transition duration.
- Guard, attack, and exposed states use both color and accompanying legend/copy.
- Evidence counts appear as exact, visually grouped quantities.
- On phone widths, navigation remains compact, charts stack, and no control may
  require horizontal scrolling.

## Review standard

For material visual changes, inspect representative desktop (1440×900), compact
(1024×768), phone (390×844), and narrow (320×568) states. Exercise all four
graph steps and the biology page, check console and first-party requests, then
review representative captures directly. Gemini Flash may critique final
captures; accept only substantiated suggestions.

