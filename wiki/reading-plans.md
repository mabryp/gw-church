# Reading Plans (Gospel Reading Plan, Year One)

**Summary:** A 2026 congregation-wide Gospel reading program published as custom HTML embeds — Matthew (spring) and Mark (summer) are live; Luke and John pages exist but are empty placeholders.

## Program shape

Branded "Gospel Reading Plan · Year One". Weekday (Mon–Fri) readings organized
into weekly cards, each with passage assignments per day and an optional
Old Testament sidebar ("why this matters" commentary). Styled, printable
(Print / Save as PDF button), self-contained HTML documents.

| Plan | Schedule | Status |
|---|---|---|
| Matthew | 14 weeks, April 6 – July 10, 2026 | Complete (ran spring 2026); includes 8 weekly quiz links (Google Forms) |
| Mark | July 13 – August 28, 2026 (7 weeks) | **Currently running** (as of 2026-07-20); no quiz links yet |
| Luke | — | Placeholder page, no content |
| John | — | Placeholder page, no content |

## Mechanics

- Quizzes are Google Forms opened from "quiz" buttons; buttons are hidden until
  a URL is present (JS toggles `.quiz-btn.active`), so quizzes appear to be
  added week by week.
- Embed sources extracted to `raw/embeds/reading-plan_{matthew,mark}-reading-plan_embed.html`.

## Migration implications

Like the [Sermon Search System](sermon-search-system.md), these are
self-contained HTML docs with no Google Sites dependency — they port directly.
Luke and John pages should either get "coming soon" content or be left
unpublished on the new site until their plans are written (site owner's call;
Mark ends Aug 28, so Luke is presumably needed by ~Aug 31, 2026).

## Sources

- raw/embeds/reading-plan_matthew-reading-plan_embed.html
- raw/embeds/reading-plan_mark-reading-plan_embed.html
- raw/reading-plan_luke-reading-plan.html (placeholder)
- raw/reading-plan_john-reading-plan.html (placeholder)
