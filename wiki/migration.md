# Migration (Google Sites → self-hosted)

**Summary:** Project page for moving gw-church.org off Google Sites onto a directly-editable static host; tracks what ports cleanly, what must be rebuilt, and open decisions.

## Why

Google Sites cannot round-trip: downloaded HTML is a rendered snapshot that
cannot be re-imported, and the Sites editor is the only way to change the live
site. A static self-hosted site makes the HTML directly editable (by the LLM,
per this repo's workflow).

## Portability assessment (from 2026-07-20 crawl)

**Ports unchanged:**
- [Sermon Search System](sermon-search-system.md) embeds — self-contained HTML + external Elasticsearch
- [Reading plan](reading-plans.md) embeds — self-contained HTML
- Google Calendar + Google Maps embeds on Home ([Connect Channels](connect-channels.md))

**Rebuild as static pages (content fully captured in wiki):**
- Home, About, [What We Believe](what-we-believe.md), [Our Pastor](charley.md),
  [Gateway Christian School](gateway-christian-school.md), Connect

**Assets still to fetch:** images (pastor photo, any hero images) — not yet
downloaded from the crawl.

**Fix during migration:** broken `/social_media` link; empty Luke/John pages
(see [Site Structure](site-structure.md) lint findings). Preserve URL paths so
existing links keep working.

## Decisions

1. **Host: Firebase Hosting** (owner's choice, 2026-07-20). Config in
   `firebase.json`: serves `site/`, cleanUrls, 301s for `/home` → `/` and the
   previously-broken `/social_media` → `/connect`. Firebase CLI is installed
   locally; project not yet created/linked (needs owner's Google account:
   `firebase login`, create project, `firebase use --add`, `firebase deploy`).
2. **Design: light refresh** (owner's choice, 2026-07-20). Same structure and
   voice; navy + lime palette taken from the church logo (`site/assets/home.png`),
   Playfair Display + Open Sans kept, sticky header, mobile hamburger nav.

## Hosting environments

Two Firebase Hosting sites in project `gw-church`, both serving `site/`,
mapped to deploy targets in `.firebaserc` / `firebase.json`:

| Target | Site | URL | Purpose |
|---|---|---|---|
| `prod` | gw-church | https://gw-church.org (and gw-church.web.app) | Production |
| `preprod` | gw-church-preprod | https://gw-church-preprod.web.app | Review changes before production |

Deploy commands (created 2026-07-22):

- Preprod only: `firebase deploy --only hosting:preprod`
- Production only: `firebase deploy --only hosting:prod`
- Both: `firebase deploy --only hosting`

Workflow: deploy to preprod, share the preprod URL for review, then deploy the
same `site/` to prod once approved. Both targets deploy the same working tree —
there is no separate preprod branch or directory.

## Open items

1. **Unassign the custom domain from the old Google Site** so it stops
   claiming gw-church.org.
3. **Elasticsearch API key scope** — verify read-only
   ([Sermon Search System](sermon-search-system.md) § Security). Confirmed the
   cluster accepts cross-origin requests, so the embeds work from any host.
4. Signed Google image URLs expire — images were captured to `site/assets/`
   (logo, pastor photo, school photo); any future images must be saved as
   files, not hotlinked.

## DNS reference (post-cutover, 2026-07-22)

Zone hosted on legacy Google Domains nameservers (ns-cloud-c*), managed via
the owner's Squarespace account. Records: `@ A 199.36.158.100` (Firebase),
`@ TXT "hosting-site=gw-church"`, `www CNAME gw-church.web.app`. Gotchas hit during
cutover, for next time: the DNS editor's Host field is zone-relative (use `@`,
not the full domain — full domain creates doubled names like
gw-church.org.gw-church.org); the old Squarespace records carried 4-hour TTLs,
so validation lagged the fix by hours; Squarespace's domain-forwarding feature
generates parking A records (198.185.159.x / 198.49.23.x) and serves a
"Coming Soon" page with its own cert — which can masquerade as a working site
in cached-DNS checks.

## Status log

- 2026-07-20: Full site crawled into `raw/`, embeds extracted, wiki compiled.
- 2026-07-20: `site/` built — all 12 pages, preserved URL paths
  (`/about/what-we-believe` etc. as directories), embeds served from
  `site/embeds/` in iframes, Luke/John get "coming soon" content. Verified in
  local preview: home, pastor page, Mark plan embed, sermon search (live
  Elasticsearch queries work — 177 results).
- 2026-07-20: **Deployed** to Firebase Hosting project `gw-church` →
  https://gw-church.web.app. Verified live: homepage renders, `/home` and
  `/social_media` 301s work, content pages and embeds serve 200.
- 2026-07-22: **DNS cutover complete.** https://gw-church.org serves the new
  site with a valid Firebase-issued certificate — verified end-to-end (all
  pages 200, correct content, redirects).
- 2026-07-22: **www live.** Owner added the www custom-domain entry and CNAME;
  cert issued (CN=www.gw-church.org, expires 2026-10-20). Both hostnames
  verified serving the site with working redirects. DNS migration finished.
- 2026-07-22: **Preprod environment created** — second hosting site
  `gw-church-preprod` with prod/preprod deploy targets (see Hosting
  environments above). Initial deploy verified at
  https://gw-church-preprod.web.app.

## Sources

- All of raw/ (crawl of 2026-07-20)
