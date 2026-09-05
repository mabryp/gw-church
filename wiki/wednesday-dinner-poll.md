# Wednesday Dinner Poll

**Summary:** A weekly congregation vote on the Wednesday dinner theme — built on a feature branch, not yet deployed or enabled. A Firestore-backed page at `/wednesday-dinner` on the existing `gw-church` Firebase project. Voting runs Sunday–Saturday for the *following* week's Wednesday, closes Saturday at midnight (announced Sunday), and is keyed by that Wednesday's date so no weekly reset is ever needed. This page carries the design, what is built and how it was verified, the console setup the owner still has to do, and how to run it locally.

## Status (as of 2026-09-05)

Repo side is complete and tested on branch `claude/weekly-dinner-poll-d8ftg6`.
Nothing is deployed and nothing is enabled on the Firebase project.

| Item | State |
|---|---|
| Design decision (Option A vs B) | Option A built, per the design's recommendation — owner has not formally confirmed |
| Page `site/wednesday-dinner/` | **Built**; verified end to end against the local emulators |
| `firestore.rules` | **Built**; 28 allow/deny cases pass in the Firestore emulator (`tests/firestore-rules/`) |
| Rules deploy workflow | **Built** (`.github/workflows/rules-deploy.yml`); has never run |
| Web App registered on `gw-church` | **No** — `firebase apps:list WEB` shows none; `firebase-config.js` holds placeholders |
| Firestore database | **Not created** — the Cloud Firestore API is not even enabled on the project |
| Anonymous auth | Not enabled |
| App Check | Not configured |
| Deploy service-account roles for rules | Not granted (see § Deploying the rules) |
| Theme list | **Decided** (owner, 2026-09-05) — 13 themes in `scripts/poll-defaults.json`, seeded by `scripts/seed-poll-defaults.sh` |
| Close time / `closesNote` | Owner input needed (optional) |

Verified 2026-09-05 from the owner's Mac (`firebase login:list` → owner
account; `firebase use` → `gw-church`).

## Requirements (owner, 2026-09-04)

1. Refreshes each week for a new vote.
2. Easy way to identify the results.
3. One vote per person.
4. Easy to manage.

## Design decisions

### One vote per person: pick a tier deliberately

Genuine one-vote-per-person requires *identifying* the voter. Everything short
of that — cookies, `localStorage`, IP checks, anonymous uids — is a speed bump,
not enforcement.

| Tier | Mechanism | Friction | Real enforcement |
|---|---|---|---|
| Honor system | Required name field, de-dupe by name in results | none | no |
| **Device-bound** | Anonymous uid + required name, one vote doc per uid | none | catches every realistic case |
| Identity-bound | Google sign-in / per-household emailed code | sign-in | yes |

**Built: device-bound.** This repo's own precedent argues against the top
tier for congregation-facing things — quiz forms are explicitly checked for
anonymous accessibility (see [Reading Plans](reading-plans.md) and the
2026-09-01 log entries), so requiring a Google account to vote on taco night
would be a step backwards for the same audience. The realistic failure mode
here is **accidental** double-voting (a double tap; voting on a phone and again
on a laptop), not ballot stuffing — device-bound plus a visible name list
catches exactly that. Upgrading later is a one-line auth change plus one rule.

### Schedule: vote a week ahead, close Saturday, announce Sunday

Owner's rule (2026-09-05): voting is **never for the Wednesday of the week
we are in**. The ballot that runs Sunday through Saturday is for the
Wednesday of the **following** week; it closes at the end of Saturday so the
winner can be announced Sunday and people have until Wednesday to prepare.
Example: Sun Sep 6 – Sat Sep 12 votes for Wed Sep 16; announced Sun Sep 13.

The close is **Saturday 11:59 pm Chicago** (`CLOSE_HOUR = 24` in the page
script — the one line to change for an earlier cutoff). The page shows a
live countdown and locks the form the moment it reaches zero.

### Weekly refresh: key by date, reset nothing

