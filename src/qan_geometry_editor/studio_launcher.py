"""QAN Geometry Studio launcher.

Starts a local read-only HTTP server for the bundled WebGL pages and opens
QAN Studio / Tokyo EVA City in the user's default browser.
"""
from __future__ import annotations
import http.server
import socket
import sys
import threading
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import messagebox

def viewer_root() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "viewer"
    return Path(__file__).resolve().parents[2] / "viewer"

def main():
    root = tk.Tk()
    root.title("QAN Geometry Studio")
    root.geometry("440x270")
    root.resizable(False, False)
    root.configure(bg="#151b24")
    base = viewer_root()
    if not (base / "editor.html").exists():
        messagebox.showerror("QAN Studio", f"Viewer files were not found: {base}")
        return

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(base), **kwargs)
        def log_message(self, *_args):
            pass

    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    origin = f"http://127.0.0.1:{port}"

    tk.Label(root, text="QAN GEOMETRY STUDIO", bg="#151b24", fg="#e8f3ff",
             font=("Segoe UI", 16, "bold")).pack(pady=(20, 5))
    tk.Label(root, text="Local WebGL workspace · QAN PI · Tokyo EVA City",
             bg="#151b24", fg="#9fb3c8", font=("Segoe UI", 9)).pack(pady=(0, 18))

    def open_page(path):
        url = f"{origin}/{path}"
        webbrowser.open(url, new=2)

    tk.Button(root, text="Open QAN Geometry Editor Studio", command=lambda: open_page("editor.html"),
              bg="#25445c", fg="white", activebackground="#376987", relief="flat",
              font=("Segoe UI", 10, "bold"), width=36, pady=9).pack(pady=5)
    tk.Button(root, text="Open Tokyo EVA City 3D Observer", command=lambda: open_page("tokyo-eva-city.html"),
              bg="#25445c", fg="white", activebackground="#376987", relief="flat",
              font=("Segoe UI", 10, "bold"), width=36, pady=9).pack(pady=5)
    tk.Label(root, text=f"Local server: {origin}\nInternet is required for Three.js / map data CDN.",
             bg="#151b24", fg="#8da6ba", font=("Segoe UI", 8), justify="center").pack(pady=10)

    def close():
        server.shutdown()
        server.server_close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", close)
    root.mainloop()

if __name__ == "__main__":
    main()
