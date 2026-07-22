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

## [2026-07-20] site | Deployed to Firebase Hosting
Owner had already created Firebase project `gw-church` and logged in the CLI.
Linked the repo via `.firebaserc` (no `firebase init` needed — firebase.json
already present) and deployed 20 files. Live at https://gw-church.web.app.
Verified redirects (/home → /, /social_media → /connect) and 200s on content
pages and embeds. Remaining for owner: add gw-church.org as custom domain in
Firebase console, update DNS, disconnect Google Sites from the domain; verify
Elasticsearch API key is read-only.

## [2026-07-20] site | Standardized reading plan design
Rebuilt the Matthew and Mark plan documents on a single shared template
(shared `reading-plan.css`, identical markup): brand hero, print button,
intro, uniform week cards, OT-connections box, Three C's section. Matthew
keeps quiz buttons and "why these matter" notes; Mark keeps weekly summaries.
Content preserved verbatim; fixed Matthew's footer (Mark is weeks 15–21, not
15–20). Verified in preview (14+7 weeks, 8 active quizzes) and deployed.
Originals untouched in raw/embeds/. Wiki: reading-plans.md updated.

## [2026-07-21] site | Built and linked Week 11 & 12 quizzes
Discovered the owner's existing quiz system in Google Drive (gospel_quiz sheet
with bound "Quiz Builder" Apps Script; questions existed for W11/W12 but no
forms). Drove the owner's Chrome (with permission) to run Validate + "Build
quiz by ID" for W11 and W12, producing two auto-graded Google Forms. Captured
their published /viewform URLs, wired them into the Matthew plan's
data-quiz-url slots, verified 10 active quiz buttons in preview, deployed.
Weeks 9/10/13/14 await questions from the owner. Wiki: reading-plans.md
documents the quiz system and repeat procedure.

## [2026-07-21] query | Sermon PDF ownership
Owner asked whose account holds the study-section PDFs. Queried
sermon_notes_v3 (213 docs with file_url) and sampled Drive metadata: all PDFs
are owned by [owner school-domain account] (school Workspace domain), not the
personal gmail that owns everything else. Filed as a dependency/risk note in
sermon-search-system.md.

## [2026-07-21] site | Pushed repo to GitHub
Created private repo https://github.com/mabryp/gw-church (owner's mabryp
account) and pushed main. The wiki, raw sources, and site now have an offsite
backup; future commits should be pushed. Also mapped current DNS for the
cutover: apex A 198.185.159.145 (Squarespace forwarding, apex → www),
www CNAME ghs.googlehosted.com (Google Sites), nameservers
ns-cloud-c*.googledomains.com (Google Cloud DNS / legacy Google Domains,
now managed via Squarespace).

## [2026-07-22] site | DNS cutover complete — gw-church.org live on Firebase
Walked the owner through the cutover: diagnosed the initial ACME 403 (old
Squarespace A records still in place), then a Host-field typo that put the
TXT/A records at gw-church.org.gw-church.org, then a 4-hour TTL wait on the
old records. Set a monitor on Firebase's edge; cert for gw-church.org issued
and verified: all pages 200 over HTTPS on the custom domain, correct content,
redirects working. Remaining: www cert (needs its own console entry),
unassigning the domain from the old Google Site. migration.md updated with a
DNS reference section.

## [2026-07-22] site | www live — DNS migration finished
Owner added the www custom-domain entry in the Firebase console and swapped
the www record to the desired CNAME (gw-church.web.app). Confirmed via the
Hosting REST API that validation was already passing (the interim A record
also pointed at Firebase, so no TTL exposure), monitored the edge, and the
cert issued (CN=www.gw-church.org). Verified both hostnames serve the site
with correct titles and redirects. Only the Google Sites domain unassignment
remains. Next up: ingest raw/Mark_Quiz_Bank_Template.xlsx and build the Mark
quizzes.

## [2026-07-22] site | Embeds now auto-size — whole page scrolls
Owner flagged that reading plans scrolled inside their frame (a Google Sites
leftover feel). Added a same-origin auto-height script to the four embed
wrapper pages (both reading plans, Charley's Notes, Search Sermons): the
iframe now sizes to its content (ResizeObserver keeps it in sync as search
results change), and .embed-frame.tall lost its border/box so content flows
as part of the page. Verified in preview (Matthew 7198px tall, no inner
scroll; search page resizes with results) and deployed. Fixed-height frames
remain only for the cross-origin calendar/map embeds on Home.
