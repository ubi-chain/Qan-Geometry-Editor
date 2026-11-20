"""Command-line entry point."""
import argparse
from .core import cube, grid, validate_mesh, write_obj, write_json

def main() -> None:
    p = argparse.ArgumentParser(description="Generate lightweight QAN quad meshes.")
    p.add_argument("--shape", choices=["cube", "city-grid"], default="cube")
    p.add_argument("--size", type=float, default=10.0)
    p.add_argument("--output", default="qan-model.obj")
    p.add_argument("--format", choices=["obj", "json"], default="obj")
    args = p.parse_args()
    mesh = cube(args.size) if args.shape == "cube" else grid()
    (write_obj if args.format == "obj" else write_json)(mesh, args.output)
    print(validate_mesh(mesh))
    print(f"Wrote {args.output}")

if __name__ == "__main__":
    main()
