# NOTE (17 Sept 2026): this analyses the OLD instrument and is kept for the
# archived intro-class data in archive/2026-09-intro-run/. The current design
# is analysed by coveredbox-critical.R.

# ============================================================
#  coveredbox-rep.R
#  Class replication of Huang, Spelke & Snedeker (2013), Experiment 1.
#
#  DESIGN
#    Term (scalar "some" vs. number "two") is WITHIN subjects as of 2 Sept 2026;
#    order is randomised and recorded in first_term. Within a term,
#    the three CRITICAL trials come first, then the six control trials, so the
#    response that carries the argument is given before anyone has seen a trial
#    type they could compare it against. That is a weakened version of Huang et
#    al., who put trial type between subjects too; the cost is a fixed order,
#    which the report should say out loud.
#
#    Each trial: three boxes, two open and one covered. Qualtrics randomises
#    the choice order, so the covered box's position is counterbalanced and the
#    export records which BOX was chosen, not which position.
#
#  RESPONSE CODES
#    1 = the first open box   2 = the second open box   3 = the COVERED box
#  Choice IDs are stable no matter what order the boxes are displayed in, and
#  what 1 and 2 mean varies by trial type, so build-qsf.py writes choice-map.csv
#  and this script reads it rather than hard-coding the mapping.
#
#  The covered box's position is counterbalanced by hand across the three tokens
#  of each trial type (first, second, third), not randomised: a QSF cannot carry
#  choice randomisation that has been verified to import.
#
#  THE PROBE
#    In none of Huang et al.'s trial types is the covered box unambiguously
#    correct -- it is always the diagnostic option -- so only familiarization
#    establishes that it is ever right. A participant who reads *some* as
#    lower-bounded then never needs it again, and if it goes dead for them, a
#    low covered-box rate is EXTINCTION rather than semantics.
#
#    The probe trial, which is ours and not theirs, names an object that is in
#    neither open box. The covered box is correct whatever anyone's semantics.
#    It comes after the critical trials, so it cannot prime them. If scalar
#    participants pass it, their low critical rate is not extinction. If they
#    fail it, that is a finding about the paradigm and belongs in the report.
#
#  THE QUESTION
#    On critical trials the subset/exact match is absent. Anyone holding out
#    for it must take the covered box. Huang et al. found 13% covered for
#    some(NONE,ALL) but 100% for two(1,3v5): adults let *some* stay
#    lower-bounded, but treated *two* as exact.
# ============================================================
rm(list = ls())
library(tidyverse)

# Take the most recent export in results/, so re-downloading mid-class picks up
# automatically without editing this line. Falls back to the simulated set.
exports <- list.files("results", pattern = "\\.csv$", full.names = TRUE)
data_file <- if (length(exports)) exports[which.max(file.mtime(exports))] else
             "coveredbox-fake-data.csv"
cat("Reading:", data_file, "\n")

raw <- read_csv(data_file, col_types = cols(.default = col_character())) |>
  slice(-(1:2))                              # drop Qualtrics' two metadata rows

#View(raw)

# Qualtrics exports preview and test runs alongside real ones, so taking the
# survey yourself to check it lands in the class data unless they are dropped.
drop_test_runs <- function(d) {
  if ("Status" %in% names(d))
    d <- filter(d, !Status %in% c("Survey Preview", "Survey Test", "Spam", "1", "2", "8"))
  if ("DistributionChannel" %in% names(d))
    d <- filter(d, !DistributionChannel %in% c("preview", "test"))
  d
}

finished <- raw |> filter(Finished %in% c("True","TRUE","true","1"))
complete <- drop_test_runs(finished)
if (nrow(finished) > nrow(complete))
  cat("Dropped", nrow(finished) - nrow(complete), "preview/test response(s).\n\n")

#View(complete)

# what each choice ID means, per question -- written by build-qsf.py
cmap <- read_csv("choice-map.csv", show_col_types = FALSE) |>
  filter(choice_id != "correct") |>
  mutate(choice_id = as.integer(choice_id))

if (interactive()) View(cmap)

