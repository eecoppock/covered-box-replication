#!/usr/bin/env python3
"""
Builds the Qualtrics survey for the Huang, Spelke & Snedeker Exp. 1 replication.

    python3 build-qsf.py [BASE_URL]        # full survey
    python3 build-qsf.py [BASE_URL] --test # two-question smoke test

HOW THIS FILE IS BUILT, AND WHY. Qualtrics rejects a malformed import outright
("Something went wrong and the project wasn't created") with no diagnostic, so
nothing here is invented. The template is CoveredBoxtest.qsf -- a real export
from this account containing exactly the question type we need, a horizontal
multiple choice between graphic options. Its SurveyEntry, and every element
except the questions, blocks and flow, are carried over untouched. That also
avoids inheriting another survey's library references, which an earlier version
did and which may well be why it would not import.

Two things worth knowing, both learned the hard way:
  * graphic choices need Configuration.LabelPosition = "BELOW"
  * blocks carry NO Options key at all -- not even Options: null

Choice IDs are stable whatever order the boxes appear in:
    1 = first open box   2 = second open box   3 = the COVERED box
What 1 and 2 mean varies by trial type, so choice-map.csv records it.
"""
import json, copy, sys, csv, hashlib

args = [a for a in sys.argv[1:] if not a.startswith("--")]
TEST = "--test" in sys.argv
BASE = args[0] if args else "IMAGE_BASE_URL"
TEMPLATE = "qsf-template.json"
OUT = "_import-smoke-test.qsf" if TEST else "HuangSnedeker_replication.qsf"

def img(name, w=280):
    return (f'<img src="{BASE}/{name}.png" '
            f'style="width:100%;max-width:{w}px;height:auto;" alt="">')

def bid(seed):
    h = hashlib.md5(seed.encode()).hexdigest()
    alnum = "".join(c for c in h if c.isalnum())[:15]
    return "BL_" + alnum

import design

PREAMBLE = (
 "<p>On each screen you will see three boxes. Two are open, so you can see what "
 "is inside. The third is closed, so you cannot.</p><p>Each time, choose the box "
 "that matches the description. <b>If neither open box matches, the box you want "
 "must be the closed one.</b></p><p>These first few screens are practice.</p><br>")

# ---------------------------------------------------------------- build
tpl = json.load(open(TEMPLATE))
SID = tpl["SurveyEntry"]["SurveyID"]
qsf = {"SurveyEntry": copy.deepcopy(tpl["SurveyEntry"]), "SurveyElements": []}
qsf["SurveyEntry"]["SurveyName"] = ("Covered box — import test" if TEST
                                    else "Covered box replication")

# Strip the institutional branding. A QSF exported from a Qualtrics account that
# has a brand carries its ID in SurveyOptions.Skin.brandingId, and the survey
# then renders with the university's header, colours and logo. Setting it to
# null gives the plain "*simple" theme. This is enforced here as well as in the
# template, so that re-vendoring the template from a fresh export cannot quietly
# bring the branding back. SkinLibrary stays as it is: that is the account's
# library namespace, not anything the participant sees.
for _e in qsf["SurveyElements"]:
    if _e.get("Element") == "SO" and isinstance(_e.get("Payload"), dict):
        _skin = _e["Payload"].get("Skin")
        if isinstance(_skin, dict):
            _skin["brandingId"] = None
mc_tpl = [e for e in tpl["SurveyElements"]
          if e.get("Element")=="SQ" and e["Payload"]["QuestionType"]=="MC"][0]
# A free-text question type, vendored into the template from Homework/hw4-form.qsf,
# which is a real export from the same account containing one. The rule here is
# never to invent a Qualtrics question type: an invented one fails the import
# with no diagnostic beyond "something went wrong and the project wasn't created".
te_tpl = [e for e in tpl["SurveyElements"]
          if e.get("Element")=="SQ" and e["Payload"]["QuestionType"]=="TE"][0]
for e in tpl["SurveyElements"]:
    if e.get("Element") not in ("SQ","BL","FL"):
        qsf["SurveyElements"].append(copy.deepcopy(e))

qid=[0]
rot_i=[0]          # counts only the image questions, so feedback screens
                   # inserted between them do not shift the rotation
def mc(tag, prompt, boxes, preamble=""):
    qid[0]+=1; q=f"QID{qid[0]}"
    names = boxes + ["covered"]
    el = copy.deepcopy(mc_tpl)
    el["PrimaryAttribute"]=q; el["SecondaryAttribute"]=prompt[:95]
    p = el["Payload"]
    p["QuestionText"] = preamble + f'<span style="font-size:19px;">{prompt}</span>'
    p["DataExportTag"]=tag; p["QuestionID"]=q
    p["QuestionDescription"]=prompt[:95]
    p["Choices"] = {str(i+1): {"Display": img(n)} for i,n in enumerate(names)}
    rot = rot_i[0] % 3; rot_i[0]+=1
    p["ChoiceOrder"] = (["3","1","2"] if rot==0 else
                        ["1","3","2"] if rot==1 else ["1","2","3"])
    p["Validation"]["Settings"]["ForceResponse"]="ON"
    p["NextChoiceId"]=4
    qsf["SurveyElements"].append(el)
    return q

