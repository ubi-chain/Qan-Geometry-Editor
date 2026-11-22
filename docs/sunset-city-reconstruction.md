# Sunset City — QAN PI procedural 3D reconstruction

This viewer is a people-free, procedural 3D interpretation of the user-provided sunset city wallpaper.

## Open
Serve the repository root over HTTP, then open:
`http://localhost:8000/viewer/wallpaper-3d.html`

The page uses Three.js 0.160.0 from jsDelivr CDN. Internet access is required for the module imports.

## Scene interpretation
- Sunset gradient sky, sun disc and distant ridgelines.
- Polygonal conical mountain with a separate snow cap.
- Dense, deterministic procedural city blocks and lit-window texture.
- Signature twin towers and four slim industrial towers.
- Empty observation terrace with railings; no people or human meshes are generated.
- QAN PI / τ drive angular sampling, radial city arrangement and camera orbit.

## Controls
- Drag: orbit the camera around the scene (full 360° azimuth).
- Wheel: zoom.
- Right-drag: pan.
- Buttons: reset view, automatic slow orbit, wireframe, sunset/daylight.
- Sliders: orbit speed and city density.

## Reconstruction caveat
The input is a single 2D image. Geometry on hidden sides, exact depth, building footprints and mountain profile cannot be recovered uniquely. This is a stylized, dimensionless scene reconstruction, not a photogrammetric model. No source-image pixels are used as a background texture, which keeps the pictured people out of the 3D scene. The geometry is a visual reference only, not a survey or engineering model.
