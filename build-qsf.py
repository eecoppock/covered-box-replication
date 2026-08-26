#!/usr/bin/env python3
"""
Builds the Qualtrics survey for the Huang, Spelke & Snedeker Exp. 1 replication.

    python3 build-qsf.py [BASE_URL]

Each trial is a multiple-choice question whose three answer choices are the three
box images, shown side by side.

DESIGN NOTE ON THE FILE FORMAT. A QSF is picky, and Qualtrics rejects the whole
import with no diagnostic if anything is off. So this script only emits
structures that appear in QSFs known to import: the MC payload copies the key
set and order Qualtrics itself exports, every block carries Options: null, and
the flow uses nothing beyond Root, Block and BlockRandomizer. In particular
there is no choice-order randomisation and no RecodeValues, because neither
could be verified against a working example.

Position is therefore counterbalanced by hand instead: within each trial type
the three tokens put the covered box first, second and third. That is fully
balanced rather than merely random, which is if anything better.

Choice IDs are stable and mean the same thing on every trial regardless of the
order they are displayed in:

    1 = the "less" box   2 = the other open box   3 = the COVERED box

What "the other open box" is varies by trial type, so build-qsf.py also writes
choice-map.csv saying what each ID means where. The analysis reads it.
"""
import json, copy, sys, csv

BASE = sys.argv[1] if len(sys.argv) > 1 else "IMAGE_BASE_URL"
TEMPLATE, OUT = "qsf-template.json", "HuangSnedeker_replication.qsf"
SID = "SV_5oCoveredBox1"

def img(name, w=290):
    return (f'<img src="{BASE}/{name}.png" '
            f'style="width:100%;max-width:{w}px;height:auto;" alt="">')

SCALAR_SETS = [(1,"Zip","cookies"), (2,"Mo","apples"), (3,"Dax","balloons")]
NUMBER_SETS = [(1,"fish",3), (2,"birds",5), (3,"flowers",3)]

# (tag, prompt, [box for choice 1, box for choice 2], meaning of choice 1 and 2)
def trials():
    out=[]
    for s,who,obj in SCALAR_SETS:
        p=f"Give me the box where {who} has some of the {obj}."
        out.append(("scalar","critical",s,p,[f"scalar_s{s}_NONE",f"scalar_s{s}_ALL"],
                    ["none","all"]))
    for s,who,obj in SCALAR_SETS:
        p=f"Give me the box where {who} has some of the {obj}."
        out.append(("scalar","noneSome",s,p,[f"scalar_s{s}_NONE",f"scalar_s{s}_SOME"],
                    ["none","match"]))
        out.append(("scalar","someAll",s,p,[f"scalar_s{s}_SOME",f"scalar_s{s}_ALL"],
                    ["match","all"]))
    for s,obj,more in NUMBER_SETS:
        p=f"Give me the box with two {obj}."
        out.append(("number","critical",s,p,[f"number_s{s}_1",f"number_s{s}_{more}"],
                    ["one","more"]))
    for s,obj,more in NUMBER_SETS:
        p=f"Give me the box with two {obj}."
        out.append(("number","oneTwo",s,p,[f"number_s{s}_1",f"number_s{s}_2"],
                    ["one","match"]))
        out.append(("number","twoMore",s,p,[f"number_s{s}_2",f"number_s{s}_{more}"],
                    ["match","more"]))
    return out

FAM = [("fam1", "1", ["fam1_yes","fam1_no"]),   # red star visible -> choice 1
       ("fam2", "1", ["fam2_yes","fam2_no"]),
       ("fam3", "3", ["fam3_no_a","fam3_no_b"]), # not visible -> covered
       ("fam4", "3", ["fam4_no","fam1_no"])]
FAM_PROMPT = "Give me the box with the red star."

INSTRUCTIONS = (
 "<p>On each screen you will see three boxes. Two are open, so you can see what "
 "is inside. The third is closed, so you cannot.</p>"
 "<p>Each time, choose the box that matches the description. <b>If neither open "
 "box matches, then the box you want must be the closed one.</b></p>"
 "<p>A few practice screens come first.</p>")

# ---------------------------------------------------------------- build
tpl = json.load(open(TEMPLATE))
qsf = {"SurveyEntry": dict(tpl["SurveyEntry"]), "SurveyElements": []}

# the active response set must name the RS element, or the import fails silently
rs = [e for e in tpl["Boilerplate"] if e["Element"] == "RS"][0]["PrimaryAttribute"]
qsf["SurveyEntry"].update({"SurveyID": SID, "SurveyName": "Covered box replication",
    "SurveyDescription": None, "SurveyStatus": "Inactive",
    "SurveyActiveResponseSet": rs, "SurveyLanguage": "EN"})

for e in tpl["Boilerplate"]:
    c = copy.deepcopy(e); c["SurveyID"] = SID
    qsf["SurveyElements"].append(c)