def feedback(tag, text):
    """Huang et al. gave feedback after every trial of the first familiarization
    pass, and let people open the covered box while searching. Qualtrics can do
    neither, so the equivalent is a screen that states where the target was.
    Built on the same MC payload as everything else, with a single Continue
    option, because introducing a new question type is how a QSF import fails."""
    qid[0]+=1; q=f"QID{qid[0]}"
    el = copy.deepcopy(mc_tpl)
    el["PrimaryAttribute"]=q; el["SecondaryAttribute"]=tag
    p = el["Payload"]
    p["QuestionText"] = f'<span style="font-size:18px;">{text}</span>'
    p["DataExportTag"]=tag; p["QuestionID"]=q
    p["QuestionDescription"]=tag
    p["Selector"]="SAVR"
    p["Configuration"]={"QuestionDescriptionOption":"UseText"}
    p["Choices"]={"1":{"Display":"Continue"}}
    p["ChoiceOrder"]=["1"]
    p["Validation"]["Settings"]["ForceResponse"]="OFF"
    p["NextChoiceId"]=2
    qsf["SurveyElements"].append(el)
    return q

def text_entry(tag, prompt, required=True):
    """One free-text box. Used for the Kerberos ID, which is what turns twelve
    anonymous rows into twelve students who can be given a check and, more to
    the point, tells you which student is the missing thirteenth."""
    qid[0]+=1; q=f"QID{qid[0]}"
    el = copy.deepcopy(te_tpl)
    el["PrimaryAttribute"]=q; el["SecondaryAttribute"]=tag
    p = el["Payload"]
    p["QuestionText"]=prompt
    p["DataExportTag"]=tag; p["QuestionID"]=q
    p["QuestionDescription"]=tag
    p["Validation"]={"Settings":{"ForceResponse":"ON" if required else "OFF",
                                 "Type":"None"}}
    qsf["SurveyElements"].append(el)
    return q

def text_mc(tag, prompt, options):
    """A plain text multiple choice. Same payload as the graphic questions but
    vertical and without LabelPosition, which matches the other QSF here known
    to import (Emotion_words.qsf, SAVR with text choices)."""
    qid[0]+=1; q=f"QID{qid[0]}"
    el = copy.deepcopy(mc_tpl)
    el["PrimaryAttribute"]=q; el["SecondaryAttribute"]=prompt[:95]
    p = el["Payload"]
    p["QuestionText"] = f'<span style="font-size:18px;">{prompt}</span>'
    p["DataExportTag"]=tag; p["QuestionID"]=q
    p["QuestionDescription"]=prompt[:95]
    p["Selector"]="SAVR"
    p["Configuration"]={"QuestionDescriptionOption":"UseText"}
    p["Choices"]={str(i+1): {"Display": o} for i,o in enumerate(options)}
    p["ChoiceOrder"]=[str(i+1) for i in range(len(options))]
    p["Validation"]["Settings"]["ForceResponse"]="OFF"
    p["NextChoiceId"]=len(options)+1
    qsf["SurveyElements"].append(el)
    return q

def block(seed, desc, qids, typ="Standard"):
    be=[]
    for i,q in enumerate(qids):
        if i: be.append({"Type":"Page Break"})
        be.append({"Type":"Question","QuestionID":q})
    return {"Type":typ,"Description":desc,"ID":bid(seed),"BlockElements":be}

rows=[("question","choice_id","meaning")]
blocks=[]

if TEST:
    f0 = design.familiarization()[0]; c0 = design.scalar_block()[1]
    qs=[mc("t1", f0[1], f0[2], PREAMBLE), mc("t2", c0[1], c0[2])]
    blocks.append(block("test","Default Question Block",qs,typ="Default"))
    flow_inner=[{"ID":blocks[0]["ID"],"Type":"Block","FlowID":"FL_2"}]
    count=3
