# QAN Geometry Editor

Free, quad-first 3D geometry editor and lightweight geometry library using QAN PI concepts. The prototype focuses on editable quad meshes, validation summaries, and exportable reference geometry for a fictional 10 km × 10 km Third-City-inspired environment and a conceptual linear/maglev system.

**Version:** 0.6.0 (prototype)  
**Code license:** MIT  
**Documentation:** CC BY 4.0  
**Author:** Independent Developer

## Features

- Windows desktop app built with Python's standard Tkinter GUI.
- Pure-Python library package: qan_geometry.
- Quad cube, configurable 2D quad terrain grid, and linear guideway reference mesh.
- Basic topology counts: vertices, quad faces, boundary edges, non-manifold edges.
- Export to Wavefront OBJ and QAN Geometry JSON.
- Command-line generator.
- Browser-based Three.js viewers: Tokyo EVA City and West Japan Neo World with QAN PI orbit observation.
- Blender-inspired QAN Studio WebGL workspace with scene collection, object tools, transform gizmos, vertex-level Edit Mesh mode, Blender-style G/R/S, Tab, Shift+D, X/Delete and Ctrl shortcuts, Japanese/English/Chinese/Korean UI switching, prompt-based primitive generation, project save/load, GLB/glTF import/export, OBJ and QAN JSON export.
- Blender add-on: import/export QAN quad-mesh JSON and generate supported geometry from Japanese/English prompts.
- GitHub Actions workflow builds a Windows x64 executable and Python wheel/sdist artifacts.

## Blender integration and prompt generation

Install the add-on from blender/qan_geometry_addon.py:

1. Blender → Edit → Preferences → Add-ons → Install from Disk.
2. Select qan_geometry_addon.py and enable **QAN Geometry Tools**.
3. In the 3D Viewport press N and open the **QAN** tab.
4. Import/export QAN JSON or enter a geometry prompt and choose Generate Geometry from Prompt.

Example prompts:
- 10m cube
- 10km city grid 40x40
- width=10000 depth=10000 cells_x=80 cells_y=80 terrain
- 1km maglev guideway segments=30
- length=2500 rail_width=12 segments=50 linear guideway

The prompt parser is constrained and deterministic. It recognizes cube, quad terrain/grid, and guideway terms with numeric parameters; it is not an LLM and does not execute arbitrary code. See [Blender and Prompt Workflow](docs/blender-and-prompt-workflow.md).

QAN JSON export from Blender preserves quad faces. Non-quad polygons are skipped and reported. Materials, modifiers, UVs, armatures, animation and node graphs are not serialized.

## Run from source

```bash
python -m pip install .
qan-geometry-editor
```

Generate a cube:
```bash
qan-geometry --shape cube --size 10 --output cube.obj
```

Generate the 10 km terrain grid:
```bash
qan-geometry --shape city-grid --format json --output third-city-terrain.json
```

## Build locally on Windows

```powershell
python -m pip install . pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --name QAN-Geometry-Editor --collect-all qan_geometry src/qan_geometry_editor/app.py
```

The executable is created at dist/QAN-Geometry-Editor.exe. Windows builds must be produced on Windows; the GitHub Actions workflow does this automatically when manually run or when a v* tag is pushed. Download the workflow artifact from the Actions run.

## Python library

```python
from qan_geometry import cube, grid, validate_mesh, write_obj

mesh = cube(size=12)
print(validate_mesh(mesh))
write_obj(mesh, "cube.obj")

terrain = grid(width=10_000, depth=10_000, cells_x=100, cells_y=100)
```

## QAN Studio — Blender-inspired WebGL editor

Open [QAN Studio](viewer/editor.html) for the dark 3D workspace. It includes a scene collection, object creation, orbit/pan/zoom, move/rotate/scale gizmos, numeric transforms, solid/wireframe/X-Ray display, edge and vertex overlays, click-to-select vertex editing, constrained prompt generation, QAN project save/load, GLB/glTF import/export, and OBJ/QAN JSON export. Face/edge component editing and full Blender parity remain future work. See [Studio editor documentation](docs/studio-editor.md) for setup and limitations.

Run `python -m http.server 8000` from the repository root and visit `http://localhost:8000/viewer/editor.html`. Three.js is loaded from jsDelivr, so an internet connection is required.

## Interactive 3D viewer

A browser scene with procedural Third-City-inspired city blocks, elevated guideway, orbit/pan/zoom controls, speed control and an animated train.

