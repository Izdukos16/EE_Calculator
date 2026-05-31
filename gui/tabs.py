"""
GUI tabs
one build function per calculator tab
"""

import tkinter as tk
from tkinter import ttk

from tools.calculators import (     #importing the functions from calculators file
    find_combinations, fmt_r,
    vdiv_vout, vdiv_r1, vdiv_r2,
    idiv_currents, idiv_find_r2,
    ohm_solve,
)
from gui.widgets import (       #importing the functions from the widgets file
    BG,
    FONT_sm, clear_entries,
    labeled_entry, labeled_combo,
    button_row,  result_box,
    show_result, get_float, get_optional_float,
)

#TAB 1 -- Resistor Combinations

def build_resistor_tab(notebook):
    """
    Resistor combinations tab
    Finds series or paralel resistor combinations from the E24 standard series
    that are closest to a target resistance value within a given error margin.
    """

    #Create the tab frame and add it to the notebook
    frame = tk.Frame(notebook, bg=BG)
    notebook.configure(style="TNotebook")
    notebook.add(frame, text="Resistor Combinations")
    frame.columnconfigure(1, weight=1)

    #inputs
    e_target = labeled_entry(frame, "Target (Ohms):", default="", row=0, col=0)
    e_maxerr = labeled_entry(frame, "Max accepted error (%):", default="", row=1, col=0)
    v_mode = labeled_combo(frame, "Mode:", ["Series", "Paralel"], row=2, col=0)
    v_count = labeled_combo(frame, "Resistors:", ["2", "3"], row=3, col=0)

    #result box
    res_frame, res_text = result_box(frame)
    res_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=10, pady=6)
    frame.rowconfigure(5, weight=1)
    frame.columnconfigure(0, weight=1)

    def calculate():
        try:
            target = get_float(e_target, "Target")
            maxxerr = get_float(e_maxerr, "Max accepted error")
            mode = v_mode.get().lower() #reading the selected operation mode (series/paralel)
            count = int(v_count.get()) #reading the selected number of resistors

            matches = find_combinations(target, mode, count, maxxerr)

            if not matches:
                show_result(res_text, f"No combinations found whithin +- {maxxerr}% of {fmt_r(target)}.\n", is_error=True)
                return

            sep = " + " if mode == "series" else " || "     #separation characters based on operation mode
            lines = [f"Target: {fmt_r(target)} | {mode} | {count} resistors\n\n"]
            for m in matches:
                combo_str = sep.join(fmt_r(v) for v in m["values"])
                lines.append(
                    f" {combo_str:<32}= {fmt_r(m['result']):<12}"
                    f"{m['error_pct']:+.2f}%\n"
                )
            show_result(res_text, "".join(lines))

        except Exception as e:
            show_result(res_text, f"Error: {e}", is_error=True)

    def clear_res_comb():
        clear_entries(e_target, e_maxerr)   #clear input fields
        show_result(res_text, "")           #clear result box

    button_row(frame, "Find Combinations", calculate, clear_res_comb, row=4)

#TAB 2 -- Voltage divider

def build_vdiv_tab(notebook):
    """
    Voltage divider tab
    Modes of operation:
    -R1, R2 known -> calculate Vout
    -Vout and R1 known -> solve for R2
    -Vout and R2 known -> solve for R1
    Also shows total current and power dissipated in each resistor.
    """

    frame = tk.Frame(notebook, bg=BG)
    notebook.add(frame, text="Voltage Divider")
    frame.columnconfigure(1, weight=1)

    modes = [                   #mode selection fields
        "R1, R2 -> Vout",
        "Vout, R1 -> R2",
        "Vout, R2 -> R1",
    ]

    v_mode = labeled_combo(frame, "Mode:", modes, row=0, col=0)

    #inputs
    e_vin = labeled_entry(frame, "Vin (V):", default="", row=1, col=0)
    e_vout = labeled_entry(frame, "Vout (V):", default="", row=2, col=0)
    e_r1 = labeled_entry(frame, "R1 (Ohms):", default="", row=3, col=0)
    e_r2 = labeled_entry(frame, "R2 (Ohms):", default="", row=4, col=0)

    ttk.Label(frame, text="Leave the unknown field empty.", font=FONT_sm, foreground="#aaaaaa", background=BG).grid(row=5, column=0, sticky="w", padx=10, pady=(0, 4)) #hint label, guides the user

    #result box
    res_frame, res_text = result_box(frame)
    res_frame.grid(row=7, column=0, columnspan=2,  sticky="nsew", padx=10, pady=6)
    frame.rowconfigure(7, weight=1)

    def calculate():
        try:
            mode = v_mode.get()
            vin = get_float(e_vin, "Vin")

            if "R1, R2" in mode:
                r1 = get_float(e_r1, "R1")
                r2 = get_float(e_r2, "R2")
                res = vdiv_vout(vin, r1, r2)

            elif "R1 -> R2" in mode:
                vout = get_float(e_vout, "Vout")
                r1 = get_float(e_r1, "R1")
                res = vdiv_r2(vin, vout, r1)

            else:
                vout = get_float(e_vout, "Vout")
                r2 = get_float(e_r2, "R2")
                res = vdiv_r1(vin, vout, r2)

            show_result(res_text,
                    f"Vin = {res['vin']:.4f} V\n"
                    f"Vout = {res['vout']:.4f} V\n"
                    f"R1 = {fmt_r(res['r1'])}\n"
                    f"R2 = {fmt_r(res['r2'])}\n"
                    f"Current = {res['i_mA']:.3f} mA\n"
                    f"P (R1) = {res['p_r1_mW']:.3f} mW\n"
                    f"P (R2) = {res['p_r2_mW']:.3f} mW\n"
            )

        except Exception as e:
            show_result(res_text, f"Error: {e}", is_error=True)

    def clear_vdiv():
        clear_entries(e_vin, e_vout, e_r1, e_r2)    #clear input fields
        show_result(res_text, "")                   #clear result box

    button_row(frame, "Calculate", calculate, clear_vdiv, row=6)

