# Wednesday Dinner Poll (design)

**Summary:** Design options for a weekly congregation poll on the Wednesday dinner theme — requirements are a fresh vote each week, readable results, one vote per person, and low management overhead; the recommended build is a Firestore-backed page on the existing Firebase project, keyed by ISO week so nothing needs resetting.

## Requirements (owner, 2026-09-04)

1. Refreshes each week for a new vote.
2. Easy way to identify the results.
3. One vote per person.
4. Easy to manage.

## The constraint that shapes everything

Genuine one-vote-per-person requires *identifying* the voter. Everything short
of that — cookies, `localStorage`, IP checks, anonymous uids — is a speed bump,
not enforcement. So there are three tiers:

| Tier | Mechanism | Friction | Real enforcement |
|---|---|---|---|
| Honor system | Required name field, de-dupe by name in results | none | no |
| **Device-bound** | Anonymous uid (or `localStorage`) + required name, one vote doc per uid | none | catches every realistic case |
| Identity-bound | Google sign-in / per-household emailed code | sign-in required | yes |

This repo's own precedent argues against the top tier for congregation-facing
things: the quiz forms are explicitly checked for anonymous accessibility (see
[Reading Plans](reading-plans.md) and the 2026-09-01 log entries). Requiring a
Google account to vote on taco night would be a step backwards for the same
audience. The realistic failure mode here is **accidental** double-voting
(double-tap; voting on phone then laptop), not ballot stuffing — device-bound +
name de-dupe catches exactly that.

## The trick that removes the weekly chore

Derive the poll id from the date rather than resetting anything: the page
computes the ISO week of the upcoming Wednesday (e.g. `2026-W37`) and reads and
writes only under that key. A new week is a new key, so "refreshes each week"
happens with no cron job, no archiving, and no button for anyone to forget to
press. This applies to both options below.

## Option A — Firestore page on the site (recommended)

A new page under `site/` (e.g. `/wednesday-dinner`) using the Firebase project
that already hosts the site.

**Data model**

    polls/{weekId}                  # e.g. 2026-W37 — optional override doc
      themes: ["Taco Night", "Spaghetti", "Soup & Salad", "Breakfast for Dinner"]
      closesAt: <timestamp>         # e.g. Tuesday 6pm
    polls/{weekId}/votes/{uid}
      name:  "Jane D."
      theme: "Taco Night"
      at:    <serverTimestamp>

The vote document's **id is the uid**, so one-vote-per-voter is a property of
the data model rather than a check that can be skipped. Re-voting before close
is a plain update, so "change your mind" is free.

**Auth:** Firebase **Anonymous** auth — invisible, no sign-in UI, gives a
per-browser uid that security rules can enforce against. Swapping it for Google
sign-in later is a one-line change plus one rule, if the owner ever wants hard
enforcement.

**Rules** enforce: uid matches the doc id, `theme` is in the week's allowed
list, `name` is non-empty and length-capped, `request.time < closesAt`, and no
deletes. Add **App Check** (reCAPTCHA v3) so the open write path can't be
scripted.

**Results:** a section on the same page reads the week's `votes` subcollection
and tallies client-side — trivial at congregation scale (tens of votes). Live
bar chart, plus previous weeks' winners. No Sheet access to hand out; anyone
can bookmark the page.

**Managing the options:** default theme list lives in the page code and is used
whenever no `polls/{weekId}` doc exists, so it runs untouched forever; writing
an override doc (small admin page, or the Firebase console) customises any
given week. That keeps week-to-week changes out of the PR workflow, which
matters for collaborators new to git (see [Git Basics](git-basics.md)).

**Costs:** Firestore + Anonymous auth + App Check must be enabled once in the
Firebase console (owner, ~15 min). A `firestore.rules` file is a *new* deploy
surface — the current workflows deploy hosting only and path-filter on
`site/**` and `firebase.json` ([CI/CD](ci-cd.md)), so they need a
`firebase deploy --only firestore:rules` step and `firestore.rules` added to
their path filters. Well inside the free tier.

## Option B — prefilled Google Form (same-week shortcut)

One permanent Form, never reset. The site page computes the week id in JS and
builds a **prefilled link** (`?usp=pp_url&entry.<id>=2026-W37`), so every
response carries its week and the responses Sheet pivots by week. No Apps
Script, no weekly clearing, no new infrastructure — the same Forms/Sheets
toolchain already used for quizzes.

Trade-offs: results live in a Sheet rather than on the site; the prefilled week
field is visible and editable; de-duplication is by name, by eye. Form's own
"limit to 1 response" is *not* usable here — it requires Google sign-in, and it
would then also require clearing responses weekly to let people vote again.

## Recommendation

Option A. It satisfies all four requirements properly and, once built, has no
recurring task at all — the weekly refresh is arithmetic on the date, and
results are a public page rather than a spreadsheet someone has to be granted.
Option B is the right call only if a poll is wanted live this week; migrating
B → A later is straightforward since the vote records carry the same shape.

Not yet built or decided as of 2026-09-04 — this page records the analysis, not
a shipped feature.

## Sources

Not compiled from `raw/` — authored 2026-09-04 in response to an owner query,
from this repo's own configuration (`firebase.json`, `.firebaserc`,
`.github/workflows/*.yml`, `site/`) and [CI/CD](ci-cd.md),
[Reading Plans](reading-plans.md).
