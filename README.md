# QAN Geometry Editor

Free, quad-first 3D geometry editor and lightweight geometry library using QAN PI concepts. The prototype focuses on editable quad meshes, validation summaries, and exportable reference geometry for a fictional 10 km × 10 km Third-City-inspired environment and a conceptual linear/maglev system.

**Version:** 0.2.0 (prototype)  
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
- Browser-based Three.js viewer with animated conceptual maglev train.
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
