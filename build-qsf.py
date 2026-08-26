#!/usr/bin/env python3
"""
Builds the Qualtrics survey for the Huang, Spelke & Snedeker Exp. 1 replication.

Each trial is a multiple-choice question whose three answer choices are the three
box images. Qualtrics randomises choice order, which counterbalances the covered
box's position; the export records WHICH BOX was chosen, not which position.

    python3 build-qsf.py [BASE_URL]

BASE_URL is where the PNGs in stimuli/ are served from. Leave it as the default
placeholder and find-replace later, or pass a real URL to get a survey that works
the moment it is imported.
"""
import json, copy, sys, os

BASE = sys.argv[1] if len(sys.argv) > 1 else "IMAGE_BASE_URL"
TEMPLATE = "qsf-template.json"   # vendored; this repo has no outside deps
OUT = "HuangSnedeker_replication.qsf"

def img(name, w=300):
    return (f'<img src="{BASE}/{name}.png" '
            f'style="width:100%;max-width:{w}px;height:auto;" alt="">')

# recode: 1 = less/none  2 = subset or exact match  3 = more/all  4 = covered box
SCALAR_SETS = [(1,"Zip","cookies"), (2,"Mo","apples"), (3,"Dax","balloons")]
NUMBER_SETS = [(1,"fish",3), (2,"birds",5), (3,"flowers",3)]

def scalar_trials():
    out=[]
    for s,name,obj in SCALAR_SETS:
        p=f"Give me the box where {name} has some of the {obj}."
        out.append(("crit", f"scalar_critical_s{s}", p,
                    [(1,f"scalar_s{s}_NONE"),(3,f"scalar_s{s}_ALL"),(4,"covered")]))
    for s,name,obj in SCALAR_SETS:
        p=f"Give me the box where {name} has some of the {obj}."
        out.append(("ctrl", f"scalar_noneSome_s{s}", p,
                    [(1,f"scalar_s{s}_NONE"),(2,f"scalar_s{s}_SOME"),(4,"covered")]))
        out.append(("ctrl", f"scalar_someAll_s{s}", p,
                    [(2,f"scalar_s{s}_SOME"),(3,f"scalar_s{s}_ALL"),(4,"covered")]))
    return out

def number_trials():
    out=[]
    for s,obj,more in NUMBER_SETS:
        p=f"Give me the box with two {obj}."
        out.append(("crit", f"number_critical_s{s}", p,
                    [(1,f"number_s{s}_1"),(3,f"number_s{s}_{more}"),(4,"covered")]))
    for s,obj,more in NUMBER_SETS:
        p=f"Give me the box with two {obj}."
        out.append(("ctrl", f"number_oneTwo_s{s}", p,
                    [(1,f"number_s{s}_1"),(2,f"number_s{s}_2"),(4,"covered")]))
        out.append(("ctrl", f"number_twoMore_s{s}", p,
                    [(2,f"number_s{s}_2"),(3,f"number_s{s}_{more}"),(4,"covered")]))
    return out

FAM = [  # (tag, correct recode, boxes)
 ("fam1", 1, [(1,"fam1_yes"),(3,"fam1_no"),(4,"covered")]),
 ("fam2", 1, [(1,"fam2_yes"),(3,"fam2_no"),(4,"covered")]),
 ("fam3", 4, [(1,"fam3_no_a"),(3,"fam3_no_b"),(4,"covered")]),
 ("fam4", 4, [(1,"fam4_no"),(3,"fam1_no"),(4,"covered")]),
]
FAM_PROMPT = "Give me the box with the red star."

INSTRUCTIONS = (
 "<p>In this task you will see three boxes on each screen. Two of them are open, "
 "so you can see what is inside. The third is closed, so you cannot.</p>"
 "<p>Each time, you will be asked for the box that matches a description. "
 "<b>If neither open box matches, then the box you want must be the closed "
 "one.</b></p><p>There are a few practice screens first.</p>")

# ---------------------------------------------------------------- build
tpl = json.load(open(TEMPLATE))
text_tpl = tpl["TextQuestion"]

qsf = {"SurveyEntry": dict(tpl["SurveyEntry"]), "SurveyElements": []}
qsf["SurveyEntry"].update({
    "SurveyID":"SV_HuangSnedekerRep", "SurveyName":"Covered box replication",
    "SurveyDescription":None, "SurveyStatus":"Inactive"})

for e in tpl["Boilerplate"]:
    c=copy.deepcopy(e); c["SurveyID"]="SV_HuangSnedekerRep"
    qsf["SurveyElements"].append(c)

qid = [0]
def new_qid():
    qid[0]+=1; return f"QID{qid[0]}"

