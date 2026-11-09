# Homepage

**Summary:** The gw-church.org landing page (`site/index.html`): visitor-first copy adopted 2026-11-09 from an owner-supplied template; service time, worship style, and family details supplied by the owner the same day.

## Structure (since 2026-11-09)

Follows the owner's sample (`raw/sample_landing_page.txt`) section for
section, with [Gateway Church](gateway-church.md) facts filled in:

1. **Hero** — logo, "Welcome to Gateway Church", tagline "Rooted in God's
   Word. A home for your family." (owner's direction 2026-11-09: lead with a
   high view of Scripture and family orientation, aimed at believing families
   seeking a biblically grounded church; the sample's "There's a place for you
   here." was dropped), then the "Join us this Sunday" box with time and
   street address and two buttons: *Plan Your Visit* (anchor to the visit
   section below) and *Watch a Sermon* (the YouTube channel's live-streams
   tab, see [Connect Channels](connect-channels.md)). The two welcome
   paragraphs follow the box (moved below it 2026-11-09 so the box is above
   the fold on phones; left-aligned under 860px).
2. **What to expect** — arrival; worship "mostly contemporary with
   traditional influences", prayer, sermon rooted in Scripture; "We are a
   Bible-believing church"; children's church and nursery care during the
   service (facts in [Gateway Church](gateway-church.md) § Sunday service).
3. **Life together** — "a young, vibrant group"; weekday community; links to
   the [Wednesday Dinner](wednesday-dinner-poll.md) page and the
   [reading plan](reading-plans.md); keeps the pre-2026 "a place to be known …
   rest, heal, learn, grow, lead, and make an impact" line. The former
   "multi-cultural, community-oriented" wording was dropped at the owner's
   request (2026-11-09).
4. **Calendar** — two Google Calendar embeds of the same public calendar:
   month grid (`.cal-month`) on wide screens, agenda list (`.cal-agenda`)
   under 860px; CSS shows one or the other.
5. **Plan your visit** (`#visit`) — address, phone, email, connect link, map
   embed (the former "Find Us" section, renamed to match the button).
6. **Closing** — "We hope to see you soon." + *Plan Your Visit* button.

Button and visit-box styles live in `site/css/style.css` under "Homepage:
visitor-first landing" (`.btn`, `.btn-outline`, `.btn-row`, `.visit`,
`.tagline`, `.closing`, `.cal-month`/`.cal-agenda`, phone rules in the
860px media query). The logo PNG is opaque white, so `.hero .logo` uses
`mix-blend-mode: multiply` to hide its box.

## Design review (2026-11-09, PR #13 preview)

Reviewed at 1280px and 390px. Findings, highest impact first. Items 1, 3, 5,
6 applied the same day on the owner's go-ahead; 2 and 4 wait on the owner:

1. **Sunday CTA is below the fold on phones.** Logo (≈250px) + h1 + tagline
   + two centered paragraphs push the "Join us this Sunday" box past the first
   screen at 390×844. Fix: order hero as logo → h1 → tagline → visit box →
   paragraphs, and cap the logo at ~200px on small screens.
2. **No photograph.** The page claims "young, vibrant" and "family" with
   text only. A real congregation/family photo under the hero would carry the
   message; owner must supply an image file (never hotlink — see
   [Migration](migration.md) open item 4).
3. **Calendar embed is noise on phones.** Month grid at 390px shows truncated
   "Reading Plan Jo…" chips every weekday and unreadable Sunday entries. Fix:
   serve the embed in `mode=AGENDA` below 860px (two iframes toggled by CSS)
   or replace with a short "This week" list.
4. **Calendar shows Sunday entries at 10:15** ("10:15 Message: …") while the
   page says 10:00 a.m. — owner to confirm which is right.
5. **Logo PNG has an opaque white box** visible against the off-white page
   background. Fix: transparent PNG, or white hero background.
6. **Long centered paragraphs** in the hero (4–5 lines centered) read worse
   than left-aligned; consider one shorter paragraph, or left-align on phones.

Minor: touch targets, contrast, and heading hierarchy pass; phone menu is
14 items long but usable.

## Earlier version (2026-07-20 to 2026-11-09)

Logo + discipleship lede ("Each of us is called to be a disciple of Christ…"),
two columns "What You'll Find" / "We're Here for You", Calendar, Find Us —
a light restyle of the Google Sites homepage captured in `raw/home.html`.
The discipleship sentence and mission motifs remain recorded in
[Gateway Church](gateway-church.md) § Mission and voice.

## Sources

- raw/sample_landing_page.txt (owner's template, added 2026-11-09)
- raw/home.html (original Google Sites homepage)
- Owner's direct answers in session, 2026-11-09 (service time, worship style,
  children's church/nursery, "young and vibrant", Bible-believing, drop
  "multi-cultural")
