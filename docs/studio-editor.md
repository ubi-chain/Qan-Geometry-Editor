# QAN Geometry Editor Studio 0.3.0

## Blender-inspired WebGL workspace

Run `python -m http.server 8000` from the repository root and open `http://localhost:8000/viewer/editor.html`. The page loads Three.js ES modules from jsDelivr and requires an internet connection.

### Included prototype features
- Dark workspace with scene collection, 3D viewport, transform properties, and status bar.
- Add cube, UV sphere, plane, quad grid, and conceptual maglev guideway.
- Orbit, pan, zoom, focus, grid and axes toggles.
- Object duplicate/delete, plus scene-level undo/redo history (up to 60 snapshots) and Ctrl+Z / Ctrl+Shift+Z / Ctrl+D / Delete shortcuts.
- Object-level move / rotate / scale gizmos and numeric transforms.
- Solid, wireframe, and X-Ray display modes; optional edge and vertex overlays.
- Deterministic prompt parser for cube, quad grid/terrain, and guideway geometry.
- Export scene as Wavefront OBJ or QAN JSON.
- Viewport counters for objects, draw calls, and triangles.

### Honest feature boundary
This is a Blender-inspired editor prototype, not a complete Blender replacement. The Edit Mesh control is a workflow placeholder: per-vertex, edge, and face selection and component transforms are not implemented. The browser QAN JSON exporter currently emits triangle faces from Three.js buffer geometry; use the Python/Blender quad-first library for quad-preserving geometry. Material controls are viewport-only. Node graphs, modifiers, UV editing, sculpting, rigging, animation timelines, physics, undo/redo, GLB import/export, and production-grade persistence are not included. No generated rail or terrain geometry is engineering-certified.

### Current limitations

- Undo/redo snapshots cover object creation, deletion, duplication, and numeric/object transforms; they do not yet represent vertex-level edits.
- The Edit Mesh control is still a workflow placeholder. Component selection and vertex/edge/face transforms are not implemented.

### Next milestones
1. Vertex / edge / face selection and component editing.
2. Undo/redo, snapping, and selection tools.
3. GLB/glTF import/export and Blender round-trip tests.
4. Modifier stack, UV tools, and material serialization.
5. Automated browser and Blender compatibility tests.
