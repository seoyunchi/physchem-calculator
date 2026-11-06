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
MONO_FONT = ("Courier", 11)

R = 8.314  # J / (mol K)

def fmt(x):
    return "%.6g" % x

# ================= CALCULATIONS (with steps) =================

def calc_ideal_gas(v):
    p, V, n, T = v["p"], v["V"], v["n"], v["T"]
    known = [x for x in (p, V, n, T) if x is not None]
    if len(known) != 3:
        return "Fill in exactly 3 boxes, leave 1 empty."
    if p is None:
        ans = n * R * T / V
        return "p = nRT / V\n  = %s x %s x %s / %s\n  = %.2f kPa" % (fmt(n), fmt(R), fmt(T), fmt(V), ans)
    if V is None:
        ans = n * R * T / p
        return "V = nRT / p\n  = %s x %s x %s / %s\n  = %.4f L" % (fmt(n), fmt(R), fmt(T), fmt(p), ans)
    if n is None:
        ans = p * V / (R * T)
        return "n = pV / RT\n  = %s x %s / (%s x %s)\n  = %.4f mol" % (fmt(p), fmt(V), fmt(R), fmt(T), ans)
    ans = p * V / (n * R)
    return "T = pV / nR\n  = %s x %s / (%s x %s)\n  = %.2f K" % (fmt(p), fmt(V), fmt(n), fmt(R), ans)

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
    return ("dG = dH - T dS\n"
            "  = %s - %s x %s / 1000\n"
            "  = %.2f kJ/mol\n%s" % (fmt(dH), fmt(T), fmt(dS), dG, verdict))

def calc_clapeyron(v):
    p1, T1, dH, T2 = v["p1"], v["T1"], v["dH"], v["T2"]
    if None in (p1, T1, dH, T2):
        return "Please fill in all 4 boxes."
    lnr = -dH * 1000.0 / R * (1.0 / T2 - 1.0 / T1)
    p2 = p1 * math.exp(lnr)
    return ("ln(p2/p1) = -dHvap / R x (1/T2 - 1/T1)\n"
            "  = -%s / %s x (1/%s - 1/%s)\n"
            "  = %.4f\n"
            "p2 = p1 x e^(%.4f)\n"
            "  = %.2f kPa" % (fmt(dH * 1000.0), fmt(R), fmt(T2), fmt(T1), lnr, lnr, p2))

def calc_molar_mass(v):
    dTf, Kf, w, W = v["dTf"], v["Kf"], v["w"], v["W"]
    if None in (dTf, Kf, w, W):
        return "Please fill in all 4 boxes."
    if dTf == 0 or W == 0:
        return "dTf and solvent mass cannot be 0."
    M = Kf * w * 1000.0 / (dTf * W)
    return ("M = Kf x w x 1000 / (dTf x W)\n"
            "  = %s x %s x 1000 / (%s x %s)\n"
            "  = %.2f g/mol" % (fmt(Kf), fmt(w), fmt(dTf), fmt(W), M))

# ================= UNIT CONVERTER =================

CONVERT = {
    "Pressure": ({"Pa": 1.0, "kPa": 1000.0, "atm": 101325.0, "mmHg": 133.322, "bar": 100000.0}, "Pa"),
    "Volume": ({"L": 1.0, "mL": 0.001, "m^3": 1000.0, "cm^3": 0.001}, "L"),
    "Energy": ({"J": 1.0, "kJ": 1000.0, "cal": 4.184, "kcal": 4184.0, "L atm": 101.325, "eV": 1.602e-19}, "J"),
}
TEMP_UNITS = ["K", "degC", "degF"]
CATEGORIES = ["Pressure", "Volume", "Energy", "Temperature"]

def to_kelvin(value, unit):
    if unit == "K":
        return value
    if unit == "degC":
        return value + 273.15
    return (value - 32.0) * 5.0 / 9.0 + 273.15

def from_kelvin(k, unit):
    if unit == "K":
        return k
    if unit == "degC":
        return k - 273.15
    return (k - 273.15) * 9.0 / 5.0 + 32.0