The poll key is the target Wednesday's date, `YYYY-MM-DD` (e.g.
`2026-09-16`), computed from the current Chicago date: Sunday adds 10 days,
Monday 9 … Saturday 4. The page reads and writes only under that key, so a
new week is a new key and "refreshes each week" happens with no cron job, no
archiving, and no button for anyone to forget to press. Old weeks stay in
the database as history.

### Preview traffic never touches the live tally

Firestore rules and data are project-wide — one database serves prod, preprod
and every PR preview channel. So the page picks its top-level collection by
hostname: `polls` on `gw-church.org` / `www.gw-church.org` /
`gw-church.web.app` / `gw-church.firebaseapp.com`, and `polls-preview`
everywhere else (preprod, PR previews, localhost). The rules cover both
collections identically, and the page shows a yellow "Preview copy" banner
whenever it is on the preview collection. Rules deploy from `main` only.

### Option A — Firestore page on the site (built)

A page at `/wednesday-dinner` on the Firebase project that already hosts the
site. Live tally on the page itself; no spreadsheet access to hand out;
nothing to do week to week.

### Option B — prefilled Google Form (not built)

One permanent Form, never reset, with the week id prefilled from the site so
the responses Sheet pivots by week. Kept here as the fallback if a poll is
wanted live before the Firebase setup is done; it does not give live results
on the site and de-duplicates only by eye.

## What is built

| File | Purpose |
|---|---|
| `site/wednesday-dinner/index.html` | The page, on the shared site template. ES-module script: anonymous sign-in, week id, config load, live tally via `onSnapshot`, vote / re-vote via `setDoc` on `votes/{uid}`. Remembers the voter's name in `localStorage`. |
| `site/wednesday-dinner/firebase-config.js` | The public Firebase web-app config. **Placeholders** until a Web App exists. Not a secret (see § Console setup step 0). |
| `site/css/style.css` | New `Wednesday dinner poll` section at the end. |
| `firestore.rules` | Security rules (below), including the server-side voting window. |
| `firestore.indexes.json` | Empty; required by the `firestore` block. |
| `firebase.json` | New `firestore` block (rules + indexes) and `emulators` block (auth 9099, firestore 8080, hosting 5050). |
| `.github/workflows/rules-deploy.yml` | Deploys rules + indexes when they change on `main`. |
| `tests/firestore-rules/` | 28-case rules test (`npm install && npm test`). |
| `scripts/poll-defaults.json` | The canonical default theme list (13 themes, owner-supplied 2026-09-05), a per-theme `examples` map shown under each choice, and optional `closesNote`. |
| `scripts/seed-poll-defaults.sh` | Writes that file to `polls/defaults` and `polls-preview/defaults` — `emulator` or `prod` (needs `gcloud` as the owner). Re-run whenever the list changes. |
| `.gitignore` | Emulator logs, `.firebase/`, `node_modules/`. |

Page behaviour worth knowing:

- The SDK is loaded from `www.gstatic.com/firebasejs/12.18.0` (app, auth,
  firestore modules). No build step.
- On `localhost` / `127.0.0.1` the page connects to the local emulators
  instead of the real project, so it runs fully with placeholder config.
- If neither the week doc nor `defaults` exists, the page says "The poll is
  not set up yet" rather than showing an empty form.