# ---- familiarization ------------------------------------------------------
# Two trials where the red star is visible, two where it is not. Anyone who
# misses one was not reading the instructions.
correct <- c(fam1 = "1", fam2 = "1", fam3 = "3", fam4 = "3")
fam <- complete |>
  select(ResponseId, all_of(names(correct))) |>
  pivot_longer(-ResponseId, names_to = "trial", values_to = "resp") |>
  mutate(ok = resp == correct[trial]) |>
  group_by(ResponseId) |>
  summarise(n_correct = sum(ok, na.rm = TRUE), .groups = "drop") |>
  mutate(passed = n_correct == 4)

cat("Familiarization:\n")
cat("  completed responses :", nrow(complete), "\n")
cat("  failed              :", sum(!fam$passed), "\n")
print(count(fam, n_correct))

# The covered box is bracketed. fam3 and fam4 require it BEFORE any test trial;
# the probe requires it AFTER all of them. Report the front end over every
# completed response, not just those who survive exclusion -- among the included
# it is 100% by construction, which says nothing.
front <- complete |>
  select(ResponseId, fam3, fam4) |>
  pivot_longer(-ResponseId, names_to = "trial", values_to = "resp") |>
  summarise(chose_covered = mean(resp == "3", na.rm = TRUE), n = n())
cat("  covered-box trials (fam3, fam4), all completed responses:",
    sprintf("%.0f%% correct", 100 * front$chose_covered), "\n")

# language background, asked last and optional. Reported in aggregate: this is
# classroom data from identifiable people, and in a group of thirty a rare
# answer plus a response pattern can identify someone.
lang <- complete |>
  filter(ResponseId %in% fam$ResponseId[fam$passed]) |>
  transmute(participant = ResponseId,
            first_language = case_when(first_language == "1" ~ "English",
                                       first_language == "2" ~ "another language",
                                       first_language == "3" ~ "declined",
                                       TRUE ~ "no answer"))

dat <- complete |>
  filter(ResponseId %in% fam$ResponseId[fam$passed]) |>
  select(ResponseId, matches("^(scalar|number)_")) |>
  pivot_longer(-ResponseId, names_to = "q", values_to = "resp") |>
  filter(!is.na(resp), resp != "") |>
  # shape fillers carry no object set, so their tag has two parts not three
  separate_wider_delim(q, "_", names = c("term", "trial_type", "set"),
                       too_few = "align_start") |>
  mutate(set = replace_na(set, "s0")) |>
  mutate(participant = ResponseId,
         term      = factor(term, levels = c("scalar", "number")),
         critical  = trial_type %in% c("critical", "criticalOneSet"),
         probe     = trial_type %in% c("probe", "probeEarly"),
         resp      = as.integer(resp),
         covered   = resp == 3,
         # shape fillers have no object set, so their tag has no _sN part
         question  = if_else(set == "s0", paste0(term, "_", trial_type),
                             paste0(term, "_", trial_type, "_", set))) |>
  left_join(cmap, by = c("question", "resp" = "choice_id")) |>
  mutate(match_box = meaning == "match") |>
  select(participant, term, trial_type, set, resp, meaning, critical, probe,
         covered, match_box) |>
  # first_term is embedded data stamped by the survey flow. Order is what turns
  # the within-subjects design from "contaminated" into "analysable": meeting the
  # numerals first should teach that the covered box is often the answer, which
  # should raise the scalar rate when scalar comes second.
  left_join(select(complete, ResponseId, first_term),
            by = c("participant" = "ResponseId")) |>
  mutate(order = factor(if_else(as.character(term) == first_term,
                                "first", "second"),
                        levels = c("first", "second")))

# ---- checks ---------------------------------------------------------------
n_expected <- length(unique(cmap$question[grepl("^scalar_", cmap$question)]))
chk <- dat |> group_by(participant) |>
  summarise(n = n(), terms = n_distinct(term), .groups = "drop")
if (any(chk$n != 2 * n_expected | chk$terms != 2)) {
  warning("Some participants do not have the expected ", 2 * n_expected,
          " trials across both terms:")
  print(filter(chk, n != 2 * n_expected | terms != 2))
} else cat("\nOK:", nrow(chk), "participants,", 2 * n_expected,
           "trials each, both terms each.\n")
cat("\nOrder assignment (which term came first):\n")
print(count(distinct(dat, participant, first_term), first_term))

