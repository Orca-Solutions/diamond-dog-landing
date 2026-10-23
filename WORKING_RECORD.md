# Working record

## 2026-10-20 — Coming-soon website and brand handoff

Jason approved Diamond Dog's brand direction and requested a coming-soon site, a separate branch, and a separate repository containing both the site and brand kit. The OrcaOS tool repository is outside this change's scope.

Implemented a buildless, responsive static page using the approved symmetrical logo, black mascot with diamond collar tag, warm paper/ink palette, acid and lilac accents, and locally bundled fonts. The primary line is “Delegate work, not your identity.” The page explains bounded work and records, distinguishes accepted requests from unknown delivery, and gives honest early-stage answers. No launch date, signup flow, shipped-product claim, or permission-centric language is invented.

The evidence card is an illustrative marketing scenario. Both evidence labels remain visible when selecting either explanation. It does not restyle the fixed inspector evaluation screens. The final GitHub link points to the existing tool repository under its current OrcaOS name.

Verification: local HTTP 200; JavaScript syntax check; desktop, 1024px tablet, 800px narrow tablet, 390px phone and 320px small-phone viewport inspection. Repaired a narrow-tablet illustration/copy overlap by switching to the stacked layout earlier. Checked Accepted/Unknown explanation changes and FAQ expansion. Checked small-screen document width for horizontal overflow and browser warnings/errors (none reported). The main landmark encompasses all page sections. Visible focus treatment, reduced-motion CSS, alternative text, and native disclosure controls are present. No formal assistive-technology audit was performed.

Review: author verification sufficient — static presentation, copy, and local illustrative interactions; no custom authentication, payments, external writes, or sensitive-data handling.

Delivery: new private repository `Orca-Solutions/diamond-dog-landing`; implementation branch `codex/diamond-dog-coming-soon`. No automatic GitHub deployment is configured. Merge remains Jason's action. The owner-private Sites deployment is tracked in the delivery receipt beside this record. Public launch/domain and source/brand licensing remain unresolved choices, not implementation blockers for private review.

## 2026-10-20 — Repository destination correction

Jason requested `Orca-Solutions/diamond-dog-landing` as the delivery destination. The repository was empty; seeded its base from the original README-only baseline, then pushed the existing implementation and this signed reference correction on the working branch. Website and brand assets are unchanged, so the prior browser verification and private deployment remain applicable. The prior repository is retained; its PR is superseded by the PR in the requested destination.

## 2026-10-21 — Public-domain launch preparation

Jason confirmed `diamonddog.orcasolutions.dev` and requested launch. PR #1 is
merged as `6a9166149fe3640a553c9766cce9f97294633986`; GitHub now reports the
repository public. Frontend/domain management prepared a separate Git-connected
Cloudflare Pages rollout serving only `site/`. No brand-kit publication through
the web root, backend, secret, storage, paid upgrade or OrcaOS tool change is
needed. The existing private Sites review remains a separate deployment mirror.

Updated the canonical URL and Open Graph image/URL to the public domain and
documented the intended Git production/preview setup and rollback. These are
metadata and hosting-documentation changes; page appearance and JavaScript are
unchanged, so the October 20 viewport and interaction evidence remains applicable.
Author checks cover JavaScript syntax, local asset references and whitespace.
Production activation and normal public-domain HTTPS acceptance are recorded
separately in the linked DevOps record; this source change does not prove launch.

## 2026-10-21 — Favicon fallbacks and 16px tab icon

Jason confirmed the SVG favicon shows in the live tab and asked for the optional
fallbacks. The page linked only `assets/favicon.svg`, so `/favicon.ico` returned
404 and there was no home-screen icon for iPhone and iPad.

Added `site/favicon.ico` (16, 32 and 48 px) and `site/apple-touch-icon.png`
(180 px, rendered from the brand-kit avatar: full mark on acid with its own
margin), both at the web root where browsers and crawlers look by default, and
linked them beside the SVG. The ICO is declared `sizes="32x32"` so browsers that
support SVG keep choosing the SVG.

The kit's 16 px frame was a straight downscale of the micro mark and blurred the
eyes and nose into the face. Replaced it with a hand-placed 16 px drawing on whole
pixels: same silhouette, two-pixel eyes, and an open two-by-two nose (the diamond
cannot be drawn at that size; mark-process already allows limited detail at
16 px). The brand kit's `favicon-16.png` and `favicon.ico` were updated to match;
the 32 and 48 px frames, the SVG and every other asset are unchanged.

