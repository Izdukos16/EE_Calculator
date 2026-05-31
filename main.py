import tkinter as tk
from tkinter import ttk
from gui import tabs            #tab builder functions
from gui.widgets import BG

def main():
    window = tk.Tk()
    window.title("EE Calculator")
    window.geometry("640x480")              #initial size(width x height)
    window.minsize(640, 480)                #minimum resize limit
    window.configure(background="#1e1e1e")  #dark BG color

    style = ttk.Style()         #ttk style controls the appearance of all tkk widgets
    style.theme_use("clam")     #build in theme

    style.configure(
        "TNotebook",        #tab container settings
        background=BG,
        borderwidth=0
    )

    style.configure(
        "TNotebook.Tab",        #individual tab appearance(unselected)
        background="#2b2b2b",
        foreground="white",
        padding=[10, 5],
        borderwidth=0
    )


    style.map(
        "TNotebook.Tab",            #tab appearance changes based on state
        background=[
            ("selected", "#1e1e1e"),    #selected tab matches window bg
            ("active", "#3a3a3a")       #hovered tab is slightly lighter
        ],
        foreground=[
            ("selected", "white")    #selected tab stays white
        ]
    )

    style.configure(
        "TFrame",               #frame bg config
        background="#1e1e1e"
    )

    style.configure(
        "TLabel",           #white text on dark bg
        background=BG,
        foreground="white",
    )

    style.configure(
        "TEntry",
        fieldbackground="#2b2b2b",   #input field bg
        background="#2b2b2b",
        foreground="white",          #typed text color
        insertcolor="white"          #cursor color
    )

    style.configure(
        "TCombobox",                #dropdown appearance
        fieldbackground="#2b2b2b",
        background="#2b2b2b",
        foreground="white",
        arrowcolor="white"
    )

    style.map(
        "TCombobox",
        fieldbackground=[("readonly", "#2b2b2b"), ("focus", "#3a3a3a")],
        foreground=[("readonly", "white"), ("focus", "white")]
    )

    style.layout("TNotebook", [])   #remove all default notebook tab bar layout to allow custom styling

    notebook = ttk.Notebook(window)     #holds all calculator tabs
    notebook.configure(style="TNotebook")
    notebook.pack(fill = "both", expand = True) #makes the notebook resize corectly with the window

    #Each function adds one tab to the notebook
    tabs.build_resistor_tab(notebook)   #Resistor Combinations
    tabs.build_vdiv_tab(notebook)       #Voltage divider
    tabs.build_idiv_tab(notebook)       #Current divider
    tabs.build_ohm_tab(notebook)        #Ohm's Law

    window.mainloop()       #keeps the window open and processes all user events

#Standard Python entry point guard
#Ensures main() only runs when the file is executed directly
if __name__ == "__main__":
    main()