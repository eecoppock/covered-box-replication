#!/usr/bin/env python3
"""
Stimuli for a class replication of Huang, Spelke & Snedeker (2013), Experiment 1.

Emits ONE IMAGE PER BOX, so each trial can be a Qualtrics multiple-choice
question with graphic answer choices. Qualtrics then randomises choice order
itself, which counterbalances the covered box's position for free, and the
export records which box was chosen rather than which position.

Generic characters and objects; nothing here is under copyright.

    python3 make-stimuli.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

BOX_W, BOX_H = 420, 400
PAD = 14
EDGE = (40, 40, 40)
OUT = "stimuli"

def font(sz):
    for p in ("/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Supplemental/Arial.ttf"):
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

def blank(covered=False):
    img = Image.new("RGB", (BOX_W, BOX_H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    if covered:
        d.rounded_rectangle([PAD, PAD+34, BOX_W-PAD, BOX_H-PAD], radius=16,
                            fill=(150,150,155), outline=EDGE, width=5)
        d.rounded_rectangle([PAD-8, PAD, BOX_W-PAD+8, PAD+58], radius=10,
                            fill=(120,120,126), outline=EDGE, width=5)
        f = font(120); t = "?"
        d.text(((BOX_W-d.textlength(t, font=f))/2, BOX_H/2-70), t,
               fill=(245,245,245), font=f)
    else:
        d.rounded_rectangle([PAD, PAD, BOX_W-PAD, BOX_H-PAD], radius=16,
                            fill=(252,252,250), outline=EDGE, width=5)
    return img, d

# ------------------------------------------------------------------ objects
# Every object draws inside roughly a 36 x 36 box at s = 1.0. That matters: the
# scalar panels lay objects out on a grid, and an object wider than the grid
# spacing turns a countable set into an uncountable smear. Birds were ~90px wide
# against 38px spacing, which made "Bix has all of the birds" unreadable and the
# covered box a reasonable answer to a trial that should have had a visible one.
def cookie(d,x,y,s=1.0):
    r=int(17*s)
    d.ellipse([x-r,y-r,x+r,y+r], fill=(214,170,110), outline=(120,88,48), width=2)
    for dx,dy in ((-.32,-.26),(.32,-.06),(0,.38),(-.38,.32)):
        d.ellipse([x+dx*r-2,y+dy*r-2,x+dx*r+2,y+dy*r+2], fill=(90,62,38))

def apple(d,x,y,s=1.0):
    r=int(16*s)
    d.ellipse([x-r,y-r+2,x+r,y+r+2], fill=(206,64,58), outline=(120,32,30), width=2)
    d.line([x,y-r,x+2,y-r-int(8*s)], fill=(96,62,32), width=3)
    d.ellipse([x+2,y-r-int(11*s),x+int(12*s),y-r-int(3*s)],
              fill=(96,158,74), outline=(52,100,44))

def balloon(d,x,y,s=1.0):
    r=int(15*s)
    d.ellipse([x-r,y-r-3,x+r,y+r-1], fill=(158,104,196), outline=(96,58,128), width=2)
    d.polygon([(x-4,y+r-2),(x+4,y+r-2),(x,y+r+5)], fill=(96,58,128))
    d.line([x,y+r+4,x+3,y+r+int(13*s)], fill=(90,90,90), width=2)

def fish(d,x,y,s=1.0):
    bw,bh=int(13*s),int(9*s)
    d.ellipse([x-bw,y-bh,x+bw,y+bh], fill=(92,160,214), outline=EDGE, width=2)
    d.polygon([(x+bw-1,y),(x+bw+int(7*s),y-int(7*s)),(x+bw+int(7*s),y+int(7*s))],
              fill=(92,160,214), outline=EDGE)
    d.ellipse([x-bw+4,y-3,x-bw+8,y+1], fill=(255,255,255), outline=EDGE)

def bird(d,x,y,s=1.0):
    bw,bh=int(11*s),int(8*s)
    d.ellipse([x-bw,y-bh+2,x+bw,y+bh+2], fill=(230,168,60), outline=EDGE, width=2)
    hr=int(6*s)
    d.ellipse([x+bw-hr,y-bh-hr,x+bw+hr,y-bh+hr], fill=(230,168,60), outline=EDGE, width=2)
    d.polygon([(x+bw+hr-1,y-bh-1),(x+bw+hr+int(6*s),y-bh+1),(x+bw+hr-1,y-bh+4)],
              fill=(214,96,40), outline=EDGE)

def flower(d,x,y,s=1.0):
    import math
    r=int(8*s)
    for a in range(5):
        ang=math.radians(a*72-90)
        px,py=x+math.cos(ang)*10*s, y+math.sin(ang)*10*s
        d.ellipse([px-r,py-r,px+r,py+r], fill=(226,110,150), outline=(150,60,96), width=2)
    rr=int(6*s)
    d.ellipse([x-rr,y-rr,x+rr,y+rr], fill=(244,206,74), outline=(150,110,30), width=2)

def mushroom(d,x,y,s=1.0):
    w,h=int(17*s),int(10*s)
    d.rectangle([x-int(5*s),y-2,x+int(5*s),y+int(13*s)],
                fill=(242,232,208), outline=(150,140,116))
    d.pieslice([x-w,y-h-int(8*s),x+w,y+h+int(2*s)], 180, 360,
               fill=(206,72,64), outline=(130,36,32))
    for dx,dy in ((-.45,-.25),(.4,-.35),(0,-.55)):
        r=int(3.2*s)
        d.ellipse([x+dx*w-r,y+dy*h-r-4,x+dx*w+r,y+dy*h+r-4], fill=(250,244,236))

def carrot(d,x,y,s=1.0):
    h,w=int(19*s),int(8*s)
    d.polygon([(x,y+h),(x-w,y-h//2),(x+w,y-h//2)],
              fill=(232,132,44), outline=(160,84,20))
    for dx in (-1,1):
        d.polygon([(x+dx*2,y-h//2),(x+dx*w,y-h),(x-dx*1,y-h//2+2)],
                  fill=(96,158,74), outline=(52,100,44))

def star(d,x,y,s=1.0):
    import math
    pts=[]
    for i in range(10):
        ang=math.radians(i*36-90); rr=(17 if i%2==0 else 7)*s
        pts.append((x+math.cos(ang)*rr, y+math.sin(ang)*rr))
    d.polygon(pts, fill=(244,196,58), outline=(150,116,20))

def heart(d,x,y,s=1.0):
    r=int(8*s)
    d.ellipse([x-2*r,y-r-3,x,y+r-3], fill=(216,74,102), outline=(140,40,62))
    d.ellipse([x,y-r-3,x+2*r,y+r-3], fill=(216,74,102), outline=(140,40,62))
    d.polygon([(x-2*r+1,y-1),(x+2*r-1,y-1),(x,y+int(15*s))],
              fill=(216,74,102), outline=(140,40,62))

def leaf(d,x,y,s=1.0):
    h,w=int(17*s),int(11*s)
    d.polygon([(x,y-h),(x+w,y),(x,y+h),(x-w,y)],
              fill=(104,166,86), outline=(56,104,50))
    d.line([x,y-h+2,x,y+h-2], fill=(56,104,50), width=2)

def shape_star(d,x,y,col=(214,60,60),s=1.0):
    import math
    pts=[]
    for i in range(10):
        ang=math.radians(i*36-90); rr=(22 if i%2==0 else 9)*s
        pts.append((x+math.cos(ang)*rr, y+math.sin(ang)*rr))
    d.polygon(pts, fill=col, outline=EDGE)

def shape_tri(d,x,y,col=(78,158,86),s=1.0):
    d.polygon([(x,y-20*s),(x-20*s,y+16*s),(x+20*s,y+16*s)], fill=col, outline=EDGE)

def shape_sq(d,x,y,col=(232,150,52),s=1.0):
    d.rectangle([x-17*s,y-17*s,x+17*s,y+17*s], fill=col, outline=EDGE)

def shape_hex(d,x,y,col=(120,110,200),s=1.0):
    import math
    d.polygon([(x+math.cos(math.radians(a*60))*20*s,
               y+math.sin(math.radians(a*60))*20*s) for a in range(6)],
              fill=col, outline=EDGE)

# ------------------------------------------------------------------ layouts
def character(d,x,y,colour,name):
    bw,bh=62,76
    d.rounded_rectangle([x-bw//2,y-bh,x+bw//2,y], radius=15, fill=colour,
                        outline=EDGE, width=2)
    hr=28
    d.ellipse([x-hr,y-bh-hr*2+4,x+hr,y-bh+4], fill=colour, outline=EDGE, width=2)
    for dx in (-10,10):
        d.ellipse([x+dx-5,y-bh-hr-5,x+dx+5,y-bh-hr+6], fill=(255,255,255),
                  outline=EDGE, width=1)
        d.ellipse([x+dx-2,y-bh-hr-1,x+dx+2,y-bh-hr+3], fill=EDGE)
    f=font(21)
    d.text((x-d.textlength(name,font=f)/2, y+9), name, fill=EDGE, font=f)

def cluster(d,cx,top,n,draw):
    if n==0: return
    cols=2 if n>1 else 1
    rows=(n+cols-1)//cols
    SX, SY = 46, 44          # > the 36px object footprint, so sets stay countable
    for i in range(n):
        r,c=divmod(i,cols)
        draw(d, int(cx+(c-(cols-1)/2)*SX), int(top-(rows-1-r)*SY))

def scalar_box(n_target, n_other, obj, names, total=4):
    img,d = blank()
    base = BOX_H - 76
    d.line([BOX_W//2, PAD+18, BOX_W//2, BOX_H-PAD-18], fill=(222,222,222), width=2)
    character(d, 112, base, (108,150,220), names[0])
    character(d, 308, base, (232,178,80), names[1])
    cluster(d, 112, base-158, n_target, obj)
    cluster(d, 308, base-158, n_other,  obj)
    return img

def number_box(n, obj):
    img,d = blank()
    cx,cy = BOX_W//2, BOX_H//2
    pos={0:[],1:[(0,0)],2:[(-70,0),(70,0)],3:[(-76,-58),(76,-58),(0,58)],
         5:[(-92,-68),(92,-68),(0,0),(-92,68),(92,68)]}[n]
    for dx,dy in pos: obj(d, cx+dx, cy+dy, 1.7)
    return img

def familiar_box(shapes):
    img,d = blank()
    cx,cy = BOX_W//2, BOX_H//2
    pos={1:[(0,0)],2:[(-62,0),(62,0)],3:[(-70,-46),(70,-46),(0,50)]}[len(shapes)]
    for (dx,dy),sh in zip(pos,shapes): sh(d, cx+dx, cy+dy)
    return img

# ------------------------------------------------------------------ emit
import design

DRAW = {"cookie":cookie, "apple":apple, "balloon":balloon, "fish":fish,
        "bird":bird, "flower":flower, "star":star, "heart":heart, "leaf":leaf,
        "carrot":carrot, "mushroom":mushroom}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith(".png"): os.remove(os.path.join(OUT,f))
    n=0
    blank(covered=True)[0].save(f"{OUT}/covered.png"); n+=1

    # only the boxes the design actually calls for
    for t in design.all_trials():
        i   = t["set"]-1
        obj = DRAW[design.OBJECTS[i][0]]
        for box in t["boxes"]:
            tag = box.rsplit("_",1)[1]
            if t["term"]=="scalar":
                names = design.NAMES[i]
                counts = {"NONE":(0,4), "SOME":(2,2), "ALL":(4,0),
                          "EMPTY":(0,0)}[tag]
                scalar_box(counts[0], counts[1], obj, names).save(f"{OUT}/{box}.png")
            else:
                number_box(int(tag), obj).save(f"{OUT}/{box}.png")
            n+=1

    SH = {"star":shape_star, "tri":shape_tri, "sq":shape_sq, "hex":shape_hex}
    for name, shapes in design.FAM_SHAPES.items():
        familiar_box([SH[x] for x in shapes]).save(f"{OUT}/{name}.png"); n+=1
    print(f"wrote {n} box images to {OUT}/")

    # Regenerate the contact sheet. Every stimulus bug so far -- birds smeared
    # into an uncountable pile, flowers standing in for leaves -- would have been
    # obvious in one glance at this page, and invisible in the code.
    import html as _html
    files = sorted(f for f in os.listdir(OUT) if f.endswith(".png"))
    groups = {"Familiarization": [f for f in files if f.startswith("fam")],
              "Covered box":     [f for f in files if f == "covered.png"],
              "Scalar panels":   [f for f in files if f.startswith("scalar")],
              "Number panels":   [f for f in files if f.startswith("number")]}
    cards = ""
    for name, fs in groups.items():
        if not fs: continue
        cards += f"<h2>{_html.escape(name)}</h2>\n<div class=grid>\n"
        for f in fs:
            cards += (f'<figure><img src="{OUT}/{f}" alt="{f}" loading="lazy">'
                      f'<figcaption>{f[:-4]}</figcaption></figure>\n')
        cards += "</div>\n"
    open("index.html","w").write(f"""<!doctype html>