- [Open viewer source](viewer/index.html)
- [Viewer documentation](docs/third-city-maglev-viewer.md)

To preview locally, run python -m http.server 8000 from the repository root and open http://localhost:8000/viewer/. For a public URL, enable GitHub Pages with the repository root as the publishing source.

## Scope and safety

This is an early geometry prototype, not a complete CAD or railway engineering tool. The 10 km terrain grid is a flat reference surface. No geospatial elevation data, rail dynamics, structural analysis, certified clearance calculations, robust self-intersection detection, or engineering validation are included. Linear/maglev assets and the Third-City-inspired setting are fictional visualization references only.

## Roadmap

- Interactive native editor viewport with orbit/pan/zoom and vertex/face selection.
- GLB/glTF import/export and Blender round-trip tests.
- Quad-first primitives, LOD generation, instancing and spatial chunking.
- QAN PI integration through a validated, versioned data schema.
- Robust topology, intersection and clearance checks with documented limitations.

## License

Source code: MIT (see LICENSE). Documentation: CC BY 4.0 (see docs/LICENSE-DOCS.md).


## QAN PI Sunset City reconstruction (people-free)

A procedural Three.js scene reconstructs the supplied sunset-city wallpaper as editable polygonal scene elements, intentionally omitting all people. It includes a polygonal mountain and snow cap, sunset sky, sun, dense city blocks, landmark towers, and an empty observation terrace with railings. QAN PI / tau are used for angular sampling, radial city layout, and orbit calculations.

- [Open the 360-degree WebGL viewer source](viewer/wallpaper-3d.html)
- [Reconstruction notes and controls](docs/sunset-city-reconstruction.md)

Run `python -m http.server 8000` from the repository root and visit `http://localhost:8000/viewer/wallpaper-3d.html`. The page loads Three.js from jsDelivr, so an internet connection is required. This is a stylized interpretation from one 2D image; hidden surfaces and exact depth are inferred, not photogrammetrically recovered.


## Geometry Studio 0.7 — Blender-inspired workflow

The browser-based Studio now includes a Blender-inspired starter set of everyday operations: modal G/R/S transforms with numeric input and X/Y/Z constraints, Numpad orthographic-style views, quick cube add, hide/reveal, Apply Transforms, Origin to Geometry, smooth/flat shading, Mirror X Copy and Array ×3. These are lightweight QAN implementations, not bundled third-party add-ons or a full Blender modifier stack. See [Studio controls and limitations](docs/studio-editor.md).

## Windows executable

