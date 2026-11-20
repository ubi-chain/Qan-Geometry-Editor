# QAN Geometry Editor — Blender and Prompt Workflow

## Blender add-on

Install blender/qan_geometry_addon.py:
1. Open Blender → Edit → Preferences → Add-ons → Install from Disk.
2. Select qan_geometry_addon.py and enable **QAN Geometry Tools**.
3. In the 3D Viewport press N and open the **QAN** tab.

### Supported operations
- Import qan-geometry/0.1 and qan-geometry/0.2 quad-mesh JSON.
- Export the active Blender mesh to QAN JSON.
- Export keeps quad polygons. Non-quad polygons are skipped and counted in the operator report; they are not silently converted.
- Prompt-to-mesh creates a supported primitive or parametric quad surface without executing Python, expressions, shell commands, or arbitrary code.

Blender units are scene units. The add-on does not assign a real-world unit scale automatically.

## Prompt feature

The prompt parser is deliberately constrained and deterministic. It recognizes a small vocabulary and numeric parameters; it is not an LLM and does not interpret arbitrary natural language.

Examples:
- 10m cube or size=25 cube
- 10km city grid 40x40
- width=10000 depth=10000 cells_x=80 cells_y=80 terrain
- 1km maglev guideway segments=30
- length=2500 rail_width=12 segments=50 linear guideway

Supported concepts:
- Cube: cube, 立方体, キューブ; parameter size / 辺 / 一辺.
- Quad terrain: grid, terrain, city, 地形, 都市, グリッド, 地面; parameters width, depth, cells_x, cells_y.
- Guideway slab: maglev, guideway, linear, リニア, 線路, 軌道; parameters length, rail_width, segments.

The parser uses safe regular expressions and fixed geometry constructors. Do not paste secrets or expect unsupported requests (for example, "build a complete realistic city") to be inferred; use concise parameter prompts.

## QAN JSON schema

qan-geometry/0.2 retains name, vertices, and faces from 0.1. Each face must contain exactly four distinct valid vertex indices. Coordinates are stored in Blender scene units. Optional metadata may describe source and units.

## Limitations

- This is a Blender interoperability add-on and constrained prompt generator, not a full Blender replacement or AI model.
- Materials, modifiers, armatures, animation, UVs, and node graphs are not serialized in QAN JSON.
- Export only includes quad faces from the active mesh object. Non-quads are skipped and reported.
- No engineering validation, collision clearance, rail dynamics, or structural certification is provided.
- Compatibility target is Blender 3.6+; validate in the target Blender release before production use.