Verification: compared three hand-drawn 16 px candidates against the current SVG
render at real size on light and dark tab colors; checked that each ICO frame is
byte-for-byte the intended image; loaded the page in Chromium and confirmed every
icon link returns 200 with the right content type and no console errors. Chrome
and Firefox still render the SVG in the tab, so on a standard-resolution screen
they show the softer scaled SVG; the hand-drawn 16 px frame is what ICO-reading
contexts (older Safari, Windows shortcuts, search results) see. Not checked on a
real iPhone or on the deployed domain.

## 2026-10-21 — Clarity refinements from the brand review

A brand review of the live page found no brand drift and suggested two clarity
refinements. Jason asked for both without changing identity, colors, mascot or
voice.

The hero now adds one plain sentence under the descriptor: "The aim: let software
edit your documents, send your mail or pay a bill, without handing it the keys to
everything else." "The aim" keeps it honest that nothing has shipped. The hero's
desktop minimum height grew from 765px to 830px so the rule below it no longer
runs through the illustration caption.

For a "Follow development" destination that needs no new account, added a static
`updates.html` page with dated notes and a hand-written Atom feed (`feed.xml`).
The closing section now leads with "Follow development" and keeps "Explore the
project" as a secondary button. Still no signup collection, analytics, cookies or
backend. An email list remains a later option and would need a mail service
account, a privacy note and Jason's choice of provider.

Verification: local HTTP 200 for both pages and the feed; feed parses as XML;
1440, 1100, 1024, 800, 390 and 320px viewport inspection of both pages with no
horizontal overflow and no console warnings or errors. Production URLs
(`/updates`) rely on Cloudflare Pages' default extensionless HTML serving and
were not checked from this environment.

Review: author verification sufficient — static copy and layout only.

## 2026-10-21 — Back to a single page

After PR #4 merged, Jason asked for a single landing page only. Removed
`updates.html`, `feed.xml` and their styles, and restored the closing panel's
single "Explore the project" button. The hero's plain-benefit sentence and the
taller desktop hero stay. A "Follow development" destination is deferred; an
email list would need a mail-service account and Jason's choice of provider.

## 2026-10-22 — Consistency fixes from a second review

A review of the live page suggested small consistency fixes; Jason asked for them.

- One status phrase, "In development", in the header, hero eyebrow, meta and
  Open Graph descriptions, and the social card. The hero note drops "First
  experiment under way." The FAQ still explains the experiment in prose.
- The share title now matches the page title: "Diamond Dog — Delegate work, not
  your identity."
- The receipt header read as "ACTIVITY RECORD014" in plain text. It now has a
  space between its two labels and reads "ACTIVITY RECORD NO. 014".
- Footer adds "Made by Orca Solutions · 2026".
- The closing panel names the licenses: GPLv3 for the runtime; MIT for the SDK,
  interfaces and examples.

`site/assets/social.png` was edited in place: its last line now reads "In
development." in the same IBM Plex Mono size and position. The brand kit's
`applications/social-preview.{svg,png}` are the v1 handoff and still say
"First experiment under way."

Verification: 1440, 1100, 1024, 800, 390 and 320px inspection with no horizontal
overflow and no console warnings or errors; receipt header text checked with
`innerText`; social card compared against a re-render of the original line.

## 2026-10-22 — The dog as a recurring character

Jason asked for playful art to fill the page's empty space and give Diamond Dog
some personality: curious and mischievous, and he always follows the rules.

Added five inline SVG spot illustrations drawn in the mark's flat geometry
(folded ears, paper eye dots, the open diamond nose, acid collar and lilac tag):
a head and paws peeking over the rule at the bottom of the hero; a paper dog
sitting on the floor of the dark receipt section, looking up at the receipt
("Sits. Waits for sign-off."); a butt-up dog digging a hole beside the FAQ
("Digging. Within scope."); a dog lying along the bottom edge of the lilac
closing block; and paw prints walking toward "Back to top". Every drawing is
`aria-hidden` and `focusable="false"`; the two mono captions are ordinary text.
Colors come from the brand tokens through `currentColor` and a `--dog-bg`
variable, so one drawing works on paper, ink and lilac.

