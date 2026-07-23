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
(gw-church.org). **All site changes deploy to preprod FIRST** for owner review:

1. `firebase deploy --only hosting:preprod`, then share the preprod URL.
2. Wait for the owner's explicit acceptance.
3. Only then `firebase deploy --only hosting:prod`.

Never deploy to prod without a preprod review of the same changes — even for
"trivial" fixes, and even if asked to "deploy" without specifying a target
(deploy to preprod and ask). Log every deploy with the `site` prefix, noting
which target.

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
