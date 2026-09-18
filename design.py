"""
The design, in one place, so make-stimuli.py and build-qsf.py cannot drift.

Huang, Spelke & Snedeker (2013), Experiment 4, reduced to what a class-sized
sample allows. See the long note below for what Exp 4 is and why it is the
target rather than Exp 1.
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
# The sequence every participant sees, in order. Written out rather than
# derived from counts, because the ORDER is the design at this point: what comes
# before what does as much work here as how many of each there are.
#
#   anchor          "all" first, so the domain of the partitive is settled
#                   before any "some" trial. See the note below.
#   probeEarly      a covered-box "none" trial. Breaks the all/some adjacency --
#                   otherwise the anchor's answer and the first critical trial's
#                   lower-bounded answer are the same configuration on
#                   consecutive screens, which all but demonstrates the
#                   equivalence under test -- and re-establishes the covered box
#                   right where extinction would bite.
#   criticalOneSet  OURS, and first among the critical trials: the domain
#                   loophole is closed here, so the first "some" judgment anyone
#                   makes is one the global reading cannot reach. That also
#                   settles the domain further before Huang et al.'s trials run.
#   critical        Huang et al.'s, for comparability with the published rate.
#   shape           familiarization-style filler: find a coloured shape. No
#                   quantifier in it at all, so it resets attention between
#                   critical trials without priming some, all or none. One of
#                   the three needs the covered box.
#   probe           the covered box again, at the end, under the most
#                   extinction pressure the study can apply.
# Rewritten 17 September 2026 to follow Huang, Spelke & Snedeker (2013)
# EXPERIMENT 4, which is the closest of their four to what can be run on a
# class in Qualtrics.
#
# Why Experiment 4 rather than Experiment 1. Exp 1 put trial type between
# subjects as well as term -- six cells of ten, and a participant saw three
# tokens of ONE trial type and no fillers whatever. Exp 4 keeps only the
# critical trial types, so everyone is in the cell that matters; it was run on
# fifty adults over Mechanical Turk rather than in a lab, which is much nearer
# to a Qualtrics survey; and, in their words, the three critical tokens "were
# randomized with three filler trials that were similar to those used in the
# Familiarization phase".
#
# Exp 4 also rebuilds the number trials so that both conditions look alike:
# Cookie Monster with 1 of 4 cookies against Cookie Monster with 3 of 4, asked
# as "give me the box where Cookie Monster has two of the cookies", because
# "these configurations ensured that the items in each box were matched for
# complexity across the scalar and number conditions". Their number trials are
# therefore the same two-character possession display as the scalar ones, not a
# bare count of fish.
#
# Their adult results in Exp 4: some(NONE,ALL) covered box 31%, total set 60%;
# two(1,3) covered box 92%, lower-bounded option 7%. The 31% is the benchmark
# the preregistered test in coveredbox-critical.R runs against; note it is 18
# points above the 13% of Exp 1, on the same trial type, which is itself worth
# showing a class.
#
# Everything this repository used to add -- anchorAll, probeEarly, probe,
# criticalOneSet, shape fillers, the four control trial types -- is gone. See
# archive/ for those designs, the intro-class data they produced, and why.

OBJECTS = [("cookie","cookies"), ("apple","apples"), ("balloon","balloons"),
           ("fish","fish"),      ("bird","birds"),   ("flower","flowers"),
           ("star","stars"),     ("heart","hearts"), ("leaf","leaves"),
           ("carrot","carrots"), ("mushroom","mushrooms")]

NAMES = [("Zip","Nub"), ("Mo","Pim"), ("Dax","Wug"), ("Tev","Lom"), ("Bix","Rud"),
         ("Kel","Sap"), ("Jom","Nid"), ("Vex","Pol"), ("Gub","Tam"), ("Ral","Fen"),
         ("Sib","Yon")]

LANGUAGE_Q = ("Is English your first language? <em>(optional)</em>",
              ["Yes", "No", "Prefer not to say"])

# Feedback after each trial of the FIRST familiarization pass. Huang et al. gave
# feedback there and let adults open the covered box while searching; the
# nearest thing Qualtrics allows is a screen saying where the target was.
FAM_FEEDBACK = {
 "1": "It was in the box on the left. When you can see what is being asked "
      "for, choose the box it is in.",
 "2": "It was in the box on the right. When you can see what is being asked "
      "for, choose the box it is in.",
 "3": "Neither open box had one, so it was in the closed box. When you cannot "
      "see what is being asked for, it is in the closed one.",
}

PASS2_NOTE = ("<p>Now the same four practice screens again. This time there is "
              "no feedback, and the closed box stays closed.</p><br>")

# ---- boxes ------------------------------------------------------------------
# Every open box is one image, drawn by make-stimuli.py, and its name carries
# everything needed to draw it: which object set, how many the TARGET character
# has, how many the other one has. Four objects per box throughout, as in
# Huang et al.
def box(set_i, n_target, n_other):
    return f"s{set_i}_{n_target}_{n_other}"

NONE_ = lambda i: box(i, 0, 4)   # target has none, other has all
ALL_  = lambda i: box(i, 4, 0)   # target has all, other has none
ONE_  = lambda i: box(i, 1, 3)   # the less-than option in two(1,3)
THREE_= lambda i: box(i, 3, 1)   # the more-than option in two(1,3), and the
                                 # "has some of them" box in the fillers

# ---- object and character assignment ---------------------------------------
# Disjoint across roles so nothing carries over.
CRIT_SCALAR = [1, 2, 3]    # cookies, apples, balloons
CRIT_NUMBER = [4, 5, 6]    # fish, birds, flowers
FILLERS     = [7, 8, 9]    # stars, hearts, leaves
FAM_SETS    = [10, 11]     # carrots, mushrooms

# ---- the trial list ---------------------------------------------------------
# A trial is (tag, prompt, [box1, box2], meaning1, meaning2, correct).
# "correct" is set only where there is a right answer: the familiarization and
# the fillers. The criticals are the measurement and have none.
#
# Fillers and familiarization use a BARE INDEFINITE -- "has a carrot" -- so no
# quantity judgment is involved and no partitive presupposition is in play.
# What varies across the two boxes is which character has the thing, or whether
# the named object is present at all. Neither ever shows the 4-0 configuration,
# because that box is the dependent variable and nobody should be taught how to
# treat it.

def _fam():
    c, m = FAM_SETS                       # carrots, mushrooms
    cn, mn = NAMES[c-1], NAMES[m-1]
    return [
      ("fam1", f"Give me the box where {cn[0]} has a carrot.",
       [NONE_(c), THREE_(c)], "other has them", "match", "2"),
      ("fam2", f"Give me the box where {mn[0]} has a mushroom.",
       [THREE_(m), NONE_(m)], "match", "other has them", "1"),
      ("fam3", f"Give me the box where {cn[0]} has a mushroom.",
       [THREE_(c), NONE_(c)], "wrong object", "wrong object", "3"),
      ("fam4", f"Give me the box where {mn[0]} has a carrot.",
       [NONE_(m), THREE_(m)], "wrong object", "wrong object", "3"),
    ]

def _fillers():
    a, b, c = FILLERS                     # stars, hearts, leaves
    an, bn, cn = NAMES[a-1], NAMES[b-1], NAMES[c-1]
    return [
      ("fill1", f"Give me the box where {an[0]} has a star.",
       [THREE_(a), NONE_(a)], "match", "other has them", "1"),
      ("fill2", f"Give me the box where {bn[0]} has a heart.",
       [NONE_(b), THREE_(b)], "other has them", "match", "2"),
      # the one filler answered by the covered box, placed late, where
      # extinction would otherwise start to bite
      ("fill3", f"Give me the box where {cn[0]} has a carrot.",
       [THREE_(c), NONE_(c)], "wrong object", "wrong object", "3"),
    ]

def _scalar_criticals():
    out = []
    for n, i in enumerate(CRIT_SCALAR, start=1):
        target = NAMES[i-1][0]; plural = OBJECTS[i-1][1]
        out.append((f"scalar_critical_s{i}",
                    f"Give me the box where {target} has some of the {plural}.",
                    [NONE_(i), ALL_(i)], "none", "all", None))
    return out

def _number_criticals():
    out = []
    for n, i in enumerate(CRIT_NUMBER, start=1):
        target = NAMES[i-1][0]; plural = OBJECTS[i-1][1]
        out.append((f"number_critical_s{i}",
                    f"Give me the box where {target} has two of the {plural}.",
                    [ONE_(i), THREE_(i)], "one", "three", None))
    return out

def familiarization():
    """Four trials, run twice by build-qsf.py. Two answered by an open box,
    two by the covered box, as in Huang et al."""
    return _fam()

def scalar_block():
    """Three fillers interleaved with the three criticals. Huang et al.
    randomized the six; the order here is fixed, so that every critical has a
    filler before it and the covered-box filler falls late rather than beside
    the first and most naive critical."""
    f = _fillers(); c = _scalar_criticals()
    return [f[0], c[0], f[1], c[1], f[2], c[2]]

def number_block():
    return _number_criticals()

def all_trials():
    return familiarization() + scalar_block() + number_block()

def all_boxes():
    """image name -> (object set, n_target, n_other), for make-stimuli.py"""
    out = {}
    for _tag, _p, boxes, _m1, _m2, _c in all_trials():
        for b in boxes:
            s_i, nt, no = (int(x) for x in b[1:].split("_"))
            out[b] = (s_i, nt, no)
    return out
