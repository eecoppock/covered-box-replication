# Covered-box demo — Huang, Spelke & Snedeker (2013), Experiment 1

Huang, Y. T., Spelke, E., & Snedeker, J. (2013). What exactly do numbers mean?
*Language Learning and Development* 9(2), 105–129.

[doi:10.1080/15475441.2012.658731](https://doi.org/10.1080/15475441.2012.658731)

Built for LX 433/533/733 Experimental Pragmatics at Boston University, where the
class runs it on themselves the day the paper is read.

**This is the in-class demonstration, not the graded replication.** The written-up
replication is Panizza, Chierchia & Clifton (2009) Exp. 1, whose forced choice
between *exactly two* and *at least two* is the same on every screen and so needs
no decoding step before the analysis can start. The covered box is here because
it is the paradigm worth *seeing* — the inference is visible in where your hand
goes — and because the two studies disagree in an interesting way about whether
numerals behave like *some*. Running it takes about eight minutes and gives the
class its own data to argue with while reading the paper.

Everything here is generated from the two scripts. The stimuli are original and
generic, so nothing in this repository is anyone else's copyright.

## The question and the result

Three boxes on each trial: two open, one covered. *Give me the box where Zip has
some of the cookies*, or *Give me the box where Tev has two of the fish*. On
**critical** trials the subset or exact match is absent, so anyone holding out
for it must take the covered box.

This repository targets their **Experiment 4**, the online-adult version; see
the design section for why. Both experiments are given here because the gap
between them is itself part of what the class should see.

| critical trial | Exp 4 adults, n = 25/cell | Exp 1 adults, n = 10/cell |
|---|---|---|
| some(NONE, ALL) | **31%** took the covered box | **13%** |
| two(1, 3) / two(1, 3∨5) | **92%** | **100%** |

Either way the contrast is large: *some* and *two* are not the same kind of
meaning, in a population that computes scalar implicatures robustly elsewhere.
But their own scalar rate moved eighteen points between two of their own
designs, which is worth knowing before arguing about whether a class-sized
replication succeeded.

## Files

| | |
|---|---|
| `design.py` | the trial assignment, imported by both generators |
| `make-stimuli.py` | writes the box images to `stimuli/` — one image per box |
| `build-qsf.py` | writes `HuangSnedeker_replication.qsf` and `columns.txt` |
| `qsf-template.json` | Qualtrics boilerplate, vendored so the build has no outside dependencies |
| `coveredbox-critical.R` | **the analysis.** Carries the preregistered rule at the top |
| `columns.txt` | response columns in survey order — the contract between the two |
| `archive/` | the designs that have been run or built and dropped, with their data |
| `coveredbox-rep.R` | superseded. Analyses the pre-17-Sept instrument; kept for the archived intro-class data |
| `make-fake-data.R` | superseded. Writes the old column shape |

Everything is generated. Change the constants at the top of `make-stimuli.py`
(counts, colours, names) and rerun; nothing is hand-drawn.

**Look at `index.html` after every regeneration.** `make-stimuli.py` rewrites it
as a contact sheet of every image. Both stimulus bugs found so far — birds drawn
~90px wide against 38px grid spacing, so four of them smeared into an
uncountable pile and *Bix has all of the birds* had no readable answer; and a
probe naming leaves against boxes of flowers — were invisible in the code and
obvious in one glance at that page. Objects are now normalised to a ~36px
footprint against 46px spacing, but the check is cheaper than the reasoning.

## Getting the images into Qualtrics

Each trial is a multiple-choice question whose three **answer choices are the
box images**. Qualtrics randomises choice order, which counterbalances the
covered box's position for free, and the export records *which box* was chosen
rather than which position. That is why the stimuli are one-image-per-box rather
than one composite per trial.

**This is already done.** The stimuli are served from this repository, and
`HuangSnedeker_replication.qsf` points at them, so the survey works the moment
it is imported — nothing to upload to the Qualtrics graphics library, no
placeholders to swap. All 26 referenced URLs were checked and resolve.

The base URL currently in the QSF is **raw.githubusercontent**:

> `https://raw.githubusercontent.com/eecoppock/covered-box-replication/main/stimuli`

GitHub Pages is also enabled and `index.html` is a contact sheet of all 30
images, but the Pages build has not gone green. If it does, switch with

```
python3 build-qsf.py https://eecoppock.github.io/covered-box-replication/stimuli
```

Either host is fine at this scale: about 1,500 image requests for a class of 40,
cached after the first participant. Raw URLs are pinned to the `main` branch, so
renaming the branch would break them.

To point somewhere else entirely, pass any base URL:
`python3 build-qsf.py https://your.url/stimuli`.

The reason this matters: a QSF cannot reference images in a Qualtrics library,
because their IDs do not exist until upload. Hosting them sidesteps that
entirely — otherwise it is 22 questions × 3 choices of manual insertion.

## Design: Huang et al.'s Experiment 4

Rewritten **17 September 2026**. Everything this repository had added was
removed, and the instrument now follows their **Experiment 4**, which of their
four is the closest to what a class can run in Qualtrics.

### Why Experiment 4 and not Experiment 1

Experiment 1 put trial type between subjects as well as term: sixty
undergraduates in six cells of ten, and *"this ensured that adult responses
reflected a naïve understanding of the sentences rather than any inferences
about the study that might emerge by comparing different trial types."* A
participant saw three tokens of one trial type and **no fillers at all**.

Experiment 4 keeps only the critical trial types, so everyone is in the cell
that matters. It was run on fifty adults over Mechanical Turk rather than in a
lab, which is far nearer to a survey link. And the three critical tokens *"were
randomized with three filler trials that were similar to those used in the
Familiarization phase."*

It also rebuilds the number trials so the two conditions look alike: Cookie
Monster with 1 of 4 cookies against Cookie Monster with 3 of 4, asked as *give
me the box where Cookie Monster has two of the cookies*, because *"these
configurations ensured that the items in each box were matched for complexity
across the scalar and number conditions."* Their number trials are the same
two-character possession display as the scalar ones, not a bare count of fish.

Their adult results there: `some(NONE,ALL)` covered box **31%**, total set 60%;
`two(1,3)` covered box **92%**, lower-bounded option 7%. Note that 31% against
the 13% of Experiment 1, on the same trial type. Their own scalar rate moved
eighteen points between two of their own designs, which is worth showing a class
before anyone argues about whether ours replicates.

### What runs now

| | |
|---|---|
| 0 | **welcome and consent**, text only |
| 1–4 | familiarization, pass 1, each followed by a feedback screen |
| 5–8 | familiarization, pass 2, no feedback |
| 9 | filler, answered by an open box |
| 10 | `some(NONE,ALL)` — cookies |
| 11 | filler, answered by an open box |
| 12 | `some(NONE,ALL)` — apples |
| 13 | filler, answered by the **covered** box |
| 14 | `some(NONE,ALL)` — balloons |
| 15 | filler, open box |
| 16 | `two(1,3)` — fish |
| 17 | filler, open box |
| 18 | `two(1,3)` — birds |
| 19 | filler, **covered** box |
| 20 | `two(1,3)` — flowers |
| 21 | first language, optional |
| 22 | **BU Kerberos ID**, required |
| 23 | may your responses be analysed? |

Twenty-eight screens counting the welcome and the four feedback pages, of which each participant sees one of the two object assignments. The number block is interleaved the same way the scalar block is: Exp 4's number condition had its three fillers too, and this block runs last, where extinction pressure is highest and where there would otherwise be no covered-box trial for six screens. Response **3** is the
covered box throughout, and its position rotates across trials.

**Every box in the study is the same display**: two named characters either side
of a divider, four objects split between them. Familiarization and fillers
included. The shape panels are gone. A participant who has practised on floating
coloured triangles has not practised the task, and with the probe removed the
familiarization is the only thing establishing that the covered box is ever the
answer, so it has to be the same shape as the thing it prepares for.

Familiarization and fillers ask with a **bare indefinite** — *give me the box
where Ral has a carrot* — and two rules hold across every practice box, both
asserted by `pbox()` in `design.py`.

**Nobody holds two of the same kind.** That is what keeps the indefinite off a
scale: *a heart* is underinformative against two hearts, not against a heart and
a leaf. Characters may hold several *different* objects, so the practice
displays vary in shape and the step up to four objects on a test trial is
smaller.

**The two characters hold disjoint kinds**, with one deliberate exception below.
Hearts on both sides of the divider make a harder discrimination but an
avoidably confusing display when the question is about one person, and the
possession swap between the two boxes already forces attention to who has what.
Note this is one way the practice differs from the criticals, where both
characters do share a kind.

The exception is `fill2`, *give me the box where both Vex and Pol have a heart*,
whose near-miss box gives a heart to one of them only. Overlap confuses a
question about one character and is the content of a question about two. It is
the only trial that forces a check of both sides and of how the objects are
distributed, which is what the critical trial demands when Zip has all the
cookies and Nub has none. *Both* is a maximal quantifier, and the last maximal
quantifier in a practice trial cost us the experiment, but `anchorAll`
quantified over **the cookies**, the same domain the critical asks about, while
this quantifies over the two characters, where there is barely a scale. The
conjunction phrasing, *where Vex has a heart and Pol has a heart*, is the
zero-risk version if it ever looks worth taking.

No practice box shares a configuration with a test trial: the scalar criticals
use 0 of 4 and 4 of 4, the number criticals 1 of 4 and 3 of 4, and no practice
character holds more than one of anything.

### The welcome screen

Screen one is a text-only consent screen, written around the standard elements:
what it is, how long, voluntary, risks, benefits, what happens to the data, whom
to ask. **It is a draft and has not been reviewed by anyone at BU.** Check it
against whatever the CRC actually asks for before treating it as a consent form,
and note that a class demonstration run for teaching rather than for
generalisable knowledge may not meet the definition of human subjects research
at all, in which case the language is good practice rather than a requirement.

The tension it is written around is real and worth naming: **HW 3 is graded
check-or-zero, and consent that a grade depends on is not voluntary.** The
resolution is to separate the two things. The check is for taking part in the
class activity, which the Kerberos ID records. A separate question at the end,
`data_use`, asks whether the responses may be included in the class analysis,
and the welcome screen promises that saying no there does not affect credit.
`coveredbox-critical.R` honours that: the completion check counts everyone, and
the exclusion happens afterwards.

The text-only question type is vendored from the Rohde replication in this
course, which uses one for its own intro screen. Same rule as the others: clone
a type that has imported, never invent one.

### The identifier

The survey ends with a **required** free-text Kerberos ID, placed after
everything including the optional language question so it cannot colour a single
response. It is the roster's `coder` column, so `coveredbox-critical.R` joins
straight onto `Roster/roster-merged.csv` and prints who has not taken it by
name, plus any ID that matches nobody and anyone who took it twice. The grading
matters less than the gap: at twelve participants the identity of the person who
did not take it is worth chasing the same afternoon.

The free-text question type is **vendored into `qsf-template.json` from
`Homework/hw4-form.qsf`**, which is a real export from the same account that
contains one. The standing rule in this repository is never to invent a
Qualtrics question type, because an invented one fails the import with no
diagnostic beyond *"Something went wrong and the project wasn't created."*

### Counterbalancing, and what is still confounded

**Object set is counterbalanced against the term.** Half the participants get
the scalar trials on cookies, apples and balloons and the number trials on fish,
birds and flowers; the other half get the reverse. A block randomiser picks one
and stamps `objects` as embedded data, so the assignment is recorded rather than
inferred. Huang et al. did not need this: Experiment 4 was between subjects and
used Cookie Monster with cookies in both conditions. We separated the objects so
that the same participant does not meet the same material twice under two
different prompts, and that separation would otherwise have left object set
perfectly confounded with the term. Counterbalancing costs nothing, since every
participant still does three scalar criticals and the replication comparison
keeps everyone.

**Order is not counterbalanced, and this is a trade-off rather than an
oversight.** Scalar always runs first. Counterbalancing would mean half the
participants meet *two* before *some*, and the scalar cell is the measurement;
its value depends on those people being naive about the task's quantity
dimension. We bought a naive scalar cell at the price of an order confound in
the *some*-against-*two* contrast. The confound runs conservative: the number
block sits last, where extinction pressure is highest, so any order effect
should depress the number rate and pull it toward the scalar rate, working
against the asymmetry rather than for it.

**Two things are going on in this study and they are not the same kind of
claim.** The *some*-against-*two* contrast is the experiment: same people, same
session, same displays, one word changed. The comparison of our scalar rate
against Huang et al.'s 31% is a replication check, not an experiment, because
everything varies between us and them — population, platform, year, sample size
— so it isolates no cause. It is what the preregistered rule is about, since
"did removing the anchor recover their result" is the question, but preregistered
is not the same as experimental, and a write-up should not blur them.

**Smaller departures.** Both terms go to the same participant, which their
between-subjects design forbids; it buys the class the contrast and is the
reason order is confounded at all. The six test screens in each block are
interleaved in a fixed order rather than randomized, so every critical has a
filler before it and the covered-box filler falls late. Feedback on the first
familiarization pass is a screen saying where the target was, since Qualtrics
cannot let anyone open a box.

### What was removed, and why

`anchorAll`, `probeEarly`, `probe`, `criticalOneSet`, the shape fillers, and the
four control trial types. Each was defensible alone; together they put nine
quantity questions in front of every participant before the block was over,
which is the comparison across trial types the authors designed against.

The intro-class run of 2–3 September, on that instrument, gave a scalar critical
rate of **81%**, with familiarization at 35/35 and the probes at 35/35, 35/35,
35/35 and 34/35. Block order did not explain it, since scalar-first participants
were at 78%, and the domain did not either, since `criticalOneSet` came out at
83% like the rest. Design, data and numbers are in `archive/2026-09-intro-run/`.

The first suspect was `anchorAll`, whose boxes were `SOME` and `ALL` and whose
prompt asked for *all*, so the participant had to discriminate the two displays
and label the fuller one two screens before being asked about *some*. A
replacement asking for *half* was built and dropped within the hour, because an
anchor about proportions makes *what proportion does he have* the question under
discussion, which promotes the very inference the paradigm exists to cancel.
That version is in `archive/2026-09-anchorhalf-superseded/`.

The rule the episode produced, worth applying to anything added later: **a trial
whose correct answer is the covered box teaches the covered box and nothing
else; a trial whose correct answer is an open box teaches a mapping from a
quantifier word to a picture, and participants generalise it.**

### The preregistered test

About twelve participants, all in the scalar critical cell, tested against
Experiment 4's **.31** with an exact binomial, the participant as the unit:

| covered box, of 12 | rate | p vs .31 |
|---|---|---|
| 0 | 0% | .023 |
| 4 | 33% | 1.00 |
| 6 | 50% | .21 |
| 7 | 58% | .057 |
| **8** | **67%** | **.012** |
| 10 | 83% | .0003 |

**Fewer than eight of twelve and we have not separated from them. Eight or more
and we have.** Power is 96% against a true rate of .83, which is what the intro
class produced, 58% against .65 and 30% against .55; the middle of the range is
out of reach at this sample size, which is a limitation to state rather than
discover. The rule lives at the top of `coveredbox-critical.R` and should be on
the board before anyone opens the survey.


### Stripping the institutional branding

A QSF exported from an account that has a brand carries its ID in
`SurveyOptions.Skin.brandingId`, and the survey then renders with the
university's header, colours and logo. Setting that field to `null` leaves the
plain `*simple` theme, which is what this survey uses.

It is the **only** field that matters. Everything else in Survey Options is
identical between a branded and an unbranded export, `SkinLibrary` included —
that is the account's library namespace, not anything a participant sees.
Established 18 Sept 2026 by diffing against an unbranded export made by hand in
Qualtrics, kept in `qualtrics draft export/`.

`build-qsf.py` sets the field to `null` on every build as well as in
`qsf-template.json`, so re-vendoring the template from a fresh export cannot
quietly bring the branding back.

### A note on hand-writing QSFs

Qualtrics rejects a malformed import outright, with no diagnostic beyond
*"Something went wrong and the project wasn't created."* So the survey is not
constructed from scratch: `CoveredBoxtest.qsf` is a real export from the same
account containing exactly the question type needed — a horizontal multiple
choice between graphic options — and `build-qsf.py` clones it, replacing only
the questions, blocks and flow. Every other element is carried over untouched.

Two details that cost several failed imports:

- Graphic choices need `Configuration.LabelPosition = "BELOW"`.
- Blocks carry **no `Options` key at all** — not `Options: null`, absent.

Also: build from an export of *this* account. An earlier version borrowed
boilerplate from a different survey and inherited its `SurveyOwnerID`, brand
ID, and a `BallotBoxStuffingPreventionMessageLibrary` pointing at that survey's
message library.

`python3 build-qsf.py <base-url> --test` writes `_import-smoke-test.qsf`, two
questions in one block with no randomiser. If a full import ever fails again,
try that first: it separates "the structure is wrong" from "something in the
bulk is wrong".

## One thing the analysis will hit, and it is worth a paragraph

*(Written for the old instrument. The separation point still holds, but `coveredbox-critical.R` fits no model at all: with one cell and a published benchmark the test is an exact binomial.)*

The number condition sits at or near **100%**, so a logistic model of the
critical trials is **completely separated**: no finite log-odds describes the
difference, the estimate runs to infinity, and the standard error with it. R
reports an enormous coefficient with a p-value near 1, which looks exactly like a
null result and is the opposite of one. `coveredbox-rep.R` detects this and skips
the model rather than printing nonsense. The effect is not too small to estimate.
It is too large.

On the fake data the Mann–Whitney (Huang et al.'s own test) gives
p ≈ 4 × 10⁻⁸ with 19 and 17 participants.

## Revised 2 Sept 2026 — within subjects, and shorter

*(Superseded by the 17 September rewrite above. Kept because the two problems it describes are real and would come back if the trial list ever grows again.)*

Taking it revealed two problems. The critical/filler alternation was perfectly
regular, so the critical trials were predictable; and all four visible-answer
controls sat at the end, so the covered box was live for a run of trials and
then dead for a run of trials. Both are fixed: controls are now interleaved
among the critical trials, and the gaps between critical trials are uneven
(positions 3, 6, 10).

**Everyone now sees both terms**, in a randomised order recorded as `first_term`
embedded data. Blocks are 11 trials instead of 14 — three critical trials rather
than four, since with a ~90-point effect the fourth bought nothing and the slot
is worth more as camouflage. 27 questions total.

**The first block is the replication.** The pooled scalar rate is contaminated:
half the participants met the numerals first, and that exposure should push
*some* toward an exact reading. `coveredbox-rep.R` reports scalar-FIRST against
Huang et al.'s .13, then the order effect, then the within-subjects paired test.
First-block data is also poolable with data collected under the old
between-subjects version.

The flow uses a randomiser over two **Groups**, each stamping `first_term`
before running its blocks — not a `Branch`, which has been the fragile part of
every QSF in this project.

## Still to do

- Choice-order randomisation is off on every question and the covered box is
  always choice 3. Not a threat to the between-condition comparison, since the
  position is constant across terms, and the covered box is identified by its
  image rather than its slot. Worth fixing anyway.
- The shape fillers still announce themselves — different syntax, no character
  name, a different visual world. Frame-matched fillers (*the box where Dax has
  the striped balloon*: same frame, same objects, no quantifier) would camouflage
  properly, but need new images.
- The bird drawing is passable but not lovely; `make-stimuli.py::bird` is where
  to fix it.
