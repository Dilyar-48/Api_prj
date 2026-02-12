import requests

def spn_sizes(s):
    toponym_size_w = abs(
        float(s["lowerCorner"].split()[0]) - float(s["upperCorner"].split()[0]))
    toponym_size_h = abs(
        float(s["lowerCorner"].split()[1]) - float(s["upperCorner"].split()[1]))
    max_coord = min(toponym_size_w, toponym_size_h)
    return str(round(max_coord, int(str(max_coord).count("0") + 1)))