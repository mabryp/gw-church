# Reading Plans (Gospel Reading Plan, Year One)

**Summary:** A 2026 congregation-wide Gospel reading program published as custom HTML embeds — Matthew (spring), Mark (summer), and Luke (fall 2026) are live on the shared template; Luke's 108-question quiz bank is drafted in the repo but its Google Forms are not yet built; John has no content yet.

## Program shape

Branded "Gospel Reading Plan · Year One". Weekday (Mon–Fri) readings organized
into weekly cards, each with passage assignments per day and an optional
Old Testament sidebar ("why this matters" commentary). Styled, printable
(Print / Save as PDF button), self-contained HTML documents.

| Plan | Schedule | Status |
|---|---|---|
| Matthew | 14 weeks, April 6 – July 10, 2026 | Complete (ran spring 2026); includes 8 weekly quiz links (Google Forms) |
| Mark | July 13 – August 28, 2026 (7 weeks) | **Currently running** (as of 2026-07-20); no quiz links yet |
| Luke | August 31 – October 30, 2026 (9 weeks, weeks 22–30) | Page live (merged 2026-08-30). Quiz bank drafted (`luke_quiz_bank.csv`, W22–W30); forms not built, no quiz links yet |
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
URL into the MARK/MATTHEW data in `tools/build_plans.py` → rebuild → deploy.

2026-07-22: **All 7 Mark quizzes live.** The LLM drafted the 84-question bank
(repo: `mark_quiz_bank.csv`, owner-reviewed), loaded it into the sheet's
questions tab via a temporary Firebase-hosted copy + IMPORTDATA + paste-values
(byte-exact, checksum-verified; the Sheets import picker is unreachable to
automation), ran Build quiz by ID for W15–W21 (W21 needed a retry after an
Apps Script "exceeded maximum execution time"), validated every form (title +
12 questions + anonymous 200), and wired the URLs through build_plans.py.
Quiz URLs now live ONLY in tools/build_plans.py — edit there and rebuild,
never in the generated HTML (hand-edits get clobbered on rebuild).

### Results shown to quiz takers (fixed 2026-07-22)

The Quiz Builder script creates forms with "Release grades: Later, after
manual review" and all respondent-visibility settings off, so submitters saw
nothing after submitting. Google exposes these settings in NO API (Forms API
and Apps Script both lack them) — they are UI-only. All 17 live quiz forms
(W1–W8, W11–W12, W15–W21) were fixed by hand in the Forms editor: Release
grades = Immediately after each submission; Missed questions, Correct
answers, and Point values all visible. (W1–W8 already had
immediately+missed-questions set — presumably manually — and needed only the
last two toggles.) **After any future Quiz Builder run, open the new form's
Settings and make these same changes** — the script cannot do it. All readings, dates, titles, and prose carried over
verbatim. One correction: Matthew's footer said Mark would be "Weeks 15–20";
Mark actually runs weeks 15–21, so the footer now says 15–21. Original designs
remain in `raw/embeds/`. Luke and John should use this same template when
their plans are written.

## Luke schedule (from Gateway Public Calendar, retrieved 2026-08-30)

Joy Dumont (joy.dumont@gw-school.org) entered the Luke plan as all-day events
on the Gateway Public Calendar, most of them the night of 2026-08-29/30
("Gospel Reading Plan - Four Portraits, One Christ"). Weekday cadence,
Mon Aug 31 – Fri Oct 30, 2026; following Mark (weeks 15–21) these are
presumably weeks 22–30. Bridge events during Mark's final week: Aug 25
Luke 1:1-2, Aug 26 Luke 1:3-4, Aug 28 "Reflective Reading" (a Mark→Luke
transition blurb).

| Week (Mon–Fri) | Readings |
|---|---|
| Aug 31 – Sep 4 | 1:1-38 · 1:39-80 · 2:1-20 · 2:21-40 · 2:41-52 (Fri OT: Isaiah 40, 1 Samuel 2, Micah 5) |
| Sep 7 – 11 | 3 · 4:1-30 · 4:31-44 · 4:16-21 · Review 4:16-21 (Fri OT: Isaiah 61, Psalm 2) |
| Sep 14 – 18 | 5 · 6:1-26 · 6:27-49 · *(Thu–Fri empty)* |
| Sep 21 – 25 | 7 · 8:1-25 · 8:26-56 · Review · Review |
| Sep 28 – Oct 2 | 9:1-36 · 9:37-62 · Reflection · *(Thu–Fri empty)* |
| Oct 5 – 9 | 10 · 11 · 12:1-34 · 12:35-59 · *(Fri empty)* |
| Oct 12 – 16 | 13 · 14 · 15 · *(Thu–Fri empty)* |
| Oct 19 – 23 | 16 · 17 · 18 · 19:1-27 · 19:28-48 |
| Oct 26 – 30 | 20-21 · 22 · 23 · 24:1-35 · 24:36-53 |

