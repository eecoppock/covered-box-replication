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

# nine objects, each with its plural for the number prompt
OBJECTS = [("cookie","cookies"), ("apple","apples"), ("balloon","balloons"),
           ("fish","fish"),      ("bird","birds"),   ("flower","flowers"),
           ("star","stars"),     ("heart","hearts"), ("leaf","leaves")]

NAMES = [("Zip","Nub"), ("Mo","Pim"), ("Dax","Wug"), ("Tev","Lom"), ("Bix","Rud"),
         ("Kel","Sap"), ("Jom","Nid"), ("Vex","Pol"), ("Gub","Tam")]

# trial types, in presentation order: critical first, then the two controls
SCALAR_TYPES = ["critical", "noneSome", "someAll"]
NUMBER_TYPES = ["critical", "oneTwo",   "twoMore"]

# which two open boxes each trial type shows (choice 1, choice 2)
SCALAR_BOXES = {"critical": ("NONE","ALL"),   # no subset match -> covered box
                "noneSome": ("NONE","SOME"),
                "someAll":  ("SOME","ALL")}
NUMBER_BOXES = {"critical": (1,"more"),        # no exact match -> covered box
                "oneTwo":   (1,2),
                "twoMore":  (2,"more")}

# what choices 1 and 2 mean, for choice-map.csv
SCALAR_MEANING = {"critical": ("none","all"), "noneSome": ("none","match"),
                  "someAll":  ("match","all")}
NUMBER_MEANING = {"critical": ("one","more"), "oneTwo": ("one","match"),
                  "twoMore":  ("match","more")}

MORE = [3, 5, 3, 5, 3, 5, 3, 5, 3]     # the "more than two" count, per set

def scalar_trials():
    """nine trials: sets 0-2 critical, 3-5 noneSome, 6-8 someAll"""
    for i in range(9):
        kind = SCALAR_TYPES[i // 3]
        target, other = NAMES[i]
        _, plural = OBJECTS[i]
        yield dict(term="scalar", kind=kind, set=i+1,
                   prompt=f"Give me the box where {target} has some of the {plural}.",
                   boxes=[f"scalar_s{i+1}_{b}" for b in SCALAR_BOXES[kind]],
                   meaning=SCALAR_MEANING[kind])

def number_trials():
    """nine trials: sets 0-2 critical, 3-5 oneTwo, 6-8 twoMore"""
    for i in range(9):
        kind = NUMBER_TYPES[i // 3]
        _, plural = OBJECTS[i]
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