#TAB 3 -- Current Divider

def build_idiv_tab(notebook):
    """
    Current divider tab
    Modes of operation:
    -R1, R2 known -> calculate branch currents
    -Target I1 and R1 known -> calculate R2
    Also shows paralell resistance and voltage across both resistors.
    """
    frame = tk.Frame(notebook, bg=BG)
    notebook.configure(style="TNotebook")
    notebook.add(frame, text="Current Divider")
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(0, weight=1)

    modes = [                           #mode selection field
        "R1, R2 -> branch currents",
        "Target I1 + R1 -> R2"
    ]

    #inputs
    v_mode = labeled_combo(frame, "Mode:", modes, row=0, col=0)
    e_itot = labeled_entry(frame, "Itot (mA):", default="", row=1, col=0)
    e_r1 = labeled_entry(frame, "R1 (Ohms)", default="", row=2, col=0)
    e_r2 = labeled_entry(frame, "R2 (Ohms):", default="", row=3, col=0)
    e_i1 = labeled_entry(frame, "I1 (mA):", default="", row=4, col=0)

    ttk.Label(frame, text="For mode 2: fill Target I1, leave R2 emplty.", font=FONT_sm, foreground="#aaaaaa", background=BG).grid(row=5, column=0, columnspan=2, sticky="w", padx=10) #hint label

    #result box
    res_frame, res_text = result_box(frame)
    res_frame.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=10, pady=6)
    frame.rowconfigure(7, weight=1)

    def calculate():
        try:
            mode = v_mode.get()
            itot = get_float(e_itot, "Itot")
            r1 = get_float(e_r1, "R1")

            if "R1, R2" in mode:
                r2 = get_float(e_r2, "R2")
                res = idiv_currents(itot, r1, r2)
            else:
                i1t = get_float(e_i1, "Target I1")
                res = idiv_find_r2(itot, i1t, r1)

            show_result(res_text,
                        f"  I1 (R1 branch)  = {res['i1_mA']:.4f} mA\n"
                        f"  I2 (R2 branch)  = {res['i2_mA']:.4f} mA\n"
                        f"  R parallel      = {fmt_r(res['r_paralel'])}\n"
                        f"  Voltage across  = {res['voltage_V']:.4f} V\n"
            )

        except Exception as e:
            show_result(res_text, f"Error: {e}", is_error=True)

    def clear_idiv():
        clear_entries(e_itot, e_r1, e_r2, e_i1)     #clear input fields
        show_result(res_text, "")                   #clear result box

    button_row(frame, "Calculate", calculate, clear_idiv, row=6)

#TAB 4 -- Ohm's Law

def build_ohm_tab(notebook):
    """
    Ohm's Law tab
    Entry any two of the fields and the remaining two are calculated
    """
    frame = tk.Frame(notebook, bg=BG)
    notebook.add(frame, text="Ohm's Law")
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(0, weight=1)

    ttk.Label(frame, text="Enter any two values and leave the rest empty.", font=FONT_sm, foreground="#aaaaaa", background=BG).grid(row=5, column=0, columnspan=2, sticky="w", padx=10) #hint label

    #inputs
    e_v = labeled_entry(frame, "Voltage (V):", default="", row=1, col=0)
    e_i = labeled_entry(frame, "Current (A):", default="", row=2, col=0)
    e_r = labeled_entry(frame, "Resistance (Ohms):", default="", row=3, col=0)
    e_p = labeled_entry(frame, "Power (W):", default="", row=4, col=0)

    res_frame, res_text = result_box(frame)
    res_frame.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=10, pady=6)
    frame.rowconfigure(7, weight=1)

    def calculate():
        try:
            # read all four fields, empty ones return None
            v = get_optional_float(e_v)
            i = get_optional_float(e_i)
            r = get_optional_float(e_r)
            p = get_optional_float(e_p)

            res = ohm_solve(v=v, i=i, r=r, p=p) #function that determines which tow are known and solves the rest

            show_result(res_text,
                        f" V = {res['v']:.5f} V\n"
                        f" I = {res['i'] * 1000:.5f} mA\n"      #convert A to mA
                        f" R = {fmt_r(res['r'])}\n"
                        f" P = {res['p'] * 1000:.5f} mW\n"      #convert W to mW
            )

        except Exception as e:
            show_result(res_text, f"Error: {e}", is_error=True)

    def clear_ohm():
        clear_entries(e_v, e_i, e_r, e_p)       #clear input fields
        show_result(res_text, "")               #clear result box

    button_row(frame, "Solve", calculate, clear_ohm, row=6)