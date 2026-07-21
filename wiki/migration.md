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

## Open items

1. **DNS cutover:** point gw-church.org at Firebase Hosting after deploy
   (owner controls registrar; also disconnect the domain from Google Sites).
2. **Elasticsearch API key scope** — verify read-only before go-live
   ([Sermon Search System](sermon-search-system.md) § Security). Confirmed the
   cluster accepts cross-origin requests, so the embeds work from any host.
3. Signed Google image URLs expire — images were captured to `site/assets/`
   (logo, pastor photo, school photo); any future images must be saved as
   files, not hotlinked.

## Status log

- 2026-07-20: Full site crawled into `raw/`, embeds extracted, wiki compiled.
- 2026-07-20: `site/` built — all 12 pages, preserved URL paths
  (`/about/what-we-believe` etc. as directories), embeds served from
  `site/embeds/` in iframes, Luke/John get "coming soon" content. Verified in
  local preview: home, pastor page, Mark plan embed, sermon search (live
  Elasticsearch queries work — 177 results). Not yet deployed.

## Sources

- All of raw/ (crawl of 2026-07-20)
