# QAN Geometry Editor Studio 0.4.0

## Blender-inspired WebGL workspace

Run `python -m http.server 8000` from the repository root and open `http://localhost:8000/viewer/editor.html`. The page loads Three.js ES modules from jsDelivr and requires an internet connection.

### Included prototype features
- Dark workspace with scene collection, 3D viewport, transform properties, and status bar.
- Add cube, UV sphere, plane, quad grid, and conceptual maglev guideway.
- Orbit, pan, zoom, focus, grid and axes toggles.
- Object duplicate/delete, scene-level undo/redo snapshots and common keyboard shortcuts.
- Object-level move / rotate / scale gizmos and numeric transforms.
- Solid, wireframe, and X-Ray display modes; optional edge and vertex overlays.
- **Edit Mesh vertex mode:** click a displayed vertex, edit its local X/Y/Z coordinates, and apply the change to the mesh. Vertex edits are included in geometry snapshots.
- Deterministic prompt parser for cube, quad grid/terrain, and guideway geometry.
- **QAN project save/load** using the versioned `qan-studio-project/1.0` JSON schema.
- **GLB/glTF import and GLB export** using Three.js GLTFLoader / GLTFExporter.
- Export scene as Wavefront OBJ or QAN JSON.
- Viewport counters for objects, draw calls, and triangles.

### Current editing scope
Edit Mesh currently supports direct vertex selection and numeric coordinate editing. Edge-loop selection, face selection, extrusion, inset, bevel, proportional editing, and snapping are not implemented yet. The editor is Blender-inspired, not a complete Blender replacement.

### Data and compatibility notes
- QAN project files preserve mesh vertex/index buffers, object transforms, basic material color, and roughness. They do not serialize node graphs, modifiers, UV maps, armatures, animation, or physics.
- GLB import currently imports mesh objects and basic materials; complex scenes and animation require additional validation.
- GLB export writes the current scene meshes and supported basic material properties.
- Browser QAN JSON export is a triangle-oriented interchange format; use the Python/Blender quad-first library for quad-preserving workflows.
- Undo/redo is a lightweight scene snapshot system; large meshes may consume substantial memory.
- No generated rail or terrain geometry is engineering-certified.

### Preview and desktop launcher

Start a local HTTP server from the repository root and open `http://localhost:8000/viewer/editor.html`. The Windows Studio executable launches the local browser-based workspace; it is not a native embedded viewport. Internet access is required for Three.js modules.
