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
         ("Sib","Yon"), ("Quo","Bev"), ("Hix","Dru"), ("Nal","Pex")]

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
# Every open box is one image and its name is its recipe, so make-stimuli.py
# draws straight from the design and there is no tag table to drift.
#
# TEST boxes:      s<nameset>_<target count>_<other count>, one object kind
# PRACTICE boxes:  p<nameset>_<target's objects>__<other's objects>

def box(set_i, n_target, n_other):
    return f"s{set_i}_{n_target}_{n_other}"

def pbox(set_i, t_objs, o_objs, shared=False):
    """shared=True lifts the disjointness rule, and is for the one filler whose
    prompt is about BOTH characters. Overlap confuses a question about one
    person and is the content of a question about two."""
    assert shared or not (set(t_objs) & set(o_objs)), \
           "characters must hold disjoint kinds unless the prompt asks about both"
    assert len(set(t_objs)) == len(t_objs) and len(set(o_objs)) == len(o_objs), \
           "nobody holds two of the same kind"
    return f"p{set_i}_{'-'.join(t_objs)}__{'-'.join(o_objs)}"

NONE_ = lambda i: box(i, 0, 4)
ALL_  = lambda i: box(i, 4, 0)
ONE_  = lambda i: box(i, 1, 3)
THREE_= lambda i: box(i, 3, 1)

# ---- object and character assignment ---------------------------------------
# Object set is COUNTERBALANCED against scale type. Version A gives the scalar
# trials cookies/apples/balloons and the number trials fish/birds/flowers;
# version B swaps them. Huang et al. did not need this, because Exp 4 was
# between subjects and used Cookie Monster with cookies in both conditions. We
# separated the objects so the same participant does not meet the same material
# twice under two different prompts, and that separation would otherwise leave
# object set perfectly confounded with the term. Counterbalancing costs nothing:
# every participant still does three scalar criticals, so the replication
# comparison keeps everyone, and only the some-against-two contrast gains.
#
# Order is NOT counterbalanced and cannot be without giving something up: the
# scalar cell is the measurement and its value depends on those participants
# being naive about the task's quantity dimension, so scalar always runs first.
# That is a declared trade-off, not an oversight.
SETS_A = {"scalar": [1, 2, 3], "number": [4, 5, 6]}   # cookies… / fish…
SETS_B = {"scalar": [4, 5, 6], "number": [1, 2, 3]}   # fish…    / cookies…
VERSIONS = {"A": SETS_A, "B": SETS_B}
SFILL_NAMES = [7, 8, 9]       # Jom/Nid, Vex/Pol, Gub/Tam
FAM_NAMES   = [10, 11]        # Ral/Fen, Sib/Yon
NFILL_NAMES = [12, 13, 14]    # Quo/Bev, Hix/Dru, Nal/Pex

# ---- the trial list ---------------------------------------------------------
# A trial is (tag, prompt, [box1, box2], meaning1, meaning2, correct).
# "correct" is set only where there is a right answer: familiarization and the
# fillers. The criticals are the measurement and have none.
#
# Two rules hold across every practice box, and pbox() asserts both.
#
#   NOBODY HOLDS TWO OF THE SAME KIND. That is what keeps the indefinite in the
#   prompt off a scale: "a heart" is underinformative against two hearts, not
#   against a heart and a leaf. An early version gave the target three carrots
#   and asked for "a carrot", which made the correct box true-but-
#   underinformative -- the same relation the ALL box bears to "some" -- and,
#   because that box was keyed correct, would have excluded anyone who read the
#   indefinite exactly, i.e. the implicature computers.
#
#   THE TWO CHARACTERS HOLD DISJOINT KINDS. Hearts on both sides of the divider
#   are a harder discrimination but an avoidably confusing display, and the
#   possession swap between the two boxes already forces attention to WHO has
#   what. Note this is one way the practice differs from the criticals, where
#   both characters do share a kind; nothing else about the format does.
#
# Characters may hold SEVERAL different objects, so the practice displays are
# not all the same shape and the step up to four objects on a test trial is
# smaller.

def _fam():
    r, sb = FAM_NAMES
    rn, sn = NAMES[r-1], NAMES[sb-1]
    return [
      ("fam1", f"Give me the box where {rn[0]} has a carrot.",
       [pbox(r, ["mushroom"], ["carrot"]),
        pbox(r, ["carrot"], ["mushroom"])], "other has it", "match", "2"),
      ("fam2", f"Give me the box where {sn[0]} has a mushroom.",
       [pbox(sb, ["mushroom"], ["carrot","leaf"]),
        pbox(sb, ["leaf"], ["mushroom","carrot"])], "match", "other has it", "1"),
      ("fam3", f"Give me the box where {rn[0]} has a leaf.",
       [pbox(r, ["carrot"], ["mushroom"]),
        pbox(r, ["mushroom"], ["carrot"])], "no leaf", "no leaf", "3"),
      ("fam4", f"Give me the box where {sn[0]} has a carrot.",
       [pbox(sb, ["mushroom","leaf"], ["carrot"]),
        pbox(sb, ["leaf"], ["carrot","mushroom"])], "no carrot", "no carrot", "3"),
    ]

