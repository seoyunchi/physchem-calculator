import tkinter as tk
import math

# ================= STYLE SETTINGS =================
# Change these values to restyle the app. Colors are hex codes.
BG = "#FFF8E7"          # window background: warm paper
CARD = "#FFFFFF"        # input area background
FG = "#4A3F35"          # main text color
ACCENT = "#E8A87C"      # button color
ACCENT_FG = "#FFFFFF"   # button text color
TITLE_FONT = ("Helvetica", 16, "bold")
LABEL_FONT = ("Helvetica", 11)
ENTRY_FONT = ("Helvetica", 11)
RESULT_FONT = ("Helvetica", 12, "bold")
HINT_FONT = ("Helvetica", 10, "italic")

R = 8.314  # J / (mol K)

# ================= CALCULATIONS =================

def calc_ideal_gas(v):
    p, V, n, T = v["p"], v["V"], v["n"], v["T"]
    known = [x for x in (p, V, n, T) if x is not None]
    if len(known) != 3:
        return "Fill in exactly 3 boxes, leave 1 empty."
    if p is None:
        return "p = %.2f kPa" % (n * R * T / V)
    if V is None:
        return "V = %.4f L" % (n * R * T / p)
    if n is None:
        return "n = %.4f mol" % (p * V / (R * T))
    return "T = %.2f K" % (p * V / (n * R))

def calc_delta_g(v):
    dH, dS, T = v["dH"], v["dS"], v["T"]
    if None in (dH, dS, T):
        return "Please fill in all 3 boxes."
    dG = dH - T * dS / 1000.0
    if dG < -0.01:
        verdict = "Spontaneous (dG < 0)"
    elif dG > 0.01:
        verdict = "Non-spontaneous (dG > 0)"
    else:
        verdict = "At equilibrium (dG = 0)"
    return "dG = %.2f kJ/mol\n%s" % (dG, verdict)

def calc_clapeyron(v):
    p1, T1, dH, T2 = v["p1"], v["T1"], v["dH"], v["T2"]
    if None in (p1, T1, dH, T2):
        return "Please fill in all 4 boxes."
    p2 = p1 * math.exp(-dH * 1000.0 / R * (1.0 / T2 - 1.0 / T1))
    return "p2 = %.2f kPa" % p2

def calc_molar_mass(v):
    dTf, Kf, w, W = v["dTf"], v["Kf"], v["w"], v["W"]
    if None in (dTf, Kf, w, W):
        return "Please fill in all 4 boxes."
    if dTf == 0 or W == 0:
        return "dTf and solvent mass cannot be 0."
    M = Kf * w * 1000.0 / (dTf * W)
    return "M = %.2f g/mol" % M

# ================= FORMULA LIST =================

TOOLS = [
    {
        "name": "1. Ideal Gas   pV = nRT",
        "hint": "Units: p in kPa, V in L, n in mol, T in K. Leave ONE box empty, the app solves for it.",
        "fields": [
            ("Pressure p (kPa)", "p", ""),
            ("Volume V (L)", "V", ""),
            ("Amount n (mol)", "n", ""),
            ("Temperature T (K)", "T", ""),
        ],
        "calc": calc_ideal_gas,
    },
    {
        "name": "2. Gibbs Energy   dG = dH - T dS",
        "hint": "Units: dH in kJ/mol, dS in J/(mol K), T in K. dG < 0 means spontaneous.",
        "fields": [
            ("Enthalpy dH (kJ/mol)", "dH", ""),
            ("Entropy dS (J/mol K)", "dS", ""),
            ("Temperature T (K)", "T", ""),
        ],
        "calc": calc_delta_g,
    },
    {
        "name": "3. Vapor Pressure   Clausius-Clapeyron",
        "hint": "Ethanol: dHvap = 43.41 kJ/mol (your lab value). Finds vapor pressure p2 at T2.",
        "fields": [
            ("Pressure p1 (kPa)", "p1", "101.3"),
            ("Temperature T1 (K)", "T1", "351.5"),
            ("dHvap (kJ/mol)", "dH", "43.41"),
            ("Temperature T2 (K)", "T2", ""),
        ],
        "calc": calc_clapeyron,
    },
    {
        "name": "4. Molar Mass from Freezing Point",
        "hint": "Kf of water = 1.86 K kg/mol. dTf = freezing point depression. Finds molar mass M.",
        "fields": [
            ("dTf (K)", "dTf", ""),
            ("Kf (K kg/mol)", "Kf", "1.86"),
            ("Solute mass w (g)", "w", ""),
            ("Solvent mass W (g)", "W", ""),
        ],
        "calc": calc_molar_mass,
    },
]

