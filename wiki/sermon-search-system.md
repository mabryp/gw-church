# Sermon Search System

**Summary:** The site's most technically distinctive asset — two custom-embed search apps (Search Sermons, Charley's Notes) backed by a hosted Elasticsearch cluster; fully independent of Google Sites, so it ports to any host unchanged.

## Architecture

Both pages under "Gateway Study" are custom HTML embeds running
**Searchkit + InstantSearch.js** (loaded from jsDelivr CDN), querying an
**Elastic Cloud** deployment directly from the browser:

- **Host:** `https://gateway.es.us-central1.gcp.cloud.es.io/`
- **Auth:** API key embedded in the page source (base64, visible to anyone
  who views source — see Security below)

## The two apps

| Page | Index | Notable fields |
|---|---|---|
| Search Sermons | `gateway_sermons_v3` | title, video_description, transcript, quote, summary, verses, topics, songs, published_at, books, thumbnails.default.url |
| Charley's Notes | `sermon_notes_v3` | filename, summary, verses, commentary, books, topics, file_url, corrected_text, owner, category |

Search Sermons indexes **YouTube sermon videos** (transcripts, thumbnails,
publish dates — see [Connect Channels](connect-channels.md) for the channel).
Charley's Notes indexes **[Charley](charley.md)'s sermon-note documents**
(files with OCR/corrected text and commentary). Both offer faceting by topics,
books, and verses; date filtering via flatpickr.

## Migration implications

The embeds are self-contained HTML documents (extracted to
`raw/embeds/gateway-study_*.html`). They do not depend on Google Sites at all —
on the new site they become either iframes or inlined pages. **This system is
the reason a static-site migration is low-risk.**

## PDF hosting dependency

The `file_url` links in `sermon_notes_v3` (213 docs) point to PDFs in Google
Drive owned by **[owner school-domain account]** — a Workspace account on the
[school](gateway-christian-school.md)'s domain, not the personal
[owner personal gmail] account that owns the site, quiz sheet, and Firebase
project (verified by sampling files across the index, 2026-07-21; the index's
`owner` field is a content label — "charley"/"phill" — not the Google account).
RISK: if the gw-school.org Workspace or that account is ever suspended,
renamed, or cleaned up, every sermon-note PDF link breaks at once. Options if
that becomes a concern: transfer the Drive folder to the gmail account, or
re-host the PDFs (e.g., Firebase Hosting under `site/`) and update `file_url`
in the index.

## Security

The Elasticsearch API key is publicly visible in page source (unavoidable for a
serverless client-side search, and already public today). ACTION ITEM for the
site owner: confirm the key is scoped **read-only to these two indices**; if it
has write or cluster privileges, rotate it and issue a search-only key before
(or during) migration.

## Sources

- raw/embeds/gateway-study_search-sermons_embed.html
- raw/embeds/gateway-study_charleys-notes_embed.html
