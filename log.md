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

## [2026-07-22] site | All 7 Mark quizzes built and live
Owner approved the drafted 84-question bank and asked for same-day go-live.
Loaded the questions into gospel_quiz via a temp Firebase-hosted CSV +
IMPORTDATA + paste-as-values (checksum-verified byte-exact; the import picker
iframe is unreachable to automation). Sheet validation passed (190 rows).
Drove Quiz Builder for W15–W21: two menu misfires typed into cells (caught,
reverted via undo/Escape with zero damage) and W21 hit an Apps Script
execution-time limit (clean retry succeeded). Validated all 7 forms — correct
titles, 12 questions each with passages, anonymously reachable — captured
published URLs, wired them into tools/build_plans.py, rebuilt both plans,
removed the temp CSV, deployed, and confirmed 7 active quiz buttons on the
live Mark plan. Renamed mark_quiz_bank_DRAFT.csv → mark_quiz_bank.csv.

## [2026-07-22] site | Quiz takers now see their results
Owner reported quiz submitters saw nothing after submitting. Root cause: the
Quiz Builder script creates forms set to "Release grades: Later, after manual
review" with all respondent-visibility toggles off; these settings have no
API, so all 17 live quiz forms (Matthew W1-W8/W11-W12, Mark W15-W21) were
fixed by hand in the Forms editor via Chrome: release grades → immediately,
missed questions/correct answers/point values → visible. W1-W8 were already
half-configured (immediately + missed questions) and needed only the last two
toggles. Each form's final state screenshot-verified. Repeat-procedure note
added to reading-plans.md for future builds.

## [2026-07-22] site | Our Pastor page: Chris Dumont placeholder
Owner reported Charley has retired and Chris Dumont is now lead pastor; no
photo of Chris yet. Rewrote site/about/our-pastor/index.html as honest
placeholder content: Chris Dumont named as lead pastor with a "photo coming
soon" block (new .photo-placeholder CSS rule) and TODO markers for photo/bio,
plus a Pastor Emeritus section preserving Charley's story and linking his
notes/sermon search. Updated About hub card ("Meet Pastor Chris Dumont").
Wiki synced: created chris-dumont.md; updated charley.md, gateway-church.md,
site-structure.md, index.md. Not yet deployed.

## [2026-07-22] site | Deployed Chris Dumont placeholder
Owner approved deploying the pastor-transition placeholder as-is. Ran
`firebase deploy --only hosting` (21 files, release complete); verified live
at gw-church.web.app/about/our-pastor — page shows Chris Dumont, the
photo-coming-soon block, and the Pastor Emeritus section; no Charley-as-
current-pastor copy remains.

## [2026-07-22] site | Preprod hosting environment stood up
Owner requested a test site for reviewing changes before production. Created
second Firebase Hosting site gw-church-preprod in project gw-church, mapped
deploy targets (prod → gw-church, preprod → gw-church-preprod) in .firebaserc,
converted firebase.json hosting config to a two-target array (identical
settings), and deployed → https://gw-church-preprod.web.app (verified 200,
pastor page shows Chris Dumont content). Documented environments and deploy
commands in migration.md. Also committed the earlier pastor-transition
changes (bfa4eb9).

## [2026-07-22] site | Deploy rule: preprod-first, prod only after acceptance
Owner directive: all site changes go to preprod (gw-church-preprod.web.app)
for review first; production is deployed only after explicit acceptance.
Codified as CLAUDE.md § Deploy (binding workflow) and noted in migration.md
Hosting environments section.

## [2026-07-22] site | CI/CD pipeline: PR previews + prod-on-merge
Owner approved git-driven deploys so other developers can ship without GCP
credentials. Created service account github-action-hosting@gw-church (roles:
firebasehosting.admin, serviceusage.apiKeysViewer), stored its key as GitHub
secret FIREBASE_SERVICE_ACCOUNT_GW_CHURCH (local key deleted). Added
.github/workflows/preview-deploy.yml (PRs touching site/ or firebase.json →
preview channel on preprod site, URL commented on PR, 7-day expiry) and
prod-deploy.yml (push to main → prod live + preprod live mirror). Branch
protection on main NOT enabled — GitHub free plan blocks it on private repos
(403); rule enforced via CLAUDE.md instead. CLAUDE.md § Deploy rewritten for
the PR path + new § Collaboration (multi-developer, agent-through-repo
conventions). New wiki page ci-cd.md; migration.md and index.md updated.

## [2026-07-22] site | CI/CD pipeline verified end-to-end
Prod path: push to main (pastor-transition site changes) triggered the
Deploy-to-production run — prod + preprod mirror deploys succeeded via the
service account. Preview path: test PR #1 triggered Deploy-PR-preview, which
commented and served a working preview URL (gw-church-preprod--pr1-...,
HTTP 200); PR closed unmerged, branch deleted. Pipeline live.

## [2026-07-24] site | Privacy scan, history scrub, repo made public
Owner authorized making the repo public after a personal-data scan. Findings
and actions: (1) owner's work email was author/committer on all commits →
history rewritten with git-filter-repo, all commits now use the GitHub
noreply address, repo-local git config set to match (NOTE: commit SHAs
changed; SHAs cited in earlier log entries no longer resolve); (2) personal
gmail + school-account emails and their account-ownership mapping in
sermon-search-system.md and log.md → replaced with neutral placeholders in
files AND all history; (3) Elasticsearch API key in the embeds (already
public on the live site) verified read-only via _has_privileges — no
write/cluster privileges, cannot enumerate indices; re-scope recommendation
recorded in sermon-search-system.md § Security. Pre-rewrite backup bundle
saved locally. Repo flipped public, then branch protection enabled on main
(1 approving review; admin exempt for wiki commits). CLAUDE.md and ci-cd.md
updated. Residual public-by-design: church contact info, mark_quiz_bank.csv
(quiz answer key), raw/ site crawl.

## [2026-08-02] query | Collaborator onboarding: Alex
Owner added a second collaborator, Alex (GitHub: adcast1016-cpu, write
access), who is new to git and the LLM-wiki workflow. CLAUDE.md § Collaboration
gained a "Who's who" list mapping first names to GitHub logins and a standing
teaching-mode instruction: in Alex's sessions, explain git/deploy operations
before running them, define jargon, and narrate state after each step. No
site/ changes.

## [2026-08-02] ingest | wiki/git-basics.md (collaborator onboarding)
Authored wiki/git-basics.md at the owner's request: a deliberately short git
primer for Alex — core terms, this repo's branch/PR/preview workflow, a
command cheat sheet, and how to learn alongside the AI. Indexed under "The
project". CLAUDE.md teaching-mode note now points to it and caps lesson
length so teaching doesn't crowd out website work.
