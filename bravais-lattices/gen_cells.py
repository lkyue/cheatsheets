#!/usr/bin/env python3
"""Generate TikZ macros for the Bravais lattice reference sheet.

Every cell is built from its lattice vectors and projected orthographically
with a real camera, so the panels are true axonometric views: a cubic cell
looks like a cube, and a 90 degree corner reads as a 90 degree corner.  Cells
are scaled to fit a fixed square panel; edges of faces turned away from the
camera are drawn lighter, and the three faces turned towards it carry a very
light wash, so the cell reads as a solid body rather than a wire frame.  The
geometry therefore follows from the cell parameters and cannot be misplaced by
hand.

Output: cells.tex  (included by bravais-lattices.tex)
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

# the six faces, as corner indices (i * 4 + j * 2 + k for corner (i, j, k))
FACES = [
    [0, 4, 6, 2],
    [1, 5, 7, 3],
    [0, 1, 5, 4],
    [2, 3, 7, 6],
    [0, 1, 3, 2],
    [4, 5, 7, 6],
]

FACE_OF_EDGE = [
    [f for f, face in enumerate(FACES) if a in face and b in face] for a, b in EDGES
]

FACE_CENTRES = [
    (0.5, 0.5, 0.0),
    (0.5, 0.5, 1.0),
    (0.5, 0.0, 0.5),
    (0.5, 1.0, 0.5),
    (0.0, 0.5, 0.5),
    (1.0, 0.5, 0.5),
]

# Orthographic camera: it sits at AZIMUTH degrees in the xy-plane (measured
# from +x towards +y) and ELEVATION degrees above that plane.  a then points
# up-right, b up-left and c straight up, and the three faces at the origin are
# visible at a, b and c.
#
# -125 / 30 is deliberately not the isometric -135 / 35.26: in an isometric
# view the centre of a cubic cell falls exactly behind the corner at (0, 0, 1),
# so the body-centre point of a body-centred lattice would be hidden by a
# corner point.  This view keeps them a couple of millimetres apart.
AZIMUTH, ELEVATION = -125.0, 30.0


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


def camera(azimuth, elevation):
    """Screen axes for an orthographic view: (view direction, right, up)."""
    ca, sa = math.cos(math.radians(azimuth)), math.sin(math.radians(azimuth))
    ce, se = math.cos(math.radians(elevation)), math.sin(math.radians(elevation))
    view = (ce * ca, ce * sa, se)  # from the cell towards the camera
    right = (-sa, ca, 0.0)
    up = (-ca * se, -sa * se, ce)
    return view, right, up


VIEW, RIGHT, UP = camera(AZIMUTH, ELEVATION)


def project(p):
    x, y, z = p
    return (
        x * RIGHT[0] + y * RIGHT[1] + z * RIGHT[2],
        x * UP[0] + y * UP[1] + z * UP[2],
    )


def at(coefs, vecs):
    return tuple(sum(f * v[i] for f, v in zip(coefs, vecs)) for i in range(3))


def cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def facing(vecs):
    """How squarely each face in FACES faces the camera (> 0: visible)."""
    corners = [at((i, j, k), vecs) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
    centre = tuple(sum(c[d] for c in corners) / 8 for d in range(3))
    out = []
    for face in FACES:
        p0, p1, p3 = corners[face[0]], corners[face[1]], corners[face[3]]
        n = cross(
            tuple(a - b for a, b in zip(p1, p0)), tuple(a - b for a, b in zip(p3, p0))
        )
        fc = tuple(sum(corners[i][d] for i in face) / 4 for d in range(3))
        to_face = tuple(fc[d] - centre[d] for d in range(3))
        if sum(a * b for a, b in zip(n, to_face)) < 0:
            n = tuple(-t for t in n)
        depth = sum(n[d] * VIEW[d] for d in range(3)) / (math.hypot(*n) or 1.0)
        out.append(depth)
    return out


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
    corners = [at((i, j, k), vecs) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
    centre = [at(e, vecs) for e in extras]
    label_at = [tuple(1.17 * comp for comp in v) for v in vecs]

    P = fitter([project(p) for p in corners + centre + label_at], size, pad)
    pts = [P(project(p)) for p in corners]
    near = [f > 1e-9 for f in facing(vecs)]

    out = [f"\\newcommand{{\\cell{name}}}{{%"] + panel(size, frame)
    for face, vis in zip(FACES, near):
        if vis:
            poly = " -- ".join(f"({num(pts[i][0])},{num(pts[i][1])})" for i in face)
            out.append(f"  \\fill[face wash] {poly} -- cycle;")
    for (i, j), faces in zip(EDGES, FACE_OF_EDGE):
        style = "cell edge" if any(near[f] for f in faces) else "cell edge back"
        out.append(
            f"  \\draw[{style}] ({num(pts[i][0])},{num(pts[i][1])}) -- "
            f"({num(pts[j][0])},{num(pts[j][1])});"
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


def triad(name="Triad", size=18.0):
    """Key figure: the three cell vectors from one origin, with the angles
    alpha (between b and c), beta (between a and c) and gamma (between a and b).

    Arrows keep their projected lengths; the alpha and beta arcs sit at 0.66 of
    an arrow, the gamma arc outside the arrow heads because in this view gamma's
    bisector runs along c.
    """
    vecs = lattice(1.0, 1.0, 1.0, 90, 90, 90)
    span = max(math.hypot(*project(v)) for v in vecs)
    k = size * 0.33 / span
    tips = {t: (k * project(v)[0], k * project(v)[1]) for v, t in zip(vecs, "abc")}
    ang = {t: math.degrees(math.atan2(q[1], q[0])) for t, q in tips.items()}
    arc_r, outer_r = 0.66 * size * 0.33, 1.52 * size * 0.33

    out = [f"\\newcommand{{\\cell{name}}}{{%"]
    for tag in ("a", "b", "c"):
        out.append(
            f"  \\draw[triad axis] (0,0) -- ({num(tips[tag][0])},{num(tips[tag][1])});"
        )

    def arc(a1, a2, radius, label, where):
        out.append(
            f"  \\draw[angle arc] (0,0) ++({num(a1)}:{num(radius)}mm) "
            f"arc ({num(a1)}:{num(a2)}:{num(radius)}mm);"
        )
        mid = math.radians(a1 + (a2 - a1) * where)
        out.append(
            f"  \\node[angle label] at ({num(radius * math.cos(mid))},"
            f"{num(radius * math.sin(mid))}) {{{label}}};"
        )

    arc(ang["b"], ang["c"], arc_r, "$\\alpha$", 0.42)
    arc(ang["a"], ang["c"], arc_r, "$\\beta$", 0.42)
    arc(ang["a"], ang["b"], outer_r, "$\\gamma$", 0.50)

    for tag, q in tips.items():
        n = math.hypot(*q) or 1.0
        # c shares its tip with the gamma arc, so it sits beside the head
        ox, oy = (-2.7, 0.9) if tag == "c" else (2.0 * q[0] / n, 2.0 * q[1] / n)
        out.append(
            f"  \\node[axis label small] at ({num(q[0] + ox)},{num(q[1] + oy)}) {{${tag}$}};"
        )
    out.append("  \\fill[lattice point] (0,0) circle (0.55pt);")
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
    return cell3d(
        name,
        vecs,
        [(2 / 3, 1 / 3, 1 / 3), (1 / 3, 2 / 3, 2 / 3)],
        size=size,
        dot=dot,
        frame=False,
    )


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
    "poster": dict(
        out="cells.tex",
        c3=28.0,
        d3=1.00,
        c2=33.0,
        d2=1.00,
        prism=22.0,
        dp=0.95,
        key=18.0,
    ),
    "desk": dict(
        out="cells-desk.tex",
        c3=42.0,
        d3=1.40,
        c2=34.0,
        d2=1.05,
        prism=28.0,
        dp=1.20,
        key=21.0,
    ),
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
    )
    chunks.append(triad(size=p["key"]))

    two_d = [
        (
            "Oblique",
            (1.0, 0.0),
            (0.78 * math.cos(math.radians(70)), 0.78 * math.sin(math.radians(70))),
        ),
        ("RectP", (1.0, 0.0), (0.0, 0.72)),
        ("Square", (1.0, 0.0), (0.0, 1.0)),
        ("Hexagonal", (1.0, 0.0), (-0.5, math.sqrt(3) / 2)),
    ]
    chunks.append(
        cell2d(
            "Oblique",
            two_d[0][1],
            two_d[0][2],
            I_RANGE,
            J_RANGE,
            size=p["c2"],
            dot=p["d2"],
        )
    )
    chunks.append(
        cell2d(
            "RectP",
            two_d[1][1],
            two_d[1][2],
            I_RANGE,
            J_RANGE,
            size=p["c2"],
            dot=p["d2"],
        )
    )
    chunks.append(
        cell2d(
            "RectC",
            (1.0, 0.0),
            (0.0, 0.72),
            I_RANGE,
            J_RANGE,
            centred=True,
            size=p["c2"],
            dot=p["d2"],
        )
    )
    chunks.append(
        cell2d(
            "Square",
            two_d[2][1],
            two_d[2][2],
            I_RANGE,
            J_RANGE,
            size=p["c2"],
            dot=p["d2"],
        )
    )
    chunks.append(
        cell2d(
            "Hexagonal",
            two_d[3][1],
            two_d[3][2],
            I_RANGE,
            J_RANGE,
            size=p["c2"],
            dot=p["d2"],
        )
    )

    with open(p["out"], "w") as fh:
        fh.write("\n\n".join(chunks) + "\n")
    print(
        f"{p['out']}: 14 cells at {p['c3']} mm, 5 patches at {p['c2']} mm, "
        f"angle key at {p['key']} mm"
    )


if __name__ == "__main__":
    import sys

    main(sys.argv[1] if len(sys.argv) > 1 else "poster")
