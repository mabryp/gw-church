# Wednesday Dinner Poll

**Summary:** A weekly congregation vote on the Wednesday dinner theme — designed, not built. The recommended build is a Firestore-backed page on the existing `gw-church` Firebase project, keyed by the ISO week of the upcoming Wednesday so no weekly reset is ever needed. This page carries the design, the console setup, a draft data model and security rules, and the commands to verify project state from an authenticated machine.

## Status (as of 2026-09-05)

Nothing is built and nothing is enabled. Design only, on branch
`claude/weekly-dinner-poll-d8ftg6`.

| Item | State |
|---|---|
| Design decision (Option A vs B) | Option A recommended, owner has not confirmed |
| Web App registered on `gw-church` | **No** — the site loads no Firebase SDK today |
| Firestore database | Not created |
| Anonymous auth | Not enabled |
| App Check | Not configured |
| `firestore.rules` in repo | Drafted on this page only, not committed |
| Theme list / close time | **Owner input needed** |

Work continues from the owner's Mac, which is Firebase-authenticated; the web
session could not reach Firebase at all (see § Why this needed a local machine).

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

**Recommended: device-bound.** This repo's own precedent argues against the top
tier for congregation-facing things — quiz forms are explicitly checked for
anonymous accessibility (see [Reading Plans](reading-plans.md) and the
2026-09-01 log entries), so requiring a Google account to vote on taco night
would be a step backwards for the same audience. The realistic failure mode
here is **accidental** double-voting (a double tap; voting on a phone and again
on a laptop), not ballot stuffing — device-bound plus name de-dupe catches
exactly that. Upgrading later is a one-line auth change plus one rule.

### Weekly refresh: key by date, reset nothing

Derive the poll id from the date rather than clearing anything: the page
computes the ISO week of the **upcoming Wednesday** (e.g. `2026-W37`) and reads
and writes only under that key. A new week is a new key, so "refreshes each
week" happens with no cron job, no archiving, and no button for anyone to
forget to press. The ballot rolls over on **Thursday** — Mon/Tue/Wed vote on
this week's dinner, Thu–Sun vote on next week's.

### Option A — Firestore page on the site (recommended)

A new page under `site/` (e.g. `/wednesday-dinner`) on the Firebase project
that already hosts the site. Live tally on the page itself; no spreadsheet
access to hand out; nothing to do week to week.

### Option B — prefilled Google Form (same-week shortcut)

One permanent Form, never reset. The site page computes the week id in JS and
builds a **prefilled link** (`?usp=pp_url&entry.<id>=2026-W37`), so every
response carries its week and the responses Sheet pivots by week. No Apps
Script, no weekly clearing, no new infrastructure — the same Forms/Sheets
toolchain already used for quizzes.

Trade-offs: results live in a Sheet rather than on the site; the prefilled week
field is visible and editable; de-duplication is by name, by eye. The Form's
own "limit to 1 response" is *not* usable here — it requires Google sign-in,
and would then also require clearing responses weekly for people to vote again.

### Recommendation

Option A. It satisfies all four requirements properly and, once built, has no
recurring task at all. Option B is the right call only if a poll is wanted live
this week; migrating B → A later is straightforward since the vote records
carry the same shape.

## Data model (draft)

    polls/defaults                  # permanent; themes used when a week has no doc
      themes: ["Taco Night", "Spaghetti", "Soup & Salad", "Breakfast for Dinner"]

    polls/{weekId}                  # OPTIONAL per-week override, e.g. 2026-W37
      themes:   [...]               # overrides defaults for that week
      closesAt: <timestamp>         # optional hard deadline

    polls/{weekId}/votes/{uid}
      name:  "Jane D."
      theme: "Taco Night"
      at:    <serverTimestamp>

The vote document's **id is the uid**, so one-vote-per-voter is a property of
the data model rather than a check that can be skipped. Re-voting before close
is a plain update, so "change your mind" is free.

**Deadline trade-off, decided deliberately.** A truly zero-touch poll cannot
have a server-enforced deadline, because enforcing one requires a per-week
document with a `closesAt` — i.e. a weekly chore, the thing the whole design
avoids. So: `polls/defaults` carries no `closesAt` and the page shows the
deadline in the UI only; writing a `polls/{weekId}` doc for a given week adds a
hard, rule-enforced deadline for that week. Zero-touch by default, teeth
available when wanted. A late vote on a dinner theme is not a security problem.

## Security rules (draft — NOT yet tested)

