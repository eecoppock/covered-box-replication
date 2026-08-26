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
#   critical   (NONE,ALL) / (1, 3v5)   the headline. No match is visible, so a
#                                      participant who insists on one must take
#                                      the covered box. 13% vs 100%.
#
#   strong     (SOME,ALL) / (2, 3v5)   NOT a comprehension check. A subset match
#                                      and a total-set match are both visible and
#                                      adults take the subset 90% of the time --
#                                      Huang et al. call this "a robust ability
#                                      to calculate the scalar implicature". It
#                                      is what makes the critical result strange:
#                                      the implicature is computed when it picks
#                                      something out, and abandoned when it does
#                                      not. Half the argument lives here.
#
#   weak       (NONE,SOME) / (1, 2)    this one really is a comprehension check:
#                                      it shows only that "some" is not "none"
#                                      and "two" is not "one".
#
# Statistically none of it needs replication -- simulated power for the critical
# contrast is 1.00 at eight participants per term with one trial each. Extra
# trials buy item generality and a graded per-participant rate, so they go where
# the argument is.
N_TRIALS = {"critical": 2, "weak": 1, "strong": 2, "probe": 1}

# nine objects, each with its plural for the number prompt
OBJECTS = [("cookie","cookies"), ("apple","apples"), ("balloon","balloons"),
           ("fish","fish"),      ("bird","birds"),   ("flower","flowers"),
           ("star","stars"),     ("heart","hearts"), ("leaf","leaves")]

NAMES = [("Zip","Nub"), ("Mo","Pim"), ("Dax","Wug"), ("Tev","Lom"), ("Bix","Rud"),
         ("Kel","Sap"), ("Jom","Nid"), ("Vex","Pol"), ("Gub","Tam")]

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
ORDER  = ["critical", "strong", "weak", "probe"]   # critical first, probe last
SCALAR = {"critical":"critical", "weak":"noneSome", "strong":"someAll", "probe":"probe"}
NUMBER = {"critical":"critical", "weak":"oneTwo",   "strong":"twoMore",  "probe":"probe"}

# which two open boxes each trial type shows (choice 1, choice 2)
SCALAR_BOXES = {"critical": ("NONE","ALL"),   # no subset match -> covered box
                "noneSome": ("NONE","SOME"),
                "someAll":  ("SOME","ALL"),
                "probe":    ("NONE","SOME")}  # of the WRONG object
NUMBER_BOXES = {"critical": (1,"more"),        # no exact match -> covered box
                "oneTwo":   (1,2),
                "twoMore":  (2,"more"),
                "probe":    (1,"more")}        # of the WRONG object

# what choices 1 and 2 mean, for choice-map.csv
SCALAR_MEANING = {"critical": ("none","all"), "noneSome": ("none","match"),
                  "someAll":  ("match","all"), "probe": ("wrong","wrong")}
NUMBER_MEANING = {"critical": ("one","more"), "oneTwo": ("one","match"),
                  "twoMore":  ("match","more"), "probe": ("wrong","wrong")}

MORE = [3, 5, 3, 5, 3, 5, 3, 5, 3]     # the "more than two" count, per set

# The object the PROBE asks for. It must be unmistakably absent from the boxes,
# which is a stronger requirement than merely being a different word: picking it
# by offset once landed on "leaves" while the boxes showed flowers, and a
# participant entitled to wonder whether those pink things count as leaves is a
# participant whose probe response means nothing. So it is named here, chosen to
# be as far from any object drawn as the inventory allows, and it is deliberately
# something no box in the study ever contains.
PROBE_NAMED = "hearts"

def _plan():
    """roles in presentation order, repeated N_TRIALS times each"""
    return [role for role in ORDER for _ in range(N_TRIALS[role])]

def scalar_trials():
    for i,role in enumerate(_plan()):
        kind = SCALAR[role]
        target, other = NAMES[i]
        _, plural = OBJECTS[i]
        if kind == "probe":
            plural = PROBE_NAMED
        yield dict(term="scalar", kind=kind, set=i+1,
                   prompt=f"Give me the box where {target} has some of the {plural}.",
                   boxes=[f"scalar_s{i+1}_{b}" for b in SCALAR_BOXES[kind]],
                   meaning=SCALAR_MEANING[kind])

def number_trials():
    for i,role in enumerate(_plan()):
        kind = NUMBER[role]
        _, plural = OBJECTS[i]
        if kind == "probe":
            plural = PROBE_NAMED
        counts = [MORE[i] if b == "more" else b for b in NUMBER_BOXES[kind]]
        yield dict(term="number", kind=kind, set=i+1,
                   prompt=f"Give me the box with two {plural}.",
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
