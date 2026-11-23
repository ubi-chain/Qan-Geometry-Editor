#!/usr/bin/env python3
"""Create a 30-frame orbit GIF for the conceptual QAN West Japan Neo World."""
from __future__ import annotations
import math, os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
W,H=960,540
TAU=math.tau
OUT=Path(os.environ.get("OUTPUT_GIF","dist/QAN-West-Japan-Neo-World.gif"))
REGIONS=[
("KYUSHU",(-255,90),[(-80,155),(-48,190),(8,180),(48,146),(62,100),(48,55),(18,25),(28,-28),(4,-74),(-35,-102),(-76,-80),(-104,-35),(-118,25),(-108,92)],(23,83,91)),
("CHUGOKU",(100,-95),[(-150,35),(-125,66),(-78,74),(-34,58),(8,67),(55,53),(104,47),(147,25),(157,-4),(130,-29),(82,-22),(38,-34),(-8,-24),(-55,-42),(-106,-30),(-145,-8)],(30,73,101)),
("SHIKOKU",(75,78),[(-115,18),(-76,48),(-24,56),(28,48),(78,35),(124,10),(116,-24),(78,-46),(25,-53),(-30,-48),(-84,-27),(-117,-4)],(43,83,73))]
def font(n,b=False):
    for p in (["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if b else ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]):
        try:return ImageFont.truetype(p,n)
        except OSError:pass
    return ImageFont.load_default()
def project(x,z,y,a):
    xr=x*math.cos(a)-z*math.sin(a);zr=x*math.sin(a)+z*math.cos(a)
    elev=.58;sc=1.25
    return (W*.5+xr*sc,H*.59+(zr*math.sin(elev)-y*math.cos(elev))*sc,zr*math.cos(elev)+y*math.sin(elev))
def poly_contains(x,y,p):
    c=False;j=len(p)-1
    for i in range(len(p)):
        xi,yi=p[i];xj,yj=p[j]
        if (yi>y)!=(yj>y) and x<(xj-xi)*(y-yi)/((yj-yi) or 1e-9)+xi:c=not c
        j=i
    return c
def make_city():
    import random
    random.seed(20261123);out=[]
    for name,(cx,cz),p,color in REGIONS:
        for _ in range(1000):
            x=random.uniform(-155,155);z=random.uniform(-105,190)
            if not poly_contains(x,z,p):continue
            d=math.hypot(x,z);h=3+random.random()**2*(9+max(0,1-d/180)*42)
            out.append((x+cx,z+cz,h,random.uniform(1.4,3.4),random.uniform(1.3,3.3),color))
    return out
def frame(a,buildings):
    im=Image.new("RGB",(W,H),(5,12,22));d=ImageDraw.Draw(im,"RGBA")
    # atmospheric star grid / sea
    for y in range(130,H,42):d.line((0,y,W,y),fill=(13,42,59,70),width=1)
    for x in range(20,W,55):d.line((x,110,x,H),fill=(13,42,59,55),width=1)
    for name,(cx,cz),p,color in REGIONS:
        pts=[project(x+cx,z+cz,0,a)[:2] for x,z in p]
        d.polygon(pts,fill=(*color,255),outline=(94,221,238,255))
    # city blocks with bright roof facets
    ordered=sorted(buildings,key=lambda b:project(b[0],b[1],b[2],a)[2])
    for x,z,h,w,dep,c in ordered:
        p0=project(x-w/2,z-dep/2,0,a);p1=project(x+w/2,z-dep/2,0,a);p2=project(x+w/2,z+dep/2,0,a);p3=project(x-w/2,z+dep/2,0,a)
        t0=project(x-w/2,z-dep/2,h,a);t1=project(x+w/2,z-dep/2,h,a);t2=project(x+w/2,z+dep/2,h,a);t3=project(x-w/2,z+dep/2,h,a)
        d.polygon([p0[:2],p1[:2],t1[:2],t0[:2]],fill=(13,43,62,255))
        d.polygon([p1[:2],p2[:2],t2[:2],t1[:2]],fill=(22,65,81,255))
        d.polygon([t0[:2],t1[:2],t2[:2],t3[:2]],fill=(62,116,139,255))
    # inter-island elevated maglev corridors
    paths=[[(-250,15,85),(-190,24,15),(-120,30,-30),(-40,28,-10),(25,34,-60),(100,30,-110),(205,26,-95)],[(-240,22,115),(-170,26,170),(-80,25,160),(0,32,130),(90,28,80),(170,26,5)]]
    for path in paths:
        pts=[project(x,z,y,a)[:2] for x,y,z in path]
        d.line(pts,fill=(66,222,255,255),width=4,joint="curve")
        for x,y,z in path:
            bx,by=project(x,z,0,a)[:2];tx,ty=project(x,z,y,a)[:2]
            d.line((bx,by,tx,ty),fill=(119,169,188,220),width=2)
    # PI arc and radial energy grid
    for radius,color in [(225,(57,154,201,190)),(290,(42,105,148,170))]:
        pts=[project(radius*math.cos(t),radius*.56*math.sin(t),38,a)[:2] for t in [TAU*i/360 for i in range(361)]]
        d.line(pts,fill=color,width=2)
    # offshore wind / solar markers
    for i in range(9):
        x=-360+i*90;z=260;px,py,_=project(x,z,20,a)
        d.ellipse((px-3,py-3,px+3,py+3),fill=(111,244,229,255))
    d.rounded_rectangle((18,16,580,96),radius=10,fill=(4,18,31,225),outline=(53,125,158,220))
    d.text((34,26),"QAN PI  /  WEST JAPAN NEO WORLD",font=font(23,True),fill=(226,248,255))
    d.text((35,62),"CHUGOKU  ·  SHIKOKU  ·  KYUSHU  /  3D ARCHIPELAGO",font=font(12,True),fill=(100,221,247))
    d.rounded_rectangle((W-235,18,W-18,88),radius=8,fill=(4,18,31,220),outline=(53,125,158,200))
    d.text((W-218,29),f"ORBIT  {int(math.degrees(a))%360:03d}°",font=font(16,True),fill=(226,248,255))
    d.text((W-218,57),f"URBAN NODES  {len(buildings):,}",font=font(11),fill=(159,199,219))
    d.text((18,H-32),"FICTIONAL FUTURE CITY / SCHEMATIC GEOGRAPHY / NOT A SURVEY-GRADE DIGITAL TWIN",font=font(10,True),fill=(144,190,211))
    return im
def main():
    OUT.parent.mkdir(parents=True,exist_ok=True);b=make_city()
    frames=[frame(TAU*i/30,b) for i in range(30)]
    frames[0].save(OUT,save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True,disposal=2)
    print(f"GIF written: {OUT} ({OUT.stat().st_size:,} bytes)")
if __name__=="__main__":main()
