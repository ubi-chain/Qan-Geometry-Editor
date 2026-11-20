import tempfile
import unittest
from pathlib import Path

from qan_geometry import cube, grid, linear_guideway, validate_mesh, write_obj, write_json


class GeometryTests(unittest.TestCase):
    def test_cube_is_closed_quad_mesh(self):
        mesh = cube(10)
        stats = validate_mesh(mesh)
        self.assertEqual(stats["vertices"], 8)
        self.assertEqual(stats["quad_faces"], 6)
        self.assertTrue(stats["is_closed_manifold"])

    def test_city_grid_dimensions_and_topology(self):
        mesh = grid(width=10_000, depth=10_000, cells_x=10, cells_y=10)
        stats = validate_mesh(mesh)
        self.assertEqual(stats["vertices"], 121)
        self.assertEqual(stats["quad_faces"], 100)
        self.assertEqual(stats["boundary_edges"], 40)
        self.assertEqual(stats["non_manifold_edges"], 0)

    def test_guideway_is_closed_quad_mesh(self):
        mesh = linear_guideway(length=100, segments=4)
        stats = validate_mesh(mesh)
        self.assertEqual(stats["quad_faces"], 18)
        self.assertTrue(stats["is_closed_manifold"])

    def test_invalid_dimensions_are_rejected(self):
        with self.assertRaises(ValueError):
            cube(0)
        with self.assertRaises(ValueError):
            grid(cells_x=0)

    def test_obj_and_json_export(self):
        mesh = cube(2)
        with tempfile.TemporaryDirectory() as tmp:
            obj_path = Path(tmp) / "cube.obj"
            json_path = Path(tmp) / "cube.json"
            write_obj(mesh, obj_path)
            write_json(mesh, json_path)
            self.assertIn("\nf ", obj_path.read_text(encoding="utf-8"))
            self.assertIn('"schema": "qan-geometry/0.1"', json_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
