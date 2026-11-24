"""Standalone launcher for the integrated OZ 3D world demo."""
from __future__ import annotations
import http.server, socket, sys, threading, tkinter as tk, webbrowser
from pathlib import Path
from tkinter import messagebox

def main():
    base = (Path(sys._MEIPASS) / "viewer") if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS") else Path(__file__).resolve().parents[2] / "viewer"
    page = base / "oz-main-area-sports-arena.html"
    if not page.exists():
        root = tk.Tk(); root.withdraw(); messagebox.showerror("OZ World", f"Viewer file not found: {page}"); return
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs): super().__init__(*args, directory=str(base), **kwargs)
        def log_message(self, *_args): pass
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0)); port = probe.getsockname()[1]
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{port}/oz-main-area-sports-arena.html"
    root = tk.Tk(); root.title("OZ Main Area × Sports Arena"); root.geometry("460x210"); root.resizable(False, False); root.configure(bg="#081525")
    tk.Label(root, text="OZ VIRTUAL WORLD", bg="#081525", fg="#dff8ff", font=("Segoe UI", 17, "bold")).pack(pady=(24, 5))
    tk.Label(root, text="MAIN AREA × SPORTS ARENA · DEMO v0.2", bg="#081525", fg="#8fc9df", font=("Segoe UI", 9)).pack(pady=(0, 18))
    def open_world(): webbrowser.open(url, new=2)
    tk.Button(root, text="OPEN 3D WORLD", command=open_world, bg="#14506a", fg="white", relief="flat", font=("Segoe UI", 11, "bold"), padx=28, pady=10).pack()
    tk.Label(root, text="Local viewer server · Internet required for Three.js CDN", bg="#081525", fg="#8da6ba", font=("Segoe UI", 8)).pack(pady=14)
    def close(): server.shutdown(); server.server_close(); root.destroy()
    root.protocol("WM_DELETE_WINDOW", close); root.mainloop()

if __name__ == "__main__": main()