# QAN PI — Tokyo EVA City Observer

## What this project builds

- `viewer/tokyo-eva-city.html`: interactive Three.js WebGL observer with orbit, pan, zoom, night lighting, density control, screenshots, and a conceptual elevated bridge / transit network.
- `scripts/generate_tokyo_eva_gif.py`: creates a 24-frame orbit GIF for the Tokyo concept scene.
- `src/qan_geometry/pi.py`: QAN PI parametric helpers for radians/degrees, polar coordinates, circular rings, helices, circumference, and area.
- `src/qan_geometry_editor/studio_launcher.py`: Windows desktop launcher that starts a local HTTP server and opens either the WebGL Studio or Tokyo EVA City in the default browser.
- GitHub Actions builds `QAN-Geometry-Editor.exe`, `QAN-Geometry-Studio.exe`, and `QAN-Tokyo-EVA-City.gif` and publishes them to the `latest` prerelease.

## Coverage and geometry status

The observer is a lightweight, stylized metropolitan visualization, not a survey-grade digital twin or a complete reconstruction of every Tokyo building.

- The 23 special-ward boundary layer is loaded from an OSM-derived TopoJSON pack (medium simplification).
- Building massing is generated deterministically inside those ward polygons for responsive WebGL viewing; it is not the surveyed PLATEAU building mesh.
- Tama relief and the Izu/Ogasawara island inset are generalized schematic geometry and are not displayed at true regional scale.
- Elevated rings, radial links, ramps, piers, and maglev-like corridors are QAN PI concept infrastructure. They are not existing or approved structures.
- The Tokyo Metropolitan Government's Digital Twin portal is the official reference for the wider 23-ward, Tama, and island 3D model coverage. Its published model list was updated 2026-11-20: https://info.tokyo-digitaltwin.metro.tokyo.lg.jp/3dmodel/

## QAN PI geometry

The Python API uses radians internally and defines `TAU = 2 * PI`. The observer samples circular geometry as `TAU * i / segments`, uses polar coordinates for ring and radial layouts, and uses a helix sampler as a basis for ramps. It does not claim that the circle constant is a new value of pi; it is a reusable parametric geometry convention.

## Data and attribution

- Ward boundary source: https://github.com/hwcharlton/geo-data (OSM-derived, ODbL-1.0).
- Attribution: © OpenStreetMap contributors.
- Official Tokyo model reference: https://info.tokyo-digitaltwin.metro.tokyo.lg.jp/3dmodel/
- The generated GIF is a Produced Work visualizing derived boundary geometry and conceptual city masses. Do not redistribute the underlying OSM-derived boundary database without meeting ODbL terms.

## Run locally

From the repository root:

```bash
python -m pip install .
python -m http.server 8000
```

Open:
- `http://localhost:8000/viewer/editor.html`
- `http://localhost:8000/viewer/tokyo-eva-city.html`

The viewer loads Three.js and TopoJSON from public CDNs, so an internet connection is required. For the GIF:

```bash
python -m pip install Pillow
python scripts/generate_tokyo_eva_gif.py
```

## Desktop applications

- `QAN-Geometry-Editor.exe`: lightweight Tkinter quad-mesh editor (cube, city grid, guideway, OBJ/QAN JSON export).
- `QAN-Geometry-Studio.exe`: launcher for the local WebGL Studio and Tokyo EVA City observer. It opens the user's default browser and hosts the bundled HTML files on localhost.

The Studio executable is a launcher around the WebGL application, not a native Blender replacement. Both applications are Windows x64 preview builds and are not code-signed. The Studio and city observer require internet access for CDN libraries and ward data.
