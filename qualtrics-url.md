# Qualtrics links — covered-box replication

## Live, from 18 September 2026

**https://bostonu.qualtrics.com/jfe/form/SV_0HFaY3KvHhJD6R0**

The Experiment 4 rebuild: welcome and consent screen, familiarization run twice
with feedback on the first pass, three fillers interleaved with three scalar
criticals, the same for the number block, then language, Kerberos ID and the
data-use question. Object set is counterbalanced by a block randomiser and
recorded as `objects`. Institutional branding stripped, so it renders plain.

Built from `HuangSnedeker_replication.qsf` in this folder. Rebuild with

    python3 build-qsf.py https://raw.githubusercontent.com/eecoppock/covered-box-replication/main/stimuli

and import as a NEW project rather than editing the live one, so that each
instrument stays tied to the data it produced.

Analysed by `coveredbox-critical.R`, which carries the preregistered rule.

## Superseded

**`SV_0jhdOUbkNhtMM62`** — the within-subjects instrument with the anchor, the
probes, `criticalOneSet`, the shape fillers and the Huang controls. This is the
survey the intro class took on 2–3 September 2026, and the one the archived data
in `archive/2026-09-intro-run/` came from. **Leave it alone.** Editing it would
break the link between that design and that data.

**`SV_1GMnqdyC8V1vmqa`** — the earlier between-subjects version, 33 questions.
No data collected under it that is still in use.
