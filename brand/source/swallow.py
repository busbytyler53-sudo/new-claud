# right half of a top-down swallow, x>=0, centred on x=0
HALF = [("M", 0, -62), ("C", 5, -62, 9, -57, 9, -49), ("C", 9, -44, 10, -40, 12, -36),
        ("C", 40, -44, 80, -38, 118, -10), ("C", 84, -20, 48, -16, 16, 2),
        ("C", 14, 10, 12, 16, 10, 22), ("L", 38, 100), ("C", 30, 96, 18, 70, 4, 38), ("L", 0, 34)]
def swallow_d():
    pts = HALF
    fwd = []
    for seg in pts:
        fwd.append(seg[0] + " ".join(f"{v:g}" for v in seg[1:]))
    # mirror back: reverse segments, negate x
    back = []
    cur = [(p[-2], p[-1]) for p in pts]
    for i in range(len(pts) - 1, 0, -1):
        seg = pts[i]; start = cur[i - 1]
        if seg[0] == "C":
            back.append(f"C{-seg[3]:g} {seg[4]:g} {-seg[1]:g} {seg[2]:g} {-start[0]:g} {start[1]:g}")
        else:
            back.append(f"L{-start[0]:g} {start[1]:g}")
    return "".join(fwd) + "".join(back) + "Z"
