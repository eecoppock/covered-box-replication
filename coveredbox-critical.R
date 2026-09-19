# Covered box, critical cells only — analysis
#
# For the design rewritten on 17 September 2026 to follow Huang, Spelke &
# Snedeker (2013) EXPERIMENT 4: three fillers interleaved with three tokens of
# the scalar critical some(NONE,ALL), then three of the number critical
# two(1,3). `coveredbox-rep.R` analyses the OLD instrument and is kept for the
# archived intro-class data; it will not run on this export.
#
# Huang et al., Experiment 4, adults (n = 25 per condition, Mechanical Turk):
#   some(NONE,ALL)  covered box 31%   total set 60%
#   two(1,3)        covered box 92%   lower-bounded option 7%
#
# Their Experiment 1 gave 13% on the same scalar trial type, with no fillers and
# trial type between subjects. The 18-point gap between their own two designs is
# worth putting in front of the class.

library(tidyverse)

# ---- the preregistered rule ------------------------------------------------
# Written down before the data existed. Twelve participants, all of them in the
# scalar critical cell, tested against Exp 4's .31 with an exact binomial, the
# participant as the unit and "took the covered box" meaning on a majority of
# the three tokens.
#
#   fewer than 8 of 12 -> we did not separate from Huang et al.
#   8 or more of 12    -> we differ from them, as the intro-class run did
#
# (0 of 12 also rejects, p = .023, in the other direction: far FEWER covered-box
# choices than they got. Worth knowing, but not what we predicted.)
#
# Power: 96% against a true rate of .83, which is what the intro class produced;
# 58% against .65; 30% against .55. The middle of the range is out of reach at
# this n, which is a limitation to state rather than discover.
H0        <- 0.31
THRESHOLD <- 8

# ---- read the newest export ------------------------------------------------
f <- list.files("results", pattern = "\\.csv$", full.names = TRUE)
stopifnot(length(f) > 0)
f <- f[which.max(file.mtime(f))]
cat("reading", f, "\n")

raw <- read_csv(f, show_col_types = FALSE) |> slice(-(1:2))   # two header rows

# Object set is counterbalanced, so each participant answers only one version's
# columns and the other version's are blank. The critical tags carry their
# object set (scalar_critical_s1 is cookies, s4 is fish), so the two versions
# never collide and the analysis just gathers whatever is filled in.
SCALAR <- grep("^scalar_critical_", names(raw), value = TRUE)
NUMBER <- grep("^number_critical_", names(raw), value = TRUE)
FAM2   <- c("fam1_p2", "fam2_p2", "fam3_p2", "fam4_p2")
FAM_KEY  <- c(fam1_p2 = "2", fam2_p2 = "1", fam3_p2 = "3", fam4_p2 = "3")
FILL_KEY <- c(fill1 = "1", fill2 = "1", fill3 = "3",
              nfill1 = "1", nfill2 = "2", nfill3 = "3")
FILL     <- setNames(rep(FILL_KEY, each = 2),
                     paste0(rep(names(FILL_KEY), each = 2), c("_A", "_B")))

dat <- raw |>
  filter(Finished %in% c("True", "1", "TRUE")) |>
  mutate(participant = row_number())

cat("\nresponses:", nrow(raw), " finished:", nrow(dat), "\n")