Motion is one short tail wag every eight seconds (staggered per dog) and an
occasional sideways glance from the peeking dog. `prefers-reduced-motion` now
cancels animations as well as transitions. No new files, scripts or requests;
the page stays buildless.

Verification: full-page Chromium screenshots at 1440, 900 and 390 px; the
desktop hero, receipt, FAQ and closing placements were checked at actual size,
the peeking dog moves to the right edge on narrow layouts, the receipt section
gains bottom room for the sitting dog, and the paw prints hide where the footer
wraps. Not checked with a screen reader beyond the hidden-decorative markup, and
not checked on the deployed domain.

## 2026-10-22 — Sticky ink header, receipt ribbon and collar tidy-up

Jason asked for a sticky header in lilac or ink with the logo mark bigger, one
more mischievous dog on the bar, a long receipt looping down the empty gap in
the receipt section, the digging dog moved right into its gap, and tidier
collars and tags.

The header is now a full-width sticky ink bar (84 px, 64 px on narrow screens)
with the paper mark at 60 px beside a smaller paper wordmark (`assets/mark-paper.svg`
and the new `assets/wordmark-paper.svg`, both from the brand kit); the combined
`logo.svg` stays in the footer. Ink was chosen over lilac so the bar bookends
the dark receipt section and keeps lilac for the closing block; switching is a
one-line change. `scroll-padding-top` matches the bar so anchor links land
below it, and focus rings on the bar use acid. A dog hangs down from the bar's
underside at the top of the page, paws over the edge; `script.js` adds
`is-scrolled` to the header after 8 px of scroll so he slides back up and fades,
staying out of the way of content. Without JavaScript he simply stays put.

A paper receipt ribbon with mono-style print lines now runs down the gap
between the copy and the card in the receipt section (hidden below 1100 px
where the gap disappears). The digging dog sits right-aligned in the FAQ's
left column, closer to the questions. Collars are one clean band with the
lilac tag hanging from its lower edge on the sitting, digging and resting dogs.

Verification: Chromium screenshots at 1440, 900 and 390 px at the top of the
page and after scrolling; the bar sticks, the hanging dog hides on scroll, the
ribbon clears both the copy and the card at 1440 px, and anchors land under
the bar. Not checked with a screen reader or on the deployed domain.

## 2026-10-22 — Coloured full stops on the section titles

Jason asked for the final full stop of the four major titles in acid or lilac,
leaning acid, and wondered about splitting by background. Compared all-acid,
all-lilac and both splits at 1440 px (comparison image shared in the project
thread). Shipped lilac on paper and acid on ink: each colour sits on the
background where it has the most punch, acid stays the focal point in the dark
section where it already colours the eyebrow, and the receipt title keeps its
lilac "unknown" without a second lilac beside it. The stop is a `<span class="stop">`
inside the heading, so screen readers still read the sentence; swapping the
colours is two lines in `styles.css`.

## 2026-10-22 — Looping receipt and the hanging dog, second pass

Jason wanted the receipt ribbon more three-dimensional, looping over itself,
and only filling the gap rather than running edge to edge; and the header dog
read as upside down to him, so he asked for the head flipped with the pupils
still looking down.

The ribbon is now generated geometry (a torn top edge, a short fall, one loop
that crosses over itself, then a fall into a curl) rendered as flat quads with
a shade that darkens as the paper turns sideways and a warmer tone where it
climbs and shows its back, thin ink edges, and print lines across the straight
runs. The generator is a short Python script kept with the working notes of
this change, not in the repository; the output is the inline SVG in
`index.html`. It sits at 37% from the left, 120 px down, and hides below
1100 px. The header dog now hangs by his paws with his head upside down and
his pupils toward the page.

Verification: 1440 px screenshots of the receipt section and the header at
the top of the page; the loop clears the copy and the card at that width.

## 2026-10-22 — Collars to the brand book, and a receipt that reads

Jason said the collars still weren't landing, that the ribbon's "writing" was
sometimes just lines all the way across, and that he pictured the receipt
starting higher, above the writing, filling the space above and to the right
rather than the gap in between.

