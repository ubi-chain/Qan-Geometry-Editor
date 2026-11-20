# QAN PI and Geometry Reference

**Project:** QAN Geometry Editor  
**Spec revision:** 0.1.0  
**Status:** Consolidated reference; formulas below are mathematical definitions, not all implemented features.

## 1. Design principles

- Prefer quad faces (four vertices per face) for editable base meshes.
- Reuse shared vertices and edges; avoid duplicate or overlapping faces.
- Target manifold topology where a closed solid is intended.
- Reject degenerate faces and invalid vertex indices.
- Check normals, self-intersections, face overlap and clearance as separate validation stages.
- Use metres as the default world unit. Keep units explicit in serialized data.
- Keep generated geometry deterministic from the same parameters.

Recommended QAN geometry intent:

```text
FACE_MODE: QUAD
VERTEX_PER_FACE: 4
TOPOLOGY: MANIFOLD
SELF_INTERSECTION: FALSE
FACE_OVERLAP: FALSE
NORMAL_CHECK: TRUE
CLEARANCE_CHECK: TRUE
DEGENERATE_FACE: REJECT
OUTPUT: MESH
```

The current Python validator checks face indices/quad shape, boundary edges and non-manifold edge counts. It does **not** yet perform robust geometric self-intersection, overlap, normal-orientation or clearance tests.

## 2. QAN PI mathematical reference

Use the following canonical definitions:

| Symbol / function | Definition | Meaning |
|---|---|---|
| `PI`, `pi`, `π` | `Math.PI` | Circle constant |
| `TAU`, `tau`, `τ` | `2 * PI` | Full turn in radians |
| `e` | `Math.E` | Euler's number |
| `π(r)` | `π × r²` | Circle area |
| `π(面積, r)` | `π × r²` | Circle area from radius |
| `π(円周, r)` | `2 × π × r` | Circumference |
| `π(度, d)` | `d × π / 180` | Degrees to radians |
| `π(ラジアン, x)` | `x × 180 / π` | Radians to degrees |

Equivalent helper functions:

```python
import math

PI = math.pi
TAU = 2.0 * math.pi
E = math.e

def deg_to_rad(degrees: float) -> float:
    return degrees * PI / 180.0

def rad_to_deg(radians: float) -> float:
    return radians * 180.0 / PI

def circumference(radius: float) -> float:
    return TAU * radius

def circle_area(radius: float) -> float:
    return PI * radius * radius
```

Validation requirements for implementation:
- Reject negative radii; radius zero may be allowed and should return zero.
- Validate finite numeric inputs (reject NaN and infinity).
- Use radians internally for trigonometric functions.
- Preserve the original input unit in UI labels and export metadata.

## 3. Geometry calculations

### Circle and rotation

[
C = 2\pi r, \qquad A = \pi r^2
]

[
\theta_{rad} = \theta_{deg}\frac{\pi}{180}, \qquad
\theta_{deg} = \theta_{rad}\frac{180}{\pi}
]

2D rotation about an origin:

[
x' = x\cos\theta - y\sin\theta, \qquad
y' = x\sin\theta + y\cos\theta
]

3D rotation should use a documented axis and right-handed coordinate convention. The editor should not silently mix degrees and radians.

### Grid sizing

For a rectangular grid of width (W), depth (D), and cell counts (n_x,n_y):

[
\Delta x = W/n_x, \qquad \Delta y = D/n_y
]

[
V=(n_x+1)(n_y+1), \qquad F=n_xn_y
]

For the 10,000 m × 10,000 m reference terrain with 100 × 100 cells:
- bounds: x and y from -5,000 m to +5,000 m
- spacing: 100 m
- vertices: 10,201
- quad faces: 10,000

## 4. 10 km × 10 km Third-City-inspired reference scene

This is an original fictional city visualization, not a recreation of a copyrighted city or a real-world infrastructure plan.

Recommended layer structure:
1. Terrain base
2. District blocks
3. Buildings (LOD0 / LOD1 / LOD2)
4. Roads and pedestrian paths
5. Linear / maglev guideway and stations
6. Supports, portals and maintenance access (visual reference only)
7. Green buffers and open space
8. Utilities and visual energy infrastructure