# ---- who took it -----------------------------------------------------------
# The survey ends with a required Kerberos ID, which is the roster's `coder`
# column, so completion can be checked against the class list without matching
# on names. The point is less the grading than the gap: at this n the identity
# of the person who did NOT take it is worth chasing the same afternoon.
ROSTER <- "../../Roster/roster-merged.csv"
if ("kerberos" %in% names(dat) && file.exists(ROSTER)) {
  took <- tolower(trimws(dat$kerberos))
  took <- took[took != "" & !is.na(took)]
  roster_all <- read_csv(ROSTER, show_col_types = FALSE) |>
    filter(!is.na(coder), coder != "") |>
    mutate(coder = tolower(trimws(coder)),
           enrolled = !is.na(Course) & Course != "")
  class_list <- filter(roster_all, enrolled)          # auditors are not graded
  auditors   <- filter(roster_all, !enrolled)
  missing  <- setdiff(class_list$coder, took)
  unknown  <- setdiff(took, class_list$coder)
  dupes    <- took[duplicated(took)]
  cat(sprintf("\nCompletion: %d of %d enrolled\n",
              sum(class_list$coder %in% took), nrow(class_list)))
  if (nrow(auditors))
    cat(sprintf("  auditing: %d of %d took it (not graded, but their data counts)\n",
                sum(auditors$coder %in% took), nrow(auditors)))
  if (length(missing))
    cat("  not yet taken:", paste(
      class_list$Name[match(missing, class_list$coder)], collapse = "; "), "\n")
  unknown <- setdiff(unknown, auditors$coder)
  if (length(unknown))
    cat("  IDs not on the roster (typos?):", paste(unknown, collapse = ", "), "\n")
  if (length(dupes))
    cat("  took it more than once:", paste(unique(dupes), collapse = ", "), "\n")
} else {
  cat("\n(no kerberos column or no roster; skipping the completion check)\n")
}

# ---- exclusion: the second familiarization pass ----------------------------
# Huang et al. included everyone, because every adult got these right. The
# first pass had feedback and is not a test, so the criterion is the second.
fam <- dat |>
  select(participant, all_of(FAM2)) |>
  pivot_longer(-participant, names_to = "trial", values_to = "resp") |>
  mutate(ok = resp == FAM_KEY[trial]) |>
  group_by(participant) |>
  summarise(fam_correct = sum(ok), .groups = "drop")

cat("\nFamiliarization, second pass — how many of 4 correct:\n")
print(count(fam, fam_correct))

keep <- fam$participant[fam$fam_correct == 4]
cat("included:", length(keep), "of", nrow(dat), "\n")
if (length(keep) < nrow(dat))
  cat("  (3 of 4 is defensible if recruitment is tight; say which rule was used)\n")

# ---- the fillers -----------------------------------------------------------
# Three trials with a right answer, sitting among the criticals. Two are
# answered by an open box and one by the covered box, so they check both that
# attention held and that the covered box was still live while it mattered.
# With the probe gone these are the only such check left.
fill <- dat |>
  select(participant, any_of(names(FILL))) |>
  pivot_longer(-participant, names_to = "trial", values_to = "resp") |>
  filter(!is.na(resp), resp != "") |>
  mutate(ok = resp == FILL[trial],
         trial = sub("_[AB]$", "", trial))

cat("\nFillers — proportion correct:\n")
print(fill |> group_by(trial) |> summarise(correct = mean(ok), n = n(), .groups = "drop"))
covered_fillers <- c("fill3", "nfill3")
if (mean(fill$ok[fill$trial %in% covered_fillers]) < .8)
  cat("!! Under 80% on the fillers answered by the covered box. A low\n",
      "   critical rate may be the covered box having gone dead rather than\n",
      "   anything about *some*.\n", sep = "")

# ---- the criticals ---------------------------------------------------------
# ---- consent to analyse ----------------------------------------------------
# The welcome screen promises that saying no here does not affect credit, so the
# completion check above counts everyone and this exclusion happens after it.
if ("data_use" %in% names(dat)) {
  declined <- dat$participant[dat$data_use == "2" & !is.na(dat$data_use)]
  if (length(declined)) {
    cat(sprintf("\n%d participant(s) asked to be left out of the analysis.\n",
                length(declined)))
    keep <- setdiff(keep, declined)
  }
}

long <- dat |>
  filter(participant %in% keep) |>
  select(participant, objects, all_of(c(SCALAR, NUMBER))) |>
  pivot_longer(c(-participant, -objects), names_to = "trial", values_to = "resp") |>
  filter(!is.na(resp), resp != "") |>
  mutate(term    = if_else(str_starts(trial, "scalar"), "scalar", "number"),
         covered = resp == "3")

# ---- the counterbalance ----------------------------------------------------
# Version A gives the scalar trials cookies, apples and balloons; version B
# gives them fish, birds and flowers. Without this, object set would move with
# the term and the some-against-two contrast could not tell the two apart. A
# large gap between the versions means the materials are doing work of their
# own, which belongs in the write-up whichever way the headline goes.
cat("\nObject-set counterbalance:\n")
print(long |> group_by(objects, term) |>
        summarise(covered = mean(covered), participants = n_distinct(participant),
                  .groups = "drop") |>
        pivot_wider(names_from = term, values_from = covered))
