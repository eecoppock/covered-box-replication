"""
The design, in one place, so make-stimuli.py and build-qsf.py cannot drift.

Huang et al. put trial type BETWEEN subjects: a participant saw one trial type,
three times, with a different object each time. Running trial type within
subjects instead — which class-sized samples force — must not be done by
crossing object set with trial type, or every object turns up three times under
the same prompt and two of the three trials look like duplicates.

So object sets are NESTED in trial type: nine per term, three per trial type,
and every prompt in the survey is unique.
"""

# ---- how many trials of each kind ------------------------------------------
# Not all three test trial types are doing the same job, so they do not get the
# same number of trials.
#
# Every test trial shows two open boxes. What distinguishes the types is which
# two, relative to the MATCH -- the box that satisfies the description on the
# strengthened reading (the target has a proper subset / exactly two).
#
#   critical    less + more, NO match   (NONE,ALL) / (1, 3v5)
#                                      the headline. The match is absent, so a
#                                      participant who insists on one must take
#                                      the covered box. 13% vs 100%.
#
#   matchVsMore match + more            (SOME,ALL) / (2, 3v5)
#                                      NOT a comprehension check. A subset match
#                                      and a total-set match are both visible and
#                                      adults take the subset 90% of the time --
#                                      Huang et al. call this "a robust ability
#                                      to calculate the scalar implicature". It
#                                      is what makes the critical result strange:
#                                      the implicature is computed when it picks
#                                      something out, and abandoned when it does
#                                      not. Half the argument lives here.
#
#   matchVsLess less + match            (NONE,SOME) / (1, 2)
#                                      this one really is a comprehension check:
#                                      it shows only that "some" is not "none"
#                                      and "two" is not "one". 100% in the
#                                      original.
#
# Statistically none of it needs replication -- simulated power for the critical
# contrast is 1.00 at eight participants per term with one trial each. Extra
# trials buy item generality and a graded per-participant rate, so they go where
# the argument is.
#   otherQuant a filler in a DIFFERENT quantifier, whose answer is visible.
#              Without these the scalar term says "some" on five screens out of
#              six and "none" on one, which is an odd thing to put in front of
#              someone you are asking to interpret quantifiers -- the recurring
#              word invites theorising about it. Same for "two" in the number
#              term. These restore the balance and cost nothing: the answer is
#              always an open box.
#
#              One is "none"/"three", the other "all"/"five". Making *all*
#              salient should if anything INCREASE implicature computation,
#              since activated alternatives are what drive some -> not all. That
#              pushes toward the covered box, i.e. AGAINST the finding that
#              adults accept the total set as a match for "some". So the
#              manipulation is conservative: if the lower-bounded reading
#              survives with "all" primed, that is stronger evidence. They sit
#              after the critical trials in any case.
#   anchor        an "all" trial, FIRST. See the note on domain below.
#
#   criticalOneSet the same question as "critical", with the domain loophole
#                  closed. One open box holds every object on screen and the
#                  other holds none, so the global set and the box-internal set
#                  COINCIDE and the two readings cannot come apart:
#
#                    boxes  [nobody has any]  [target has all four]
#                    exclusive "some", either domain -> no match -> covered box
#                    lower-bounded "some", either    -> the full box
#
#                  Its rate against "critical" is the measure of how much of the
#                  standard result the global reading was buying: if they agree,
#                  the confound is not operating.
# This is Huang et al.'s design in full -- all three of their test conditions --
# plus additions. Their token counts were three of one condition per participant,
# since condition was between subjects for them; here everyone sees all three, so
# the counts differ while the design does not.
#   probeEarly  a covered-box "none" trial, wedged between the anchor and the
#               first critical trial. Two jobs.
#
#               Without it the anchor asks who has ALL of the cookies -- answer,
#               the full box -- and the very next screen asks who has SOME, where
#               the lower-bounded answer is again the full box. Choosing the same
#               configuration for "all" and then for "some" on consecutive
#               screens all but demonstrates the equivalence under test.
#
#               It also re-establishes the covered box immediately before the
#               critical trials, where the earlier worry about extinction
#               actually bites. Priming the covered box pushes toward implicature
#               computation and so AGAINST the finding that adults accept the
#               total set as "some", which makes it conservative, the same shape
#               of argument as for putting "all" first.
N_TRIALS = {"anchor": 1, "probeEarly": 1, "critical": 2, "criticalOneSet": 2,
            "matchVsMore": 1, "matchVsLess": 1, "otherQuant": 2, "probe": 1}

