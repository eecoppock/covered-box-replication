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
| `make-stimuli.py` | writes 30 box images to `stimuli/` — one image per box |
| `build-qsf.py` | writes `HuangSnedeker_replication.qsf` and `columns.txt` |
| `qsf-template.json` | Qualtrics boilerplate, vendored so the build has no outside dependencies |
| `make-fake-data.R` | writes `coveredbox-fake-data.csv` in real-export shape |
| `coveredbox-rep.R` | the analysis; runs on fake or real data |
| `columns.txt` | response columns in survey order — the contract between the two |

Everything is generated. Change the constants at the top of `make-stimuli.py`
(counts, colours, names) and rerun; nothing is hand-drawn.

## Getting the images into Qualtrics

Each trial is a multiple-choice question whose three **answer choices are the
box images**. Qualtrics randomises choice order, which counterbalances the
covered box's position for free, and the export records *which box* was chosen
rather than which position. That is why the stimuli are one-image-per-box rather
than one composite per trial.

**This is already done.** The stimuli are served by GitHub Pages from this
repository, and `HuangSnedeker_replication.qsf` points at them:

> https://eecoppock.github.io/covered-box-replication/stimuli/

So the survey works the moment it is imported — no uploading to the Qualtrics
graphics library, no swapping placeholders. A contact sheet of all 30 images is
at the [Pages root](https://eecoppock.github.io/covered-box-replication/).

To point it somewhere else, pass a base URL:
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
- Three tokens per trial type, with different characters and objects (cookies,
  apples, balloons; fish, birds, flowers).
- **Familiarization**: four trials, *Give me the box with the red star* — visible
  twice, hidden twice. Huang et al. gave feedback on the first pass; Qualtrics
  cannot easily, so instead these serve as the exclusion criterion. Current rule
  is all four correct; 3/4 is defensible if recruitment is tight.

Response codes are uniform across every trial:
**1** = the "less" box · **2** = the subset/exact match · **3** = the "more" box ·
**4** = the covered box. The measure of interest is the rate of **4** on critical
trials.

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