# ---- control trials: did the task work at all? ----------------------------
# When the subset/exact match IS visible, everyone should take it.
# ---- the anchor ------------------------------------------------------------
# Until 17 Sept 2026 the scalar anchor asked for ALL and its open-box answer
# was available only under the box-internal reading of the partitive, so it
# doubled as a domain diagnostic. It was also training the stronger alternative
# right before the critical trials; see the note above SCALAR in design.py.
#
# anchorHalf shows 3-1 and 1-3 and asks for HALF, so the covered box is correct
# and the trial no longer diagnoses anything about the domain. It is now a
# second covered-box establishment trial and is reported with the probes.
# The number term keeps anchorFive, an open-box trial, but the number term has
# no partitive and never had a domain ambiguity to diagnose.
anchor <- dat |> filter(trial_type %in% c("anchorHalf", "anchorFive")) |>
  group_by(term, trial_type) |>
  summarise(correct = mean(if_else(trial_type[1] == "anchorHalf",
                                   covered, match_box)),
            n = n(), .groups = "drop")
cat("\nAnchor trial — proportion correct:\n")
print(anchor)
if (any(anchor$correct[anchor$trial_type == "anchorHalf"] < .8))
  cat("!! Under 80% on the scalar anchor. Either half is not being read over\n",
      "   the box, or the covered box was not understood from familiarization.\n",
      "   Either way the scalar critical rate is hard to interpret.\n", sep = "")

# ---- domain: is anyone quantifying over the whole display? ------------------
# The diagnostic moved here when the anchor stopped carrying it. Globally read,
# a critical ALL box shows the target with four of the eight objects on screen,
# which IS "some but not all", so a whole-display reader takes the open box
# with the exclusive reading of "some" fully intact -- and the headline looks
# like a replication for the wrong reason.
#
# criticalOneSet puts every object in one box, so the two readings coincide and
# that loophole is shut. A whole-display reader therefore takes the open box on
# `critical` but not on `criticalOneSet`, and the gap between the two is the
# signature. No gap means no whole-display problem to worry about.
oneset <- dat |> filter(term == "scalar",
                        trial_type %in% c("critical", "criticalOneSet")) |>
  group_by(trial_type) |>
  summarise(covered = mean(covered), n = n(), .groups = "drop")
cat("\nScalar criticals: the ordinary ones against the closed-domain one:\n")
print(oneset)
if (nrow(oneset) == 2 &&
    abs(diff(oneset$covered)) > .15)
  cat("!! criticalOneSet differs from the ordinary criticals by more than 15\n",
      "   points. Some participants may be quantifying over the whole display.\n",
      "   criticalOneSet is the trial of record; report it separately.\n", sep = "")

HS_CONTROLS <- c("noneSome","someAll","oneTwo","twoMore")
cat("\nControl trials, Huang et al.'s — proportion taking the subset/exact match:\n")
print(dat |> filter(trial_type %in% HS_CONTROLS) |>
        group_by(term, trial_type) |>
        summarise(match = mean(match_box), n = n(), .groups = "drop"))

# Fillers in another quantifier, ours rather than theirs. Without them the
# scalar term says "some" on nearly every screen, which invites theorising
# about the recurring word. The answer is always a visible box, so these also
# double as a check that participants track the quantifier and not the display.
cat("\nShape fillers between the critical trials — proportion correct.\n",
    "No quantifier in these at all: they reset attention without priming\n",
    "some, all or none. shape2 needs the covered box:\n", sep = "")
print(dat |> filter(grepl("^shape", trial_type)) |>
        group_by(term, trial_type) |>
        summarise(correct = mean(if_else(trial_type == "shape2",
                                         covered, match_box)),
                  n = n(), .groups = "drop"))

cat("\nAdded fillers in another quantifier — proportion correct:\n")
print(dat |> filter(!critical, !probe, !trial_type %in% HS_CONTROLS,
                    !grepl("^shape", trial_type),
                    !trial_type %in% c("anchorHalf","anchorFive")) |>
        group_by(term, trial_type) |>
        summarise(correct = mean(match_box), n = n(), .groups = "drop"))

# ---- the critical comparison ---------------------------------------------
# ---- the probe: was the covered box still a live option? -----------------
probe <- dat |> filter(probe) |>
  mutate(when = if_else(trial_type == "probeEarly",
                        "1 before the critical trials",
                        "2 after everything")) |>
  group_by(term, when) |>
  summarise(passed = mean(covered), n = n(), .groups = "drop")
