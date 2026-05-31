"""
Calculator functions
"""

import math

#E24 standard resistor series

E24_SERIES = [10, 11, 12 , 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91]

def e24_series():
    """
    :return: list of floats, all E24 values in ascending order
    """
    values = []
    decade = 1
    while decade <= 1_000_000:
        for v in E24_SERIES:
            values.append(v * decade)
        decade *= 10
    return values

def fmt_r(ohms):
    """
    Format a resistance value.
    :param ohms: resistance value in ohms
    :return: formated string ("4.7 K")
    """
    if ohms >= 1_000_000:
        return f"{ohms / 1_000_000:.3g} M"
    elif ohms >= 1_000:
        return f"{ohms / 1_000:.3g} K"
    return f"{ohms:.3g} R"

#Resistor Combinations

def find_combinations(target, mode="", count="", max_err=""):
    """
    Search the E24 series resistor combinations close to a target value.
    :param target: target resistance in ohms
    :param mode: series/paralel
    :param count: number of resistors to combine (2/3)
    :param max_err: maximum accepted error(%)
    :return: list of dicts, sorted by absolute error
    """
    if target <= 0:
        raise ValueError("Target resistance must be positive!")

    values = e24_series()
    matches = []

    #Select the right formula to calculate the combined resistance based on mode of operation.
    def combo(rs):
        if mode == "series":
            return sum(rs)
        return 1.0 / sum(1.0 / r for r in rs)

    #check all unique pairs where j >= i to avoid duplicates
    if count == 2:
        for i in range(len(values)):
            for j in range(i, len(values)):
                result = combo([values[i], values[j]])
                err = (result - target) / target * 100
                if abs(err) <= max_err:
                    matches.append({"values": [values[i], values[j]], "result": result, "error_pct": err})

    #check all unique pairs where k >= j >= i
    elif count == 3:
        for i in range(len(values)):
            for j in range(i, len(values)):
                for k in range(j, len(values)):
                    result = combo([values[i], values[j], values[k]])
                    err = (result - target) / target * 100
                    if abs(err) <= max_err:
                        matches.append({"values": [values[i], values[j], values[k]],
                                        "result": result, "error_pct": err})

    #sort by closest match
    matches.sort(key=lambda x: abs(x["error_pct"]))
    return matches

#Voltage divider

def display_vdiv(vin, vout, r1, r2):
    """
    Calculate and package all voltage divider result into a dictionary.

    :return: dict with vin, vout, r1, r2, current in mA, power in mW for each resistor
    """
    i = vin / (r1 + r2)     #total current through divider
    return {
        "vin":      vin,
        "vout":     vout,
        "r1":       r1,
        "r2":       r2,
        "i_mA":     i * 1000,       #convert A to mA
        "p_r1_mW":  i ** 2 * r1 * 1000, #power in mW
        "p_r2_mW":  i ** 2 * r2 * 1000,
    }

def vdiv_vout(vin, r1, r2):
    """
    Calculate output voltage given input voltage and both resistors.

    :return: dict from display_vdiv()
    """
    if r1 + r2 == 0:
        raise ValueError("R1 + R2 can not be 0!")
    vout = vin * r2/ (r1 + r2)
    return display_vdiv(vin, vout, r1, r2)

def vdiv_r2(vin, vout, r1):
    """
    Solve for R2 given input voltage, desired output voltage and R1.

    :return: dict from display_vdiv()
    """
    if vin <= vout:
        raise ValueError("Vin must be greater than Vout!")
    r2 = r1 * vout / (vin-vout)
    return display_vdiv(vin, vout, r1, r2)

def vdiv_r1(vin, vout, r2):
    """
    Solve for R1 given input voltage, desired output voltage and R2.

    :return: dict from display_vdiv()
    """
    if vout <= 0:
        raise ValueError("Vout must be positive!")
    r1 = r2 * (vin-vout) / vout
    return display_vdiv(vin, vout, r1, r2)

#Current divider

def idiv_currents(i_total, r1, r2):
    """
    Calculate branch currents for two parallel resistors.

    :return: dict with i1_mA, i2_mA, r_paralel, voltage_V
    """
    if r1 <= 0  or r2 <= 0:
        raise ValueError("Resistances must be positive!")
    it = i_total / 1000         #convert mA to A for calculation
    i1 = it * r2 / (r1 + r2)    #current through R1
    i2 = it * r1 / (r1 + r2)    #current through R2
    rp = (r1 * r2) / (r1 + r2)  #equivalent parallel resistance
    return {
        "i1_mA": i1 * 1000,     #convert back to mA to display
        "i2_mA": i2 * 1000,
        "r_paralel": rp,
        "voltage_V": it * rp,
    }

def idiv_find_r2(i_total, i1, r1):
    """
    Find R2 needed to achieve a target current through R1.

    :return: dict from idiv_currents()
    """
    i2 = i_total - i1
    if i2 <= 0:
        raise ValueError("Target I1 must be less than total current!")
    r2 = r1 * i1 / i2
    return idiv_currents(i_total, r1, r2)

#Ohm's Law

def ohm_solve(v=None, i=None, r=None, p=None):
    """
    Solve all electrical quantities given exactly 2 known values.

    :return: dict with keys "v", "i", "r", "p"
    :raises: ValueError if fewer than 2 or more than 2 values are provided
    """
    given = sum(x is not None for x in [v, i, r, p])
    if given < 2:
        raise ValueError("Enter two values!")
    if given > 2:
        raise ValueError("Enter two values, leave the others empty!")

    #each branch solves for the two unknowns
    if   v is not None and i is not None: r = v / i; p = v * i
    elif v is not None and r is not None: i = v / r; p = v * v / r
    elif v is not None and p is not None: i = p / v; r = v * v / p
    elif i is not None and r is not None: v = i * r; p = i * i * r
    elif i is not None and p is not None: v = p / i; r = p / (i * i)
    elif r is not None and p is not None: v = math.sqrt(p * r); i = math.sqrt(p / r)  # ← fixed

    return {"v": v, "i": i, "r": r, "p": p}