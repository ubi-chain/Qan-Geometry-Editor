# QAN Geometry Editor Studio 0.7.0

## Blender-inspired WebGL workspace

Run `python -m http.server 8000` from the repository root and open `http://localhost:8000/viewer/editor.html`. Three.js modules load from jsDelivr, so an internet connection is required.

### Features
- Dark workspace, scene collection, 3D viewport and transform properties.
- Add cube, UV sphere, plane, quad grid and conceptual maglev guideway.
- Orbit, pan, zoom, focus, grid and axes toggles.
- Object duplicate/delete, scene-level undo/redo and keyboard shortcuts.
- **Blender-inspired keymap:** G/R/S start modal move/rotate/scale; X/Y/Z constrains the axis, type a numeric value, Enter confirms and Esc cancels. Tab toggles Object/Edit Mesh; Shift+A adds a cube; Shift+D duplicates; X/Delete removes; H hides and Alt+H reveals; F focuses selected; Home frames all; Ctrl+A applies transforms to mesh; Ctrl+Z / Ctrl+Shift+Z undo/redo; Ctrl+S / Ctrl+O save/open; ? opens shortcut help. Numpad 1/3/7 sets front/right/top; Ctrl+Numpad sets the opposite view; Numpad 2/4/6/8 orbits in 15-degree steps; Numpad 5 toggles narrow perspective.
- **Language selector:** Japanese, English, Simplified Chinese and Korean for the main interface controls and panel labels. Some technical status messages and generated content may remain in English.
- Object-level move/rotate/scale gizmos and numeric transforms.
- Solid, wireframe and X-Ray display modes; edge and vertex overlays.
- **Edit Mesh vertex mode:** click a displayed vertex and edit local X/Y/Z coordinates.
- **Object quick tools:** Apply Transforms bakes location/rotation/scale into mesh vertices; Origin to Geometry moves the origin to the mesh bounding-box center; Shade Smooth / Shade Flat toggles material shading; Mirror X Copy creates a mirrored duplicate; Array ×3 creates three objects spaced along world X. These are destructive/simple mesh operations, not a full Blender modifier stack.
- Deterministic prompt parser for cube, quad grid/terrain and guideway.
- QAN project save/load using `qan-studio-project/1.0`.
- GLB/glTF import and GLB export; OBJ and QAN JSON export.

### Current limitations
Edit Mesh supports direct vertex selection and numeric coordinate editing. Edge-loop selection, face selection, extrusion, inset, bevel, proportional editing, snapping, node graphs, modifiers, UV editing, rigging and animation tools are not implemented. This is Blender-inspired, not a complete Blender replacement.

QAN project files preserve mesh vertex/index buffers, object transforms and basic material color/roughness, but not modifiers, UV maps, armatures, animation, physics or shader graphs. GLB import/export supports common mesh and basic material workflows; complex scenes need additional validation.

### Preview and desktop launcher
Open `http://localhost:8000/viewer/editor.html` after starting a local server. The Windows Studio executable launches this browser-based workspace; it is not a native embedded viewport. Internet access is required for Three.js modules.


## Modal transforms, quick tools and shortcuts (0.7.0)

- Press `G`, `R`, or `S` to begin a modal transform on the selected object (move, rotate, scale).
- Press `X`, `Y`, or `Z` to constrain the transform to that axis; enter a numeric amount; press Enter to confirm or Esc to cancel.
- Rotation numeric values are degrees. Scale without an axis is uniform; axis-constrained scale changes the selected axis component.
- Numpad `7/1/3` selects top/front/right views; Ctrl+Numpad selects the opposite view. Numpad `2/4/6/8` rotates the view in 15-degree increments; Numpad `5` toggles a narrow/perspective view.
- Ctrl+Z / Ctrl+Shift+Z undo/redo; Ctrl+S / Ctrl+O save/open; Ctrl+D duplicate; Tab switches Object/Edit Mesh.

The modal transform and camera shortcuts are specific to QAN Studio and are inspired by common 3D-editor conventions. They do not reproduce every Blender keymap or every Blender transform behaviour.


## Blender-inspired object quick tools (0.7.0)

The right-side Object Quick Tools panel includes Apply Transforms, Origin to Geometry, Shade Smooth, Shade Flat, Mirror X Copy and Array ×3. The shortcuts and tools are original QAN Studio implementations inspired by common 3D workflows; they are not bundled third-party Blender add-ons and do not claim full Blender parity. Undo is available for scene operations recorded in the editor history.