# ---- the domain of "the apples", and why an "all" trial goes first ----------
# "Give me the box where Zip has some of the apples" leaves the domain of "the
# apples" open. Box-internal -- the apples in the box under consideration -- or
# global, the apples anywhere on screen?
#
# It matters, because the global reading gives a complete alternative account of
# the headline result. On a critical trial the ALL box shows Zip with four of
# the eight apples visible. Read globally that IS "some but not all", so a
# participant can take the ALL box with the exclusive reading of "some" fully
# intact. Eighty-seven percent choosing it would then say nothing about whether
# the implicature was computed.
#
# The "all" trial separates the readings, and putting it first settles the
# question before any "some" trial is seen:
#
#   box-internal  the ALL box is correct: the target has all four in that box
#   global        no box is correct -- the target has four of eight on screen --
#                 so a global reader takes the covered box
#
# And because the task presupposes an answer exists, meeting "all" first pushes
# toward the only construal on which one does. The response is also recorded:
# a participant who takes the covered box here was reading globally, and their
# later "some" responses should be read in that light.
#
# The cost is that a trial with a visible answer now precedes the critical ones,
# which cuts against putting critical trials first. Familiarization already
# shows two visible-answer trials and two requiring the covered box, so this
# adds little; and the domain confound explains away the whole finding, where
# extinction only biases it in a direction the probe measures.

# "matchVsLess" was briefly set to 0. It is the one trial type here that is a pure comprehension
# check, it sits at ceiling in the original (100%), and four familiarization
# trials plus two fillers already do that job. It was also the trial inflating
# "some": dropping it moves the scalar balance from 5/2/1 to 3/2/1.
#
# The cost is real and belongs in the report: Some(NONE,SOME) is one of Huang et
# al.'s three test conditions, so this replication does not cover their full
# design. Its display is still seen -- noneVis uses the same pair of boxes -- but
# with "none" rather than "some". Setting "matchVsLess" back to 1 restores it.

# nine objects, each with its plural for the number prompt
OBJECTS = [("cookie","cookies"), ("apple","apples"), ("balloon","balloons"),
           ("fish","fish"),      ("bird","birds"),   ("flower","flowers"),
           ("star","stars"),     ("heart","hearts"), ("leaf","leaves"),
           ("carrot","carrots"), ("mushroom","mushrooms")]

NAMES = [("Zip","Nub"), ("Mo","Pim"), ("Dax","Wug"), ("Tev","Lom"), ("Bix","Rud"),
         ("Kel","Sap"), ("Jom","Nid"), ("Vex","Pol"), ("Gub","Tam"), ("Ral","Fen"),
         ("Sib","Yon")]

# trial types, in presentation order: critical first, then the two controls
# "probe" is not in Huang et al. In no trial type of theirs is the covered box
# unambiguously correct -- it is always the diagnostic option -- so the only
# thing establishing that it is ever right is familiarization. A participant who
# reads *some* as lower-bounded then never needs it again, and if it goes dead
# for them, a low covered-box rate is extinction rather than semantics.
#
# The probe asks for an object that is in NEITHER open box, so the covered box
# is correct whatever anyone's semantics. It sits AFTER the critical trials, so
# it cannot prime them, and it turns the worry into a measurement: if scalar
# participants pass the probe, their low critical rate is not extinction.
ORDER  = ["anchor", "probeEarly", "critical", "criticalOneSet", "matchVsMore",
          "matchVsLess", "otherQuant", "probe"]
SCALAR = {"anchor":"allVis", "probeEarly":"probeEarly", "critical":"critical",
          "criticalOneSet":"criticalOneSet", "matchVsLess":"noneSome",
          "matchVsMore":"someAll", "otherQuant":["noneVis","allVis"],
          "probe":"probe"}
# The number term has no partitive and so no domain ambiguity -- "the box with
# two fish" counts within a box by construction. Its anchor is there to keep the
# two versions the same length and shape.
#
# For the same reason criticalOneSet has no work to do here, and it maps to the
# ORDINARY critical kind. Giving it an empty box would only make the standard
# critical with a 0 in place of the 1 -- no loophole closed, and a blank white
# box that reads as an image that failed to load rather than a box with nothing
# in it. The number term therefore gets four critical trials and no empty boxes.
NUMBER = {"anchor":"fiveVis", "probeEarly":"probeEarly", "critical":"critical",
          "criticalOneSet":"critical", "matchVsLess":"oneTwo",
          "matchVsMore":"twoMore", "otherQuant":["threeVis","fiveVis"],
          "probe":"probe"}

# which two open boxes each trial type shows (choice 1, choice 2)
SCALAR_BOXES = {"critical": ("NONE","ALL"),   # no subset match -> covered box
                "noneSome": ("NONE","SOME"),
                "someAll":  ("SOME","ALL"),
                "probe":    ("SOME","ALL"),   # neither shows the target with none
                "probeEarly": ("SOME","ALL"),
                "criticalOneSet": ("EMPTY","ALL"), # every object is in one box
                "noneVis":  ("NONE","SOME"),  # the NONE panel is the answer
                "allVis":   ("SOME","ALL")}   # the ALL panel is the answer
NUMBER_BOXES = {"critical": (1,"more"),        # no exact match -> covered box
                "oneTwo":   (1,2),
                "twoMore":  (2,"more"),
                "probe":    (1,2),             # neither has five or more
                "probeEarly": (1,2),
                "criticalOneSet": (0,"more"),  # every object is in one box
                "threeVis": (1,3),             # the 3 box; unambiguous, 1 < 3
                "fiveVis":  (2,5)}             # the 5 box; unambiguous, 2 < 5