```
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {

    // The week's own config doc if it exists, else the permanent defaults.
    function cfg(weekId) {
      return exists(/databases/$(database)/documents/polls/$(weekId))
        ? get(/databases/$(database)/documents/polls/$(weekId)).data
        : get(/databases/$(database)/documents/polls/defaults).data;
    }

    function validVote(c) {
      let d = request.resource.data;
      return d.keys().hasOnly(['name', 'theme', 'at'])
          && d.theme is string && d.theme in c.themes
          && d.name  is string && d.name.size() > 0 && d.name.size() <= 60
          && d.at == request.time
          && (!('closesAt' in c) || request.time < c.closesAt);
    }

    match /polls/{weekId} {
      allow read:  if true;
      allow write: if false;              // console / admin SDK only

      match /votes/{uid} {
        allow read: if true;
        allow create, update: if request.auth != null
                              && request.auth.uid == uid
                              && validVote(cfg(weekId));
        allow delete: if false;
      }
    }
  }
}
```

These rules were written without an emulator available and **have not been
run**. Before trusting them: `firebase emulators:start --only firestore` and
exercise both the allow and deny paths (wrong uid, theme not in the list,
oversized name, extra field, delete attempt, past `closesAt`).

Note `polls/defaults` must exist or every write is denied — create it first.

## Week id (verified 2026-09-05)

```js
const TZ = 'America/Chicago';
const NAMES = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];

function chicagoParts(d) {
  const f = new Intl.DateTimeFormat('en-CA', {
    timeZone: TZ, year:'numeric', month:'2-digit', day:'2-digit', weekday:'short' });
  const p = Object.fromEntries(f.formatToParts(d).map(x => [x.type, x.value]));
  return { y:+p.year, m:+p.month, d:+p.day, wd:p.weekday };
}

function isoWeekId(utc) {
  const t = new Date(Date.UTC(utc.getUTCFullYear(), utc.getUTCMonth(), utc.getUTCDate()));
  const dayNum = (t.getUTCDay() + 6) % 7;
  t.setUTCDate(t.getUTCDate() - dayNum + 3);          // nearest Thursday
  const isoYear = t.getUTCFullYear();
  const jan4 = new Date(Date.UTC(isoYear, 0, 4));
  const week = 1 + Math.round(((t - jan4)/86400000 - 3 + ((jan4.getUTCDay()+6)%7)) / 7);
  return `${isoYear}-W${String(week).padStart(2,'0')}`;
}

// The Wednesday this poll is about: this week's if Mon/Tue/Wed, else next week's.
function pollWednesday(now = new Date()) {
  const { y, m, d, wd } = chicagoParts(now);
  const idx = NAMES.indexOf(wd);
  const delta = idx <= 2 ? 2 - idx : 9 - idx;
  return new Date(Date.UTC(y, m - 1, d + delta));
}

function pollWeekId(now = new Date()) { return isoWeekId(pollWednesday(now)); }
```

Cross-checked against Python's `date.isocalendar()` over **1200 samples** —
400 consecutive days at three times of day each, chosen to straddle midnight in
Chicago. Zero mismatches, including both 2026 DST transitions (Mar 8, Nov 1)
and the year boundary: 2026 has 53 ISO weeks, and Thu 2026-12-31 correctly
rolls forward to `2027-W01`. Timezone is pinned to `America/Chicago` so a
traveller's browser cannot land on a different ballot.

## Console setup (owner, one-time)

All at `console.firebase.google.com/project/gw-church`. Steps 0–2 are about
five minutes; step 3 is the fiddly one and is optional to start.

### 0. Register a Web App — prerequisite

There isn't one yet, and App Check registration needs an app to attach to.

Gear → **Project settings** → **General** → *Your apps* → web icon `</>` →
nickname e.g. `gw-church site` → **do not** tick "Also set up Firebase Hosting"
(already configured, see [Migration](migration.md) § Hosting environments) →
**Register app**. Keep the `firebaseConfig` object it prints.

**That config, `apiKey` included, is not a secret** — it ships in the page
source of every Firebase web app and is safe to commit to this public repo. It
does mean the security rules and App Check are the only things actually
protecting the data. This is a different category from the deploy service
account, which lives only in the GitHub secret ([CI/CD](ci-cd.md) § Credentials)
and must never be pasted anywhere.

### 1. Firestore

**Build** → **Firestore Database** → **Create database**.

- **Production mode** (locked rules), *not* test mode — test mode opens the
  database to the whole internet for 30 days.
- Location `us-central1` (cheaper than the `nam5` multi-region). **Permanent** —
  it cannot be changed later without creating a new database.

Locked rules reject everything until ours are deployed; that is expected.

### 2. Anonymous auth

**Build** → **Authentication** → **Get started** → **Sign-in method** →
**Anonymous** → Enable → Save.

Then **Settings** → **Authorized domains** should list `gw-church.org` and
`gw-church-preprod.web.app` (Hosting domains are usually added automatically).

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

**c. Leave enforcement OFF** until the page is live and App Check → **APIs**
shows requests arriving as *Verified*. Enforcing before that is the standard
way to lock yourself out of your own database.

