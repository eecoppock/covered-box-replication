# The intro-class run, 2–3 September 2026

A record of the first administration of the covered-box replication, written on 17 September 2026, before `design.py` is changed.
Once the anchor trial is removed the repository will no longer describe the survey these 35 people took, so the design is frozen here alongside the data it produced.

## What was run

| | |
|---|---|
| Survey | `SV_0jhdOUbkNhtMM62`, the within-subjects version, imported 2 September 2026 |
| Live URL | https://bostonu.qualtrics.com/jfe/form/SV_0jhdOUbkNhtMM62 |
| Built from | commit **`c4cca28`**, *Within-subjects design: both terms, randomised order recorded as first_term* (2 September 2026) |
| Stimuli served from | `https://raw.githubusercontent.com/eecoppock/covered-box-replication/main/stimuli`, pinned to `main` |
| Participants | LX 331 students, the intro semantics class. The population is not recorded anywhere in the export; it is stated here because that is who was asked |
| Collection window | 2026-09-02 15:39:45 to 2026-09-03 09:11:17 |
| Responses | 35, every one finished, every one at 100% progress |

`c4cca28` is the commit whose `design.py` and `build-qsf.py` produced the exact `HuangSnedeker_replication.qsf` that was imported.
All five build artefacts were last touched by that commit, and the working tree still matched it byte for byte when this archive was made.
The three commits after it (`fc6fa1d` onward is earlier; `01da22d` and `b820467` are later) changed documentation and the analysis script, not the instrument.

Both terms were shown to every participant, in a randomised order recorded as `first_term`.
Within each block the trial sequence was

    anchor, probeEarly, critical, shape, matchVsMore,
    critical, shape, matchVsLess, otherQuant, criticalOneSet, probe

so each participant contributed three scalar critical trials and three number critical trials.

## Files here

| file | what it is |
|---|---|
| `build/` | `design.py`, `build-qsf.py`, `HuangSnedeker_replication.qsf`, `columns.txt`, `choice-map.csv` and `qsf-template.json`, all as of `c4cca28` |
| `build/stimuli/` | `scalar_s1_ALL.png` and `scalar_s1_SOME.png`, the two anchor images |
| `coveredbox-intro-2026-09-03.csv` | the export, de-identified: `IPAddress`, `LocationLatitude`, `LocationLongitude` and the four empty recipient columns are removed, all 40 remaining columns and all 35 rows kept |

The raw export stays in `../../results/`, which is gitignored and lives only in Dropbox.
It has to stay out of this repository because the repository is public, since it is what serves the stimulus images, and the raw file carries IP addresses and geolocation for 35 students.
`.gitignore` also excludes `archive/*/raw/` so that a raw copy placed here later cannot be pushed by accident.

Three exports sit in `results/`.
The 3 September and 7 September files are byte-identical, md5 `79345bfa3091e04da4c218f61846af6d`, so no response arrived after 3 September 21:39 and the 7 September file is only a re-download.
The 2 September file is an earlier partial pull.

## What came out

Response code **3** is the covered box.

| critical trials | this run | Huang et al. (2013) |
|---|---|---|
| scalar, `critical_s3` | 27/35, 77% | |
| scalar, `critical_s5` | 29/35, 83% | |
| scalar, `criticalOneSet_s8` | 29/35, 83% | |
| **scalar, pooled** | **81%** | **13%** |
| number, `critical_s3` | 33/35, 94% | |
| number, `critical_s5` | 33/35, 94% | |
| number, `critical_s8` | 32/35, 91% | |
| **number, pooled** | **93%** | **100%** |

Their 87-point contrast came out at about 12 points.
The scalar condition behaved like the number condition: participants held out for *some but not all* much as they held out for exactly two.

The instrument itself worked.
Familiarization was 35/35 on all four trials.
The probes were 35/35 for `scalar_probeEarly`, 35/35 for `scalar_probe`, 35/35 for `number_probeEarly` and 34/35 for `number_probe`, so the covered box was live for essentially every participant, including at the end under maximum extinction pressure.

Two facts bear on how the result should be read.
Block order does not explain it: participants who saw the scalar block first still took the covered box on 78% of scalar criticals, against 83% for the number-first group, so the first quantifier judgment anyone made in the study was already upper-bounded.
Domain restriction does not explain it either: `criticalOneSet`, where every object is in one box and a restricted domain is therefore unavailable, came out at 83%, the same as the other two.

The three critical trials within a participant are near-duplicates.
Thirty-one of 35 participants answered all-or-nothing across their three scalar criticals, so the participant is the unit of analysis and 35 × 3 is not 105 independent observations.

## Data quality notes, for whoever analyses this later

One of the 35 responses came through the **preview** channel rather than the anonymous link, and it took the covered box on 0 of 3 scalar criticals.
It is not known whether that response is a student or a test run by the instructor.
Excluding it moves the pooled scalar rate from 81% to 83%, so the decision does not change anything, but it should be made explicitly rather than silently.

Durations ran from 60 to 305 seconds with a median of 163, against the eight minutes the top-level README estimates.
Only one response came in under 90 seconds.

`first_language` asked *Is English your first language? (optional)* and every participant answered: 32 said yes and 3 said no.

## What is not recorded anywhere

How the survey was assigned, through which channel, whether it was required or optional, and what the class was told before taking it.
Whether any student took it more than once.
There is no consent screen in the export.

## Context that matters for interpretation

LX 331 covered *Entailment vs. implicature; the covered box* on Tuesday 8 September, five days after collection closed, so the instructor's own teaching of implicature did not contaminate this run.
The participants were nonetheless linguistics students rather than the naive adults Huang et al. recruited, which is a live alternative explanation for the result and cannot be separated from the design explanation using this dataset alone.

## Why the design is about to change

The working hypothesis is that `anchorAll` caused the failure.
Its boxes are `("SOME","ALL")` and its prompt is *give me the box where X has all of the Ys*, with the ALL box correct, so the participant is made to discriminate a SOME display from an ALL display and to attach the label *all* to the fuller one, two screens before being asked about *some*.
That trains the stronger alternative rather than merely mentioning it, which is the precondition the scalar implicature needs.
The anchor was there to fix the domain, and `criticalOneSet` closes that loophole by construction instead, which is why it can be dropped rather than replaced.

## The two images kept here

`make-stimuli.py` writes only the boxes the *current* design calls for, so when `anchorAll` was replaced on 17 September it deleted `scalar_s1_ALL.png` and `scalar_s1_SOME.png`, which are the two boxes this run's first screen showed.
The archived QSF references them by URL, and the images are served from the `main` branch of the public repository, so committing that deletion would have made this survey unreproducible with no error anywhere.
Both files were restored to `stimuli/` and a copy is kept in `build/stimuli/` so the archive does not depend on what the repository does later.

The same trap applies to any future design change: regenerate the stimuli, then check that every image an archived QSF references is still present before committing.

To recover this design later:

    git show c4cca28:design.py

or tag it, which has not been done:

    git tag intro-run-2026-09 c4cca28