Collars now follow the brand book's character constants ("a narrow acid
collar and a single lilac diamond tag", section 13, matching
`receipt-dog-personal.png`). Each band is about a third of its old width and
sits a little proud of the neck outline, as a strap does, with a thin ink rim;
a small ring tucks under the band at its lowest point and the tag hangs
straight down from it. The tag's rim and ring use a `--dog-metal` colour
(paper on the ink dogs, ink on the paper dog), which also stops the resting
dog's tag reading as a second nose. On the digging dog the band runs from the
nape into the hole and the tag dangles into it. The resting dog lifts its head
(tilted, looking toward the button) so its collar shows across the chest, and
the sitting dog's viewBox is wider so its right ear is no longer clipped.

The receipt ribbon is redrawn as a 3D paper strip: it curls in above the
eyebrow, runs right over the copy, loops once and slides under the card.
Because the strip only bends around one fixed width direction, each stretch
between folds is a single polygon with a gradient, so the shading is smooth,
there are no seams, and the page markup roughly halved (index.html 95 KB to
49 KB, 12 KB gzipped). The print is real text in IBM Plex Mono, set along the
paper with one transform per line: a day of the dog's activity records, eight
distinct ones from back yard to living room so no two match where the loop
crosses (scope, what he may read or change, sign-off, then entries such as
"SQUIRREL IGNORED", "BALL UNKNOWN", "SOFA DECLINED" and "GOOD BOY YES"), in
the brand's accepted / observed / unknown vocabulary. It is decorative and `aria-hidden`, can't be
selected or clicked, and stays hidden below 1100 px.

The generators now live in `tools/art/` (`dogs.py`, `ribbon.py`,
`receipt_text.py`; see its README) instead of scratch notes, so the art can be
changed later; both reproduce the committed markup exactly. Also fixed a small
existing bug: on narrow screens the FAQ title read "Still inthe workshop"
because its hidden line break had no space beside it.

Verification: Chromium screenshots of the receipt section at 1101, 1300, 1440
and 1920 px (the ribbon clears the eyebrow by 81 px and the heading by 60 px at
1440, and ends 42 px under the card), zoomed renders of the curl, the loop
crossing (nearer paper covers farther print) and the text, the three collars at
1x and 2x with a before/after sheet, and full pages at 1440, 900 and 390 px.
Not checked with a screen reader or on the deployed domain.

## 2026-10-22 — A receipt loop that could exist, and collars on the peeking dogs

Jason liked the collars and the receipt text but said the loop did not look
physically possible. He was right: the paper came round and passed through
itself. The loop is now a coil: as it goes round, the paper drifts sideways
along its width by a little more than its width, so it passes beside itself
and comes out nearer the viewer, the way a real curl of receipt paper does.
Overlaps are now ordered by depth at the point where they overlap. The loop is
a little tighter so the descent still clears the copy.

At his invitation the receipt is slightly more cartoonish, to match the dogs:
the smooth shading is now three flat tones per side (hard gradient stops, still
one polygon per stretch, no seams), with an ink outline along the edges and the
folds, like the collars' ink rim. The page markup shrank slightly (about 29 KB
for the ribbon).

The header dog and the hero peeking dog showed a gap at the neck between head
and paws; it is now filled with the acid collar colour, as he asked.

Verification: Chromium renders of the receipt section at 1101, 1300, 1440 and
1920 px, a 3x render of the coil, and both peeking dogs at 3x. At 1440 the
ribbon clears the eyebrow by 67 px, the heading lines by 49, 51 and 57 px, and
ends 34 px under the card (22 px at 1101). Not checked with a screen reader or
on the deployed domain.

## 2026-10-22 — Live page paired with an old stylesheet

Right after PR #7 merged, Jason saw the live page with giant solid black dogs,
a black blob through the receipt and the header dog not hiding on scroll. The
page HTML was new but `styles.css` and `script.js` were the old ones: the
symptoms match the pre-#7 stylesheet exactly (no ink header, the ribbon in the
grid flow, unstyled SVG fills). The page is fetched fresh, but the stylesheet
and script can be kept by the browser or the host's edge cache. This
container cannot reach the live domain, so the cache headers themselves were
not inspected.

