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
def cookie(d,x,y,r=15):
    d.ellipse([x-r,y-r,x+r,y+r], fill=(214,170,110), outline=(120,88,48), width=2)
    for dx,dy in ((-5,-4),(5,-1),(0,6),(-6,5)):
        d.ellipse([x+dx-2,y+dy-2,x+dx+2,y+dy+2], fill=(90,62,38))

def apple(d,x,y,r=15):
    d.ellipse([x-r,y-r+2,x+r,y+r+2], fill=(206,64,58), outline=(120,32,30), width=2)
    d.line([x,y-r,x+2,y-r-9], fill=(96,62,32), width=3)
    d.ellipse([x+2,y-r-12,x+13,y-r-3], fill=(96,158,74), outline=(52,100,44))

def balloon(d,x,y,r=15):
    d.ellipse([x-r,y-r-3,x+r,y+r+1], fill=(158,104,196), outline=(96,58,128), width=2)
    d.polygon([(x-4,y+r-1),(x+4,y+r-1),(x,y+r+6)], fill=(96,58,128))
    d.line([x,y+r+5,x+4,y+r+18], fill=(90,90,90), width=2)

def fish(d,x,y,s=1.0):
    bw,bh=int(30*s),int(18*s)
    d.ellipse([x-bw,y-bh,x+bw,y+bh], fill=(92,160,214), outline=EDGE, width=2)
    d.polygon([(x+bw-2,y),(x+bw+16*s,y-12*s),(x+bw+16*s,y+12*s)],
              fill=(92,160,214), outline=EDGE)
    d.ellipse([x-bw+8,y-6,x-bw+15,y+1], fill=(255,255,255), outline=EDGE)

def bird(d,x,y,s=1.0):
    bw,bh=int(26*s),int(17*s)
    d.ellipse([x-bw,y-bh,x+bw,y+bh], fill=(230,168,60), outline=EDGE, width=2)
    hr=int(13*s)
    d.ellipse([x+bw-6,y-bh-hr+2,x+bw+2*hr-6,y-bh+hr+2], fill=(230,168,60),
              outline=EDGE, width=2)
    d.polygon([(x+bw+2*hr-8,y-bh+2),(x+bw+2*hr+9,y-bh+5),(x+bw+2*hr-8,y-bh+9)],
              fill=(214,96,40), outline=EDGE)
    d.ellipse([x+bw+hr-8,y-bh-4,x+bw+hr-3,y-bh+1], fill=EDGE)
    d.arc([x-bw+6,y-10,x+bw-6,y+16], 200, 340, fill=EDGE, width=2)

def flower(d,x,y,s=1.0):
    r=int(11*s)
    for a in range(5):
        import math
        ang=math.radians(a*72-90); px,py=x+math.cos(ang)*15*s, y+math.sin(ang)*15*s
        d.ellipse([px-r,py-r,px+r,py+r], fill=(226,110,150), outline=(150,60,96), width=2)
    d.ellipse([x-8,y-8,x+8,y+8], fill=(244,206,74), outline=(150,110,30), width=2)

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
    for i in range(n):
        r,c=divmod(i,cols)
        draw(d, int(cx+(c-(cols-1)/2)*38), int(top-(rows-1-r)*36))

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
    pos={1:[(0,0)],2:[(-72,0),(72,0)],3:[(-78,-56),(78,-56),(0,58)],
         5:[(-92,-64),(92,-64),(0,0),(-92,64),(92,64)]}[n]
    for dx,dy in pos: obj(d, cx+dx, cy+dy)
    return img

def familiar_box(shapes):
    img,d = blank()
    cx,cy = BOX_W//2, BOX_H//2
    pos={1:[(0,0)],2:[(-62,0),(62,0)],3:[(-70,-46),(70,-46),(0,50)]}[len(shapes)]
    for (dx,dy),sh in zip(pos,shapes): sh(d, cx+dx, cy+dy)
    return img

# ------------------------------------------------------------------ emit
SCALAR_SETS = [("cookies", cookie, ("Zip","Nub")),
               ("apples",  apple,  ("Mo","Pim")),
               ("balloons",balloon,("Dax","Wug"))]
NUMBER_SETS = [("fish", fish), ("birds", bird), ("flowers", flower)]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith(".png"): os.remove(os.path.join(OUT,f))
    n=0
    blank(covered=True)[0].save(f"{OUT}/covered.png"); n+=1
    for i,(label,obj,names) in enumerate(SCALAR_SETS,1):
        for tag,(a,b) in {"NONE":(0,4), "SOME":(2,2), "ALL":(4,0)}.items():
            scalar_box(a,b,obj,names).save(f"{OUT}/scalar_s{i}_{tag}.png"); n+=1
    for i,(label,obj) in enumerate(NUMBER_SETS,1):
        for k in (1,2,3,5):
            number_box(k,obj).save(f"{OUT}/number_s{i}_{k}.png"); n+=1
    # familiarization: "Give me the box with the red star."
    fam = {"fam1_yes":[shape_star,shape_tri], "fam1_no":[shape_sq,shape_hex],
           "fam2_yes":[shape_tri,shape_star,shape_sq], "fam2_no":[shape_hex,shape_tri],
           "fam3_no_a":[shape_sq,shape_tri], "fam3_no_b":[shape_hex,shape_sq],
           "fam4_yes":[shape_star], "fam4_no":[shape_tri,shape_hex]}
    for name,shapes in fam.items():
        familiar_box(shapes).save(f"{OUT}/{name}.png"); n+=1
    print(f"wrote {n} box images to {OUT}/")
    print("scalar/number sets:", len(SCALAR_SETS), len(NUMBER_SETS))
