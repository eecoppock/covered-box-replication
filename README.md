# Class replication — Huang, Spelke & Snedeker (2013), Experiment 1

Huang, Y. T., Spelke, E., & Snedeker, J. (2013). What exactly do numbers mean?
*Language Learning and Development* 9(2), 105–129.

[doi:10.1080/15475441.2012.658731](https://doi.org/10.1080/15475441.2012.658731)

Built for LX 433/533/733 Experimental Pragmatics at Boston University, where the
class runs it on themselves in the first fifteen minutes of the first meeting —
before anyone has been told what it measures — and then writes it up.

Everything here is generated from the two scripts. The stimuli are original and
generic, so nothing in this repository is anyone else's copyright.

## The question and the result

Three boxes on each trial: two open, one covered. *Give me the box where Zip has
some of the cookies*, or *Give me the box with two fish*. On **critical** trials
the subset/exact match is absent, so anyone holding out for it must take the
covered box.

| critical trial | covered box chosen |
|---|---|
| some(NONE, ALL) — boxes show none and all | **13%** — adults accepted *all* as a match for *some* |
| two(1, 3∨5) — boxes show one and three | **100%** — adults held out for exactly two |

An 87-point contrast at n = 10 per cell. *Some* and *two* are not the same kind
of meaning, in a population that computes scalar implicatures robustly elsewhere.

## Files

| | |
|---|---|
| `design.py` | the trial assignment, imported by both generators |
| `make-stimuli.py` | writes the box images to `stimuli/` — one image per box |
| `build-qsf.py` | writes `HuangSnedeker_replication.qsf` and `columns.txt` |
| `qsf-template.json` | Qualtrics boilerplate, vendored so the build has no outside dependencies |
| `make-fake-data.R` | writes `coveredbox-fake-data.csv` in real-export shape |
| `coveredbox-rep.R` | the analysis; runs on fake or real data |
| `columns.txt` | response columns in survey order — the contract between the two |

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

## Design, and where it departs from the original

- **Term** (scalar / number) is **between subjects** — one block randomiser.
- Within a term, the **three critical trials come first**, then the six control
  trials. Huang et al. put trial type between subjects too, so that nobody could
  infer the design by comparing trial types; at class scale that would mean six
  cells of five. Critical-first preserves naïvety where it matters, at the cost
  of a fixed order. Say so in the report.
- **Fifteen screens per participant**: four familiarization, then Huang et al.'s
  three test conditions in full, our added `criticalOneSet` condition, an anchor,
  two probes, two fillers. This is their design plus additions, not a subset of
  it. Order per participant:

  | | | |
  |---|---|---|
  | 1 | `allVis` | *…has **all** of the cookies* — anchors the domain |
  | 2 | `probeEarly` | *…has **none** of the apples* — covered box; breaks the *all*/*some* adjacency |
  | 3–4 | `critical` ×2 | Huang et al.'s critical trials |
  | 5–6 | `criticalOneSet` ×2 | ours: the domain loophole closed |
  | 7 | `matchVsMore` | H&S |
  | 8 | `matchVsLess` | H&S |
  | 9–10 | fillers | *none*, *all* |
  | 11 | `probe` | covered box again, under maximum extinction pressure | Each has its own object and characters,
  so every prompt in the survey is distinct.

  Why so few, and why this split. Simulated power for the critical contrast is
  **1.00 even at eight participants per term giving one critical trial each** —
  an 87-point effect needs no replication inside a participant. Extra trials buy
  item generality and a graded per-participant rate, so they go where the
  argument is. `N_TRIALS` at the top of `design.py` sets the allocation.

  | role | trials | what it does |
  |---|---|---|
  | **anchor** — an *all* trial, **first** | 1 | fixes the domain, see below |
  | **critical** — (NONE,ALL) / (1, 3∨5) | 2 | the headline: no match visible, so anyone insisting on one must take the covered box. 13% vs 100%. |
  | **matchVsMore** — (SOME,ALL) / (2, 3∨5) | 1 | *not* a comprehension check. Both a subset and a total set are visible and adults take the subset 90% of the time — Huang et al. call this "a robust ability to calculate the scalar implicature". It is what makes the critical result strange: the implicature is computed when it picks something out and abandoned when it does not. |
  | **criticalOneSet** — (EMPTY,ALL), scalar only | 2 | **ours.** The same question with the domain loophole closed — see below |
  | **matchVsLess** — (NONE,SOME) / (1, 2) | 1 | the comprehension check: *some* is not *none*, *two* is not *one*. At ceiling in the original. |
  | **otherQuant** — *none*/*all*, *three*/*five* | 2 | balance, see below |
  | **probe** | 1 | see further below |

  The names describe which two open boxes are shown, relative to the **match** —
  the box satisfying the description on the strengthened reading (a proper
  subset / exactly two). `critical` shows neither a match nor anything like one;
  `matchVsMore` pairs the match with a larger set; `matchVsLess` pairs it with a
  smaller one.

### The added condition: `criticalOneSet`

Huang et al.'s critical display leaves the global reading available. One box has
the target with none of four objects, the other has the target with all four, so
eight are on screen — and the target holding four of eight *is* "some but not
all" globally. A participant can take that box with the exclusive reading of
*some* intact.

Ours closes it. One open box holds **every object on screen** and the other holds
**none**, so the global set and the box-internal set coincide:

| | reading | answer |
|---|---|---|
| Huang et al. | exclusive *some*, box-internal | covered |
| | exclusive *some*, **global** | **the full box** ← loophole |
| ours | exclusive *some*, either domain | covered |
| | lower-bounded *some*, either domain | the full box |

So the two conditions differ **only** in whether the global reading is available,
and the gap between their covered-box rates measures how much of the standard
result that reading was buying. If they agree, it was buying nothing. The
analysis prints them side by side.

**Scalar only.** *The box with two birds* has no partitive and so no domain
ambiguity — it counts within a box by construction. Giving the number term an
equivalent would just be the standard critical with a `0` where the `1` goes:
no loophole closed, and a blank white box that reads as an image that failed to
load rather than as a box containing nothing. The number term gets four critical
trials instead, and no empty boxes.

The scalar EMPTY panel has no such problem, because it still shows both
characters — just with nothing above them.

### The anchor, and the domain of "the apples"

*Give me the box where Zip has some of the apples* leaves open what **the
apples** ranges over. The apples in the box under consideration, or the apples
anywhere on screen?

It matters, because the global reading is a **complete alternative account of
the headline**. On a critical trial the ALL box shows the target with four of
the eight apples visible. Read globally that *is* "some but not all" — so a
participant can take the ALL box with the exclusive reading of *some* entirely
intact, and 87% choosing it would say nothing about whether the implicature was
computed.

The first trial therefore asks for the box where the target has **all** of the
objects, which separates the readings:

| domain | correct answer |
|---|---|
| box-internal | the **ALL** box — the target has all four in that box |
| global | the **covered** box — no box has all eight |

Putting it first settles the question before any *some* trial is seen, and
because the task presupposes an answer exists, meeting *all* first pushes toward
the only construal on which one does. The response is also **recorded**:
`coveredbox-rep.R` reports how many read the domain box-internally, warns if
scalar participants fall below 85%, and splits the critical rate by it.

The cost is that a trial with a visible answer now precedes the critical ones,
which cuts against critical-first. Familiarization already shows two
visible-answer trials and two requiring the covered box, so this adds little —
and the domain confound explains the whole finding away, where extinction only
biases it in a direction the probe measures.

The number term has no partitive and so no domain ambiguity: *the box with two
fish* counts within a box by construction. Its anchor is there to keep the two
versions the same length and shape.

### Fillers in another quantifier

Without them the scalar term says **some** on five screens out of six and
*none* on one. That is an odd thing to put in front of someone you are asking to
interpret quantifiers: the recurring word invites theorising about it. The
number term had the same problem with *two*.

Two fillers per term restore the balance — *none* and *all* for scalar, *three*
and *five* for number — and cost nothing, because the answer is always a visible
box. They double as a check that participants are tracking the quantifier rather
than the display: `noneVis` and `noneSome` use the very same pair of boxes and
have opposite correct answers.

Quantifier counts per participant are **some 3 / none 2 / all 1** and
**two 3 / three 1 / five 2**, against 5/1/0 before the fillers existed.

**On priming.** Putting *all* in front of a participant should if anything
*increase* implicature computation, since activated alternatives are what drive
*some* → *not all*. That pushes toward the covered box — **against** the finding
that adults accept the total set as a match for *some*. So the manipulation is
conservative: if the lower-bounded reading survives with *all* made salient,
that is stronger evidence, not weaker. The fillers sit after the critical trials
in any case.

The number fillers name the **larger** visible count, never the smaller. *Three*
against boxes of 1 and 3 has one right answer on any semantics; *three* against
1 and 5 would let a lower-bounded participant answer with the 5.

  Object sets are *nested* in trial type, not crossed with it.

  Crossing them was the first attempt and it was wrong. Huang et al. could
  cross safely because trial type was between subjects, so a participant met one
  trial type with three different objects. Run within subjects and crossing puts
  the same object under the same prompt three times — and two of those three
  show the very same box, so they read as duplicates. `design.py` holds the
  assignment, and both the stimulus generator and the QSF builder import it, so
  they cannot drift.
- **Familiarization**: four trials, each naming a **different** shape — red star,
  green triangle, purple hexagon, orange square — visible twice, hidden twice.
  Huang et al. ran theirs **twice**, eight trials with feedback on the first
  pass; this is a single pass with none, because Qualtrics cannot easily give
  feedback. That matters — see the probe.

### The probe, which is not in the original

In **none** of Huang et al.'s trial types is the covered box unambiguously
correct. It is always the diagnostic option. So the only thing establishing that
it is ever the right answer is familiarization — and a participant who reads
*some* as lower-bounded then never needs it again for the rest of the study.

If the covered box goes dead for them, a low covered-box rate on critical trials
is **extinction, not semantics**, and nothing in the original design can tell the
two apart. Weakening familiarization to a single pass, as above, makes this more
likely rather than less.

The probe puts an absent *configuration* in front of the participant while
keeping every presupposition satisfied except the one the paradigm runs on.

| term | boxes | prompt | why the covered box is right |
|---|---|---|---|
| scalar | Kel has **some** of the flowers / Kel has **all** of them | *Give me the box where Kel has **none** of the flowers.* | neither shows Kel with none |
| number | **1** flower / **2** flowers | *Give me the box with **five** flowers.* | absent under exact semantics *and* under lower-bounded |

Getting the absence in the right place took two tries, and the failures are
instructive.

The task already turns on one presupposition failure: *the box with two fish*
presupposes such a box exists, and when none is visible the inference is that it
is hidden. That is the paradigm.

An earlier probe asked for *some of the **hearts*** against boxes of flowers.
That fails a **different** presupposition — the restrictor's. *The hearts*
presupposes a salient set of hearts and there is none. A failed restrictor
invites **repair** ("they must mean the flowers") rather than the inference that
the referent is hidden, so the trial would have measured repair behaviour instead
of whether the covered box is live. Before that, an offset picked *leaves*
against flowers, which is not unmistakably absent at all.

The number probe asks for **five** rather than three for a specific reason. Ask
for three against boxes of 1 and 5 and a lower-bounded participant can answer
with the visible 5, since 5 ≥ 3 — and the lower-bounded participants are exactly
the ones whose covered box we doubt. A probe they can satisfy with an open box
is no probe. Five against 1 and 2 is absent on either semantics.

**The critical trials are bracketed by real covered-box demands**, not just by
familiarization. `probeEarly` sits immediately before them and `probe` after
everything; familiarization trials 3 and 4 come earlier still.

`probeEarly` earns its slot twice over. Without it the anchor asks who has
**all** of the cookies — answer, the full box — and the very next screen asks who
has **some**, where the lower-bounded answer is again the full box. Choosing the
same configuration for *all* and then *some* on consecutive screens all but
demonstrates the equivalence under test. It also re-establishes the covered box
at the point where extinction would actually bite, which is before the critical
trials rather than after them.

Priming the covered box pushes toward implicature computation and therefore
*against* the finding that adults accept the total set as *some* — conservative,
the same shape of argument as for putting *all* first. So the question "was it live while it mattered?" is answered on both
sides.

The probe is deliberately last rather than immediately after the critical
trials. By then five trials have gone by in which no covered answer was ever
correct — two critical, where most scalar participants take an open box, then
three controls where a match is always visible. Extinction pressure is at its
highest exactly there, so passing the probe at the end is *stronger* evidence
than passing it earlier would be. It is a conservative test.

Putting a probe *before* the critical trials was considered and rejected: a
participant who has just chosen the covered box is likelier to choose it again
on the very next screen, which is the one that matters. Familiarization already
does that job, at a safe distance.

`coveredbox-rep.R` reports the front of the bracket (fam3 and fam4, over **all**
completed responses — among the included it is 100% by construction and says
nothing) and the probe pass rate by term, warning below 80%. Whether to exclude
on the probe is a judgment the report should argue rather than assume. Huang et al. gave feedback on the first pass; Qualtrics
  cannot easily, so instead these serve as the exclusion criterion. Current rule
  is all four correct; 3/4 is defensible if recruitment is tight.

Response codes: **1** = first open box · **2** = second open box ·
**3** = the covered box. Choice IDs are stable whatever order the boxes are
displayed in; what 1 and 2 mean varies by trial type, so `build-qsf.py` writes
**`choice-map.csv`** and the analysis reads it instead of hard-coding anything.
The measure of interest is the rate of **3** on critical trials.

The covered box's position is counterbalanced **by hand** — across the three
tokens of each trial type it appears first, second and third. Qualtrics can
randomise choice order, but no QSF available here demonstrated that structure,
and an unverified guess costs the whole import. Fully balanced beats randomised
anyway at three tokens.

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

The number condition sits at or near **100%**, so a logistic model of the
critical trials is **completely separated**: no finite log-odds describes the
difference, the estimate runs to infinity, and the standard error with it. R
reports an enormous coefficient with a p-value near 1, which looks exactly like a
null result and is the opposite of one. `coveredbox-rep.R` detects this and skips
the model rather than printing nonsense. The effect is not too small to estimate.
It is too large.

On the fake data the Mann–Whitney (Huang et al.'s own test) gives
p ≈ 4 × 10⁻⁸ with 19 and 17 participants.

## Still to do

- Import and check: two blocks per term should appear in the right order, and
  choice-order randomisation should be on for every trial question.
- The bird drawing is passable but not lovely; `make-stimuli.py::bird` is where
  to fix it.
