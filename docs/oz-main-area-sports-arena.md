# OZ MAIN AREA × SPORTS ARENA — DEMO v0.2

An integrated browser-based 3D concept scene combining the OZ virtual economy's central main area with a large sports/event arena. This is an original fan-concept visualization inspired by the broad virtual-world premise of *Summer Wars*, not a reproduction of film assets or official design data.

## Integrated scene
- **OZ economy core:** stepped central communications/economy tower with luminous crown.
- **Sports arena:** eastern event district with bowl seating shell, tier rings, roof truss and illuminated inner floor.
- **Connected city:** procedural high-rise blocks, sky bridges, pedestrian/transit rings and moving traffic capsules.
- **Unified materials and animation:** canvas-generated façade textures, emissive accents, animated texture offsets, rotating orbital rings, moving traffic, and arena pulse rings are part of the same Three.js scene.
- **Interactive camera:** left-drag orbit, wheel zoom, right-drag pan, double-click reset; on-screen controls toggle motion and district labels.

## Open locally

```bash
python -m http.server 8000
```

Open `http://localhost:8000/viewer/oz-main-area-sports-arena.html`.

The viewer loads Three.js and OrbitControls from jsDelivr, so an internet connection is required. The Windows launcher opens the same bundled page through a local HTTP server.

## Controls

| Input | Action |
|---|---|
| Left mouse drag | Orbit |
| Mouse wheel | Zoom |
| Right mouse drag | Pan |
| Double-click | Reset camera |
| MOTION button | Pause / resume animation |
| LABELS button | Show / hide district labels |

## Scope

This is a stylized, procedural concept model. Building positions, dimensions, arena capacity, transport layout and urban details are illustrative rather than surveyed or engineering-validated. Materials and animation are generated at runtime and are integrated with the 3D scene; no external texture pack is required.

## Release asset

GitHub Actions builds `QAN-OZ-World.exe` for Windows x64 and publishes it with the `latest` preview release when the release workflow succeeds.