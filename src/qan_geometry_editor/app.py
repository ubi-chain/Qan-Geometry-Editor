"""Minimal dependency-free desktop preview for QAN quad meshes (Tkinter)."""
from __future__ import annotations
import tkinter as tk
from tkinter import filedialog, messagebox
from qan_geometry import cube, grid, write_obj, write_json, validate_mesh

class Editor:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("QAN Geometry Editor 0.1.0")
        root.geometry("900x650")
        self.mesh = cube(10)
        bar = tk.Frame(root, padx=8, pady=8); bar.pack(fill="x")
        tk.Button(bar, text="Cube", command=lambda: self.set_mesh(cube(10))).pack(side="left", padx=3)
        tk.Button(bar, text="10 km City Grid", command=lambda: self.set_mesh(grid())).pack(side="left", padx=3)
        tk.Button(bar, text="Export OBJ", command=self.export_obj).pack(side="left", padx=3)
        tk.Button(bar, text="Export QAN JSON", command=self.export_json).pack(side="left", padx=3)
        self.status = tk.StringVar()
        tk.Label(root, textvariable=self.status, anchor="w", padx=10).pack(side="bottom", fill="x")
        self.canvas = tk.Canvas(root, bg="#101923", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _e: self.draw())
        self.draw()

    def set_mesh(self, mesh):
        self.mesh = mesh; self.draw()

    def project(self, v):
        x, y, z = v
        return (x-y)*0.707, (x+y)*0.408-z*0.816

    def draw(self):
        c = self.canvas; c.delete("all")
        w, h = max(c.winfo_width(), 1), max(c.winfo_height(), 1)
        pts = [self.project(v) for v in self.mesh.vertices]
        span = max(max((p[0] for p in pts), default=1)-min((p[0] for p in pts), default=0),
                   max((p[1] for p in pts), default=1)-min((p[1] for p in pts), default=0), 1)
        scale = min(w, h)*0.78/span
        ox = w/2-(max(p[0] for p in pts)+min(p[0] for p in pts))*scale/2
        oy = h/2+(max(p[1] for p in pts)+min(p[1] for p in pts))*scale/2
        for face in self.mesh.faces:
            xy = []
            for idx in face:
                px, py = pts[idx]; xy.extend((ox+px*scale, oy-py*scale))
            c.create_polygon(*xy, fill="#24465c", outline="#74c9df", width=1)
        stats = validate_mesh(self.mesh)
        self.status.set(f"{self.mesh.name} | vertices {stats['vertices']} | quads {stats['quad_faces']} | boundary edges {stats['boundary_edges']} | non-manifold {stats['non_manifold_edges']}")

    def export_obj(self):
        path = filedialog.asksaveasfilename(defaultextension=".obj", filetypes=[("Wavefront OBJ","*.obj")])
        if path:
            write_obj(self.mesh, path); messagebox.showinfo("Export", f"Saved: {path}")

    def export_json(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("QAN Geometry JSON","*.json")])
        if path:
            write_json(self.mesh, path); messagebox.showinfo("Export", f"Saved: {path}")

def main():
    root = tk.Tk(); Editor(root); root.mainloop()

if __name__ == "__main__":
    main()
