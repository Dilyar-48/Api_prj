def scale_map(s, txt, max_s):
    if txt == "-":
        s -= 0.0015
        if s <= 0:
            s = 0.0015
    else:
        if s + 0.0015 <= max_s:
            s += 0.0015
    return s