# what choices 1 and 2 mean, for choice-map.csv
SCALAR_MEANING = {"critical": ("none","all"), "noneSome": ("none","match"),
                  "someAll":  ("match","all"), "probe": ("absent","absent"),
                  "criticalOneSet": ("empty","all"),
                  "probeEarly": ("absent","absent"),
                  "noneVis":  ("match","other"), "allVis": ("other","match")}
NUMBER_MEANING = {"critical": ("one","more"), "oneTwo": ("one","match"),
                  "twoMore":  ("match","more"), "probe": ("absent","absent"),
                  "criticalOneSet": ("empty","more"),
                  "probeEarly": ("absent","absent"),
                  "threeVis": ("other","match"), "fiveVis": ("other","match")}

MORE = [3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3]  # the "more than two" count, per set

# ---- the probe, and the presupposition it must not violate -----------------
# The probe needs a configuration that is absent from both open boxes, so that
# the covered box is correct on anyone's semantics. Two earlier attempts got the
# absence in the wrong place.
#
# The paradigm already runs on ONE presupposition failure: "the box with two
# fish" presupposes such a box exists, and when none is visible, the inference is
# that it must be hidden. That is the whole task.
#
# An earlier probe asked for "some of the hearts" against boxes of flowers. That
# fails a DIFFERENT presupposition -- the restrictor's. "The hearts" presupposes
# a salient set of hearts, and there is none. Failed restrictors invite repair
# ("they must mean the flowers") rather than the inference that the referent is
# hidden, so the trial would have measured repair behaviour instead of whether
# the covered box is live.
#
# So the probe keeps the restrictor satisfied and puts the absence in the
# configuration:
#   scalar  boxes show SOME and ALL of the flowers; asks who has NONE of them.
#           "The flowers" refers; no box shows the target having none.
#   number  boxes show 1 and 2 flowers; asks for FIVE. Absent under exact
#           semantics (no box has exactly five) and under lower-bounded
#           semantics (none has five or more) -- which matters, since the
#           participants whose covered box we most doubt are the lower-bounded
#           ones, and a probe they could answer with a visible box is no probe.
PROBE_COUNT = "five"

def _plan(mapping):
    """concrete trial kinds in presentation order"""
    out=[]
    for role in ORDER:
        k = mapping[role]
        for n in range(N_TRIALS[role]):
            out.append(k[n % len(k)] if isinstance(k, list) else k)
    return out

def scalar_trials():
    for i,kind in enumerate(_plan(SCALAR)):
        target, other = NAMES[i]
        _, plural = OBJECTS[i]
        quant = {"probe":"none", "probeEarly":"none",
                 "noneVis":"none", "allVis":"all"}.get(kind, "some")
        yield dict(term="scalar", kind=kind, set=i+1,
                   prompt=f"Give me the box where {target} has {quant} of the {plural}.",
                   boxes=[f"scalar_s{i+1}_{b}" for b in SCALAR_BOXES[kind]],
                   meaning=SCALAR_MEANING[kind])

def number_trials():
    for i,kind in enumerate(_plan(NUMBER)):
        _, plural = OBJECTS[i]
        counts = [MORE[i] if b == "more" else b for b in NUMBER_BOXES[kind]]
        want = {"probe":PROBE_COUNT, "probeEarly":PROBE_COUNT,
                "threeVis":"three", "fiveVis":"five"}.get(kind, "two")
        yield dict(term="number", kind=kind, set=i+1,
                   prompt=f"Give me the box with {want} {plural}.",
                   boxes=[f"number_s{i+1}_{c}" for c in counts],
                   meaning=NUMBER_MEANING[kind])

def all_trials():
    return list(scalar_trials()) + list(number_trials())


# ---- familiarization -------------------------------------------------------
# Four practice trials, each naming a different shape, two where it is visible
# and two where it is not. Same prompt four times would teach the wrong lesson
# before the test trials even start.
FAM_SHAPES = {"fam_a1": ["star","tri"],  "fam_a2": ["sq","hex"],
              "fam_b1": ["tri","sq"],    "fam_b2": ["hex","star"],
              "fam_c2": ["sq","star"],
              "fam_d1": ["star","hex"],  "fam_d2": ["tri","star"]}

FAM = [  # (tag, prompt, [choice-1 box, choice-2 box], correct choice)
 ("fam1", "Give me the box with the red star.",       ["fam_a1","fam_a2"], "1"),
 ("fam2", "Give me the box with the green triangle.", ["fam_b1","fam_b2"], "1"),
 ("fam3", "Give me the box with the purple hexagon.", ["fam_a1","fam_c2"], "3"),
 ("fam4", "Give me the box with the orange square.",  ["fam_d1","fam_d2"], "3"),
]
