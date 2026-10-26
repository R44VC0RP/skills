# Style guide: the Apollo handbook page

How the page is built, how it is written, and the taste calls that make it read
as a real 1969 NASA document rather than a pastiche. The examples in
`assets/examples/` follow every rule here; open the PNGs side by side with this
file.

## Contents

1. The genre
2. Page anatomy and space budget
3. Typography
4. Writing the content
5. Choosing the figures
6. Drawing with taste
7. Black and white only
8. Pitfalls already paid for
9. Variants and other NASA genres

## 1. The genre

The model is a "Systems Data" page from the Apollo Operations Handbook
(SM2A-03-BLOCK II-(1), North American Rockwell for NASA, 1969). Those pages are
quiet and dense: a typed running head, numbered paragraphs, one or two big line
drawings, a tab on the page edge and a dated footer. Nothing is decorative.
Every mark is there because a crew member needs it.

What makes it convincing is structure and restraint, not texture. Don't add
fake coffee stains, scan noise, rotated stamps, "CLASSIFIED" banners,
"SPECIMEN" overlays or NASA insignia. The real pages have none of those, and
they would also be noise when the page goes to a printer.

Never reproduce the NASA meatball, the worm logotype or other agency marks.
Use the subject's own program name ("PROJECT JANUS", "ARTEMIS SURFACE HABITAT") in the running
head instead. That is also how the AOH did it: the head names the spacecraft
handbook, not the agency.

## 2. Page anatomy and space budget

Top to bottom on A4 (the template's values; the AOH originals were US Letter,
see Variants):

| Block | What it holds | Height |
|---|---|---|
| Top margin | | 9 mm |
| Running head | doc number (bold), handbook title (bold), part name ("SYSTEMS DATA"), 1.5 pt rule | 15 mm |
| Opener | "SECTION 2 · SUBSECTION 2.1" and the subsystem name, centered caps | 14 mm |
| 2.x.1 INTRODUCTION. | 3 lines | 18 mm |
| Figure 2.x-1 (hero) | the main drawing + caption | 68–74 mm |
| 2.x.2 FUNCTIONAL DESCRIPTION. | 4 lines | 22 mm |
| 2.x.2.1 underlined sub-paragraph | 2 lines, often with a change bar | 11 mm |
| Figure 2.x-2 (secondary) | timeline, schematic or detail + caption | 48–54 mm |
| Lower band | 2.x.3 data table (left) beside a notice and a checklist card (right, 64 mm) | 45–50 mm |
| Footer | rule, subsystem name, Mission / Basic Date / Change Date / Page | 21 mm from the bottom |

That is full. `render.sh` prints the room left above the footer and exits 3
on overflow; aim for 4 to 10 mm. To make room, cut words before you shrink
anything: one fewer line of text is 3.6 mm, and a table row is 3.4 mm.
Shrinking type below the template's sizes is the wrong fix.

The lower band is two columns, and only the taller one sets its height. Before
cutting there, compare the table column with the notice-plus-checklist column
(in the PNG or the dev tools) and trim the taller one. A 4-line notice next to
a 7-step checklist is usually the culprit, not the table.

Fixed furniture:
- **Paragraph numbers** sit in a 19 mm column at the left margin; text starts
  after it. Body paragraphs have a 9 mm first-line indent; the first line under
  an underlined sub-heading is flush.
- **Change bar**: a 1.3 mm black bar in the left margin beside one revised
  paragraph. It goes with a Change Date in the footer, so the page reads as
  revision 2 of a living document. Use one at most.
- **Thumb tab**: a black block bleeding off the right edge, 3-letter subsystem
  code in white (AGS, PEU). Every page of the same subsection has it at the
  same height.
- **Figure code**: small Leroy text at the bottom right of each figure,
  `<TAB>-501A`, `<TAB>-502A`. It's the illustrator's art number.
