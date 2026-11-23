# QAN PI West Japan Neo World

## Scope
A lightweight, fictional near-future 3D world inspired by the geography of Kyushu, Shikoku and the Chugoku region. The viewer uses Three.js WebGL and procedural extruded island silhouettes, instanced city blocks, inter-island elevated maglev corridors, offshore energy structures and PI-based observation geometry.

This is a concept visualization, not a surveyed digital twin. The coastlines are authored schematic shapes; city blocks, transport routes and energy structures are fictional and not real infrastructure.

## Run
From the repository root:
```bash
python -m http.server 8000
```
Open `http://localhost:8000/viewer/west-japan-neo-world.html`. Three.js is loaded from jsDelivr and therefore requires an internet connection.

## Camera and combined keyboard controls
- `G`: Fly / translation mode.
- `R`: camera rotation mode.
- Fly mode: hold `W/S` forward/back, `A/D` strafe, `Q/E` down/up.
- Hold `X`, `Y` or `Z` with a movement key to constrain movement to the selected world axis. These modifiers can be combined with movement keys; holding multiple axis keys enables the selected axes together.
- `Shift`: faster movement. `Ctrl`: precision movement.
- Rotation mode: WASD rotates yaw/pitch; Q/E rolls.
- Numeric keypad: `7` top, `Ctrl+7` bottom, `1` front, `Ctrl+1` back, `3` right, `Ctrl+3` left, `9` opposite oblique, `5` perspective/focal-length toggle.
- Numpad `2/4/6/8`: orbit camera in 15-degree increments.
- Mouse drag orbits, right-drag pans, wheel zooms. Inputs are ignored while typing in a form field.

Axis constraint behaviour: when any of X/Y/Z is held, movement components outside the selected axis set are suppressed. This is a camera navigation system, not an object transform or physics simulator.

## GIF
`python scripts/generate_west_japan_gif.py` creates `dist/QAN-West-Japan-Neo-World.gif` (30 orbit frames). The GIF is a pre-rendered overview; live navigation and camera shortcuts are available in the WebGL viewer.

## Performance
City blocks use instanced meshes. Reduce the browser device-pixel ratio or lower the density slider on slower devices. The viewer is designed as a lightweight regional overview, not a high-detail building dataset.