Recommended optimization targets:
- Terrain: 100 × 100 quad grid for the base reference.
- Building LOD0: approximately 300–1,500 triangles per detailed asset.
- Building LOD1: approximately 80–300 triangles.
- Building LOD2: approximately 12–80 triangles or an impostor.
- Use instancing for repeated buildings, supports and street furniture.
- Divide large scenes into 250 m or 500 m spatial chunks.
- Keep high-detail collision/engineering geometry separate from visual LOD assets.

These are proposed content budgets, not verified performance guarantees.

## 5. Lightweight linear / maglev reference model

Suggested independent mesh groups:
- vehicle shell
- guideway deck
- supports / piers
- station platform and canopy
- tunnel portal
- visual propulsion housings
- clearance envelope
- maintenance access zone

Keep the vehicle, guideway, supports and stations as separate named objects so each can be edited and instanced independently. The current `linear_guideway` primitive is a simple segmented reference slab only. It is not a train, track system, structural design or certified clearance model.

## 6. Mesh validation pipeline

Recommended order:
1. Validate finite coordinates and index ranges.
2. Validate quad vertex count and reject repeated indices.
3. Detect zero-area / degenerate faces.
4. Build shared-edge adjacency.
5. Check boundary and non-manifold edges.
6. Check consistent winding and face normals.
7. Detect duplicate and coplanar overlapping faces.
8. Detect self-intersections between non-adjacent faces.
9. Run component-specific clearance checks.
10. Round-trip export/import tests (OBJ, GLB/glTF, QAN JSON).

Do not report a mesh as fully valid merely because its edge counts pass. Report each test separately as PASS, FAIL, or NOT_IMPLEMENTED.

## 7. QAN PI integration contract (proposed)

A future geometry request should be data, not executable source code. Suggested JSON shape:

```json
{
  "schema": "qan-geometry/0.2",
  "units": "m",
  "generator": "qan-pi",
  "operation": "grid",
  "parameters": {
    "width": 10000,
    "depth": 10000,
    "cells_x": 100,
    "cells_y": 100
  },
  "constraints": {
    "face_mode": "quad",
    "require_manifold": false,
    "reject_degenerate_faces": true
  },
  "output": {
    "formats": ["obj", "glb", "qan-json"]
  }
}
```

The bridge should validate schema, numeric ranges, operation names and resource limits before generation. Never evaluate arbitrary user-supplied code as a geometry expression. A restricted arithmetic parser is preferred over dynamic code evaluation.

## 8. Implementation status at spec revision 0.1.0

| Feature | Status |
|---|---|
| Quad cube primitive | Implemented |
| 10 km grid primitive | Implemented |
| Segmented guideway reference slab | Implemented |
| OBJ export | Implemented |
| QAN Geometry JSON export | Implemented |
| Basic edge/topology counts | Implemented |
| Robust self-intersection / overlap | Not implemented |
| Normals and clearance validation | Not implemented |
| GLB/glTF import/export | Roadmap |
| Full interactive viewport and object editing | Roadmap |
| QAN PI expression runtime / bridge | Specification only |
| City/building/railway complete asset library | Roadmap |

## 9. Versioning and project update rules

- Product label: **QAN Geometry Editor DEMO**.
- Build identifiers increase automatically for each CI run.
- Semantic versioning is maintained separately in package metadata: MAJOR.MINOR.PATCH.
- Patch: bug fixes and small compatible improvements.
- Minor: backward-compatible features.
- Major: breaking schema or API changes.
- Never label a proposal as implemented until code and tests confirm it.
- Every new formula must include its units, input domain, output meaning, and at least one test.
- Every new feature should add or update tests and this reference where relevant.

## 10. Sources and provenance

This reference consolidates the project's prior design decisions and mathematical discussion. It deliberately separates:
- mathematical identities,
- proposed QAN syntax and data contracts,
- current Python implementation,
- future roadmap items.

When importing future conversation notes, preserve original equations and constraints, record the date, and mark whether each item is implemented, proposed, rejected or needs verification.
