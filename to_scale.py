def scale_map(s, sign):
    if sign == "+": s = min((s + s / 2), 90)
    if sign == "-": s = max((s - s / 2), s / 2)
    return s

