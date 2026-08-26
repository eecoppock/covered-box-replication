# ============================================================
#  coveredbox-rep.R
#  Class replication of Huang, Spelke & Snedeker (2013), Experiment 1.
#
#  DESIGN
#    Term (scalar "some" vs. number "two") is BETWEEN subjects. Within a term,
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
#  THE QUESTION
#    On critical trials the subset/exact match is absent. Anyone holding out
#    for it must take the covered box. Huang et al. found 13% covered for
#    some(NONE,ALL) but 100% for two(1,3v5): adults let *some* stay
#    lower-bounded, but treated *two* as exact.
# ============================================================
rm(list = ls())
library(tidyverse)

data_file <- "coveredbox-fake-data.csv"     # swap for the real export
# data_file <- "CoveredBox_<date>.csv"

raw <- read_csv(data_file, col_types = cols(.default = col_character())) |>
  slice(-(1:2))                              # drop Qualtrics' two metadata rows

complete <- raw |> filter(Finished %in% c("True","TRUE","true","1"))

# what each choice ID means, per question -- written by build-qsf.py
cmap <- read_csv("choice-map.csv", show_col_types = FALSE) |>
  filter(choice_id != "correct") |>
  mutate(choice_id = as.integer(choice_id))

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

dat <- complete |>
  filter(ResponseId %in% fam$ResponseId[fam$passed]) |>
  select(ResponseId, matches("^(scalar|number)_")) |>
  pivot_longer(-ResponseId, names_to = "q", values_to = "resp") |>
  filter(!is.na(resp), resp != "") |>
  separate_wider_delim(q, "_", names = c("term", "trial_type", "set")) |>
  mutate(participant = ResponseId,
         term      = factor(term, levels = c("scalar", "number")),
         critical  = trial_type == "critical",
         resp      = as.integer(resp),
         covered   = resp == 3,
         question  = paste0(term, "_", trial_type, "_", set)) |>
  left_join(cmap, by = c("question", "resp" = "choice_id")) |>
  mutate(match_box = meaning == "match") |>
  select(participant, term, trial_type, set, resp, meaning, critical,
         covered, match_box)

# ---- checks ---------------------------------------------------------------
chk <- dat |> group_by(participant) |>
  summarise(n = n(), terms = n_distinct(term), .groups = "drop")
if (any(chk$n != 9 | chk$terms != 1)) {
  warning("Some participants do not have exactly 9 trials in one term:")
  print(filter(chk, n != 9 | terms != 1))
} else cat("\nOK:", nrow(chk), "participants, 9 trials each, one term each.\n")
cat("\nTerm assignment:\n")
print(count(distinct(dat, participant, term), term))

# ---- control trials: did the task work at all? ----------------------------
# When the subset/exact match IS visible, everyone should take it.
cat("\nControl trials — proportion choosing the subset/exact match:\n")
print(dat |> filter(!critical) |>
        group_by(term, trial_type) |>
        summarise(match = mean(match_box), n = n(), .groups = "drop"))

# ---- the critical comparison ---------------------------------------------
crit <- dat |> filter(critical) |>
  group_by(participant, term) |>
  summarise(covered = mean(covered), .groups = "drop")

cat("\nCritical trials — proportion choosing the COVERED box:\n")
print(crit |> group_by(term) |>
        summarise(mean = mean(covered), sd = sd(covered), n = n(),
                  se = sd/sqrt(n),
                  ci_low  = mean - qt(.975, n-1)*se,
                  ci_high = mean + qt(.975, n-1)*se, .groups = "drop"))
cat("Published: scalar .13, number 1.00\n")

cat("\nBetween-subjects comparison (Huang et al. used Mann-Whitney):\n")
print(wilcox.test(covered ~ term, data = crit))

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

resp_mix <- dat |>
  mutate(choice = factor(resp, levels = c(1,2,3,4),
           labels = c("less","subset / exact","more","covered"))) |>
  count(term, critical, choice) |>
  group_by(term, critical) |> mutate(p = n/sum(n)) |> ungroup() |>
  mutate(panel = if_else(critical, "critical trials", "control trials"))

p_mix <- ggplot(resp_mix, aes(choice, p, fill = term)) +
  geom_col(position = "dodge") +
  facet_wrap(~panel) +
  scale_fill_manual(values = pal) +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Where the choices went", x = NULL, y = NULL, fill = NULL) +
  theme(axis.text.x = element_text(angle = 20, hjust = 1))

dir.create("figures", showWarnings = FALSE)
ggsave("figures/coveredbox-critical.png", p_crit, width = 5.5, height = 4.2, dpi = 150)
ggsave("figures/coveredbox-choices.png",  p_mix,  width = 8,   height = 4,   dpi = 150)
cat("\nFigures written to figures/.\n")
