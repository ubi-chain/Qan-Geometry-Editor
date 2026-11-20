# QAN Geometry Editor

Free, quad-first 3D geometry editor and lightweight geometry library using QAN PI concepts. The first release focuses on editable quad meshes, validation summaries, and exportable reference geometry for a fictional 10 km × 10 km Third-City-inspired environment and a conceptual linear/maglev system.

**Version:** 0.1.0 (prototype)  
**Code license:** MIT  
**Documentation:** CC BY 4.0  
**Author:** Independent Developer

## First version

- Windows desktop app built with Python's standard Tkinter GUI.
- Pure-Python library package: `qan_geometry`.
- Quad cube and configurable 2D quad terrain grid.
- Basic topology counts: vertices, quad faces, boundary edges, non-manifold edges.
- Export to Wavefront OBJ and QAN Geometry JSON.
- Command-line generator.
- GitHub Actions workflow builds a Windows x64 `.exe` and Python wheel/sdist artifacts.

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

The executable is created at `dist/QAN-Geometry-Editor.exe`. Windows builds must be produced on Windows; the GitHub Actions workflow does this automatically when manually run or when a `v*` tag is pushed. Download the workflow artifact from the Actions run.

## Python library

```python
from qan_geometry import cube, grid, validate_mesh, write_obj

mesh = cube(size=12)
print(validate_mesh(mesh))
write_obj(mesh, "cube.obj")

terrain = grid(width=10_000, depth=10_000, cells_x=100, cells_y=100)
```

## Scope and safety

This is an early geometry prototype, not a complete CAD or railway engineering tool. The 10 km terrain grid is a flat reference surface. No geospatial elevation data, rail dynamics, structural analysis, certified clearance calculations, robust self-intersection detection, or engineering validation are included. Linear/maglev assets and the Third-City-inspired setting are intended as fictional visualization references only.

## Roadmap

- Interactive 3D viewport with orbit/pan/zoom and vertex/face selection.
- GLB/glTF import/export and Blender round-trip tests.
- Quad-first primitives, LOD generation, instancing and spatial chunking.
- QAN PI integration through a validated, versioned data schema.
- Robust topology, intersection and clearance checks with documented limitations.

## License

Source code: MIT (see `LICENSE`). Documentation: CC BY 4.0 (see `docs/LICENSE-DOCS.md`).


## Interactive 3D viewer

A live browser scene with an animated light-maglev train, procedural Third-City-inspired city blocks, elevated guideway, orbit/pan/zoom controls, speed control, density control and day/night toggle.

- [Open viewer source](viewer/index.html)
- [Viewer documentation](docs/third-city-maglev-viewer.md)

To preview locally, run `python -m http.server 8000` from the repository root and open `http://localhost:8000/viewer/`. For a public URL, enable GitHub Pages with the repository root as the publishing source.
