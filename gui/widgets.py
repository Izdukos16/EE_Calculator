"""
GUI helper functions
"""

import tkinter as tk
from tkinter import ttk

#Color Constants

BG = "#1e1e1e"
BG_panel = "#2b2b2b"
BG_widget = "#3a3a3a"   #widget bg (buttons, inputs)
BG_result = "#252526"   #result box bg
BG_error  = "#3a1f1f"   #result box when showing an error
FG_text = "#e0e0e0"     #general text color
FG_result = "#dcdcaa"   #result text color
FG_error  = "#ff8a80"   #error text color

#Font Constants
FONT = ("Times New Roman", 10)                  #standard font
FONT_bold = ("Times New Roman", 10, "bold")     #bold version
FONT_sm = ("Times New Roman", 8)                #smaller version

#Helper functions

def labeled_entry(parent, label_text, default="", row=0, col=0):
    """

    :param parent: the parent frame to place the label
    :param label_text: text to display
    :param default: pre-filled value in the entry field
    :param row: grid row to place the label
    :param col: grid column to place the label
    :return: entry widget so the tab can rad it's value

    """

    ttk.Label(parent, text=label_text).grid(row=row, column=col, sticky=tk.W, padx=8, pady=4)
    entry = ttk.Entry(parent, width=14, font=FONT)
    entry.insert(0, str(default))
    entry.grid(row=row, column=col + 1, sticky=tk.W, padx=8, pady=4)

    return entry

def labeled_combo(parent, labeled_text, options, row=0, col=0):
    """

    :param parent: the parent frame to place the label
    :param labeled_text: text to display
    :param options: list of options to display
    :param row: grid row to place the label
    :param col: grid column to place the label
    :return: StringVar linked to combox, call var.get() to read selection

    """

    ttk.Label(parent, text=labeled_text).grid(row=row, column=col, sticky=tk.W, padx=8, pady=4)
    var = tk.StringVar(value=options[0])
    combo = ttk.Combobox(parent, textvariable=var, values=options, state="readonly", width=18)
    combo.grid(row=row, column=col + 1, sticky=tk.W, pady=4)

    return var

def calc_button(parent, text, command):
    """

    :param parent: the parent frame to place the button
    :param text:  text to display
    :param command: function to call when the button is clicked
    :return: button widget is returned, must be positioned by the caller [(.grid() or .pack()]

    """
    button = tk.Button(parent, text=text, command=command, bg="#2d2d2d", fg="white", font=FONT_bold, relief="flat", bd=0,  padx=12, pady=6,  cursor="hand2", activebackground="#3c3c3c", activeforeground="white")

    return button

def button_row(parent, calc_text, calc_cmd, clear_cmd, row):
    """

    :param parent: the parent frame to place the button
    :param calc_text: label for the "Calc" button
    :param calc_cmd: function called when the "Calc" button is clicked
    :param clear_cmd: function called when the "Clear" button is clicked
    :param row: grid row in the parent frame to place the button row

    """
    btn_frame = tk.Frame(parent, bg=BG)
    btn_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=10, pady=6)
    btn_frame.columnconfigure(0, weight=1)

    calc_button(btn_frame, calc_text, calc_cmd).grid(row=0, column=0, sticky="ew", padx=(0, 4))
    tk.Button(btn_frame, text="Clear", command=clear_cmd, bg="#2d2d2d", fg="white", font=FONT, relief="flat", bd=0, padx=10, pady=6, cursor="hand2", activebackground="#3c3c3c", activeforeground="white").grid(row=0, column=1)

def result_box(parent):
    """

    :param parent: the parent frame to place the result box
    :return: the container frame (caller must position it) and the text widget (pass this to show_result() to display output)

    """
    frame = tk.Frame(parent, bg=BG, bd=0, highlightthickness=0)
    text = tk.Text(frame, font=FONT, bg="#2b2b2b", fg=FG_result, relief="flat", bd=0,  height=7, padx=10, pady=8, state="disabled", insertbackground="white", highlightthickness=0)
    text.pack(fill="both", expand=True)

    return frame, text

def show_result(text_widget, content, is_error=False):
    """

    :param text_widget: the text widget returned by result_box
    :param content: text to display
    :param is_error: if True, displays content in the error style defined at the top

    """
    text_widget.config(state="normal")
    text_widget.config(
        bg=BG_error if is_error else BG_result,
        fg=FG_error if is_error else FG_result,
    )
    text_widget.delete("1.0", "end")
    text_widget.insert("end", content)
    text_widget.config(state="disabled")

def get_float(entry, name):
    """

    :param entry: the entry widget to read from
    :param name: field name used in the error message
    :return: float value from the entry widget

    """
    val = entry.get().strip()
    if not val:
        raise ValueError(f"{name} is required")
    try:
        return float(val)
    except ValueError:
        raise ValueError(f"{val} is not a valid number for {name}")

def get_optional_float(entry):
    """
    Safely read an optional float value from the entry widget.
    Used in Ohm's Law tab where the user intentionally leaves empty fields.

    :param entry: the entry widget to read from
    :return: float value or none if empty/invalid

    """
    val = entry.get().strip()
    if not val:
        return None
    try:
        return float(val)
    except ValueError:
        return None

def clear_entries(*entries):
    """
    Clear any number of Entry widgets.
    Uses *entries so it will work for any number of fields.

    :param entries: one or more Entry widgets to clear

    """
    for entry in entries:
        entry.delete(0, "end")