def _scalar_fillers():
    a, b, c = SFILL_NAMES
    an, bn, cn = NAMES[a-1], NAMES[b-1], NAMES[c-1]
    return [
      ("fill1", f"Give me the box where {an[0]} has a star.",
       [pbox(a, ["star"], ["heart"]),
        pbox(a, ["heart"], ["star"])], "match", "other has it", "1"),
      # The one prompt about BOTH characters. It forces a check of each side and
      # of how the objects are distributed, which is what the critical trial
      # demands when Zip has all the cookies and Nub has none. The near-miss
      # box gives a heart to one of them only.
      ("fill2", f"Give me the box where both {bn[0]} and {bn[1]} have a heart.",
       [pbox(b, ["heart"], ["heart"], shared=True),
        pbox(b, ["heart"], ["star"])], "both have one", "only one of them", "1"),
      ("fill3", f"Give me the box where {cn[0]} has a carrot.",
       [pbox(c, ["star","leaf"], ["heart"]),
        pbox(c, ["heart"], ["star","leaf"])], "no carrot", "no carrot", "3"),
    ]

def _number_fillers():
    a, b, c = NFILL_NAMES
    an, bn, cn = NAMES[a-1], NAMES[b-1], NAMES[c-1]
    return [
      ("nfill1", f"Give me the box where {an[0]} has a mushroom.",
       [pbox(a, ["mushroom"], ["star"]),
        pbox(a, ["star"], ["mushroom"])], "match", "other has it", "1"),
      ("nfill2", f"Give me the box where {bn[0]} has a leaf.",
       [pbox(b, ["carrot"], ["leaf","heart"]),
        pbox(b, ["leaf"], ["carrot","heart"])], "other has it", "match", "2"),
      ("nfill3", f"Give me the box where {cn[0]} has a star.",
       [pbox(c, ["carrot","leaf"], ["mushroom"]),
        pbox(c, ["mushroom"], ["carrot","leaf"])], "no star", "no star", "3"),
    ]

def _scalar_criticals(sets):
    out=[]
    for i in sets["scalar"]:
        t=NAMES[i-1][0]; pl=OBJECTS[i-1][1]
        out.append((f"scalar_critical_s{i}",
                    f"Give me the box where {t} has some of the {pl}.",
                    [NONE_(i), ALL_(i)], "none", "all", None))
    return out

def _number_criticals(sets):
    out=[]
    for i in sets["number"]:
        t=NAMES[i-1][0]; pl=OBJECTS[i-1][1]
        out.append((f"number_critical_s{i}",
                    f"Give me the box where {t} has two of the {pl}.",
                    [ONE_(i), THREE_(i)], "one", "three", None))
    return out

def familiarization():
    """Four trials, run twice by build-qsf.py. Two answered by an open box and
    two by the covered box, as in Huang et al."""
    return _fam()

def scalar_block(version="A"):
    """Three fillers interleaved with the three criticals, as in Exp 4, where
    the critical tokens "were randomized with three filler trials that were
    similar to those used in the Familiarization phase". Fixed order rather
    than randomized, so every critical has a filler before it and the
    covered-box filler falls late rather than beside the first and most naive
    critical."""
    f=_scalar_fillers(); c=_scalar_criticals(VERSIONS[version])
    return [f[0], c[0], f[1], c[1], f[2], c[2]]

def number_block(version="A"):
    """Same shape. Exp 4's number condition had its three fillers too, and this
    block runs last, where extinction pressure is highest and where there would
    otherwise be no covered-box trial for six screens."""
    f=_number_fillers(); c=_number_criticals(VERSIONS[version])
    return [f[0], c[0], f[1], c[1], f[2], c[2]]

def all_trials():
    """Every trial in either version, for the stimulus generator."""
    out = familiarization()
    for v in VERSIONS:
        out += scalar_block(v) + number_block(v)
    seen=set(); uniq=[]
    for t in out:
        if t[0] in seen: continue
        seen.add(t[0]); uniq.append(t)
    return uniq

def all_boxes():
    """image name -> how to draw it"""
    import re
    out={}
    for _tag,_p,boxes,_m1,_m2,_c in all_trials():
        for b in boxes:
            if b.startswith("s"):
                i,nt,no=(int(x) for x in b[1:].split("_"))
                out[b]={"kind":"test","set":i,"obj":OBJECTS[i-1][0],
                        "t_n":nt,"o_n":no}
            else:
                m=re.fullmatch(r"p(\d+)_([a-z-]+)__([a-z-]+)", b)
                i,t,o_=m.groups()
                out[b]={"kind":"practice","set":int(i),
                        "t_objs":t.split("-"),"o_objs":o_.split("-")}
    return out