cat("\nProbe trials — is the covered box a live option? Asked twice, once\n",
    "immediately BEFORE the critical trials and once AFTER everything. The\n",
    "second is the harder test: by then every intervening trial has had a\n",
    "visible answer. Together they bracket the critical trials with real\n",
    "covered-box demands rather than relying on familiarization alone:\n", sep = "")
print(probe)
if (any(probe$passed < .8))
  cat("!! Under 80% on the probe. The covered box may have stopped being a live\n",
      "   option, in which case a low critical rate is extinction, not semantics.\n",
      sep = "")

crit <- dat |> filter(critical) |>
  group_by(participant, term, order) |>
  summarise(covered = mean(covered), .groups = "drop")

# Huang et al.'s critical trials and ours, side by side. The comparison IS the
# domain test: their display leaves the global reading available (the target has
# four of the eight objects on screen, which globally is "some but not all"),
# ours does not (every object is in one box, so the two domains coincide). If the
# rates agree, the global reading was not buying anything.
cat("\nCritical trials by kind — proportion choosing the COVERED box:\n")
print(dat |> filter(critical) |>
        group_by(participant, term, trial_type) |>
        summarise(covered = mean(covered), .groups = "drop") |>
        group_by(term, trial_type) |>
        summarise(covered = mean(covered), n = n(), .groups = "drop") |>
        mutate(design = if_else(trial_type == "critical",
                                "Huang et al. — global reading available",
                                "ours — domains coincide")))

cat("\nCritical trials pooled — proportion choosing the COVERED box:\n")
print(crit |> group_by(term) |>
        summarise(mean = mean(covered), sd = sd(covered), n = n(),
                  se = sd/sqrt(n),
                  ci_low  = mean - qt(.975, n-1)*se,
                  ci_high = mean + qt(.975, n-1)*se, .groups = "drop"))
cat("Published: scalar .13, number 1.00\n")

# The headline used to be split by the anchor response, which read the domain.
# anchorHalf does not measure that, so the split is by criticalOneSet instead:
# a participant who takes the covered box there is not exploiting the loophole.
oneset_p <- dat |> filter(term == "scalar", trial_type == "criticalOneSet") |>
  group_by(participant) |>
  summarise(closed_domain = mean(covered) > .5, .groups = "drop")
cat("\nScalar critical rate split by the closed-domain trial:\n")
print(crit |> filter(term == "scalar") |>
        left_join(oneset_p, by = "participant") |>
        group_by(closed_domain) |>
        summarise(covered = mean(covered), n = n(), .groups = "drop"))

# Every critical trial used a different object. If the effect lives in one
# picture rather than in the words, it shows here.
cat("\nCritical trials by item:\n")
print(dat |> filter(critical) |>
        group_by(term, set) |>
        summarise(covered = mean(covered), n = n(), .groups = "drop") |>
        arrange(term, set))

cat("\nLanguage background (optional question, asked last):\n")
print(count(lang, first_language))
cat("Huang et al. recruited English-speaking undergraduates, so this is what\n",
    "makes the comparison to their rate a check rather than an assumption.\n", sep = "")

by_lang <- crit |> left_join(lang, by = "participant") |>
  group_by(term, first_language) |>
  summarise(covered = mean(covered), n = n(), .groups = "drop")
cat("\nCritical rate by language background — small cells, read with care:\n")
print(by_lang)

# ---- screening ------------------------------------------------------------
# Decide these BEFORE looking at the critical rate. Reported as a sensitivity
# table rather than applied silently, so it is visible whether the conclusion
# depends on the rule. Huang et al. recruited English-speaking undergraduates,
# which is what makes the language screen a comparability check rather than a
# judgement about anybody.
native  <- lang$participant[lang$first_language == "English"]
fam_ok  <- fam$ResponseId[fam$n_correct == 4]
ctrl <- dat |> filter(trial_type %in% c("someAll","noneSome","oneTwo","twoMore")) |>
  group_by(participant) |> summarise(ctrl = mean(match_box), .groups = "drop")
probes <- dat |> filter(probe) |>
  group_by(participant) |> summarise(prb = mean(covered), .groups = "drop")
attentive <- ctrl$participant[ctrl$ctrl == 1]
probe_ok  <- probes$participant[probes$prb == 1]

screens <- list(
  "all participants"            = unique(crit$participant),
  "+ native English only"       = native,
  "+ perfect familiarization"   = fam_ok,
  "+ every control trial right" = attentive,
  "+ every probe right"         = probe_ok)
