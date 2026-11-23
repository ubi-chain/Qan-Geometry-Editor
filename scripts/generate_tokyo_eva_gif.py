#!/usr/bin/env python3
"""Render a lightweight orbit GIF of the QAN PI Tokyo EVA concept city.

The 23-ward outline is decoded from the OSM-derived TopoJSON pack at build time.
Buildings, Tama relief, island inset and elevated transit are explicitly marked
as a stylized observation model, not surveyed building geometry.
"""
from __future__ import annotations
import json, math, os, random, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PI = math.pi
TAU = 2 * PI
W, H = 960, 540
OUT = Path(os.environ.get("OUTPUT_GIF", "dist/QAN-Tokyo-EVA-City.gif"))
DATA_URL = "https://cdn.jsdelivr.net/gh/hwcharlton/geo-data@v1.3.0/packs/tokyo-23/admin/med.topo.json"

def decode_topology(topology):
    scale = topology.get("transform", {}).get("scale", [1, 1])
    translate = topology.get("transform", {}).get("translate", [0, 0])
    decoded = []
    for arc in topology["arcs"]:
        x = y = 0
        points = []
        for dx, dy in arc:
            x += dx; y += dy
            points.append((x * scale[0] + translate[0], y * scale[1] + translate[1]))
        decoded.append(points)
    def arc_points(index):
        pts = decoded[index] if index >= 0 else list(reversed(decoded[~index]))
        return pts
    def ring(indices):
        out = []
        for idx in indices:
            pts = arc_points(idx)
            out.extend(pts if not out else pts[1:])
        return out
    obj = topology["objects"][next(iter(topology["objects"]))]
    polys = []
    for geom in obj.get("geometries", []):
        arcs = geom.get("arcs", [])
        groups = [arcs] if geom["type"] == "Polygon" else arcs
        for polygon in groups:
            if polygon:
                coords = ring(polygon[0])
                if len(coords) > 3: polys.append(coords)
    return polys

def load_wards():
    try:
        req = urllib.request.Request(DATA_URL, headers={"User-Agent": "QAN-Geometry-Editor/0.4"})
        with urllib.request.urlopen(req, timeout=30) as r:
            topo = json.loads(r.read().decode("utf-8"))
        return decode_topology(topo), "© OpenStreetMap contributors · Tokyo 23-ward boundary"
    except Exception as exc:
        print("Ward boundary fetch failed; using schematic outline:", exc)
        outline = [(139.56,35.70),(139.60,35.80),(139.68,35.84),(139.78,35.83),
                   (139.88,35.78),(139.92,35.69),(139.88,35.60),(139.80,35.54),
                   (139.68,35.53),(139.59,35.59),(139.56,35.70)]
        return [outline], "Schematic ward outline fallback"

def local(lon, lat):
    return ((lon - 139.70) * 90.0, -(lat - 35.68) * 111.2)

def point_in_poly(x, z, poly):
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, zi = poly[i]; xj, zj = poly[j]
        if ((zi > z) != (zj > z)) and x < (xj - xi) * (z - zi) / ((zj - zi) or 1e-9) + xi:
            inside = not inside
        j = i
    return inside

def make_city(polys):
    random.seed(20261123)
    local_polys = [[local(*p) for p in poly] for poly in polys]
    buildings = []
    for poly in local_polys:
        xs = [p[0] for p in poly]; zs = [p[1] for p in poly]
        area = max(1, (max(xs)-min(xs)) * (max(zs)-min(zs)))
        target = min(260, max(28, int(area * 1.5)))
        tries = 0; made = 0
        while made < target and tries < target * 80:
            tries += 1
            x = random.uniform(min(xs), max(xs)); z = random.uniform(min(zs), max(zs))
            if not point_in_poly(x, z, poly): continue
            d = math.hypot(x, z); central = max(0, 1 - d/25)
            height = random.uniform(.18, 1.0) + random.random() ** 2 * (1.1 + central * 4.5)
            width = random.uniform(.12, .42); depth = random.uniform(.12, .42)
            buildings.append((x, z, height, width, depth))
            made += 1
    return local_polys, buildings

def font(size, bold=False):
    paths = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"]
    for path in paths:
        try: return ImageFont.truetype(path, size)
        except OSError: pass
    return ImageFont.load_default()

