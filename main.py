import tkinter as tk
from tkinter import ttk
from gui import tabs
from gui.widgets import BG

def main():
    window = tk.Tk()
    window.title("EE Calculator")
    window.geometry("640x480")
    window.minsize(640, 480)
    window.configure(background="#1e1e1e")

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "TNotebook",
        background=BG,
        borderwidth=0
    )

    style.configure(
        "TNotebook.Tab",
        background="#2b2b2b",
        foreground="white",
        padding=[10, 5],
        borderwidth=0
    )

    style.map(
        "TNotebook.Tab",
        background=[
            ("selected", BG),
            ("active", "#3a3a3a")
        ],
        foreground=[
            ("selected", "white"),
            ("active", "white")
        ]
    )

    style.configure(
        "TNotebook.Tab",
        background="#2b2b2b",
        foreground="white",
        padding = [10, 5],
        borderwidth = 0,
        font=("Times New Roman", 10)
    )

    style.map(
        "TNotebook.Tab",
        background=[
            ("selected", "#1e1e1e"),
            ("active", "#3a3a3a")
        ],
        foreground=[
            ("selected", "white")
        ]
    )

    style.configure(
        "TFrame",
        background="#1e1e1e"
    )

    style.configure(
        "TLabel",
        background=BG,
        foreground="white",
    )

    style.configure(
        "TEntry",
        fieldbackground="#2b2b2b",
        background="#2b2b2b",
        foreground="white",
        insertcolor="white"
    )

    style.configure(
        "TCombobox",
        fieldbackground="#2b2b2b",
        background="#2b2b2b",
        foreground="white",
        arrowcolor="white"
    )

    style.configure(
        "TNotebook",
        background=BG,
        borderwidth=0,
        tabmargins=0
    )

    style.map(
        "TCombobox",
        fieldbackground=[("readonly", "#2b2b2b"), ("focus", "#3a3a3a")],
        foreground=[("readonly", "white"), ("focus", "white")]
    )

    style.layout("TNotebook", [])

    notebook = ttk.Notebook(window)
    notebook.configure(style="TNotebook")
    notebook.pack(fill = "both", expand = True)

    tabs.build_resistor_tab(notebook)
    tabs.build_vdiv_tab(notebook)
    tabs.build_idiv_tab(notebook)
    tabs.build_ohm_tab(notebook)

    window.mainloop()

if __name__ == "__main__":
    main()

