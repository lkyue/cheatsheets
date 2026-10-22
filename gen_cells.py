#!/usr/bin/env python3
"""Generate TikZ macros for the Bravais lattice reference sheet.

Every cell is built from its lattice vectors, projected orthographically
(a to the right and slightly down, b receding up-left, c up), scaled to fit a
fixed square panel and written out as plain \\draw / \\fill commands in
millimetres.  The geometry therefore follows from the cell parameters and
cannot be misplaced by hand.

Output: cells.tex  (included by bravais.tex)
"""

import math

EDGES = [
    (0, 1),
    (0, 2),
    (0, 4),
    (1, 3),
    (1, 5),
    (2, 3),
    (2, 6),
    (3, 7),
    (4, 5),
    (4, 6),
    (5, 7),
    (6, 7),
]

FACE_CENTRES = [
    (0.5, 0.5, 0.0),
    (0.5, 0.5, 1.0),
    (0.5, 0.0, 0.5),
    (0.5, 1.0, 0.5),
    (0.0, 0.5, 0.5),
    (1.0, 0.5, 0.5),
]

# orthographic view: y recedes up-left, z is up
KY_X, KY_Y, KX_Y = 0.45, 0.55, 0.13


# --------------------------------------------------------------------------
# geometry
# --------------------------------------------------------------------------


def lattice(a, b, c, alpha, beta, gamma):
    """Cell vectors from the six cell parameters (angles in degrees)."""
    al, be, ga = (math.radians(t) for t in (alpha, beta, gamma))
    ca, cb, cg = math.cos(al), math.cos(be), math.cos(ga)
    sg = math.sin(ga)
    va = (a, 0.0, 0.0)
    vb = (b * cg, b * sg, 0.0)
    cz = math.sqrt(max(1.0 - ca * ca - cb * cb - cg * cg + 2 * ca * cb * cg, 0.0))
    vc = (c * cb, c * (ca - cb * cg) / sg, c * cz / sg)
    return va, vb, vc


def project(p):
    x, y, z = p
    return (x - KY_X * y, z + KY_Y * y - KX_Y * x)


def at(coefs, vecs):
    return tuple(sum(f * v[i] for f, v in zip(coefs, vecs)) for i in range(3))


def fitter(points, size, pad):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    scale = min(
        (size - 2 * pad) / max(x1 - x0, 1e-9), (size - 2 * pad) / max(y1 - y0, 1e-9)
    )
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return lambda p: ((p[0] - cx) * scale, (p[1] - cy) * scale)


def num(x):
    x = 0.0 if abs(x) < 0.005 else x
    return f"{x:.2f}"


def panel(size, on=True):
    """Fixed framing panel, so every figure has the same footprint."""
    if not on:
        return []
    r = size / 2 + 1.6
    return [
        f"  \\path[use as bounding box] (-{num(r)},-{num(r)}) rectangle ({num(r)},{num(r)});",
        f"  \\fill[diagram bg, rounded corners=1.4mm] (-{num(r)},-{num(r)}) "
        f"rectangle ({num(r)},{num(r)});",
    ]


# --------------------------------------------------------------------------
# emitters
# --------------------------------------------------------------------------


