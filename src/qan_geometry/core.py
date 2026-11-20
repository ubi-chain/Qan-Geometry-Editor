"""Pure-Python quad mesh primitives. Coordinates are metres unless stated otherwise."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
from typing import Iterable

Vec3 = tuple[float, float, float]
Face = tuple[int, int, int, int]

@dataclass
class Mesh:
    name: str
    vertices: list[Vec3]
    faces: list[Face]

    def to_dict(self) -> dict:
        return {"schema": "qan-geometry/0.1", "name": self.name,
                "vertices": [list(v) for v in self.vertices],
                "faces": [list(f) for f in self.faces]}


def cube(size: float = 1.0, name: str = "Cube", origin: Vec3 = (0, 0, 0)) -> Mesh:
    if size <= 0:
        raise ValueError("size must be greater than zero")
    x, y, z = origin
    h = size / 2
    v = [(x-h,y-h,z-h),(x+h,y-h,z-h),(x+h,y+h,z-h),(x-h,y+h,z-h),
         (x-h,y-h,z+h),(x+h,y-h,z+h),(x+h,y+h,z+h),(x-h,y+h,z+h)]
    f = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    return Mesh(name, v, f)


def grid(width: float = 10000, depth: float = 10000, cells_x: int = 100,
         cells_y: int = 100, name: str = "Third-City Terrain") -> Mesh:
    if width <= 0 or depth <= 0 or cells_x < 1 or cells_y < 1:
        raise ValueError("width/depth and cell counts must be positive")
    vertices = []
    for j in range(cells_y + 1):
        y = -depth / 2 + depth * j / cells_y
        for i in range(cells_x + 1):
            x = -width / 2 + width * i / cells_x
            vertices.append((x, y, 0.0))
    faces = []
    stride = cells_x + 1
    for j in range(cells_y):
        for i in range(cells_x):
            a = j * stride + i
            faces.append((a, a+1, a+1+stride, a+stride))
    return Mesh(name, vertices, faces)


def validate_mesh(mesh: Mesh) -> dict:
    n = len(mesh.vertices)
    invalid = [i for i, f in enumerate(mesh.faces)
               if len(f) != 4 or len(set(f)) != 4 or any(k < 0 or k >= n for k in f)]
    edges: dict[tuple[int, int], int] = {}
    for i, f in enumerate(mesh.faces):
        if i in invalid:
            continue
        for a, b in zip(f, f[1:] + f[:1]):
            e = (min(a,b), max(a,b))
            edges[e] = edges.get(e, 0) + 1
    boundary = sum(v == 1 for v in edges.values())
    non_manifold = sum(v > 2 for v in edges.values())
    return {"vertices": n, "quad_faces": len(mesh.faces),
            "invalid_faces": len(invalid), "boundary_edges": boundary,
            "non_manifold_edges": non_manifold,
            "is_closed_manifold": bool(mesh.faces) and not invalid and boundary == 0 and non_manifold == 0}


def write_obj(mesh: Mesh, path: str | Path) -> None:
    lines = [f"# QAN Geometry Editor 0.1.0", f"o {mesh.name}"]
    lines.extend("v {:.9g} {:.9g} {:.9g}".format(*v) for v in mesh.vertices)
    lines.extend("f " + " ".join(str(i+1) for i in face) for face in mesh.faces)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_json(mesh: Mesh, path: str | Path) -> None:
    Path(path).write_text(json.dumps(mesh.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