Fix: the stylesheet and script links now carry a content hash
(`styles.css?v=<hash>`), written by `tools/stamp_assets.py`, so any change to
either file changes its URL. `tools/art/ribbon.py` runs the stamp itself. The
drawings also got safe defaults in case a stylesheet is ever missing: a width
attribute on each dog SVG (its desktop size) and `fill="none"` on the
receipt's outline paths, so they degrade to small shapes instead of filling the
page. Rendering with the stylesheet is unchanged (full-page renders at 1440,
900 and 390 px match main pixel for pixel, apart from the tail-wag animation
frame); with the stylesheet blocked, every dog stays at its normal size.

Follow-ups in the same PR, at Jason's asks: the peeking pup moved from the
hero rule to the bottom of "The arrangement", peeking up over the dark receipt
section; the section labels lost their "01 / 02 / 03" prefixes; the receipt
ribbon now also shows between 1000 and 1100 px; and the stacked layout (740 to
1000 px, card under the copy) gets its own smaller receipt that coils in the
space right of the copy and hangs down behind the card's top edge (generated by
the same tool; it scales with the free width and stays at least about 20 px
from the copy). Phones still show no ribbon: there is no free space beside the
copy. The page is about 71 KB with both ribbons.

## 2026-10-23 — Dim mode for dark-mode devices, and no card numbers

Jason asked for a careful dark mode: "more a muted light mode than a true
dark", easy on the eyes in low light while the ink dogs keep their contrast.
Under `prefers-color-scheme: dark` the page stays light but dimmer: paper is
`#d2cec7` (exactly 0.86 of the normal paper, so the paper drawn into the hero
photo, the header mark and the receipt ribbon matches it through a
`brightness(.86)` filter), with slightly deeper muted text, acid, lilac, rules
and chip colours. Ink sections, buttons and dogs are unchanged. Contrast (WCAG):
body text 11.2:1, muted text 6.3:1, light text on ink 11.2:1, subtle text on
ink 6.5:1, ink on lilac 6.6:1, chips 5.9:1 and 5.7:1, focus ring 6.3:1; all
pass AA, and the main pairs pass AAA. The light page is unchanged. `theme-color`
has a matching dim value.

The three cards in "The arrangement" lost their 01 / 02 / 03 numbers, and the
titles moved up to close the gap.

Verification: full-page Chromium renders of both colour schemes at 1440 and
390 px. Not checked on a real device's dark mode.

## 2026-10-23 — Dirt out of the hole, a head bob, the torn edge, a preview switch

Follow-ups on the same branch (PR #9):

- **Dirt.** Jason: the dirt was in the wrong place and should look like it comes
  out of the hole. The four loose triangles are replaced by a lip of clods on
  the hole's far rim, clods thrown up and back along three arcs (big as they
  leave, smaller as they fly) and a pile left of the hole where they land, all
  in flat ink like the dog (`dirt()` in `tools/art/dogs.py`). The viewBox grows
  42 units to the left for the pile, so the drawing is 352 px wide (258 px on
  narrow screens) and the dog stays the same size.
- **Head bob.** The resting dog on the closing panel tilts his head left, right,
  left in time with his tail wag (same 8 s cycle and 5 s delay as the tail,
  ±5°, pivoting at the neck). Off under reduced motion, like every animation.
- **Torn edge.** Jason saw the receipt's serrated bottom edge split into two
  offset strips on his Mac. It was two tiled gradients on the tilted card, which
  some browsers rasterise apart; Chromium here showed faint seams but not the
  split. It is now one solid strip clipped to a single zigzag path (14 px teeth,
  wide enough for any card) that tucks 1 px under the card.
- **Preview switch.** On Cloudflare's branch and commit links
  (`*.diamonddog-a17.pages.dev`) a small Auto / Light / Dim switch sits bottom
  right, so dim mode can be tried without changing the device. It retargets the
  dim-mode media rule, so there is no second copy of the palette; the choice
  lasts for the tab. The live domain never shows it.

Verification: Chromium renders of the questions section at 1440, 1050, 900 and
390 px; head-bob frames at each beat of the wag; the torn edge at 1440, 1280,
1100, 900 and 390 px, light and dim, and at 1, 1.25, 1.5 and 2× pixel ratios;
the switch on a simulated preview host (each mode, reload, device dark mode) and
absent on the local host. Not checked in Safari, where the split was seen.