def mc_question(tag, prompt, choices):
    q=new_qid()
    ch={}; order=[]; recode={}
    for i,(rc,imgname) in enumerate(choices, start=1):
        ch[str(i)]={"Display": img(imgname)}
        order.append(str(i)); recode[str(i)]=str(rc)
    el={"SurveyID":"SV_HuangSnedekerRep","Element":"SQ","PrimaryAttribute":q,
        "SecondaryAttribute":prompt[:95],"TertiaryAttribute":None,
        "Payload":{
          "QuestionText": f"<p style='font-size:20px'>{prompt}</p>",
          "DefaultChoices":False,"DataExportTag":tag,"QuestionID":q,
          "QuestionType":"MC","Selector":"SAHR","SubSelector":"TX",
          "DataVisibility":{"Private":False,"Hidden":False},
          "Configuration":{"QuestionDescriptionOption":"UseText",
                           "LabelPosition":"BELOW"},
          "QuestionDescription":prompt[:95],
          "Choices":ch,"ChoiceOrder":order,
          "Validation":{"Settings":{"ForceResponse":"ON","ForceResponseType":"ON",
                                    "Type":"None"}},
          "GradingData":[],"Language":[],"NextChoiceId":len(choices)+1,
          "NextAnswerId":1,"RecodeValues":recode,
          "Randomization":{"Advanced":{"TotalRandSubset":len(choices),
              "QuestionsPerPage":"0","RandomizeAll":order,"RandomSubSet":[],
              "Undisplayed":[],"FixedOrder":order},
              "Type":"All","TotalRandSubset":len(choices)}}}
    qsf["SurveyElements"].append(el)
    return q

def db_question(tag, html):
    q=new_qid()
    el=copy.deepcopy(text_tpl); el["SurveyID"]="SV_HuangSnedekerRep"
    el["PrimaryAttribute"]=q; el["SecondaryAttribute"]=tag
    el["Payload"].update({"QuestionText":html,"DataExportTag":tag,"QuestionID":q,
                          "QuestionDescription":tag})
    qsf["SurveyElements"].append(el)
    return q

def block(bid, desc, qids, typ="Standard", randomize=True):
    b={"Type":typ,"SubType":"","Description":desc,"ID":bid,"BlockElements":[]}
    for i,q in enumerate(qids):
        if i: b["BlockElements"].append({"Type":"Page Break"})
        b["BlockElements"].append({"Type":"Question","QuestionID":q})
    b["Options"]={"BlockLocking":"false",
        "RandomizeQuestions":"Advanced" if randomize else "false"}
    if randomize:
        b["Options"]["Randomization"]={"Advanced":{"FixedOrder":[],
            "RandomizeAll":list(qids),"RandomSubSet":[],"Undisplayed":[],
            "TotalRandSubset":0,"QuestionsPerPage":"1"},"EvenPresentation":False}
    return b

blocks=[]
blocks.append(block("BL_intro","Instructions",
                    [db_question("Instructions", INSTRUCTIONS)],
                    typ="Default", randomize=False))
fam_qs=[mc_question(t, FAM_PROMPT, boxes) for t,_,boxes in FAM]
blocks.append(block("BL_fam","Familiarization", fam_qs, randomize=False))

for term, trials in (("scalar", scalar_trials()), ("number", number_trials())):
    crit=[mc_question(tag,p,ch) for kind,tag,p,ch in trials if kind=="crit"]
    ctrl=[mc_question(tag,p,ch) for kind,tag,p,ch in trials if kind=="ctrl"]
    blocks.append(block(f"BL_{term}_crit", f"{term} — critical trials", crit))
    blocks.append(block(f"BL_{term}_ctrl", f"{term} — control trials", ctrl))
blocks.append({"Type":"Trash","Description":"Trash / Unused Questions","ID":"BL_trash"})

qsf["SurveyElements"].append({"SurveyID":"SV_HuangSnedekerRep","Element":"BL",
                              "PrimaryAttribute":"Survey Blocks",
                              "SecondaryAttribute":None,"TertiaryAttribute":None,
                              "Payload":blocks})

def std(bid, fid): return {"Type":"Standard","ID":bid,"FlowID":fid,"Autofill":[]}
flow={"Type":"Root","FlowID":"FL_1","Flow":[
  std("BL_intro","FL_2"), std("BL_fam","FL_3"),
  {"Type":"BlockRandomizer","FlowID":"FL_4","SubSet":1,"EvenPresentation":True,
   "Flow":[
     {"Type":"Group","FlowID":"FL_5","Description":"scalar term","Flow":[
        std("BL_scalar_crit","FL_6"), std("BL_scalar_ctrl","FL_7")]},
     {"Type":"Group","FlowID":"FL_8","Description":"number term","Flow":[
        std("BL_number_crit","FL_9"), std("BL_number_ctrl","FL_10")]}]}],
  "Properties":{"Count":12}}
qsf["SurveyElements"].append({"SurveyID":"SV_HuangSnedekerRep","Element":"FL",
                              "PrimaryAttribute":"Survey Flow",
                              "SecondaryAttribute":None,"TertiaryAttribute":None,
                              "Payload":flow})

json.dump(qsf, open(OUT,"w"), indent=2)
qs=[e for e in qsf["SurveyElements"] if e.get("Element")=="SQ"]
print(f"wrote {OUT}: {len(qs)} questions, {len(blocks)} blocks")
for b in blocks:
    if b.get("BlockElements"):
        print(f"   {b['Description']:32s} {sum(1 for x in b['BlockElements'] if x['Type']=='Question')} questions")
missing=[]
for e in qs:
    for c in (e["Payload"].get("Choices") or {}).values():
        for tok in c["Display"].split('src="')[1:]:
            f=tok.split('"')[0].split("/")[-1]
            if not os.path.exists(f"stimuli/{f}"): missing.append(f)
print("missing stimulus files:", sorted(set(missing)) or "none")

# column manifest, in survey order, so the fake-data generator cannot drift
tags=[e["Payload"]["DataExportTag"] for e in qs
      if e["Payload"]["QuestionType"]=="MC"]
with open("columns.txt","w") as fh:
    fh.write("\n".join(tags)+"\n")
print("wrote columns.txt:", len(tags), "response columns")