if (n_distinct(long$objects) < 2)
  cat("!! Only one version of the object assignment appears. The randomiser\n",
      "   may not have fired, or everyone landed in the same cell.\n", sep = "")

cat("\nTrial-level covered-box rate, comparable with their M:\n")
print(long |> group_by(term) |>
        summarise(covered = mean(covered), trials = n(), .groups = "drop"))
cat("Published, Exp 4 adults: scalar .31, number .92\n")

by_p <- long |>
  group_by(participant, term) |>
  summarise(n_covered = sum(covered), .groups = "drop") |>
  mutate(took_covered = n_covered >= 2)

cat("\nPer participant, covered-box choices out of 3:\n")
print(by_p |> count(term, n_covered) |> pivot_wider(names_from = term,
                                                    values_from = n, values_fill = 0) |>
        arrange(n_covered))

# ---- the test --------------------------------------------------------------
sc <- by_p |> filter(term == "scalar")
k  <- sum(sc$took_covered); n <- nrow(sc)
bt <- binom.test(k, n, p = H0)

cat("\n---- the preregistered test ----\n")
cat(sprintf("%d of %d participants took the covered box on a majority of the\n", k, n))
cat(sprintf("three scalar critical trials (%.0f%%).\n", 100 * k / n))
cat(sprintf("Against Huang et al.'s %.0f%%: exact binomial p = %.4f\n", 100 * H0, bt$p.value))
cat(sprintf("95%% CI %.2f to %.2f\n", bt$conf.int[1], bt$conf.int[2]))
cat(sprintf("\nRule was: %d or more of %d means we differ from them.\n", THRESHOLD, n))
if (k >= THRESHOLD) {
  cat("VERDICT: we differ from Huang et al. The rebuild did not recover it.\n")
} else {
  cat("VERDICT: we did not separate from Huang et al. The result replicates.\n")
}
if (n != 12)
  cat(sprintf("!! The rule was set for n = 12 and n is %d. Recompute the\n", n),
      "   threshold before reading the verdict.\n", sep = "")

# ---- some against two, within the same people ------------------------------
wide <- by_p |> select(participant, term, took_covered) |>
  pivot_wider(names_from = term, values_from = took_covered)
b <- sum(wide$number & !wide$scalar, na.rm = TRUE)
c_ <- sum(wide$scalar & !wide$number, na.rm = TRUE)
cat("\n---- some vs two, paired ----\n")
cat(sprintf("covered for two but not some: %d; some but not two: %d; tied: %d\n",
            b, c_, nrow(wide) - b - c_))
if (b + c_ > 0) print(binom.test(b, b + c_, p = 0.5)) else
  cat("no discordant participants\n")

# ---- the picture -----------------------------------------------------------
p <- long |>
  group_by(term) |>
  summarise(covered = mean(covered), .groups = "drop") |>
  mutate(published = c(number = 0.92, scalar = 0.31)[term]) |>
  pivot_longer(c(covered, published), names_to = "source", values_to = "rate") |>
  ggplot(aes(x = term, y = rate, fill = source)) +
  geom_col(position = position_dodge(width = .7), width = .6) +
  geom_text(aes(label = scales::percent(rate, 1)),
            position = position_dodge(width = .7), vjust = -0.4, size = 3.4) +
  scale_y_continuous(labels = scales::percent, limits = c(0, 1.12)) +
  scale_fill_manual(values = c(covered = "#1F3A68", published = "#B8B5AC"),
                    labels = c("ours", "Huang et al.")) +
  labs(x = NULL, y = "covered box chosen", fill = NULL,
       title = "Critical trials: no subset or exact match is visible") +
  theme_minimal(base_size = 12) +
  theme(panel.grid.major.x = element_blank())
print(p)
ggsave("figures/critical-cells.png", p, width = 6, height = 4, dpi = 150)
cat("\nwrote figures/critical-cells.png\n")