qid = [0]
def mc(tag, prompt, boxes):
    """boxes = [choice-1 image, choice-2 image]; choice 3 is always the covered box."""
    qid[0] += 1; q = f"QID{qid[0]}"
    names = boxes + ["covered"]
    choices = {str(i+1): {"Display": img(n)} for i, n in enumerate(names)}
    # counterbalance: rotate so the covered box sits first / second / third
    rot = (qid[0] - 1) % 3
    order = ["3","1","2"] if rot == 0 else ["1","3","2"] if rot == 1 else ["1","2","3"]
    qsf["SurveyElements"].append({
      "SurveyID": SID, "Element": "SQ", "PrimaryAttribute": q,
      "SecondaryAttribute": prompt[:95], "TertiaryAttribute": None,
      "Payload": {
        "QuestionText": f"<span style=\"font-size:19px;\">{prompt}</span>",
        "DefaultChoices": False, "DataExportTag": tag, "QuestionID": q,
        "QuestionType": "MC", "Selector": "SAHR",
        "DataVisibility": {"Private": False, "Hidden": False},
        "Configuration": {"QuestionDescriptionOption": "UseText"},
        "QuestionDescription": prompt[:95],
        "Validation": {"Settings": {"ForceResponse": "ON", "Type": "None"}},
        "GradingData": [], "Language": [], "NextChoiceId": 4, "NextAnswerId": 1,
        "SubSelector": "TX", "Choices": choices, "ChoiceOrder": order}})
    return q, order

def db(tag, html):
    qid[0] += 1; q = f"QID{qid[0]}"
    el = copy.deepcopy(tpl["TextQuestion"]); el["SurveyID"] = SID
    el["PrimaryAttribute"] = q; el["SecondaryAttribute"] = tag
    el["Payload"].update({"QuestionText": html, "DataExportTag": tag,
                          "QuestionID": q, "QuestionDescription": tag})
    qsf["SurveyElements"].append(el)
    return q

def block(bid, desc, qids, typ="Standard"):
    be = []
    for i, q in enumerate(qids):
        if i: be.append({"Type": "Page Break"})
        be.append({"Type": "Question", "QuestionID": q})
    return {"Type": typ, "SubType": "", "Description": desc, "ID": bid,
            "BlockElements": be, "Options": None}

rows = [("question","choice_id","meaning")]
blocks = [block("BL_intro", "Instructions", [db("Instructions", INSTRUCTIONS)],
                typ="Default")]

fam_q = []
for tag, correct, boxes in FAM:
    q, _ = mc(tag, FAM_PROMPT, boxes)
    fam_q.append(q)
    rows += [(tag,"1","star-visible box"),(tag,"2","other open box"),(tag,"3","covered")]
    rows.append((tag,"correct",correct))
blocks.append(block("BL_fam", "Familiarization", fam_q))

TR = trials()
for term in ("scalar", "number"):
    crit = [t for t in TR if t[0]==term and t[1]=="critical"]
    ctrl = [t for t in TR if t[0]==term and t[1]!="critical"]
    qs = []
    for tm, kind, s, p, boxes, meanings in crit + ctrl:     # critical first
        tag = f"{tm}_{kind}_s{s}"
        q, _ = mc(tag, p, boxes)
        qs.append(q)
        rows += [(tag,"1",meanings[0]),(tag,"2",meanings[1]),(tag,"3","covered")]
    blocks.append(block(f"BL_{term}", f"{term} — critical trials then controls", qs))
blocks.append({"Type":"Trash","Description":"Trash / Unused Questions","ID":"BL_trash"})

qsf["SurveyElements"].append({"SurveyID":SID,"Element":"BL",
    "PrimaryAttribute":"Survey Blocks","SecondaryAttribute":None,
    "TertiaryAttribute":None,"Payload":blocks})

flow = {"FlowID":"FL_1","Type":"Root","Flow":[
   {"ID":"BL_intro","Type":"Block","FlowID":"FL_2"},
   {"ID":"BL_fam","Type":"Block","FlowID":"FL_3"},
   {"Type":"BlockRandomizer","FlowID":"FL_4","SubSet":1,"EvenPresentation":True,
    "Flow":[{"ID":"BL_scalar","Type":"Block","FlowID":"FL_5"},
            {"ID":"BL_number","Type":"Block","FlowID":"FL_6"}]}],
   "Properties":{"Count":7}}
qsf["SurveyElements"].append({"SurveyID":SID,"Element":"FL",
    "PrimaryAttribute":"Survey Flow","SecondaryAttribute":None,
    "TertiaryAttribute":None,"Payload":flow})

json.dump(qsf, open(OUT,"w"), indent=2)
with open("choice-map.csv","w",newline="") as fh: csv.writer(fh).writerows(rows)
mcq = [e for e in qsf["SurveyElements"] if e.get("Element")=="SQ"
       and e["Payload"]["QuestionType"]=="MC"]
with open("columns.txt","w") as fh:
    fh.write("\n".join(e["Payload"]["DataExportTag"] for e in mcq)+"\n")
print(f"wrote {OUT}: {len(mcq)} trials, {len(blocks)} blocks")
print("wrote columns.txt and choice-map.csv")