<html lang=en><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Covered-box stimuli</title>
<style>
 body{{{{font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
      max-width:1100px;margin:2.5rem auto;padding:0 1.25rem;color:#1c1c1e}}}}
 h1{{{{font-size:1.6rem;margin-bottom:.2rem}}}}
 p.sub{{{{color:#555;margin-top:0}}}}
 h2{{{{font-size:1.05rem;margin:2rem 0 .6rem;color:#444;
     border-bottom:1px solid #e3e3e6;padding-bottom:.3rem}}}}
 .grid{{{{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));
        gap:1rem}}}}
 figure{{{{margin:0}}}}
 img{{{{width:100%;border:1px solid #d8d8dc;border-radius:8px;background:#fff}}}}
 figcaption{{{{font:12px ui-monospace,SFMono-Regular,Menlo,monospace;
             color:#666;margin-top:.35rem;word-break:break-all}}}}
</style>
<h1>Covered-box stimuli</h1>
<p class=sub>Huang, Spelke &amp; Snedeker (2013) Exp. 1 &mdash; a class replication.
Generated by <code>make-stimuli.py</code>; characters and objects are original.
<a href="https://github.com/eecoppock/covered-box-replication">Source</a>.</p>
{{cards}}""")
    print("wrote index.html contact sheet")
