# Log

Append-only. Newest entries at the bottom.

## [2026-07-20] init | Repository scaffolded
Created the LLM Wiki structure per Karpathy's pattern: `raw/`, `wiki/` with
`index.md`, `CLAUDE.md` schema, and this log. Git initialized. Awaiting the
Google Sites download in `raw/` to begin ingest and migration.

## [2026-07-20] ingest | gw-church.org full crawl
Crawled all 12 pages of the live Google Site into `raw/*.html`. Discovered the
content-bearing pages hide their real content in Google Sites "custom embeds"
stored HTML-escaped in the page source; extracted 4 embed documents to
`raw/embeds/` (Matthew and Mark reading plans; Search Sermons and Charley's
Notes — both Searchkit/InstantSearch apps against Elastic Cloud, indexes
`gateway_sermons_v3` and `sermon_notes_v3`). Verified in browser that Luke and
John reading-plan pages are empty placeholders. Created 9 wiki pages
(gateway-church, charley, what-we-believe, gateway-christian-school,
connect-channels, site-structure, sermon-search-system, reading-plans,
migration) and populated the index. Lint findings recorded in site-structure:
broken /social_media homepage link, two empty pages, publicly-visible
Elasticsearch API key needing a read-only-scope check.

## [2026-07-20] site | Built site/ for Firebase Hosting
Owner chose Firebase Hosting and a light design refresh. Generated all 12 pages
as static HTML under `site/` with original URL paths preserved; navy/lime
palette from the church logo; embeds (2 reading plans, 2 search apps) copied
verbatim to `site/embeds/` and iframed. Captured logo, pastor, and school
images to `site/assets/` (source URLs are short-lived signed links). Added
`firebase.json` with redirects fixing the broken /social_media link. Verified
in local preview including live Elasticsearch search. Wiki updated:
migration.md (decisions, open items, status). Awaiting owner's Firebase
project + deploy, then DNS cutover.
