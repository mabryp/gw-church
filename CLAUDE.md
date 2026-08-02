# Gateway Site — LLM Wiki

This repository follows Karpathy's LLM Wiki pattern. The human curates sources and
asks questions; the LLM owns the wiki's structure, content, and maintenance.

Project purpose: migrate the Gateway site off Google Sites. The wiki compiles the
site's content into a durable knowledge base; a `site/` layer (added during
migration) will hold the new hosted HTML, generated from and cross-checked against
the wiki.

## Layers

- `raw/` — immutable sources. Google Sites downloads, PDFs, images, notes. The LLM
  reads these but NEVER edits, renames, or deletes anything here.
- `wiki/` — markdown pages written and maintained entirely by the LLM. One page per
  entity/concept/site-page. The human does not hand-edit these.
- `CLAUDE.md` — this schema file. Defines structure and workflows.
- `wiki/index.md` — catalog of every wiki page with a one-line summary, grouped by
  category. Updated on every ingest.
- `log.md` — append-only chronological record of all operations.
- `site/` — (future) the new hosted site's HTML/CSS. LLM-edited directly.

## Conventions

- Wiki page filenames: `kebab-case.md`, named for the entity or page they cover.
- Cross-link between wiki pages with relative markdown links: `[Page Name](page-name.md)`.
  Link liberally; a link's target should exist or be created in the same ingest.
- Every wiki page starts with a one-line **Summary** and ends with a **Sources**
  section citing the `raw/` files (with paths) it was compiled from.
- Never duplicate a fact across pages when a cross-link will do.

## Operations

### Ingest
When a new file lands in `raw/`:
1. Read it fully.
2. Create or update the relevant wiki pages (typically several per source).
3. Update `wiki/index.md`.
4. Append a log entry.

### Query
Answer questions from the wiki first, citing pages; fall back to `raw/` when the
wiki is silent. If a query surfaces something worth keeping, file it back into the
wiki as a page or addition, and log it.

### Deploy

Two Firebase Hosting targets: `preprod` (gw-church-preprod.web.app) and `prod`
(gw-church.org). **All site changes are reviewed on preprod FIRST; prod only
after the owner's explicit acceptance.** Full pipeline details:
[wiki/ci-cd.md](wiki/ci-cd.md).

**Primary path — git automation (PRs):**

1. Make site changes on a feature branch; push and open a PR to `main`.
2. GitHub Actions deploys any PR touching `site/` or `firebase.json` to a
   temporary preview channel on the preprod site and comments the URL on the
   PR. Share that URL for review.
3. Owner acceptance = the owner merging the PR. On merge, Actions deploys
   prod (gw-church.org) and re-syncs gw-church-preprod.web.app to match main.
4. Never merge a site PR yourself — the merge IS the prod approval, and it
   belongs to the owner.

**Fallback — manual CLI (owner-run sessions only):** preprod first
(`firebase deploy --only hosting:preprod`), wait for acceptance, then
`firebase deploy --only hosting:prod`. Prefer the PR path; manual prod
deploys can drift from `main`.

The preprod-first rule holds even for "trivial" fixes, and even if asked to
"deploy" without a target (use the PR path, or deploy preprod and ask). A
direct push to `main` touching `site/` auto-deploys prod — agent sessions
must never do that. Branch protection on `main` requires 1 approving review
to merge a PR; the owner (admin) is exempt from direct-push restrictions —
that exemption is for wiki/log commits, not a prod shortcut. Log every deploy
or deploy-affecting change with the `site` prefix, noting target.

### Collaboration

The repo is hosted at github.com/mabryp/gw-church (**public** as of
2026-07-24 — never commit anything personal or secret; personal emails were
scrubbed from files and git history before publication). Multiple
developers manage the agent through this same repository; deploys need no GCP
credentials — GitHub Actions holds a Firebase service account in the repo
secret `FIREBASE_SERVICE_ACCOUNT_GW_CHURCH` (see [wiki/ci-cd.md](wiki/ci-cd.md)).

- Every agent session, whoever runs it, follows this CLAUDE.md: same wiki and
  log discipline, same deploy rules.
- `site/` and `firebase.json` changes: always feature branch + PR (triggers
  the preview deploy). Wiki/log/CLAUDE.md-only changes may be committed
  directly to `main` — the deploy workflows path-filter them out.
- `git pull` at session start and push after committing — other developers
  work against the same `main`, and an unpushed wiki is invisible to them.
- Never commit credentials. The service account key exists only in the GitHub
  secret; there is no local copy.

**Who's who** (identify the session's user by their email/GitHub login; public
repo — first names and GitHub logins only, no personal emails):

- Phillip (`mabryp`) — owner/admin. Prod acceptance (merging site PRs) is his.
- Alex (`adcast1016-cpu`) — collaborator, write access. Alex is new to git and
  to the LLM-wiki workflow. In sessions run by Alex (or when unsure who is
  running the session), work in **teaching mode**: before running git or deploy
  operations, briefly explain what the command does and why; prefer small,
  reviewable steps; define jargon (branch, commit, push, PR, merge) on first
  use; and after each operation, state what changed and where things now stand.
  Keep lessons brief — teaching supports the website work, it doesn't replace
  it; point to [wiki/git-basics.md](wiki/git-basics.md) for the primer instead
  of re-explaining at length. All CLAUDE.md rules (preprod-first, no
  self-merging site PRs) apply to every collaborator equally.

### Lint
On request (or when drift is suspected): scan for contradictions, stale claims,
orphaned pages, broken cross-links, and index mismatches. Flag findings in the log
and to the user — do not silently repair anything substantive.

## Log format

Append-only entries in `log.md`, greppable prefixes:

    ## [YYYY-MM-DD] ingest | <source name>
    ## [YYYY-MM-DD] query | <topic>
    ## [YYYY-MM-DD] lint | <scope>
    ## [YYYY-MM-DD] site | <change to site/>

One short paragraph per entry: what was done, which pages were touched.