- A countdown box ("Voting closes Saturday, September 12 at 11:59 PM — 6
  days 4 hr 12 min left") ticks every second; under a day it shows hours,
  minutes and seconds. At zero the form locks and says to check back Sunday.
  A per-week doc's `closesAt` can only bring the close *earlier* than the
  Saturday default. `closesNote` is no longer displayed (the countdown
  replaces it) but is harmless if present.
- A returning voter (same browser, same week) sees their choice preselected
  and "You voted for X. Change your mind? Pick another theme and vote again."
- Each choice shows its `examples` text in small muted type under the theme
  name (e.g. Backyard BBQ: burgers, hot dogs, potato salad…). Missing
  entries simply show the name alone; the tally shows names only.
- Results list every voter's name under the theme they chose, so accidental
  duplicates are visible to everyone. Open decision § 5 below.
- The page is **not linked from the site nav or homepage** yet — reachable
  by URL only. Open decision § 4.

## Data model

    {coll}/defaults                 # permanent; used when a week has no doc
      themes:     [...]             # from scripts/poll-defaults.json (13 themes)
      examples:   { theme: "..." }  # optional; shown in small text under each choice
      closesNote: "..."             # optional, display only

    {coll}/{YYYY-MM-DD}             # OPTIONAL override for one Wednesday, e.g. 2026-09-16
      themes:     [...]             # replaces defaults for that week
      closesAt:   <timestamp>       # optional EARLIER deadline, rule-enforced

    {coll}/{YYYY-MM-DD}/votes/{uid}
      name:  "Jane D."
      theme: "Taco Night"
      at:    <serverTimestamp>

where `{coll}` is `polls` or `polls-preview`. The vote document's **id is the
uid**, so one-vote-per-voter is a property of the data model rather than a
check that can be skipped. Re-voting before close is a plain update, so
"change your mind" is free. Config docs are read-only from the client — edit
them in the Firebase console.

**Deadline is server-enforced with no weekly chore.** Because the key is the
Wednesday's date, the rules compute the voting window from the key itself:
Sunday of the previous week through Saturday. So every week has a hard
deadline automatically. The rules work in UTC and allow up to about six
hours of slack at each end (the page's countdown is exact; the rule is the
backstop against someone posting a vote after Saturday midnight). Votes for
any other Wednesday — last week's, the week after next, or a date that is
not a Wednesday — are rejected outright.

## Security rules (tested)

`firestore.rules` in the repo root. In words: anyone may read anything under
`polls` and `polls-preview`; nobody may write a config doc from the client;
a signed-in user may create or update **only** `{coll}/{date}/votes/{their
own uid}`, only when `date` is a real Wednesday whose voting window (the
previous Sunday through Saturday, UTC with ~6h slack) contains the request
time, only with exactly the fields `name` (1–60 chars), `theme` (must be in
the active theme list — the week's doc if it exists, else `defaults`) and
`at` (must be the server timestamp), and also before `closesAt` if the
week's doc has one. Deletes are denied. Every other collection is denied.

The 32 cases in `tests/firestore-rules/test.mjs` cover each clause from both
sides. The test computes the current ballot key with the same schedule logic
as the page, so the window cases (the Wednesday after next, last week's
Wednesday, a Thursday, a malformed key, an impossible date) stay valid
whatever day the suite runs. All pass against the Firestore emulator as of
2026-09-05.

## Poll key and close time (verified 2026-09-05)

Both live in the page script. The key needs no ISO-week arithmetic any more
(the earlier ISO-week design was cross-checked against Python over 1200
samples; that work is superseded). The Chicago calendar date comes from
`Intl.DateTimeFormat`, so a traveller's browser cannot land on a different
ballot. The Saturday-midnight close is computed as a real instant using
Chicago's UTC offset at that moment, so it is correct across both DST
changes. Confirmed live in the emulator on Saturday 2026-09-05: key
`2026-09-09`, countdown to Saturday, September 5 at 11:59 PM.

## Console setup (owner, one-time)

All at `console.firebase.google.com/project/gw-church` unless noted. Steps
0–2 are about five minutes; step 3 is the fiddly one and is optional to start.
Step 4 is what makes the rules deploy from GitHub work.

### 0. Register a Web App — prerequisite

Gear → **Project settings** → **General** → *Your apps* → web icon `</>` →
nickname e.g. `gw-church site` → **do not** tick "Also set up Firebase Hosting"
(already configured, see [Migration](migration.md) § Hosting environments) →
**Register app**. Or from the Mac:

```bash
firebase apps:create WEB "gw-church site" --project gw-church
firebase apps:sdkconfig WEB --project gw-church
```

Copy `apiKey` and `appId` from the printed config into
`site/wednesday-dinner/firebase-config.js` (commit on the feature branch).

**That config, `apiKey` included, is not a secret** — it ships in the page
source of every Firebase web app and is safe to commit to this public repo. It
does mean the security rules and App Check are the only things actually
protecting the data. This is a different category from the deploy service
account, which lives only in the GitHub secret ([CI/CD](ci-cd.md) § Credentials)
and must never be pasted anywhere.

### 1. Firestore, then seed `defaults`

**Build** → **Firestore Database** → **Create database**.

- **Production mode** (locked rules), *not* test mode — test mode opens the
  database to the whole internet for 30 days.
- Location `us-central1` (cheaper than the `nam5` multi-region). **Permanent** —
  it cannot be changed later without creating a new database.

Locked rules reject everything until ours are deployed; that is expected.

Then seed the two `defaults` documents, because the rules refuse every vote
until they exist. With `gcloud` logged in as the owner (the Mac's `gcloud` is
currently on the school account — `gcloud auth login` first):

```bash
scripts/seed-poll-defaults.sh prod
```

That writes `scripts/poll-defaults.json` to both `polls/defaults` (production)
and `polls-preview/defaults` (preprod and PR previews). The console works too:
collection `polls`, document `defaults`, field `themes` as an array of
strings, and the same again under `polls-preview`.

### 2. Anonymous auth

**Build** → **Authentication** → **Get started** → **Sign-in method** →
**Anonymous** → Enable → Save.

Then **Settings** → **Authorized domains** should list `gw-church.org` and
`gw-church-preprod.web.app` (Hosting domains are usually added automatically).
PR preview channels (`gw-church-preprod--pr-N-xxxx.web.app`) are subdomains
of `web.app`, which Firebase treats as authorized by default.

### 3. App Check — two parts, and do not enforce yet

Use the **reCAPTCHA Enterprise** provider, not reCAPTCHA v3: Google steers new
integrations to Enterprise and recommends v3 users upgrade. Both are invisible
to the voter; the first 10,000 assessments/month are free.

**a. Create the key** in Google Cloud, not Firebase: `console.cloud.google.com`
→ **Security** → **reCAPTCHA** → **Create key** → platform **Website**, type
**score-based** (no image challenge) → domains `gw-church.org`,
`www.gw-church.org`, `gw-church.web.app`, `gw-church-preprod.web.app` → copy the
**site key** (also public, also safe to commit).

**b. Attach it:** Firebase → **Build** → **App Check** → **Apps** → the web app
→ **reCAPTCHA Enterprise** → paste the site key. Default 1-hour TTL is fine.
The page does not load the App Check SDK yet — that is a small follow-up once
a key exists.

**c. Leave enforcement OFF** until the page is live and App Check → **APIs**
shows requests arriving as *Verified*. Enforcing before that is the standard
way to lock yourself out of your own database.

Two caveats. reCAPTCHA Enterprise is a Google Cloud service and **may require
the project on the Blaze plan** even inside its free tier — if that is
unwelcome, shipping without App Check is defensible here: the rules still cap
each identity at one vote, though anonymous auth lets a script mint unlimited
identities, so it does leave an open write path. And reCAPTCHA site keys are
domain-scoped while PR previews get a fresh subdomain per PR that the key will
not cover — harmless while enforcement is off, and another reason not to
enforce early.

### 4. Grant the deploy service account rules permissions

The hosting deploys use `github-action-hosting@gw-church.iam.gserviceaccount.com`
with hosting-only roles ([CI/CD](ci-cd.md) § Credentials). Deploying rules
needs more. From a `gcloud` session authenticated as the owner on `gw-church`:

```bash
for ROLE in roles/firebaserules.admin roles/datastore.viewer; do
  gcloud projects add-iam-policy-binding gw-church \
    --member=serviceAccount:github-action-hosting@gw-church.iam.gserviceaccount.com \
    --role=$ROLE
done
```

Unverified: these two roles are the documented minimum for
`firebase deploy --only firestore`, but the workflow has never run. If it
fails on a permission, the error names the missing one. Note the owner's
`gcloud` on the Mac is currently logged in as the school account with a
different active project — use `gcloud auth login` / `--account` first.

## Deploying the rules

`.github/workflows/rules-deploy.yml` runs `firebase deploy --only firestore`
on any push to `main` that touches `firestore.rules` or
`firestore.indexes.json`. It is a separate workflow from the hosting deploys
so a rules failure never blocks or rolls back a site deploy, and it does not
run on PRs because rules are project-wide.

**First-time bootstrap problem:** the page cannot accept votes anywhere —
including on a PR preview channel — until rules exist in the project, but
rules only deploy on merge to `main`. Resolve it once, from the Mac, after
steps 0–1 above:

```bash
firebase deploy --only firestore --project gw-church
```

This is the CLAUDE.md manual-CLI fallback and is fine here: it deploys rules,
not the site, and the rules file is the one on the branch that will be merged.

## Local development

```bash
# once: a Java runtime for the Firestore emulator. On the owner's Mac Homebrew
# openjdk is installed but not on PATH: /opt/homebrew/opt/openjdk/bin
PATH="/opt/homebrew/opt/openjdk/bin:$PATH" firebase emulators:start --only auth,firestore,hosting
```

Hosting serves on **5050** (5000 is taken by macOS AirPlay Receiver on the
owner's Mac); the preprod hosting config gets the next free port. Auth is on
9099, Firestore on 8080. The emulator starts empty, so seed the
defaults docs (the script uses the emulator's `owner` bearer token, which
bypasses rules — emulator only):

```bash
scripts/seed-poll-defaults.sh emulator
```

then open http://localhost:5050/wednesday-dinner. The `.claude/launch.json`
entry `firebase-emulators` does the same for agent sessions. Rules tests:
`cd tests/firestore-rules && npm install && npm test` (the emulator must not
already be running on 8080).

**Verified 2026-09-05** in Chromium against the emulators: page loads with no
console errors; a vote appears in the tally with the voter's name; re-voting
moves the vote rather than adding one; a second voter written directly to the
emulator appears live without reload; after reload the returning voter's theme
is preselected, name prefilled, and the "You voted for…" status shown.

## Open decisions (owner)

1. **`closesNote`** — optional display-only text such as "Voting closes
   Tuesday at 6 pm."; add it to `scripts/poll-defaults.json` and re-seed.
   (Theme list decided 2026-09-05: Backyard BBQ, Mexican, Breakfast, Asian,
   Italian, Soups / Chili / Stew, Southern Comfort, Casserole Night, Taco
   Bar, Sandwich Night, International Night, Vegan, Potluck / Mystery
   Surprise Dinner — capitalisation and separators are the agent's
   normalisation of the owner's list. The owner supplied the example dishes
   for Backyard BBQ and Southern Comfort and asked that International Night
   cover Nigerian, Chamorro (Guam), Filipino and Turkish food; the other
   eleven example lines are the agent's drafts, edit freely in the JSON.)
2. **Close time** — built as Saturday 11:59 pm. Say if it should be earlier
   (e.g. 6 pm); it is one constant in the page plus the rule's slack.
3. **Blaze plan / App Check** — acceptable for reCAPTCHA Enterprise, or ship
   without App Check?
4. **Where the page lives in the nav** — currently URL-only. Options: a
   "Wednesday Dinner" item under Connect, a link card on the homepage, or a
   new top-level item. Nav changes touch every page, so it was left out of
   the feature PR.
5. **Voter names on the page** — shown today under each theme so duplicates
   are visible. Could show counts only, or names only to the owner.

## Sources

Not compiled from `raw/` — authored 2026-09-04/05 from owner queries, this
repo's own configuration (`firebase.json`, `.firebaserc`,
`.github/workflows/*.yml`, `site/`), and [CI/CD](ci-cd.md),
[Migration](migration.md), [Reading Plans](reading-plans.md). The week-id
implementation was cross-checked against Python's ISO calendar; the rules were
run through `tests/firestore-rules/` in the Firestore emulator; the page was
driven in Chromium against the emulators (all 2026-09-05). Console click-paths
and the IAM roles for the rules deploy remain from knowledge, not executed.
