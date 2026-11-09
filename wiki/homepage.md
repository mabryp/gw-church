# Homepage

**Summary:** The gw-church.org landing page (`site/index.html`): visitor-first copy adopted 2026-11-09 from an owner-supplied template, with three facts still awaiting the owner before it can go to prod.

## Structure (since 2026-11-09)

Follows the owner's sample (`raw/sample_landing_page.txt`) section for
section, with [Gateway Church](gateway-church.md) facts filled in:

1. **Hero** — logo, "Welcome to Gateway Church", tagline "There's a place for
   you here.", two welcome paragraphs, a "Join us this Sunday" box with time
   and street address, and two buttons: *Plan Your Visit* (anchor to the
   visit section below) and *Watch a Sermon* (YouTube channel, see
   [Connect Channels](connect-channels.md)).
2. **What to expect** — arrival, service outline, visitor details.
3. **Life together** — weekday community; links to the
   [Wednesday Dinner](wednesday-dinner-poll.md) page and the
   [reading plan](reading-plans.md); keeps the pre-2026 "a place to be known …
   rest, heal, learn, grow, lead, and make an impact" line so the established
   voice survives the rewrite.
4. **Calendar** — Google Calendar embed (unchanged).
5. **Plan your visit** (`#visit`) — address, phone, email, connect link, map
   embed (the former "Find Us" section, renamed to match the button).
6. **Closing** — "We hope to see you soon." + *Plan Your Visit* button.

Button and visit-box styles live in `site/css/style.css` under "Homepage:
visitor-first landing" (`.btn`, `.btn-outline`, `.btn-row`, `.visit`,
`.tagline`, `.closing`, `mark.todo`).

## Open facts (owner must supply)

Neither the wiki nor any crawled Google Sites page states these, so the page
carries them as highlighted `<mark class="todo">` placeholders. Replace the
text and drop the `<mark>` before the PR is merged:

- **Sunday service time** (hero visit box).
- **One-phrase description of the worship portion** of the service (What to
  expect).
- **One sentence on children's programs / accessibility** (What to expect) —
  or delete the sentence if there is nothing to say.

## Earlier version (2026-07-20 to 2026-11-09)

Logo + discipleship lede ("Each of us is called to be a disciple of Christ…"),
two columns "What You'll Find" / "We're Here for You", Calendar, Find Us —
a light restyle of the Google Sites homepage captured in `raw/home.html`.
The discipleship sentence and mission motifs remain recorded in
[Gateway Church](gateway-church.md) § Mission and voice.

## Sources

- raw/sample_landing_page.txt (owner's template, added 2026-11-09)
- raw/home.html (original Google Sites homepage)