cat("\nSCREENING — does the conclusion depend on who we keep?\n")
for (nm in names(screens)) {
  keep <- Reduce(intersect, screens[seq_len(match(nm, names(screens)))])
  sub_ <- filter(crit, participant %in% keep)
  r <- sub_ |> group_by(term) |> summarise(m = mean(covered), .groups = "drop")
  cat(sprintf("  %-30s n=%2d   scalar %.2f   number %.2f\n", nm,
              n_distinct(sub_$participant),
              r$m[r$term == "scalar"], r$m[r$term == "number"]))
}
cat("  (published: scalar 0.13, number 1.00)\n")

# ---- the headline, and why it is the FIRST blocks ---------------------------
# Everyone now does both terms, so the pooled scalar rate is contaminated: half
# the participants met the numerals first, and that exposure should push "some"
# toward an exact reading. The cell that replicates Huang et al. is therefore
# scalar-FIRST, which is uncontaminated and is exactly their between-subjects
# design. Report that against .13, not the pooled rate.
first_only <- filter(crit, order == "first")
cat("\nFIRST BLOCK ONLY — the clean between-subjects replication:\n")
print(first_only |> group_by(term) |>
        summarise(mean = mean(covered), sd = sd(covered), n = n(),
                  se = sd/sqrt(n), .groups = "drop"))
cat("Published: scalar .13, number 1.00\n")
if (n_distinct(first_only$term) == 2) {
  cat("\nMann-Whitney on first blocks only (Huang et al.'s own test):\n")
  print(wilcox.test(covered ~ term, data = first_only))
} else cat("\nMann-Whitney skipped: only one term among the first blocks so far.\n")

cat("\nORDER EFFECT — same term, seen first vs second:\n")
print(crit |> group_by(term, order) |>
        summarise(covered = mean(covered), n = n(), .groups = "drop"))
sc <- filter(crit, term == "scalar")
if (n_distinct(sc$order) == 2 && nrow(sc) >= 4) {
  cat("\nDoes meeting the numerals first change how 'some' is read?\n")
  print(wilcox.test(covered ~ order, data = sc))
}

cat("\nWITHIN-SUBJECTS comparison — every participant did both terms:\n")
paired <- crit |> select(participant, term, covered) |>
  pivot_wider(names_from = term, values_from = covered) |>
  filter(!is.na(scalar), !is.na(number))
cat("  n pairs:", nrow(paired), "  mean difference (number - scalar):",
    round(mean(paired$number - paired$scalar), 3), "\n")
if (nrow(paired) >= 3) print(wilcox.test(paired$number, paired$scalar, paired = TRUE)) else
  cat("  too few pairs for a test yet.\n")

# A logistic model will not behave here, and the reason is worth a paragraph in
# the report. If one condition is at 0% or 100%, the groups are COMPLETELY
# SEPARATED: no finite log-odds can describe the difference, so the estimate
# runs off to infinity and the standard error with it. R will report a huge
# coefficient and a p-value near 1, which looks like a null result and is the
# opposite of one. The effect is not too small to estimate; it is too large.
rates <- crit |> group_by(term) |> summarise(m = mean(covered), .groups = "drop")
if (any(rates$m %in% c(0, 1))) {
  cat("\nSkipping the logistic model: ",
      paste0(rates$term, " at ", round(100*rates$m), "%", collapse = ", "),
      " — complete separation. See the note in the script.\n", sep = "")
} else if (requireNamespace("lme4", quietly = TRUE)) {
  library(lme4)
  m <- glmer(covered ~ term + (1 | participant) + (1 | set),
             data = filter(dat, critical), family = binomial)
  cat("\nMixed logistic:\n"); print(summary(m)$coefficients)
}

# stash the per-participant critical rates so the report figures can reuse them
saveRDS(crit, "figures/.crit.rds")

# ---- plots ----------------------------------------------------------------
theme_set(theme_minimal(base_size = 12))
pal <- c(scalar = "#4C72B0", number = "#CC0000")

crit_summary <- crit |> group_by(term) |>
  summarise(mean = mean(covered), n = n(), se = sd(covered)/sqrt(n),
            lo = pmax(0, mean - 1.96*se), hi = pmin(1, mean + 1.96*se),
            .groups = "drop")