def do_convert(category, value, u_from, u_to):
    if category == "Temperature":
        k = to_kelvin(value, u_from)
        ans = from_kelvin(k, u_to)
        return "%s %s = %s K\n  = %s %s" % (fmt(value), u_from, fmt(k), fmt(ans), u_to)
    table, base = CONVERT[category]
    base_value = value * table[u_from]
    ans = base_value / table[u_to]
    return ("%s %s\n"
            "  = %s x %s %s\n"
            "  = %s %s\n"
            "  = %s / %s %s\n"
            "  = %s %s" % (fmt(value), u_from, fmt(value), fmt(table[u_from]), base,
                           fmt(base_value), base, fmt(base_value), fmt(table[u_to]), u_to,
                           fmt(ans), u_to))

# ================= COMMON TABLES =================

TABLES = {
    "Gas constant R": (
        "R = 8.314 J / (mol K)\n"
        "  = 0.08206 L atm / (mol K)\n"
        "  = 1.987 cal / (mol K)\n"
        "  = 8.314e-3 kJ / (mol K)"),
    "Water constants": (
        "Kb (water) = 0.51 K kg / mol\n"
        "Kf (water) = 1.86 K kg / mol\n"
        "dHvap (water, 100 C) = 40.65 kJ / mol\n"
        "Normal boiling point = 373.15 K\n"
        "Normal freezing point = 273.15 K"),
    "dHvap of common liquids": (
        "Liquid      dHvap (kJ/mol)\n"
        "Water       40.65\n"
        "Ethanol     43.41  (your lab value)\n"
        "Benzene     30.72\n"
        "Acetone     29.10\n"
        "Methanol    35.21\n"
        "CCl4        29.80"),
    "Unit relations": (
        "1 atm = 101.325 kPa = 760 mmHg\n"
        "1 bar = 100 kPa\n"
        "1 L atm = 101.325 J\n"
        "1 cal = 4.184 J\n"
        "0 C = 273.15 K\n"
        "1 m^3 = 1000 L"),
}

# ================= TOOL LIST =================

TOOLS = [
    {
        "name": "1. Ideal Gas   pV = nRT",
        "kind": "calc",
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
        "kind": "calc",
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
        "kind": "calc",
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
        "kind": "calc",
        "hint": "Kf of water = 1.86 K kg/mol. dTf = freezing point depression. Finds molar mass M.",
        "fields": [
            ("dTf (K)", "dTf", ""),
            ("Kf (K kg/mol)", "Kf", "1.86"),
            ("Solute mass w (g)", "w", ""),
            ("Solvent mass W (g)", "W", ""),
        ],
        "calc": calc_molar_mass,
    },
    {
        "name": "5. Unit Converter",
        "kind": "converter",
        "hint": "Pick a category, enter a value, convert between units.",
    },
    {
        "name": "6. Common Tables",
        "kind": "tables",
        "hint": "Pick a table to view.",
    },
]

# ================= WINDOW =================

window = tk.Tk()
window.title("PhysChem Calculator v2")
window.geometry("560x700")
window.configure(bg=BG)

# STICKER (optional decoration, for the later shell design):
# 1. Save a small PNG image as sticker.png in the same folder as this file.
# 2. Uncomment the two lines below to show it at the top of the window.
# sticker_img = tk.PhotoImage(file="sticker.png")
# tk.Label(window, image=sticker_img, bg=BG).pack(pady=5)
# NOTE: keep the sticker_img variable, or the image will disappear.

title = tk.Label(window, text="PhysChem Calculator", font=TITLE_FONT, bg=BG, fg=FG)
title.pack(pady=(14, 2))
sub = tk.Label(window, text="Physical Chemistry A1  |  Chapters 1-4  |  v2", font=HINT_FONT, bg=BG, fg=FG)
sub.pack(pady=(0, 8))

entries = {}
conv = {}
table_widgets = {}

def build_fields(tool):
    for w in card.winfo_children():
        w.destroy()
    entries.clear()
    conv.clear()
    kind = tool.get("kind", "calc")
    if kind == "calc":
        for label_text, key, default in tool["fields"]:
            row = tk.Frame(card, bg=CARD)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=label_text, font=LABEL_FONT, bg=CARD, fg=FG, width=24, anchor="w").pack(side="left")
            e = tk.Entry(row, font=ENTRY_FONT, width=16)
            e.pack(side="left")
            if default:
                e.insert(0, default)
            entries[key] = e
    elif kind == "converter":
        build_converter()
    elif kind == "tables":
        build_tables()

