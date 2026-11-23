"""QAN Geometry: lightweight quad-first geometry primitives."""
from .core import Mesh, cube, grid, linear_guideway, validate_mesh, write_obj, write_json\nfrom .pi import PI, TAU, deg_to_rad, rad_to_deg, polar, ring_points, helix_points, circle_circumference, circle_area

__all__ = ["Mesh", "cube", "grid", "linear_guideway", "validate_mesh", "write_obj", "write_json", "PI", "TAU", "deg_to_rad", "rad_to_deg", "polar", "ring_points", "helix_points", "circle_circumference", "circle_area"]
__version__ = "0.2.0"
