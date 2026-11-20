"""QAN Geometry: lightweight quad-first geometry primitives."""
from .core import Mesh, cube, grid, linear_guideway, validate_mesh, write_obj, write_json

__all__ = ["Mesh", "cube", "grid", "linear_guideway", "validate_mesh", "write_obj", "write_json"]
__version__ = "0.2.0"
