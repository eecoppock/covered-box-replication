# ============================================================
#  make-fake-data.R  —  covered-box replication
#  LX 433/533/733 Experimental Pragmatics, Fall 2026
#
#  Writes a FAKE Qualtrics export in the same shape as the real one, so the
#  analysis can be built and debugged before any data exist. Column names and
#  order are read from columns.txt, which build-qsf.py writes, so the two
#  cannot drift apart.
#
#  Response codes (the RecodeValues set in the survey):
#     1 = the first open box    2 = the second open box    3 = the COVERED box
#  What 1 and 2 mean varies by trial type; choice-map.csv is the key.
#  On CRITICAL trials neither open box matches, so 3 is the informative answer.
#
#  ALL DATA PRODUCED BY THIS SCRIPT ARE FAKE.
# ============================================================
set.seed(2026)

n_participants <- 40
n_incomplete   <- 3     # abandoned partway, Finished = False
n_careless     <- 4     # click at random; should fail familiarization

# Published rates, Huang, Spelke & Snedeker (2013) Exp. 1
p_scalar_crit_covered <- 0.13   # some(NONE,ALL): adults took ALL as a match
p_number_crit_covered <- 1.00   # two(1,3v5): adults held out for exactly two
p_control_correct     <- 0.95   # control trials: pick the subset/exact match

cols  <- readLines("columns.txt")
out_file <- "coveredbox-fake-data.csv"

pick <- function(p_target, target, alts)
  ifelse(runif(length(target)) < p_target, target, sample(alts, 1))

resp <- as.data.frame(matrix("", nrow = n_participants, ncol = length(cols)),
                      stringsAsFactors = FALSE)
names(resp) <- cols

term <- rep(c("scalar", "number"), length.out = n_participants)
term <- sample(term)

# ---- familiarization: everyone attentive gets these right -----------------
correct_fam <- c(fam1 = 1, fam2 = 1, fam3 = 3, fam4 = 3)
for (f in names(correct_fam))
  resp[[f]] <- as.character(ifelse(runif(n_participants) < .995,
                                   correct_fam[[f]], sample(c(1,2,3), 1)))

# ---- test trials ----------------------------------------------------------
for (i in seq_len(n_participants)) {
  is_scalar <- term[i] == "scalar"
  p_cov <- if (is_scalar) p_scalar_crit_covered else p_number_crit_covered
  for (s in 1:3) {
    crit <- if (is_scalar) paste0("scalar_critical_s", s) else paste0("number_critical_s", s)
    # covered box (3), else the "more" open box (2) -- nobody picks the "less" one
    resp[[crit]][i] <- as.character(if (runif(1) < p_cov) 3 else 2)
    ctrl <- if (is_scalar)
              c(paste0("scalar_noneSome_s", s), paste0("scalar_someAll_s", s))
            else
              c(paste0("number_oneTwo_s", s),  paste0("number_twoMore_s", s))
    # on control trials the match is choice 2 for noneSome/oneTwo and
    # choice 1 for someAll/twoMore -- see choice-map.csv
    for (cn in ctrl) {
      match_id <- if (grepl("noneSome|oneTwo", cn)) 2 else 1
      resp[[cn]][i] <- as.character(
        if (runif(1) < p_control_correct) match_id else sample(setdiff(1:3, match_id), 1))
    }
  }
}

# ---- careless responders: uniform clicking everywhere ---------------------
careless <- rep(FALSE, n_participants)
if (n_careless > 0) careless[sample(n_participants, n_careless)] <- TRUE
for (nm in cols) {
  hit <- careless & resp[[nm]] != ""
  if (any(hit)) resp[[nm]][hit] <- as.character(sample(1:3, sum(hit), TRUE))
}

# ---- a few abandoned responses -------------------------------------------
if (n_incomplete > 0) {
  blank <- as.data.frame(matrix("", nrow = n_incomplete, ncol = length(cols)),
                         stringsAsFactors = FALSE)
  names(blank) <- cols
  blank$fam1 <- as.character(sample(1:3, n_incomplete, TRUE))
  resp <- rbind(resp, blank)
}

n_rows   <- nrow(resp)
finished <- c(rep("True", n_participants), rep("False", n_rows - n_participants))
stamps <- format(as.POSIXct("2026-09-03 12:35:00", tz = "UTC") +
                   cumsum(sample(30:420, n_rows, TRUE)), "%Y-%m-%d %H:%M:%S")
rid <- paste0("R_", replicate(n_rows,
        paste0(sample(c(letters, LETTERS, 0:9), 15, TRUE), collapse = "")))

meta <- data.frame(
  StartDate = stamps, EndDate = stamps, Status = "IP Address", IPAddress = "",
  Progress = ifelse(finished == "True", "100", "40"),
  `Duration (in seconds)` = as.character(round(rnorm(n_rows, 260, 70))),
  Finished = finished, RecordedDate = stamps, ResponseId = rid,
  RecipientLastName = "", RecipientFirstName = "", RecipientEmail = "",
  ExternalReference = "", LocationLatitude = "", LocationLongitude = "",
  DistributionChannel = "anonymous", UserLanguage = "EN",
  check.names = FALSE, stringsAsFactors = FALSE)

dat <- cbind(meta, resp)
dat[] <- lapply(dat, as.character)

meta_labels <- c("Start Date","End Date","Response Type","IP Address","Progress",
  "Duration (in seconds)","Finished","Recorded Date","Response ID",
  "Recipient Last Name","Recipient First Name","Recipient Email",
  "External Data Reference","Location Latitude","Location Longitude",
  "Distribution Channel","User Language")
tz <- ",\"timeZone\":\"America/Denver\""
meta_ids <- c(paste0("{\"ImportId\":\"startDate\"", tz, "}"),
  paste0("{\"ImportId\":\"endDate\"", tz, "}"),
  "{\"ImportId\":\"status\"}","{\"ImportId\":\"ipAddress\"}",
  "{\"ImportId\":\"progress\"}","{\"ImportId\":\"duration\"}",
  "{\"ImportId\":\"finished\"}",
  paste0("{\"ImportId\":\"recordedDate\"", tz, "}"),
  "{\"ImportId\":\"_recordId\"}","{\"ImportId\":\"recipientLastName\"}",
  "{\"ImportId\":\"recipientFirstName\"}","{\"ImportId\":\"recipientEmail\"}",
  "{\"ImportId\":\"externalDataReference\"}","{\"ImportId\":\"locationLatitude\"}",
  "{\"ImportId\":\"locationLongitude\"}","{\"ImportId\":\"distributionChannel\"}",
  "{\"ImportId\":\"userLanguage\"}")

header <- as.data.frame(matrix(c(meta_labels, cols,
                                 meta_ids, paste0("{\"ImportId\":\"", cols, "\"}")),
                               nrow = 2, byrow = TRUE), stringsAsFactors = FALSE)
names(header) <- names(dat)
write.csv(rbind(header, dat), out_file, row.names = FALSE, quote = TRUE, na = "")

cat("Wrote", out_file, "-", n_participants, "complete +",
    n_rows - n_participants, "incomplete.\n")
cat("Term assignment:\n"); print(table(term))
cat("Careless responders planted:", n_careless, "\n")
cat("Built-in critical covered-box rates: scalar", p_scalar_crit_covered,
    " number", p_number_crit_covered, "\n")
