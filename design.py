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
# The published effect is 13% vs 100% covered-box choices, between subjects.
# Simulated power to detect it is 1.00 even with eight participants per term
# giving ONE critical trial each, so observations per cell buy nothing
# statistically. Three critical trials are kept only for item generality --
# does it hold across objects? -- and because a 0/3..3/3 per-participant rate
# reads better than a bare yes/no. The controls exist to show the task works,
# which one trial each demonstrates and the four familiarization trials mostly
# establish already.
N_CRITICAL = 3
N_CONTROL  = 1          # per control trial type
N_PROBE    = 1          # see below

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
SCALAR_TYPES = ["critical", "noneSome", "someAll", "probe"]
NUMBER_TYPES = ["critical", "oneTwo",   "twoMore", "probe"]

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

def _plan():
    """[(trial type, index within it)], critical first"""
    out=[]
    for j,k in enumerate([N_CRITICAL, N_CONTROL, N_CONTROL, N_PROBE]):
        out += [(j, n) for n in range(k)]
    return out

def scalar_trials():
    for i,(t,_) in enumerate(_plan()):
        kind = SCALAR_TYPES[t]
        target, other = NAMES[i]
        _, plural = OBJECTS[i]
        if kind == "probe":                       # ask for an absent object
            plural = OBJECTS[(i+3) % len(OBJECTS)][1]
        yield dict(term="scalar", kind=kind, set=i+1,
                   prompt=f"Give me the box where {target} has some of the {plural}.",
                   boxes=[f"scalar_s{i+1}_{b}" for b in SCALAR_BOXES[kind]],
                   meaning=SCALAR_MEANING[kind])

def number_trials():
    for i,(t,_) in enumerate(_plan()):
        kind = NUMBER_TYPES[t]
        _, plural = OBJECTS[i]
        if kind == "probe":                       # ask for an absent object
            plural = OBJECTS[(i+3) % len(OBJECTS)][1]
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