def cell3d(name, vecs, extras=(), size=28.0, pad=2.1, dot=1.0, frame=True):
    """Parallelepiped cell with corner and centring points."""
    va, vb, vc = vecs
    corners = [at((i, j, k), vecs) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
    centre = [at(e, vecs) for e in extras]
    labels = [tuple(1.17 * comp for comp in v) for v in vecs]

    P = fitter([project(p) for p in corners + centre + labels], size, pad)
    pts = [P(project(p)) for p in corners]

    out = [f"\\newcommand{{\\cell{name}}}{{%"] + panel(size, frame)
    for i, j in EDGES:
        (x1, y1), (x2, y2) = pts[i], pts[j]
        out.append(
            f"  \\draw[cell edge] ({num(x1)},{num(y1)}) -- ({num(x2)},{num(y2)});"
        )
    o = P(project((0.0, 0.0, 0.0)))
    for v, tag in zip(vecs, ("a", "b", "c")):
        tip = P(project(v))
        lab = P(project(tuple(1.17 * comp for comp in v)))
        out.append(
            f"  \\draw[axis arrow] ({num(o[0])},{num(o[1])}) -- ({num(tip[0])},{num(tip[1])});"
        )
        out.append(
            f"  \\node[axis label small] at ({num(lab[0])},{num(lab[1])}) {{${tag}$}};"
        )
    for x, y in pts:
        out.append(f"  \\fill[lattice point] ({num(x)},{num(y)}) circle ({dot}pt);")
    for p in centre:
        x, y = P(project(p))
        out.append(f"  \\fill[centre point] ({num(x)},{num(y)}) circle ({dot}pt);")
    out.append("}")
    return "\n".join(out)


def cell2d(
    name,
    va,
    vb,
    i_range,
    j_range,
    centred=False,
    size=33.0,
    pad=2.2,
    dot=1.0,
    frame=True,
):
    """Plan view of a 2-D lattice: patch of points plus the conventional cell."""
    dots = [
        (i * va[0] + j * vb[0], i * va[1] + j * vb[1])
        for i in range(i_range[0], i_range[1] + 1)
        for j in range(j_range[0], j_range[1] + 1)
    ]
    extra = []
    if centred:
        for i in range(i_range[0], i_range[1]):
            for j in range(j_range[0], j_range[1]):
                p = (
                    (i + 0.5) * va[0] + (j + 0.5) * vb[0],
                    (i + 0.5) * va[1] + (j + 0.5) * vb[1],
                )
                if abs(i) == 0 and abs(j) == 0:
                    extra.append(p)
                else:
                    dots.append(p)

    corners = [(0.0, 0.0), va, (va[0] + vb[0], va[1] + vb[1]), vb]
    labels = [(1.26 * v[0], 1.26 * v[1]) for v in (va, vb)]
    P = fitter(dots + extra + corners + labels, size, pad)

    out = [f"\\newcommand{{\\cell{name}}}{{%"] + panel(size, frame)
    poly = " -- ".join(f"({num(P(p)[0])},{num(P(p)[1])})" for p in corners)
    out.append(f"  \\fill[cell wash] {poly} -- cycle;")
    out.append(f"  \\draw[cell edge] {poly} -- cycle;")
    o = P((0.0, 0.0))
    for v, tag in zip((va, vb), ("a", "b")):
        tip = P(v)
        lab = P((1.26 * v[0], 1.26 * v[1]))
        out.append(
            f"  \\draw[axis arrow] ({num(o[0])},{num(o[1])}) -- ({num(tip[0])},{num(tip[1])});"
        )
        out.append(
            f"  \\node[axis label small] at ({num(lab[0])},{num(lab[1])}) {{${tag}$}};"
        )
    for p in dots:
        x, y = P(p)
        out.append(f"  \\fill[lattice point] ({num(x)},{num(y)}) circle ({dot}pt);")
    for p in extra:
        x, y = P(p)
        out.append(f"  \\fill[centre point] ({num(x)},{num(y)}) circle ({dot}pt);")
    out.append("}")
    return "\n".join(out)


def hex_cell(name, size=22.0, pad=2.0, dot=0.95):
    """Hexagonal cell of the rhombohedral lattice: a 120-degree rhombic prism
    carrying three lattice points (one at the corners, two inside)."""
    vecs = lattice(1.0, 1.0, 1.25, 90, 90, 120)
    return cell3d(name, vecs, [(2 / 3, 1 / 3, 1 / 3), (1 / 3, 2 / 3, 2 / 3)],
                  size=size, dot=dot, frame=False)


# the 19 lattices
# --------------------------------------------------------------------------

THREE_D = [
    ("TriclinicP", lattice(1.00, 0.86, 0.74, 76, 83, 115), []),
    ("MonoclinicP", lattice(1.00, 0.88, 0.76, 90, 104, 90), []),
    ("MonoclinicC", lattice(1.00, 0.88, 0.76, 90, 104, 90), [(0.5, 0.5, 0.0)]),
    ("OrthoP", lattice(1.00, 0.80, 0.63, 90, 90, 90), []),
    ("OrthoC", lattice(1.00, 0.80, 0.63, 90, 90, 90), [(0.5, 0.5, 0.0)]),
    ("OrthoI", lattice(1.00, 0.80, 0.63, 90, 90, 90), [(0.5, 0.5, 0.5)]),
    ("OrthoF", lattice(1.00, 0.80, 0.63, 90, 90, 90), FACE_CENTRES),
    ("TetraP", lattice(1.00, 1.00, 1.40, 90, 90, 90), []),
    ("TetraI", lattice(1.00, 1.00, 1.40, 90, 90, 90), [(0.5, 0.5, 0.5)]),
    ("RhomboR", lattice(1.00, 1.00, 1.00, 74, 74, 74), []),
    ("HexP", lattice(1.00, 1.00, 1.20, 90, 90, 120), []),
    ("CubicP", lattice(1.00, 1.00, 1.00, 90, 90, 90), []),
    ("CubicI", lattice(1.00, 1.00, 1.00, 90, 90, 90), [(0.5, 0.5, 0.5)]),
    ("CubicF", lattice(1.00, 1.00, 1.00, 90, 90, 90), FACE_CENTRES),
]

# patch of points around the conventional cell, which sits at the origin corner
I_RANGE, J_RANGE = (-1, 2), (-1, 2)


# figure sizes per sheet: the poster is A3 portrait, the desk copy A3 landscape
PROFILES = {
    "poster": dict(out="cells.tex", c3=28.0, d3=1.00, c2=33.0, d2=1.00,
                   prism=22.0, dp=0.95),
    "desk":   dict(out="cells-desk.tex", c3=42.0, d3=1.40, c2=34.0, d2=1.05,
                   prism=28.0, dp=1.20),
}


def main(profile="poster"):
    p = PROFILES[profile]
    chunks = [
        "% Generated by gen_cells.py -- do not edit by hand.",
        "% Coordinates in millimetres; every figure fills a fixed panel.",
    ]
    for name, vecs, extras in THREE_D:
        chunks.append(cell3d(name, vecs, extras, size=p["c3"], dot=p["d3"]))
    chunks.append(hex_cell("RhomboHex", size=p["prism"], dot=p["dp"]))
    # unframed copy for the comparison figure in the notes
    ro = [c for c in THREE_D if c[0] == "RhomboR"][0]
    chunks.append(
        cell3d("RhomboRBare", ro[1], ro[2], size=p["c3"], dot=p["d3"], frame=False)
        .replace("{\\cellRhomboR}", "{\\cellRhomboRBare}")
    )

    two_d = [
        ("Oblique", (1.0, 0.0),
         (0.78 * math.cos(math.radians(70)), 0.78 * math.sin(math.radians(70)))),
        ("RectP", (1.0, 0.0), (0.0, 0.72)),
        ("Square", (1.0, 0.0), (0.0, 1.0)),
        ("Hexagonal", (1.0, 0.0), (-0.5, math.sqrt(3) / 2)),
    ]
    chunks.append(cell2d("Oblique", two_d[0][1], two_d[0][2], I_RANGE, J_RANGE,
                         size=p["c2"], dot=p["d2"]))
    chunks.append(cell2d("RectP", two_d[1][1], two_d[1][2], I_RANGE, J_RANGE,
                         size=p["c2"], dot=p["d2"]))
    chunks.append(cell2d("RectC", (1.0, 0.0), (0.0, 0.72), I_RANGE, J_RANGE,
                         centred=True, size=p["c2"], dot=p["d2"]))
    chunks.append(cell2d("Square", two_d[2][1], two_d[2][2], I_RANGE, J_RANGE,
                         size=p["c2"], dot=p["d2"]))
    chunks.append(cell2d("Hexagonal", two_d[3][1], two_d[3][2], I_RANGE, J_RANGE,
                         size=p["c2"], dot=p["d2"]))

    with open(p["out"], "w") as fh:
        fh.write("\n\n".join(chunks) + "\n")
    print(f"{p['out']}: 14 cells at {p['c3']} mm, 5 patches at {p['c2']} mm")


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "poster")
