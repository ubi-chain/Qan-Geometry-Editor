bl_info = {
    "name": "QAN Geometry Tools",
    "author": "Independent Developer",
    "version": (0, 2, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > QAN",
    "description": "Import/export QAN quad meshes and generate geometry from constrained prompts",
    "category": "Mesh",
}
import bpy, json, re
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.types import Operator, Panel

def _mesh_from_qan(data):
    if data.get("schema") not in ("qan-geometry/0.1", "qan-geometry/0.2"):
        raise ValueError("Unsupported QAN Geometry schema")
    vertices, faces = data.get("vertices", []), data.get("faces", [])
    if not vertices or not faces: raise ValueError("QAN file must contain vertices and faces")
    for face in faces:
        if len(face) != 4 or len(set(face)) != 4: raise ValueError("Only quad faces with four unique indices are supported")
        if any(not isinstance(i, int) or i < 0 or i >= len(vertices) for i in face): raise ValueError("Face index outside vertex array")
    mesh = bpy.data.meshes.new(data.get("name", "QAN Mesh") + " Mesh")
    mesh.from_pydata(vertices, [], faces); mesh.update()
    obj = bpy.data.objects.new(data.get("name", "QAN Mesh"), mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj; obj.select_set(True)
    return obj

def _num(text, patterns, default):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try: return float(match.group(1))
            except (ValueError, IndexError): pass
    return default

def _integer(text, patterns, default):
    return max(1, int(round(_num(text, patterns, default))))

def _build_prompt_mesh(prompt):
    text = prompt.lower()
    size = _num(text, [r"(?:size|辺|一辺)\s*[:=]?\s*([0-9]+(?:\.[0-9]+)?)", r"([0-9]+(?:\.[0-9]+)?)\s*m?\s*(?:cube|立方体|キューブ)"], 10.0)
    width = _num(text, [r"(?:width|幅)\s*[:=]?\s*([0-9]+(?:\.[0-9]+)?)", r"([0-9]+(?:\.[0-9]+)?)\s*(?:m|メートル)?\s*(?:×|x)\s*[0-9]+(?:\.[0-9]+)?"], 10000.0)
    depth = _num(text, [r"(?:depth|奥行|奥行き)\s*[:=]?\s*([0-9]+(?:\.[0-9]+)?)"], width)
    cx = _integer(text, [r"(?:cells_x|横分割)\s*[:=]?\s*([0-9]+)", r"([0-9]+)\s*[×x]\s*[0-9]+\s*(?:cells|分割)"], 40)
    cy = _integer(text, [r"(?:cells_y|縦分割)\s*[:=]?\s*([0-9]+)", r"[0-9]+\s*[×x]\s*([0-9]+)\s*(?:cells|分割)"], cx)
    if any(k in text for k in ("maglev","guideway","linear","リニア","線路","軌道")):
        length = _num(text,[r"(?:length|長さ)\s*[:=]?\s*([0-9]+(?:\.[0-9]+)?)",r"([0-9]+(?:\.[0-9]+)?)\s*(?:m|メートル)?\s*(?:maglev|リニア|線路|軌道)"],1000.0)
        rail_width = _num(text,[r"(?:rail_width|軌道幅|幅)\s*[:=]?\s*([0-9]+(?:\.[0-9]+)?)"],8.0)
        segments = _integer(text,[r"(?:segments|区間|分割)\s*[:=]?\s*([0-9]+)"],20)
        verts, faces, half = [], [], rail_width/2
        for i in range(segments+1):
            x=-length/2+length*i/segments
            verts.extend([(x,-half,0),(x,half,0),(x,-half,-.6),(x,half,-.6)])
        for i in range(segments):
            a,b=i*4,i*4+4
            faces.extend([(a,a+1,b+1,b),(a+2,b+2,b+3,a+3),(a,b,b+2,a+2),(a+1,a+3,b+3,b+1)])
        faces.extend([(0,2,3,1),(segments*4,segments*4+1,segments*4+3,segments*4+2)])
        return {"schema":"qan-geometry/0.2","name":"Prompt Maglev Guideway","vertices":verts,"faces":faces}
    if any(k in text for k in ("grid","terrain","city","地形","都市","グリッド","地面")):
        verts,faces=[],[]
        for j in range(cy+1):
            y=-depth/2+depth*j/cy
            for i in range(cx+1): verts.append((-width/2+width*i/cx,y,0.0))
        stride=cx+1
        for j in range(cy):
            for i in range(cx):
                a=j*stride+i; faces.append((a,a+1,a+1+stride,a+stride))
        return {"schema":"qan-geometry/0.2","name":"Prompt City Terrain","vertices":verts,"faces":faces}
    h=size/2
    verts=[(-h,-h,-h),(h,-h,-h),(h,h,-h),(-h,h,-h),(-h,-h,h),(h,-h,h),(h,h,h),(-h,h,h)]
    faces=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    return {"schema":"qan-geometry/0.2","name":"Prompt Cube","vertices":verts,"faces":faces}

class QAN_OT_import(Operator, ImportHelper):
    bl_idname="qan.import_json"; bl_label="Import QAN JSON"; filename_ext=".json"
    filter_glob: StringProperty(default="*.json", options={"HIDDEN"})
    def execute(self,context):
        try:
            with open(self.filepath,"r",encoding="utf-8") as f: _mesh_from_qan(json.load(f))
        except Exception as exc: self.report({"ERROR"},str(exc)); return {"CANCELLED"}
        return {"FINISHED"}

class QAN_OT_export(Operator, ExportHelper):
    bl_idname="qan.export_json"; bl_label="Export Active Mesh as QAN JSON"; filename_ext=".json"
    filter_glob: StringProperty(default="*.json", options={"HIDDEN"})
    def execute(self,context):
        obj=context.active_object
        if not obj or obj.type!="MESH": self.report({"ERROR"},"Select an active mesh object"); return {"CANCELLED"}
        verts=[list(v.co) for v in obj.data.vertices]; faces=[]; skipped=0
        for poly in obj.data.polygons:
            ids=list(poly.vertices)
            if len(ids)==4: faces.append(ids)
            else: skipped+=1
        if not faces: self.report({"ERROR"},"No quad faces found; convert or retopologize to quads first"); return {"CANCELLED"}
        data={"schema":"qan-geometry/0.2","name":obj.name,"vertices":verts,"faces":faces,
              "metadata":{"units":"Blender scene units","source":"Blender QAN Geometry Tools","skipped_non_quad_faces":skipped}}
        try:
            with open(self.filepath,"w",encoding="utf-8") as f: json.dump(data,f,ensure_ascii=False,indent=2)
        except Exception as exc: self.report({"ERROR"},str(exc)); return {"CANCELLED"}
        self.report({"INFO"},f"Exported {len(verts)} vertices, {len(faces)} quads; skipped {skipped} non-quads")
        return {"FINISHED"}

class QAN_OT_prompt(Operator):
    bl_idname="qan.generate_from_prompt"; bl_label="Generate Geometry from Prompt"
    def execute(self,context):
        prompt=context.scene.qan_prompt_text.strip()
        if not prompt: self.report({"WARNING"},"Enter a geometry prompt"); return {"CANCELLED"}
        try:
            data=_build_prompt_mesh(prompt); _mesh_from_qan(data)
        except Exception as exc: self.report({"ERROR"},str(exc)); return {"CANCELLED"}
        self.report({"INFO"},f"Generated {data['name']}: {len(data['vertices'])} vertices / {len(data['faces'])} quads")
        return {"FINISHED"}

class QAN_PT_panel(Panel):
    bl_label="QAN Geometry Editor"; bl_idname="QAN_PT_geometry_tools"
    bl_space_type="VIEW_3D"; bl_region_type="UI"; bl_category="QAN"
    def draw(self,context):
        layout=self.layout
        layout.label(text="QAN JSON / Blender")
        layout.operator("qan.import_json",icon="IMPORT")
        layout.operator("qan.export_json",icon="EXPORT")
        layout.separator(); layout.label(text="Prompt to Quad Mesh")
        layout.prop(context.scene,"qan_prompt_text",text="")
        layout.operator("qan.generate_from_prompt",icon="OUTLINER_OB_MESH")
        layout.label(text="Examples: 10m cube")
        layout.label(text="10km city grid 40x40")
        layout.label(text="1km maglev guideway segments 30")

classes=(QAN_OT_import,QAN_OT_export,QAN_OT_prompt,QAN_PT_panel)
def register():
    for cls in classes: bpy.utils.register_class(cls)
    bpy.types.Scene.qan_prompt_text=StringProperty(name="Geometry Prompt",default="10km city grid 40x40",
      description="Supported shapes: cube, city grid/terrain, maglev/linear guideway; use numeric parameters")
def unregister():
    del bpy.types.Scene.qan_prompt_text
    for cls in reversed(classes): bpy.utils.unregister_class(cls)
if __name__=="__main__": register()