else:
    # Huang et al. ran the four familiarization trials TWICE. On the first
    # pass adults got feedback after each choice and could open the covered box
    # while searching; on the second they were told not to open it and got no
    # feedback. Familiarization here uses the same two-character possession
    # display as the test trials, asked with a bare indefinite ("has a
    # carrot"), so the practice is the same shape as the thing practised.
    def add(tag, prompt, boxes, m1, m2, preamble=""):
        q = mc(tag, prompt, boxes, preamble)
        rows.extend([(tag,"1",m1),(tag,"2",m2),(tag,"3","covered")])
        return q

    fam=[]
    for i,(tag,prompt,boxes,m1,m2,correct) in enumerate(design.familiarization()):
        fam.append(add(tag, prompt, boxes, m1, m2, PREAMBLE if i==0 else ""))
        rows.append((tag,"correct",correct))
        fam.append(feedback(f"{tag}_fb", design.FAM_FEEDBACK[correct]))
    for i,(tag,prompt,boxes,m1,m2,correct) in enumerate(design.familiarization()):
        t2=f"{tag}_p2"
        fam.append(add(t2, prompt, boxes, m1, m2, design.PASS2_NOTE if i==0 else ""))
        rows.append((t2,"correct",correct))
    blocks.append(block("fam","Familiarization",fam,typ="Default"))

    # Test phase, counterbalanced on object set. Version A gives the scalar
    # trials cookies/apples/balloons, version B gives them fish/birds/flowers,
    # and the number trials take whichever set is left. A randomiser over two
    # Groups picks one and stamps `objects` as embedded data, so the assignment
    # is recorded rather than inferred. A Group wrapper rather than a Branch:
    # branches have been the fragile part of every QSF in this project, and a
    # randomiser over groups needs no condition logic.
    #
    # The critical tags carry their object set already (scalar_critical_s1 is
    # cookies, scalar_critical_s4 is fish), so they are unique across versions.
    # The fillers are identical in both and would collide, so they take a
    # version suffix.
    version_ids = {}
    for v in ("A", "B"):
        ids = []
        for name, trials in (("scalar", design.scalar_block(v)),
                             ("number", design.number_block(v))):
            qs = []
            for tag, prompt, boxes, m1, m2, correct in trials:
                t = tag if tag.startswith(("scalar_", "number_")) else f"{tag}_{v}"
                qs.append(add(t, prompt, boxes, m1, m2))
                if correct: rows.append((t, "correct", correct))
            blk = block(f"{name}{v}", f"{name} block, objects {v}", qs)
            blocks.append(blk); ids.append(blk["ID"])
        version_ids[v] = ids

    def _ed(value):
        return {"Type":"EmbeddedData","FlowID":f"FL_ED{value}","EmbeddedData":[
            {"Description":"objects","Type":"Custom","Field":"objects",
             "VariableType":"String","DataVisibility":[],"AnalyzeText":False,
             "Value":value}]}

    flow_inner=[{"ID":blocks[0]["ID"],"Type":"Block","FlowID":"FL_2"},
      {"Type":"BlockRandomizer","FlowID":"FL_3","SubSet":1,"EvenPresentation":True,
       "Flow":[
         {"Type":"Group","FlowID":"FL_10","Description":"objects A","Flow":[
            _ed("A"),
            {"ID":version_ids["A"][0],"Type":"Block","FlowID":"FL_12"},
            {"ID":version_ids["A"][1],"Type":"Block","FlowID":"FL_13"}]},
         {"Type":"Group","FlowID":"FL_20","Description":"objects B","Flow":[
            _ed("B"),
            {"ID":version_ids["B"][0],"Type":"Block","FlowID":"FL_22"},
            {"ID":version_ids["B"][1],"Type":"Block","FlowID":"FL_23"}]}]}]
    count=30

if not TEST:
    lang_q = text_mc("first_language", design.LANGUAGE_Q[0], design.LANGUAGE_Q[1])
    # The identifier goes LAST, after everything including the optional language
    # question, so it cannot colour a single response. It is the only required
    # question outside the trials.
    kerb_q = text_entry("kerberos", design.KERBEROS_Q)
    lang_b = block("lang", "Language background and ID", [lang_q, kerb_q])
    blocks.append(lang_b)
    flow_inner.append({"ID": lang_b["ID"], "Type": "Block", "FlowID": "FL_7"})
    for i, o in enumerate(design.LANGUAGE_Q[1], start=1):
        rows.append(("first_language", str(i), o))
    rows.append(("kerberos", "text", "BU Kerberos ID, joins to Roster/roster-merged.csv `coder`"))

blocks.append({"Type":"Trash","Description":"Trash / Unused Questions",
               "ID":bid("trash")})
qsf["SurveyElements"].append({"SurveyID":SID,"Element":"BL",
  "PrimaryAttribute":"Survey Blocks","SecondaryAttribute":None,
  "TertiaryAttribute":None,"Payload":blocks})
qsf["SurveyElements"].append({"SurveyID":SID,"Element":"FL",
  "PrimaryAttribute":"Survey Flow","SecondaryAttribute":None,
  "TertiaryAttribute":None,
  "Payload":{"Flow":flow_inner,"Properties":{"Count":count},
             "FlowID":"FL_1","Type":"Root"}})

json.dump(qsf, open(OUT,"w"), indent=2)
mcq=[e for e in qsf["SurveyElements"] if e.get("Element")=="SQ"]
print(f"wrote {OUT}: {len(mcq)} questions, {len(blocks)} blocks")
if not TEST:
    with open("choice-map.csv","w",newline="") as fh: csv.writer(fh).writerows(rows)
    with open("columns.txt","w") as fh:
        # `objects` is embedded data set by the flow and Qualtrics exports it
        # as a column like any other. Scalar always runs first, so there is no
        # order variable to record.
        fh.write("\n".join([e["Payload"]["DataExportTag"] for e in mcq]
                            + ["objects"])+"\n")
    print("wrote columns.txt and choice-map.csv")