The empty weekday slots may be intentional catch-up days or simply not yet
entered (the events were still being added when retrieved). No quiz links yet.

2026-08-30: the Luke page was built from this schedule on the shared template —
`LUKE` data added to `tools/build_plans.py` (which now also emits
`site/embeds/luke-reading-plan.html` and computes its repo root from the
script location instead of a hardcoded path), and
`site/reading-plan/luke-reading-plan/index.html` rewritten as an iframe
wrapper cloned from Matthew's. Week titles and summary paragraphs are
LLM-written in the Mark style (owner reviews on preprod); the calendar's
open weekday slots render as "Catch-Up / Reflection" day cells. This
supersedes PR #4's interim "coming soon" hero
(`site/embeds/temp-luke-reading-plan.html`), which was never merged.

### Luke quiz bank (owner-supplied 2026-09-01)

The owner supplied the Luke questions directly:
`raw/luke_quizzes_weeks_22-30.csv` — 90 questions, 10 per week for W22–W30,
in a simple 9-column format (Week, Passage, Question, Option A–D, Correct
Answer as a letter, Scripture Reference). Its week/passage groupings match the
`LUKE` weeks in `tools/build_plans.py` exactly. This replaced an earlier
108-question LLM draft, which was discarded rather than merged.

`luke_quiz_bank.csv` is the machine conversion of that source into the
23-column `gospel_quiz` schema. Question text, all four options, and the
answer key are carried over verbatim (verified row by row); everything else is
derived mechanically: `quiz_id` W<week>, `quiz_title` in the Mark convention,
`reference_id` W<week>-Q01…Q10, `topic` = the week's theme, `passages` = the
source's Scripture Reference, `tags` = chapter refs.

Three fields the source does not carry were **left blank rather than
invented** — `learning_objective`, `explanation`, `common_misconception`. In
the Matthew and Mark forms `explanation` is the feedback a taker sees after
answering, so as loaded today Luke's quizzes will grade but explain nothing.
Two more had no source value and were given a uniform setting: `difficulty`
medium / `points` 2 (20 points per quiz), and `question_type` recall.

`shuffle_answers` is **TRUE for Luke**, deliberately departing from Mark's
FALSE — see the lint finding below.

### Lint finding: answer-position bias in the Mark quizzes (2026-09-01)

In `mark_quiz_bank.csv`, 77 of 84 correct answers sit in position B (A: 1,
C: 6, D: 0), and every row sets `shuffle_answers` FALSE. If the Quiz Builder
honors that flag, a taker who always picks B scores about 92% on the seven
live Mark quizzes without reading. Not repaired here — the forms are already
built and live, and re-keying them is the owner's call. Matthew's bank is not
in the repo, so it could not be checked and may have the same problem. The
owner-supplied Luke questions are well distributed by comparison (A 27 / B 24
/ C 20 / D 19), and are loaded with `shuffle_answers` TRUE.

**Remaining steps require the owner's personal Google account** — the
`gospel_quiz` sheet is not visible to `phillip.mabry@gw-school.org`, the Drive
account agent sessions connect through (re-confirmed 2026-09-01). The
sequence:

1. Append `luke_quiz_bank.csv` to the `gospel_quiz` sheet's `questions` tab.
2. Quiz Builder → Build quiz by ID for W22 … W30 (nine runs; expect the
   occasional "exceeded maximum execution time" retry seen with W21).
3. For each new form, open Settings and set Release grades = Immediately after
   each submission, and turn on Missed questions, Correct answers, and Point
   values — these are UI-only, per the section above.
4. Paste the nine form URLs into the `LUKE` week tuples in
   `tools/build_plans.py` (last element of each tuple), rerun the script, and
   open a PR so the preview deploy can be reviewed.

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
- Gateway Public Calendar ("Reading Plan Luke …" events by Joy Dumont),
  retrieved via the owner's Google Calendar, 2026-08-30 — not in `raw/`.