p_crit <- ggplot(crit, aes(term, covered, colour = term)) +
  geom_hline(yintercept = c(.13, 1), linetype = "dotted", colour = "grey55") +
  geom_jitter(width = .12, height = .015, alpha = .45, size = 2) +
  geom_pointrange(data = crit_summary,
                  aes(term, mean, ymin = lo, ymax = hi),
                  colour = "black", size = .7, inherit.aes = FALSE) +
  scale_colour_manual(values = pal, guide = "none") +
  scale_y_continuous(labels = scales::percent, limits = c(-.03, 1.03)) +
  labs(title = "Critical trials: the subset/exact match is absent",
       subtitle = "Dotted lines are Huang, Spelke & Snedeker's 13% and 100%",
       x = NULL, y = "Chose the covered box")

p_crit

# Each term on its own, with every participant's own rate, so the two are not
# forced onto a shared axis and the spread within a condition is visible.
for (tm in c("scalar", "number")) {
  d <- filter(crit, term == tm)
  ref <- if (tm == "scalar") .13 else 1
  pb <- ggplot(d, aes(order, covered)) +
    geom_hline(yintercept = ref, linetype = "dotted", colour = "grey55") +
    geom_jitter(width = .10, height = .015, alpha = .5, size = 2,
                colour = pal[[tm]]) +
    stat_summary(fun = mean, geom = "point", size = 3.2, colour = "black") +
    stat_summary(fun.data = mean_se, geom = "errorbar", width = .12,
                 colour = "black") +
    scale_y_continuous(labels = scales::percent, limits = c(-.03, 1.03)) +
    labs(title = paste0(tm, " block, split by when it was seen"),
         subtitle = paste0("Dotted line is Huang et al.'s ",
                           scales::percent(ref, accuracy = 1)),
         x = NULL, y = "Chose the covered box")
  ggsave(file.path("figures", paste0("coveredbox-", tm, "-block.png")),
         pb, width = 5.2, height = 4, dpi = 150)
}

# There are only THREE choices and choice 3 is ALWAYS the covered box. An
# earlier version labelled the factor as if there were four, which silently
# renamed the covered box "more" -- the tall bars on the critical panel were the
# covered box wearing the wrong label. Label from choice-map.csv instead.
resp_mix <- dat |> filter(critical) |>
  mutate(choice = case_when(
           meaning == "covered"        ~ "covered box",
           meaning %in% c("all","more")~ "lower-bounded box\n(all / 3 or 5)",
           TRUE                        ~ "matches neither\n(none / empty / one)"),
         choice = factor(choice, levels = c("matches neither\n(none / empty / one)",
                                            "lower-bounded box\n(all / 3 or 5)",
                                            "covered box"))) |>
  count(term, choice) |>
  group_by(term) |> mutate(p = n/sum(n)) |> ungroup()

pub <- tibble(term = factor(c("scalar","number"), levels = c("scalar","number")),
              choice = factor("covered box",
                              levels = levels(resp_mix$choice)),
              p = c(.13, 1.00))

p_mix <- ggplot(resp_mix, aes(choice, p, fill = term)) +
  geom_col(width = .68) +
  geom_text(aes(label = scales::percent(p, accuracy = 1)), vjust = -.5,
            size = 3.4, colour = "grey25") +
  # published covered-box rate, drawn across the covered-box bar only
  geom_segment(data = pub, aes(x = 2.55, xend = 3.45, y = p, yend = p),
               linetype = "dashed", linewidth = .6, colour = "black",
               inherit.aes = FALSE) +
  geom_text(data = pub, aes(x = 3.45, y = p, label = "Huang et al."),
            hjust = 1, vjust = -.6, size = 3, colour = "grey30",
            inherit.aes = FALSE) +
  facet_wrap(~term) +
  scale_fill_manual(values = pal, guide = "none") +
  scale_x_discrete(drop = FALSE) +
  scale_y_continuous(labels = scales::percent, limits = c(0, 1.15)) +
  labs(x = NULL, y = NULL) +
  theme(axis.text.x = element_text(size = 8))

dir.create("figures", showWarnings = FALSE)
ggsave("figures/coveredbox-critical.png", p_crit, width = 5.5, height = 4.2, dpi = 150)
ggsave("figures/coveredbox-choices.png",  p_mix,  width = 8,   height = 4,   dpi = 150)
cat("\nFigures written to figures/.\n")
