#!/usr/bin/env python3
"""Simple Tkinter launcher that opens the Catchat web UI.

This script will try to use pywebview (if installed) to open an embedded
window. If pywebview is not available, it falls back to opening the URL in
the system default web browser.
"""

from __future__ import annotations

import threading
import webbrowser
import sys

try:
	import tkinter as tk
	from tkinter import messagebox
except Exception:  # pragma: no cover - environment may not have tkinter
	tk = None
	messagebox = None

try:  # pywebview (optional)
	import webview  # type: ignore
	HAS_WEBVIEW = True
except Exception:
	webview = None  # type: ignore
	HAS_WEBVIEW = False

URL = "https://awoo-co.github.io/catchat/"


def open_in_browser() -> None:
	"""Open the Catchat URL in the system default browser."""
	webbrowser.open(URL, new=2)


def open_in_webview() -> None:
	"""Open the Catchat URL in an embedded pywebview window.

	Runs webview in a background thread so the launcher window remains
	responsive. If pywebview isn't available, show an error message.
	"""
	if not HAS_WEBVIEW:
		if messagebox:
			messagebox.showerror(
				"Missing dependency",
				"pywebview is not installed.\nInstall with: pip install pywebview",
			)
		else:
			print("pywebview is not installed. Install with: pip install pywebview", file=sys.stderr)
		return

	def _run() -> None:
		# Create and show the webview window. webview.start() is blocking.
		webview.create_window("Catchat", URL)
		webview.start()

	t = threading.Thread(target=_run, daemon=True)
	t.start()


def main() -> None:
	if tk is None:
		# No tkinter available; fallback to opening the URL in the browser.
		print("Tkinter is not available in this environment. Opening in browser...")
		open_in_browser()
		return

	root = tk.Tk()
	root.title("Catchat")
	root.geometry("420x160")

	frm = tk.Frame(root, padx=12, pady=12)
	frm.pack(expand=True, fill="both")

	lbl = tk.Label(frm, text="Open Catchat web UI", font=(None, 14))
	lbl.pack(pady=(0, 10))

	btn_frame = tk.Frame(frm)
	btn_frame.pack()

	b1 = tk.Button(btn_frame, text="Open in App (embedded)", width=22, command=open_in_webview)
	b1.grid(row=0, column=0, padx=6, pady=6)

	b2 = tk.Button(btn_frame, text="Open in Browser", width=22, command=open_in_browser)
	b2.grid(row=0, column=1, padx=6, pady=6)

	if not HAS_WEBVIEW:
		note = tk.Label(frm, text="Note: For embedded view install 'pywebview' (pip install pywebview)", fg="gray")
		note.pack(pady=(10, 0))

	root.mainloop()


if __name__ == "__main__":
	main()
