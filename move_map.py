def to_move(r, l, t, b, x, y):
    x = min(max(0, x + r - l), 90)
    y = min(max(0, y + t - b), 70)
    return x, y