# ================= WINDOW =================

window = tk.Tk()
window.title("PhysChem Calculator")
window.geometry("540x580")
window.configure(bg=BG)

# STICKER (optional decoration):
# 1. Save a small PNG image as sticker.png in the same folder as this file.
# 2. Uncomment the two lines below to show it at the top of the window.
# sticker_img = tk.PhotoImage(file="sticker.png")
# tk.Label(window, image=sticker_img, bg=BG).pack(pady=5)
# NOTE: keep the sticker_img variable, or the image will disappear.

title = tk.Label(window, text="PhysChem Calculator", font=TITLE_FONT, bg=BG, fg=FG)
title.pack(pady=(14, 2))
sub = tk.Label(window, text="Physical Chemistry A1  |  Chapters 1-4", font=HINT_FONT, bg=BG, fg=FG)
sub.pack(pady=(0, 8))

entries = {}

def build_fields(tool):
    for w in card.winfo_children():
        w.destroy()
    entries.clear()
    for label_text, key, default in tool["fields"]:
        row = tk.Frame(card, bg=CARD)
        row.pack(fill="x", pady=4)
        tk.Label(row, text=label_text, font=LABEL_FONT, bg=CARD, fg=FG, width=24, anchor="w").pack(side="left")
        e = tk.Entry(row, font=ENTRY_FONT, width=16)
        e.pack(side="left")
        if default:
            e.insert(0, default)
        entries[key] = e

def current_tool():
    return next(t for t in TOOLS if t["name"] == tool_var.get())

def on_tool_change(name):
    build_fields(current_tool())
    hint_label.configure(text=current_tool()["hint"])
    result_label.configure(text="")

def read_entries():
    vals = {}
    for key, e in entries.items():
        s = e.get().strip()
        if s == "":
            vals[key] = None
        else:
            try:
                vals[key] = float(s)
            except ValueError:
                return None
    return vals

def on_calculate():
    vals = read_entries()
    if vals is None:
        result_label.configure(text="Please enter numbers only.")
        return
    try:
        result_label.configure(text=current_tool()["calc"](vals))
    except Exception as ex:
        result_label.configure(text="Error: " + str(ex))

def on_clear():
    for e in entries.values():
        e.delete(0, tk.END)
    result_label.configure(text="")

picker_frame = tk.Frame(window, bg=BG)
picker_frame.pack(pady=5)
tk.Label(picker_frame, text="Formula:", font=LABEL_FONT, bg=BG, fg=FG).pack(side="left", padx=5)
tool_var = tk.StringVar(window)
tool_var.set(TOOLS[0]["name"])
menu = tk.OptionMenu(picker_frame, tool_var, *[t["name"] for t in TOOLS], command=on_tool_change)
menu.configure(font=LABEL_FONT, bg=CARD, fg=FG)
menu.pack(side="left")

card = tk.Frame(window, bg=CARD, padx=16, pady=12)
card.pack(padx=16, pady=10, fill="x")

hint_label = tk.Label(window, text="", font=HINT_FONT, bg=BG, fg=FG, wraplength=470, justify="left")
hint_label.pack(padx=16, pady=4)

btn_frame = tk.Frame(window, bg=BG)
btn_frame.pack(pady=8)
calc_btn = tk.Button(btn_frame, text="Calculate", font=LABEL_FONT, bg=ACCENT, fg=ACCENT_FG, padx=18, pady=6, command=on_calculate)
calc_btn.pack(side="left", padx=6)
clear_btn = tk.Button(btn_frame, text="Clear", font=LABEL_FONT, bg=CARD, fg=FG, padx=18, pady=6, command=on_clear)
clear_btn.pack(side="left", padx=6)

result_label = tk.Label(window, text="", font=RESULT_FONT, bg=BG, fg=FG, wraplength=470, justify="left")
result_label.pack(pady=10, padx=16)

foot = tk.Label(window, text="Tip: close the window to stop. Run again with: python3 physchem.py", font=HINT_FONT, bg=BG, fg=FG)
foot.pack(side="bottom", pady=8)

build_fields(TOOLS[0])
hint_label.configure(text=TOOLS[0]["hint"])
window.mainloop()
