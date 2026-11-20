# QAN PI × THIRD CITY × LIGHT MAGLEV — 3D Viewer

A browser-based, interactive Three.js reference scene.

## Open
Open `viewer/index.html` through GitHub Pages or any static web server. The viewer loads Three.js from jsDelivr, so internet access is required.

## Controls
- Left drag: orbit
- Right drag: pan
- Mouse wheel: zoom
- Pause/resume train
- Adjust train speed and city density
- Toggle day/night and reset camera

## Scene
- 10 km × 10 km reference ground plane
- Procedural original sci-fi mountain-city layout
- Instanced low-poly building blocks
- Elevated closed-loop guideway, piers, four station concepts
- Animated light-maglev train following a Catmull-Rom track path
- QAN PI constants (π, τ) used for deterministic angular calculations

## Scope
This is a real-time visual simulation and interactive reference model. It is not a physically validated maglev design, rail alignment, civil engineering model, structural analysis, signalling system, or passenger-operating system. Track radii, clearances, support spacing, vehicle dimensions and speed are illustrative only. Do not use for construction, procurement, safety certification or real-world operation.

## Run locally
From the repository root:
```bash
python -m http.server 8000
```
Then visit `http://localhost:8000/viewer/`.
