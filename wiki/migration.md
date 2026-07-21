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

## Open decisions

1. **Host:** GitHub Pages vs Netlify vs Cloudflare Pages (all free-tier static).
2. **DNS cutover:** domain currently points at Google Sites; owner controls
   registrar/DNS.
3. **Elasticsearch API key scope** — verify read-only before go-live
   ([Sermon Search System](sermon-search-system.md) § Security).

## Status log

- 2026-07-20: Full site crawled into `raw/`, embeds extracted, wiki compiled.
  `site/` layer not yet started.

## Sources

- All of raw/ (crawl of 2026-07-20)
