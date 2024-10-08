import numpy as np

prefix = ["T", "G", "M", "k", "", "m", "\mu ", "n", "p", "f", "a", "z", "y"]

def round(value, sig_figs=3):
    rounded_value = np.round(value, -int(np.floor(np.log10(np.abs(value))) - (sig_figs - 1)))
    if int(rounded_value) == rounded_value:
        return int(rounded_value)
    else:
        return np.round(value, -int(np.floor(np.log10(np.abs(value))) - (sig_figs - 1)))

def unit_prefix(value):
    if value < 0:
        factor = -1
    else:
        factor = 1

    value = np.abs(value)

    if value == 0:
        return 0, ""
    p = 4
    while value < 1:
        value *= 1000
        p += 1
    while value >= 1000:
        value /= 1000
        p -= 1
    
    return factor * value, prefix[p]

def unit(value, unit):
    value, p = unit_prefix(value)
    rounded_value = round(value)
    value = f"{rounded_value:.{3 - int(np.floor(np.log10(np.abs(rounded_value)))) - 1}f}"
    return f"{value} $[{p}{unit}]$"

def unit_uncertainty(value, uncertainty, unit):
    value, p = unit_prefix(value)
    uncertainty, p2 = unit_prefix(uncertainty)
    rounded_value = round(value)
    rounded_uncertainty = round(uncertainty)
    value = f"{rounded_value:.{3 - int(np.floor(np.log10(np.abs(rounded_value)))) - 1}f}"
    uncertainty = f"{rounded_uncertainty:.{3 - int(np.floor(np.log10(np.abs(rounded_uncertainty)))) - 1}f}"
    return f"{value} $\pm$ {uncertainty} $[{p}{unit} \pm {p2}{unit}]$"
