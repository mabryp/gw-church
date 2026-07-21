# Site Structure (gw-church.org on Google Sites)

**Summary:** Complete page map of the current Google Site as crawled 2026-07-20, including per-page content type and known defects.

## Page map

| Path | Title | Content type |
|---|---|---|
| `/home` | Home | Text + Google Calendar embed + Google Maps embed |
| `/about` | About | Text (address/contact only) |
| `/about/what-we-believe` | What We Believe | Text — statement of faith, see [What We Believe](what-we-believe.md) |
| `/about/our-pastor` | Our Pastor | Text + photo, see [Charley](charley.md) |
| `/about/gateway-christian-school` | Gateway Christian School | Text, see [Gateway Christian School](gateway-christian-school.md) |
| `/connect` | Connect | Text + Facebook/YouTube links, see [Connect Channels](connect-channels.md) |
| `/reading-plan/matthew-reading-plan` | Matthew Reading Plan | Custom HTML embed, see [Reading Plans](reading-plans.md) |
| `/reading-plan/mark-reading-plan` | Mark Reading Plan | Custom HTML embed |
| `/reading-plan/luke-reading-plan` | Luke Reading Plan | **Placeholder — title only, no content** |
| `/reading-plan/john-reading-plan` | John Reading Plan | **Placeholder — title only, no content** |
| `/gateway-study/charleys-notes` | Charley's Notes | Custom HTML embed — Elasticsearch search app, see [Sermon Search System](sermon-search-system.md) |
| `/gateway-study/search-sermons` | Search Sermons | Custom HTML embed — Elasticsearch search app |

`/reading-plan`, `/gateway-study` are nav groupings only (no pages; direct requests 404).

## Site-wide furniture

- Header: site name + nav (Home, Reading Plan ▾, Gateway Study ▾, About ▾, Connect) + search
- Footer on every page: address / phone / email block
- Fonts: Playfair Display (headings) + Open Sans (body)
- Header background: lime/chartreuse green

## Known defects (lint findings, 2026-07-20)

1. **Broken link:** homepage links to `http://gw-church.org/social_media` — the page 404s. Probably meant `/connect`.
2. **Empty pages:** Luke and John reading plans are published but have no content (plans presumably not written yet — Matthew ran Apr–Jul 2026, Mark runs Jul–Aug 2026; see [Reading Plans](reading-plans.md)).
3. **Exposed API key** in search embeds — see [Sermon Search System](sermon-search-system.md).

## Sources

- raw/*.html (all 12 pages, crawled 2026-07-20)
- raw/embeds/*.html (extracted custom-embed sources)
