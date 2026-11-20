import unittest
from qan_geometry import cube, grid, linear_guideway, validate_mesh

class GeometryTests(unittest.TestCase):
    def test_cube_is_closed_quad_manifold(self):
        result = validate_mesh(cube(2))
        self.assertEqual(result["vertices"], 8)
        self.assertEqual(result["quad_faces"], 6)
        self.assertTrue(result["is_closed_manifold"])

    def test_guideway_is_closed_reference_mesh(self):
        result = validate_mesh(linear_guideway(length=100, width=8, segments=4))
        self.assertEqual(result["quad_faces"], 18)
        self.assertTrue(result["is_closed_manifold"])

    def test_city_grid_dimensions(self):
        mesh = grid(width=10000, depth=10000, cells_x=100, cells_y=100)
        self.assertEqual(len(mesh.vertices), 10201)
        self.assertEqual(len(mesh.faces), 10000)
        self.assertEqual(validate_mesh(mesh)["boundary_edges"], 400)

if __name__ == "__main__":
    unittest.main()