def render_frame(angle, polys, buildings, attribution):
    im = Image.new("RGB", (W,H), (5,12,21)); d = ImageDraw.Draw(im, "RGBA")
    elev = .48; scale = 8.1
    def project(x,z,y=0):
        xr = x*math.cos(angle) - z*math.sin(angle)
        zr = x*math.sin(angle) + z*math.cos(angle)
        sx = W*.48 + xr*scale
        sy = H*.60 + (zr*math.sin(elev) - y*math.cos(elev))*scale
        depth = zr*math.cos(elev) + y*math.sin(elev)
        return (sx,sy,depth)
    # Ground ward silhouettes
    for poly in polys:
        pts = [project(x,z)[:2] for x,z in poly]
        d.polygon(pts, fill=(16,34,48,255), outline=(45,104,135,190))
    # Tama relief silhouette, generalized to the west
    tama = [(-48,-12),(-44,-17),(-35,-18),(-25,-14),(-20,-8),(-21,2),(-29,9),(-40,10),(-48,4)]
    d.polygon([project(x,z,0)[:2] for x,z in tama], fill=(19,53,48,230), outline=(72,139,112,190))
    # Buildings sorted by camera depth
    ordered = sorted(buildings, key=lambda b: project(b[0],b[1],b[2])[2])
    for x,z,h,w,dep in ordered:
        p0=project(x-w/2,z-dep/2,0); p1=project(x+w/2,z-dep/2,0)
        p2=project(x+w/2,z+dep/2,0); p3=project(x-w/2,z+dep/2,0)
        t0=project(x-w/2,z-dep/2,h); t1=project(x+w/2,z-dep/2,h)
        t2=project(x+w/2,z+dep/2,h); t3=project(x-w/2,z+dep/2,h)
        shade=max(20,min(90,int(35+h*7)))
        d.polygon([p0[:2],p1[:2],t1[:2],t0[:2]], fill=(18,49,69,255))
        d.polygon([p1[:2],p2[:2],t2[:2],t1[:2]], fill=(27,68,88,255))
        d.polygon([t0[:2],t1[:2],t2[:2],t3[:2]], fill=(shade,shade+35,shade+48,255))
    # QAN PI elevated loops and radial links
    for radius, height, color in [(9.4,2.0,(60,216,255,255)),(14.4,2.8,(255,153,85,255))]:
        pts=[]
        for i in range(721):
            a=TAU*i/720
            pts.append(project(radius*math.cos(a), radius*.82*math.sin(a), height)[:2])
        d.line(pts, fill=color, width=4, joint="curve")
        for i in range(0,96,6):
            a=TAU*i/96
            base=project(radius*math.cos(a),radius*.82*math.sin(a),0)[:2]
            top=project(radius*math.cos(a),radius*.82*math.sin(a),height)[:2]
            d.line([base,top],fill=(102,139,157,210),width=2)
    for i in range(12):
        a=TAU*i/12
        pts=[project(0,0,2.1)[:2],project(7*math.cos(a),5.7*math.sin(a),2.4)[:2],
             project(14*math.cos(a),11.5*math.sin(a),2.8)[:2]]
        d.line(pts,fill=(74,183,239,220),width=2)
    # island inset (not to scale)
    for i,(x,z) in enumerate([(34,-7),(36,-12),(38,-17),(40,-22),(42,-27)]):
        px,py,_=project(x,z,.4)
        d.ellipse((px-5,py-3,px+5,py+3),fill=(63,142,125,255),outline=(159,226,203,255))
    # Title and technical readout
    d.rounded_rectangle((18,16,555,94),radius=10,fill=(5,18,31,225),outline=(45,100,130,220))
    d.text((34,27),"QAN PI  /  TOKYO EVA CITY",font=font(24,True),fill=(224,246,255,255))
    d.text((35,61),"23 WARDS CORE  ·  TAMA  ·  ISLANDS INSET  ·  PI VIADUCT",font=font(11,True),fill=(101,215,245,255))
    d.rounded_rectangle((W-280,18,W-18,91),radius=8,fill=(5,18,31,220),outline=(45,100,130,200))
    d.text((W-263,30),f"ORBIT  {int(math.degrees(angle))%360:03d}°",font=font(15,True),fill=(223,242,255,255))
    d.text((W-263,57),f"BUILDING MASSES  {len(buildings):,}",font=font(11),fill=(155,190,211,255))
    d.text((18,H-37),"CONCEPTUAL MASSING / BRIDGES ARE PROPOSED DESIGN, NOT EXISTING INFRASTRUCTURE",font=font(10,True),fill=(151,190,208,255))
    d.text((W-380,H-37),attribution[:55],font=font(9),fill=(122,157,177,255))
    return im

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    polys, attribution = load_wards()
    local_polys, buildings = make_city(polys)
    frames=[]
    for i in range(24):
        frames.append(render_frame(TAU*i/24, local_polys, buildings, attribution))
    frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=110, loop=0, optimize=True, disposal=2)
    print(f"GIF written: {OUT} ({OUT.stat().st_size:,} bytes)")

if __name__ == "__main__":
    main()
