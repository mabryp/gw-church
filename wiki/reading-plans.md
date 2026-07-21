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

## Standardized template (2026-07-20)

On the migrated site both plans were rebuilt on one shared template
(`site/embeds/reading-plan.css` + identical markup structure), replacing the
two divergent original designs. Unified features: navy/lime brand hero with
meta pills, print button + print styles, "How to Use This Plan" intro, week
cards (number badge / title / dates / five day cards), lime OT-connections box,
and the "Three C's of Reading" section — now on both plans. Matthew keeps its
quiz buttons (10 live Google Form links; weeks 9, 10, 13, 14 activate when a
URL is added to `data-quiz-url`) and its italic "why these matter" OT notes;
Mark keeps its weekly summary paragraphs.

### Quiz system (discovered in owner's Google Drive, 2026-07-21)

Quizzes are managed by the `gospel_quiz` Google Sheet
(id `1IHJE85YwPSAOf2GkK6-Z0a9e2L4aA1_dnOj1KIUeqVA`): a `questions` tab in a
rich CSV schema (quiz_id W<n>, 4 answer choices, correct answer, passages,
points 1–3 by difficulty) and a bound Apps Script with a **Quiz Builder** menu
("Build quiz by ID" prompts for e.g. `W11`, creates an auto-graded Form named
"Week n — Matthew … (Topic)" in Drive, shows its URL in a dialog; a `quizes`
registry tab exists but the script does not populate it — URLs must be
captured from the dialog or from the form's /viewform redirect).
2026-07-21: built W11 and W12 forms this way and linked them on the site.
Questions for W9, W10, W13, W14 do not exist yet — owner will supply; after
appending them to the sheet, repeat: Quiz Builder → Build quiz by ID → wire
URL into `site/embeds/matthew-reading-plan.html` → deploy. All readings, dates, titles, and prose carried over
verbatim. One correction: Matthew's footer said Mark would be "Weeks 15–20";
Mark actually runs weeks 15–21, so the footer now says 15–21. Original designs
remain in `raw/embeds/`. Luke and John should use this same template when
their plans are written.

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
