"""
GUI helper functions
"""

import tkinter as tk
from tkinter import ttk

#Constants

BG = "#1e1e1e"
BG_panel = "#2b2b2b"
BG_widget = "#3a3a3a"
BG_result = "#252526"
BG_error  = "#3a1f1f"
FG_text = "#e0e0e0"
FG_result = "#dcdcaa"
FG_error  = "#ff8a80"
FONT = ("Times New Roman", 10)
FONT_bold = ("Times New Roman", 10, "bold")
FONT_sm = ("Times New Roman", 8)

#Helper functions

def labeled_entry(parent, label_text, default="", row=0, col=0):

    ttk.Label(parent, text=label_text).grid(row=row, column=col, sticky=tk.W, padx=8, pady=4)
    entry = ttk.Entry(parent, width=14, font=FONT)
    entry.insert(0, str(default))
    entry.grid(row=row, column=col + 1, sticky=tk.W, padx=8, pady=4)

    return entry

def labeled_combo(parent, labeled_text, options, row=0, col=0):

    ttk.Label(parent, text=labeled_text).grid(row=row, column=col, sticky=tk.W, padx=8, pady=4)
    var = tk.StringVar(value=options[0])
    combo = ttk.Combobox(parent, textvariable=var, values=options, state="readonly", width=18)
    combo.grid(row=row, column=col + 1, sticky=tk.W, pady=4)

    return var

def calc_button(parent, text, command):
    button = tk.Button(parent, text=text, command=command, bg="#2d2d2d", fg="white", font=FONT_bold, relief="flat", bd=0,  padx=12, pady=6,  cursor="hand2", activebackground="#3c3c3c", activeforeground="white")

    return button

def button_row(parent, calc_text, calc_cmd, clear_cmd, row):
    btn_frame = tk.Frame(parent, bg=BG)
    btn_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=10, pady=6)
    btn_frame.columnconfigure(0, weight=1)

    calc_button(btn_frame, calc_text, calc_cmd).grid(row=0, column=0, sticky="ew", padx=(0, 4))
    tk.Button(btn_frame, text="Clear", command=clear_cmd, bg="#2d2d2d", fg="white", font=FONT, relief="flat", bd=0, padx=10, pady=6, cursor="hand2", activebackground="#3c3c3c", activeforeground="white").grid(row=0, column=1)

def result_box(parent):
    frame = tk.Frame(parent, bg=BG, bd=0, highlightthickness=0)
    text = tk.Text(frame, font=FONT, bg="#2b2b2b", fg=FG_result, relief="flat", bd=0,  height=7, padx=10, pady=8, state="disabled", insertbackground="white", highlightthickness=0)
    text.pack(fill="both", expand=True)

    return frame, text

def show_result(text_widget, content, is_error=False):
    text_widget.config(state="normal")
    text_widget.config(
        bg=BG_error if is_error else BG_result,
        fg=FG_error if is_error else FG_result,
    )
    text_widget.delete("1.0", "end")
    text_widget.insert("end", content)
    text_widget.config(state="disabled")

def get_float(entry, name):
    val = entry.get().strip()
    if not val:
        raise ValueError(f"{name} is required")
    try:
        return float(val)
    except ValueError:
        raise ValueError(f"{val} is not a valid number for {name}")

def get_optional_float(entry):
    val = entry.get().strip()
    if not val:
        return None
    try:
        return float(val)
    except ValueError:
        return None

def clear_entries(*entries):
    for entry in entries:
        entry.delete(0, "end")