- **Footer**: the subsystem name centered, then the dated line. Basic Date is
  the first version (a repo's first commit; a plausible date for fiction).
  Change Date is the latest change. Leave Mission blank unless it means
  something.
- **Doc number**: pattern after `SM2A-03-BLOCK II-(1)`: a 2–4 letter code plus
  a digit and A (`JN2A`, `IT2A`), then `-03-BLOCK I-(1)`.

## 3. Typography

| Role | Face | Size | Notes |
|---|---|---|---|
| Running head, body, captions, tables, notices | Iowan Old Style, letter-spaced 0.055em | 8 pt / 1.33 | Stands in for the IBM Selectric proportional typewriter text of the AOH. Georgia is the fallback. Bold only in the doc number, the title and notice tags. |
| Paragraph headings, opener | same, caps, tracked 0.08–0.12em | 8 pt | `INTRODUCTION.` with the period, as typed. Level-4 headings are mixed case and underlined: `Clock Synchronization.` |
| Every label inside a drawing | Routed Gothic Narrow (Leroy template lettering), caps | 2.05–2.5 mm | Callouts 2.35, secondary lines 2.05, view titles and big letters 2.5 (regular width). |
| Figure codes, thumb tab | Routed Gothic | 2.4 mm / 8 pt | |
| Crew checklists | Letter Gothic (IBM Selectric) | 7.1 pt | The Apollo and early Shuttle Flight Data File face. Use it only for checklists, so it means "procedure". |

Why these: the AOH body is typed on an IBM Selectric with wide letter spacing.
The drawings are lettered with a Leroy scriber template. Checklists are Letter
Gothic. Helvetica belongs to the 1975 Graphics Standards Manual era (after
Apollo). Futura is for covers and flight plan titles. Don't mix in the user's
usual UI fonts; this genre is the explicit request.

Leroy's plain "1" reads as "I" ("API VI", "TI"). The template swaps only U+0031
to a flagged 1. Keep the swap for anything with versions, subscripts or part
numbers; drop it for a strictly period-accurate page.

All caps is correct here: headings, every drawing label and placarded control
names are caps; body text is sentence case. That overrides any general "no all
caps" design rule, because it is the genre being asked for.

## 4. Writing the content

Voice: an operations handbook. Third person, present tense, declarative, one
fact per sentence where possible. No marketing, no "seamless", no
exclamation marks, no second person outside checklists. Read a paragraph of the
AOH aloud: "The SECS is an integrated subsystem consisting of twelve
controllers." That flat confidence is the tone.

Structure the explanation around one idea: the sentence the reader must leave
with ("the machine brews at sea-level pressure inside a sealed circuit"; "matter
entering either aperture exits the other"). Put it in the introduction. Draw it in the hero figure. Let every
other block support it.

- **2.x.1 INTRODUCTION.** What it is, the key idea, a pointer to figure 2.x-1.
  Three lines.
- **2.x.2 FUNCTIONAL DESCRIPTION.** How it works, in the order things happen
  when it runs. Four lines. Points to figure 2.x-2.
- **2.x.2.1 Underlined mechanism.** The single most interesting mechanism,
  stated as a rule or formula, in two lines. Keep a formula on one line with
  `<span class="nowrap">`.
- **Controls** are named in caps exactly as placarded: BREW, APERTURE SEL,
  AGS MAIN A. Quote on-screen strings exactly, in quotes.
- **Numbers carry units.** Physical subjects: metric first with imperial in
  parentheses in text ("300 meters (984 feet)"). On drawings, only
  dimensions get dual units: inches first with millimetres in brackets
  ("27.60 [701]"), as US drafting did. Every other drawing label (pressure,
  temperature, power, rate) uses the single unit its gauge or spec reads
  ("0–12 BAR", "93 °C"). Software: the real constants from the code.
- **References**: lowercase in running text, "(figure 2.1-1)". Captions read
  `Figure 2.1-1.` then a Title Case caption. Table captions go above the table:
  `Table 2.1-1. Recording Format Data`.
- **Data table**: two columns, Parameter and Value, 6 to 8 rows. Pick the
  numbers a reader asks for first (size, rate, limits, capacity, timing).
  Values don't wrap.
- **Notice**: one per page, three lines at most, centered underlined tag.
  NOTE is information, CAUTION protects data or equipment, WARNING protects
  people. For fiction, a deadpan WARNING about the absurd failure mode is where
  the one joke goes.
- **Checklist card** (Flight Data File syntax): a black title bar with the
  procedure name on the left and who does it on the right. Then numbered
  steps: `CONTROL - action`, with the control in caps as placarded and the
  action in lowercase. Verification lines start with `√`, are indented and have
  no number. Use FDF abbreviations where they fit (cb circuit breaker, tb
  talkback, bp barber pole, rpt repeat). Six or seven lines, each at most 34
  characters, so the 64 mm card never wraps.

**Real subjects (a codebase, a product):** read the spec and the code first.
Grep every constant you print (sizes, limits, intervals, retries, key bindings,
UI strings) and use the code's numbers when the docs disagree. Name the files
you checked in your reply. A wrong number on a page this precise-looking is
worse than leaving the row out.

**Fiction:** keep it internally consistent. The table, the dimensions, the
schematic labels and the text must agree. Allow one or two nods to the source
(Portal's "speedy thing goes in": the momentum rule; moon rock: the caution),
always delivered straight. Original names beat borrowed ones: "Handheld
Aperture Projector, Project JANUS", not the game's trademark.

## 5. Choosing the figures

Two figures per page: a hero (66–72 mm viewBox height) and a secondary
(44–50 mm). The secondary may carry one or two "DETAIL A/B" insets on its right,
separated by a thin vertical rule. Choose by what the subject is:

| Subject | Hero figure | Good secondaries |
|---|---|---|
| Physical device | General arrangement: side elevation, callouts, dimensions, centerline, section view, axes | Functional or electrical schematic |
| Software or system architecture | Functional block diagram: dashed panels as process or trust boundaries, drums as storage, boxes as components, labelled wires | Timeline, sequence diagram, byte or part layout |
| Process over time | Timeline in flight-plan style: lanes, clock axis, events as dashed verticals | Sequence detail, state table |
| Protocol | Sequence diagram as a detail | Message or packet layout strip |
| Control or electrical system | Schematic: breakers, switches, bus bars, talkbacks, hex terminals | Panel layout |

Mapping software onto period symbols works well and reads instantly:
- Storage (databases, buckets, disks): drums, a cylinder with an elliptical top.
- Runtimes and boundaries (browser, cloud, device): dashed panels, with the
  name small at the top left inside.
- Data flow: wires with arrowheads, named in small caps on the wire.
- Fan-out: a vertical bus with junction dots.
- One-way tools or outputs: a column of boxes fed by a bus, headed by its
  trigger ("ON JOB COMPLETE").
- Time: a horizontal axis with major ticks every 10 units and minor every 2,
  events as dashed verticals, markers as small filled triangles.

## 6. Drawing with taste

Line weights, in millimetres on paper:

| Line | Width | Class |
|---|---|---|
| Object outline | 0.42 | `.o`, `.of` |
| Box outline | 0.45 | `.box` |
| Wire | 0.30 | `.w`, `.wa` |
| Section cut | 0.50, long-short dash | `.cut` |
| Thin detail, extension lines | 0.17 | `.t` |
| Leaders and dimension lines | 0.16 | `.ld`, `.dim` |
| Hidden line | 0.22, dashed 1.3/0.7 | `.hid` |
| Centerline | 0.16, dash-dot | `.cl` |

Arrowheads are small: 2.1 × 1.05 mm for leaders and 2.4 × 1.3 mm for wires.
Default SVG markers come out several millimetres long and look amateurish; the
template's markers are already sized.

Labels:
- Every label is caps Leroy. Name the things the text, table or checklist
  mention, plus whatever a curious reader would point at. Twelve to fourteen
  callouts is the ceiling for a hero drawing.
- Text is never crossed by any line. Start a leader just outside its label,
  at the end nearest the part, at least 0.6 mm clear of the letters. For a
  label below the part, the leader starts at or above baseline − 2.3 for
  `.lbl` (baseline − 2.0 for `.lbl-s`). For a label above the part, it starts
  0.8 or more below the baseline. Closer than that renders as touching. Run it
  straight to the part and end on an edge or inside the shape.
  Leaders may cross object lines; they must not cross other labels, other
  leaders, dimension lines or extension lines. When two leaders would cross,
  swap the labels' positions.
- If a label doesn't fit, move it or drop it. Don't shrink it below 2.05 mm.
- Group labels in calm rows above and below the object instead of scattering
  them. Align their left edges where you can.
- `(3)` after a name means three of them ("FIELD SHAPING PRONG (3)").

Dimensions: thin extension lines from the object, a dimension line with an
arrowhead only at each extension line, and the value centered in a gap in the
line: `27.60 [701]`. Vertical values are rotated to read bottom to top.

Schematics: dashed panel boundaries; junction dots where wires join and none
where they only cross; arrows show the direction of data or signal; breakers,
switches and talkbacks drawn with the period symbols (`references/svg-parts.md`).
Hex terminals only when the text refers to them by number.

Differentiate with pattern, not colour: 45° hatching for one category (video,
section cut faces, aperture B), plain outline for another, dotted outline for
absent or pending, and the stipple fill (`.grain`) for powder, granules or
packed material. Give each pattern one meaning per page: if hatching means
"cut face" in the hero figure, don't use it for coffee grounds in the
schematic. Explain each in a small legend if it isn't labelled in place.

Room above the top edge: when a part needs to rise above the figure's first
row (a breaker handle above a top wire, a title above a chart), start the
viewBox at a negative y (`viewBox="0 -3.6 180 50"`) rather than pushing
everything down. Keep the total height the same so the page budget holds.

Whitespace: let panels breathe 2–3 mm inside their border. Keep figure edges
aligned to the text column, and keep the right edge of figure codes on the
column's right edge.

Review every drawing at 300 dpi; `scripts/check.py` cuts half-width tiles at
about 12 px per mm. Most of the craft is fixing what only shows up there: a
leader through a word or touching it, two labels touching, a dimension value
sitting on its line, a marker on a tick label. Expect three to six
render-and-check passes before a page is clean.

## 7. Black and white only

The page is one-colour printing, like the original. Ink is pure `#000000` and
the printed paper is pure white. The template gives the screen a faint cream
paper and switches to white for print, because printers halftone any tint or
grey into a visible dot pattern (this happened on the first test print).
`check.py` fails if any other colour reaches the PDF. Hatching and the barber
pole pattern are fine: they are black lines on white.

## 8. Pitfalls already paid for

- **Print-media variable order**: `@media print { :root { --paper: #fff } }`
  must come after the `:root` block, or the screen colour wins and prints as
  dots.
- **`var()` in SVG attributes**: `fill="var(--paper)"` doesn't work in
  presentation attributes. Use `style="fill: var(--paper)"` or a class.
- **Markers**: use `markerUnits="userSpaceOnUse"` with explicit small sizes.
  For dimension lines put the marker only at the extension-line end
  (`marker-start` on each half of a split line); otherwise arrows point at the
  text.
- **Silent overflow**: `.page` has `overflow: hidden`, so an overfull page is
  clipped, not flagged. `render.sh` reads the template's fit check and exits 3
  on overflow; `check.py` works on the PDF and can't see it.
- **Local fonts**: Chrome needs `--allow-file-access-from-files` (in
  `render.sh`). The fonts folder must sit next to the HTML file.
- **Glyph coverage**: Routed Gothic lacks `≤ − ≈`; they fall back to Helvetica,
  which looks fine at label sizes.
- **Shared defs**: the template defines markers and patterns once in a hidden
  SVG (`nh-leader`, `nh-arrow`, `nh-dim`, `nh-hatch`, `nh-bp`, `nh-dots`).
  Use them; don't add per-figure markers or redefine the ids.

## 9. Variants and other NASA genres

- **US Letter** (the AOH's real size): set `@page { size: letter }`, make
  `.page` 215.9 × 279.4 mm and trim about 17 mm from the budget (usually the
  secondary figure). `render.sh` detects `size: letter`.
- **Multi-page sections**: repeat the head, tab and footer on every page.
  Number pages `2.1-1`, `2.1-2`. A large drawing may take a whole page with only
  its caption, as the AOH foldouts did. Keep figure and table numbering running
  through the subsection.
- **Controls and displays page**: replace the figures with a panel drawing
  (grid-referenced) and a tabulated list (Location, Name and Position, Function,
  Circuit Breaker, Power Source).
- **Engineering drawing sheet**: landscape, border with zone letters and
  numbers, title block bottom right (title as "NOUN, MODIFIER, MODIFIER —
  TYPE", drawing number, scale, sheet), revision block top right, a NOTES list
  ("1. INTERPRET DRAWING PER …", "UNLESS OTHERWISE SPECIFIED DIMENSIONS ARE IN
  INCHES"), all lettering in Leroy.
- **NASA Technical Note cover** (1960s): large "NASA TECHNICAL NOTE", report
  number (`NASA TN D-1234`), title in caps, authors, a center line
  ("NATIONAL AERONAUTICS AND SPACE ADMINISTRATION · WASHINGTON, D. C. · JUNE
  1965"), set in a Times-like serif.
- **1975 Graphics Standards era**: Helvetica Light text with Helvetica Medium
  headings, flush left and ragged right, outline boxes around technical
  diagrams, one or two spot colours (NASA red). Only when the user asks for
  that look; never draw the worm.