def build_converter():
    conv["cat_var"] = tk.StringVar(card)
    conv["cat_var"].set("Pressure")
    r1 = tk.Frame(card, bg=CARD)
    r1.pack(fill="x", pady=4)
    tk.Label(r1, text="Category:", font=LABEL_FONT, bg=CARD, fg=FG, width=24, anchor="w").pack(side="left")
    tk.OptionMenu(r1, conv["cat_var"], *CATEGORIES, command=on_cat_change).pack(side="left")
    conv["unit_frame"] = tk.Frame(card, bg=CARD)
    conv["unit_frame"].pack(fill="x", pady=4)
    r2 = tk.Frame(card, bg=CARD)
    r2.pack(fill="x", pady=4)
    tk.Label(r2, text="Value:", font=LABEL_FONT, bg=CARD, fg=FG, width=24, anchor="w").pack(side="left")
    conv["val_entry"] = tk.Entry(r2, font=ENTRY_FONT, width=16)
    conv["val_entry"].pack(side="left")
    build_unit_menus()

def build_unit_menus():
    f = conv["unit_frame"]
    for w in f.winfo_children():
        w.destroy()
    cat = conv["cat_var"].get()
    if cat == "Temperature":
        units = TEMP_UNITS
    else:
        units = list(CONVERT[cat][0].keys())
    conv["from_var"] = tk.StringVar(f)
    conv["from_var"].set(units[0])
    conv["to_var"] = tk.StringVar(f)
    conv["to_var"].set(units[1])
    tk.Label(f, text="From:", font=LABEL_FONT, bg=CARD, fg=FG).pack(side="left")
    tk.OptionMenu(f, conv["from_var"], *units).pack(side="left")
    tk.Label(f, text="  ->  ", font=LABEL_FONT, bg=CARD, fg=FG).pack(side="left")
    tk.Label(f, text="To:", font=LABEL_FONT, bg=CARD, fg=FG).pack(side="left")
    tk.OptionMenu(f, conv["to_var"], *units).pack(side="left")

def on_cat_change(name):
    build_unit_menus()
    result_label.configure(text="")

def build_tables():
    table_widgets["var"] = tk.StringVar(card)
    table_widgets["var"].set("Gas constant R")
    r = tk.Frame(card, bg=CARD)
    r.pack(fill="x", pady=4)
    tk.Label(r, text="Table:", font=LABEL_FONT, bg=CARD, fg=FG, width=24, anchor="w").pack(side="left")
    tk.OptionMenu(r, table_widgets["var"], *list(TABLES.keys()), command=on_table_change).pack(side="left")
    t = tk.Text(card, font=MONO_FONT, width=52, height=10, bg=CARD, fg=FG, relief="flat")
    t.pack(pady=6)
    t.insert("1.0", TABLES["Gas constant R"])
    t.configure(state="disabled")
    table_widgets["text"] = t

def on_table_change(name):
    t = table_widgets["text"]
    t.configure(state="normal")
    t.delete("1.0", tk.END)
    t.insert("1.0", TABLES[name])
    t.configure(state="disabled")
    result_label.configure(text="")

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
    tool = current_tool()
    kind = tool.get("kind", "calc")
    if kind == "calc":
        vals = read_entries()
        if vals is None:
            result_label.configure(text="Please enter numbers only.")
            return
        try:
            result_label.configure(text=tool["calc"](vals))
        except Exception as ex:
            result_label.configure(text="Error: " + str(ex))
    elif kind == "converter":
        s = conv["val_entry"].get().strip()
        try:
            value = float(s)
        except ValueError:
            result_label.configure(text="Please enter a number.")
            return
        try:
            result_label.configure(text=do_convert(conv["cat_var"].get(), value, conv["from_var"].get(), conv["to_var"].get()))
        except Exception as ex:
            result_label.configure(text="Error: " + str(ex))
    else:
        result_label.configure(text="Pick a table above.")

def on_clear():
    for e in entries.values():
        e.delete(0, tk.END)
    if "val_entry" in conv:
        conv["val_entry"].delete(0, tk.END)
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

foot = tk.Label(window, text="Tip: close the window to stop. Run again with: python3 physchem2.py", font=HINT_FONT, bg=BG, fg=FG)
foot.pack(side="bottom", pady=8)

build_fields(TOOLS[0])
hint_label.configure(text=TOOLS[0]["hint"])
window.mainloop()
