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
mc_tpl = [e for e in tpl["SurveyElements"]
          if e.get("Element")=="SQ" and e["Payload"]["QuestionType"]=="MC"][0]
for e in tpl["SurveyElements"]:
    if e.get("Element") not in ("SQ","BL","FL"):
        qsf["SurveyElements"].append(copy.deepcopy(e))

qid=[0]
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
    rot = (qid[0]-1) % 3
    p["ChoiceOrder"] = (["3","1","2"] if rot==0 else
                        ["1","3","2"] if rot==1 else ["1","2","3"])
    p["Validation"]["Settings"]["ForceResponse"]="ON"
    p["NextChoiceId"]=4
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
    qs=[mc("t1", design.FAM[0][1], design.FAM[0][2], PREAMBLE),
        mc("t2", design.all_trials()[9]["prompt"], design.all_trials()[9]["boxes"])]
    blocks.append(block("test","Default Question Block",qs,typ="Default"))
    flow_inner=[{"ID":blocks[0]["ID"],"Type":"Block","FlowID":"FL_2"}]
    count=3
else:
    fam=[]
    for i,(tag,prompt,boxes,correct) in enumerate(design.FAM):
        fam.append(mc(tag, prompt, boxes, PREAMBLE if i==0 else ""))
        rows += [(tag,"1","first open box"),(tag,"2","second open box"),
                 (tag,"3","covered"),(tag,"correct",correct)]
    blocks.append(block("fam","Familiarization",fam,typ="Default"))
    term_ids=[]
    for term in ("scalar","number"):
        qs=[]
        for t in design.all_trials():
            if t["term"] != term: continue
            tag=(f"{term}_{t['kind']}" if t["set"] == 0
                 else f"{term}_{t['kind']}_s{t['set']}")
            qs.append(mc(tag, t["prompt"], t["boxes"]))
            rows += [(tag,"1",t["meaning"][0]),(tag,"2",t["meaning"][1]),
                     (tag,"3","covered")]
        b=block(term,f"{term} — critical trials then controls",qs)
        blocks.append(b); term_ids.append(b["ID"])
    flow_inner=[{"ID":blocks[0]["ID"],"Type":"Block","FlowID":"FL_2"},
      {"Type":"BlockRandomizer","FlowID":"FL_3","SubSet":1,"EvenPresentation":True,
       "Flow":[{"ID":term_ids[0],"Type":"Block","FlowID":"FL_4"},
               {"ID":term_ids[1],"Type":"Block","FlowID":"FL_5"}]}]
    count=8

if not TEST:
    lang_q = text_mc("first_language", design.LANGUAGE_Q[0], design.LANGUAGE_Q[1])
    lang_b = block("lang", "Language background", [lang_q])
    blocks.append(lang_b)
    flow_inner.append({"ID": lang_b["ID"], "Type": "Block", "FlowID": "FL_7"})
    for i, o in enumerate(design.LANGUAGE_Q[1], start=1):
        rows.append(("first_language", str(i), o))

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
        fh.write("\n".join(e["Payload"]["DataExportTag"] for e in mcq)+"\n")
    print("wrote columns.txt and choice-map.csv")