Two caveats. reCAPTCHA Enterprise is a Google Cloud service and **may require
the project on the Blaze plan** even inside its free tier — if that is
unwelcome, shipping without App Check is defensible here: the rules still cap
each identity at one vote, though anonymous auth lets a script mint unlimited
identities, so it does leave an open write path. And reCAPTCHA site keys are
domain-scoped while PR previews get a fresh subdomain per PR
(`gw-church-preprod--pr-7-abc123.web.app`) that the key will not cover —
harmless while enforcement is off, and another reason not to enforce early.

## Verifying from a local machine

Run from an authenticated Mac. Command names are from knowledge, not verified
here (see below); if one has been renamed, `firebase --help` will say.

```bash
git fetch origin && git checkout claude/weekly-dinner-poll-d8ftg6

# identity and project
firebase login:list
firebase projects:list
firebase use gw-church

# step 0 — which web apps exist, and their config
firebase apps:list WEB
firebase apps:sdkconfig WEB

# step 1 — does the database exist, and where
firebase firestore:databases:list
# alternative: gcloud firestore databases list --project=gw-church

# step 2 — is Anonymous auth actually on? (look for signIn.anonymous.enabled)
curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://identitytoolkit.googleapis.com/admin/v2/projects/gw-church/config" \
  | python3 -m json.tool

# step 3 — App Check enforcement state per service
curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://firebaseappcheck.googleapis.com/v1/projects/gw-church/services" \
  | python3 -m json.tool
```

A live check of Anonymous auth needing **no credential at all** — only the
public API key, so it runs from anywhere:

```bash
API_KEY=...   # from firebase apps:sdkconfig
curl -s -X POST -H 'Content-Type: application/json' -d '{"returnSecureToken":true}' \
  "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=$API_KEY"
```

An `idToken` in the response means Anonymous auth is on; `OPERATION_NOT_ALLOWED`
means it is off. Note this **creates a throwaway anonymous user** in the
project — delete it from Authentication → Users, or ignore it.

## Repo changes the build will need

Deliberately **not** made yet: `firebase.json` is path-filtered by both deploy
workflows, so editing it triggers a deploy. These belong in the feature PR, not
a wiki commit.

1. **`firebase.json`** — add a `firestore` block alongside `hosting`:

       "firestore": { "rules": "firestore.rules", "indexes": "firestore.indexes.json" }

2. **`firestore.rules`** — new file, from the draft above.

3. **Both workflows** — `.github/workflows/preview-deploy.yml` and
   `prod-deploy.yml` path-filter on `site/**` and `firebase.json` only, and use
   `FirebaseExtended/action-hosting-deploy`, which deploys **hosting only**. So
   `firestore.rules` would sit in the repo and never deploy. Needs
   `firestore.rules` added to both path filters plus a `firebase deploy --only
   firestore:rules` step using the same service account. See
   [CI/CD](ci-cd.md).

Rules are project-wide, not per-hosting-target — the `gw-church` project has one
Firestore database shared by prod and preprod, so a rules deploy from a PR
preview would affect production data. Either deploy rules only from `main`, or
namespace preprod writes under a separate collection prefix. **Unresolved.**

## Why this needed a local machine

The Claude Code web session runs in a sandboxed container whose egress proxy
returns **403 at CONNECT** for `firebase.google.com`,
`console.firebase.google.com`, `gw-church.org`, and `gw-church.web.app`.
`*.googleapis.com` *is* reachable and returns real responses — a Firestore
admin call got a genuine `401 CREDENTIALS_MISSING` — so an authenticated
session could in principle drive the admin APIs from there. It was not worth
it: `firebase login:ci` tokens and service-account JSON are long-lived and
full-access, and pasting one into a chat transcript is a poor trade for
information the console shows directly. If a future session does need it,
`gcloud auth print-access-token` is scoped and expires in about an hour.

Verified locally in that session and unaffected by the proxy: `firebase.json`
and `.firebaserc` are valid and mutually consistent (targets `prod` →
`gw-church`, `preprod` → `gw-church-preprod`), and the week-id logic above.

## Open decisions

1. **Option A or B** — owner's call.
2. **Theme list** — starting options for `polls/defaults`.
3. **Close time** — Tuesday 6pm was a placeholder; also whether a hard
   rule-enforced deadline is wanted at all (see § Data model).
4. **Blaze plan** — acceptable for reCAPTCHA Enterprise, or ship without App
   Check?
5. **Rules and preprod** — how to keep PR previews from writing to production
   poll data.

## Sources

Not compiled from `raw/` — authored 2026-09-04/05 from an owner query, this
repo's own configuration (`firebase.json`, `.firebaserc`,
`.github/workflows/*.yml`, `site/`), and [CI/CD](ci-cd.md),
[Migration](migration.md), [Reading Plans](reading-plans.md). The week-id
implementation was executed and cross-checked against Python's ISO calendar in
session; the security rules and console click-paths were not executed.