A Windows x64 desktop preview build is published from GitHub Actions. After a successful `main` build, download `QAN-Geometry-Editor.exe` from the [latest Windows preview release](https://github.com/ubi-chain/Qan-Geometry-Editor/releases/tag/latest). This desktop executable packages the lightweight Tkinter quad-mesh editor (`src/qan_geometry_editor/app.py`); it is separate from the browser-based Three.js Studio at `viewer/editor.html`. The first launch may be flagged by Windows SmartScreen because the build is not code-signed.


## QAN PI × Tokyo EVA City

Open [Tokyo EVA City 3D Observer](viewer/tokyo-eva-city.html) for a WebGL observation scene with QAN PI elevated ring roads, radial bridges, Tama terrain, and an island inset. The 23-ward boundary shape is loaded from an OSM-derived TopoJSON dataset. Building masses are generated for a lightweight visualization; proposed viaducts are conceptual and are not existing infrastructure. Tama and island geometry is schematic, not at true scale. See [Tokyo EVA City scope and sources](docs/tokyo-eva-city.md).

### QAN PI helpers

The Python package now exposes `PI`, `TAU`, degree/radian conversion, polar coordinates, circular ring sampling, helix sampling, circumference, and circle area.

```python
from qan_geometry import ring_points, helix_points, circle_circumference

ring = ring_points(radius=9000, segments=720, y=2000)
ramp = helix_points(radius=4500, pitch=2200, turns=1.5)
print(circle_circumference(9000))
```

### Latest Windows and GIF release

The GitHub Actions release publishes these assets when the build succeeds:

- `QAN-Geometry-Editor.exe` — lightweight Tkinter quad-mesh desktop editor.
- `QAN-Geometry-Studio.exe` — desktop launcher for the WebGL Studio and Tokyo EVA City observer.
- `QAN-Tokyo-EVA-City.gif` — 24-frame orbit preview.

Download from [Latest QAN Geometry + Tokyo EVA City Release](https://github.com/ubi-chain/Qan-Geometry-Editor/releases/tag/latest). The Studio and city observer require internet access for public CDN libraries and boundary data. The EXEs are unsigned preview builds.


## QAN PI × West Japan Neo World

Open [West Japan Neo World 3D Observer](viewer/west-japan-neo-world.html) for a near-future concept world inspired by **Kyushu, Shikoku and Chugoku**. It includes procedural island silhouettes, instanced city blocks, fictional inter-island maglev corridors, offshore energy structures and a PI-based observation arc. The geography is schematic and the infrastructure is fictional, not a surveyed digital twin or a depiction of existing transport.

- [Open the WebGL observer](viewer/west-japan-neo-world.html)
- [World design, controls and limitations](docs/west-japan-neo-world.md)
- [GIF generator](scripts/generate_west_japan_gif.py)

Run `python -m http.server 8000` from the repository root and visit `http://localhost:8000/viewer/west-japan-neo-world.html`. Three.js loads from jsDelivr, so an internet connection is required.

### Combined camera shortcuts

- `G` fly / translation mode; `R` camera rotation mode.
- Hold `W/A/S/D` to move forward/left/back/right; `Q/E` moves down/up.
- Hold `X`, `Y`, and/or `Z` together with movement keys to constrain movement to selected world axes.
- `Shift` accelerates; `Ctrl` provides precision movement.
- In rotation mode, WASD rotates yaw/pitch and Q/E rolls the camera.
- Right numeric keypad: `7` top, `Ctrl+7` bottom, `1` front, `Ctrl+1` back, `3` right, `Ctrl+3` left, `9` opposite oblique, `5` perspective toggle; `2/4/6/8` orbit in 15-degree steps.

Generate the orbit GIF locally with `python -m pip install Pillow` then `python scripts/generate_west_japan_gif.py`. GitHub Actions also creates the GIF as a release asset when the build completes.


## Blender quick-tools starter set

The QAN Blender add-on includes quick primitive creation (cube, UV sphere, plane and quad grid), apply transforms, bevel modifier, subdivision-surface modifier, and smooth shading, alongside QAN JSON import/export and constrained prompt-to-mesh generation. Install `blender/qan_geometry_addon.py` from Blender Preferences → Add-ons → Install from Disk, then use the QAN tab in the 3D Viewport sidebar. These are a small native Blender starter set, not a bundle of third-party plugins.


## OZ MAIN AREA × SPORTS ARENA — DEMO v0.2

An integrated Three.js virtual-world scene combining the OZ economy / social main area with a large sports and live-event arena. The scene unifies its procedural 3D geometry, canvas-generated architectural textures and real-time animation: central OZ tower, arena bowl and roof, illuminated district towers, sky bridges, orbital transit rings, moving traffic capsules and animated arena pulse rings.

- [Open OZ 3D WebGL demo](viewer/oz-main-area-sports-arena.html)
- [Design, controls and limitations](docs/oz-main-area-sports-arena.md)
- Controls: left-drag orbit, wheel zoom, right-drag pan, double-click reset; MOTION and LABELS toggles.
- Windows launcher: `QAN-OZ-World.exe` (built by GitHub Actions and included in the latest release after a successful workflow).

Run `python -m http.server 8000` from the repository root and open `http://localhost:8000/viewer/oz-main-area-sports-arena.html`. Three.js and OrbitControls load from jsDelivr, so an internet connection is required. This is a procedural fan-concept scene, not an official or surveyed reconstruction.

## GEO STUDIO — Social Rehabilitation concept

A beginner-friendly concept for connecting 3D regional maps with community learning, SST practice, and access to local support. The social rehabilitation modules are a proposed development direction; they are not a currently certified medical or welfare service.

- [Open the easy Japanese user guide](docs/social-rehabilitation-quickstart.md)
- GEO WORLD: explore public regional maps and community resources.
- VIRTUAL DAYCARE: proposed online group and community activity spaces.
- SST LAB: proposed practice for conversation, problem-solving, and daily-life skills.
- LEARNING / RURAL WORK: proposed IT, 3D, agriculture, and local-learning activities.
- SUPPORT NETWORK: proposed directory and referral links to qualified local services.

The design prioritizes low-bandwidth access, 2D fallback, optional audio/text participation, privacy, consent, and the ability to pause or leave activities. It does not provide diagnosis, treatment, emergency response, or replace in-person professional support. Any real medical or disability-welfare service must be operated by an appropriately licensed/designated provider and meet the applicable staffing, privacy, safety, and reimbursement requirements.
