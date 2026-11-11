// ============================================================
//  Moments of Inertia — one-page cheatsheet
//  Typst 0.15 + CeTZ 0.5.2
// ============================================================
#set document(title: "Moments of Inertia — common sections and bodies", author: "cheatsheet")
#import "@preview/cetz:0.5.2"
// selective import: `cetz.draw: *` would shadow Typst's own `grid`
#import cetz.draw: line, rect, circle, arc, content, set-style

// ---------- page ----------
#set page(paper: "a4", flipped: true, margin: (x: 5mm, y: 4.5mm))
#set text(size: 7.2pt, fill: rgb("#16181d"), font: "New Computer Modern")
#set par(leading: 1.0em, justify: false)

// ---------- palette ----------
#let cA = rgb("#1d5c9e")
#let cB = rgb("#a9501a")
#let tA = rgb("#dfe9f7")
#let tB = rgb("#f7e3d2")
#let ink = rgb("#16181d")
#let soft = rgb("#5c6470")
#let rule = rgb("#c7ccd3")
#let axiscol = rgb("#c2410c")

// ---------- drawing helpers ----------
#let T = 5pt

#let fig(tint, body) = box(
  width: 2.15cm,
  height: 1.62cm,
  align(center + horizon, cetz.canvas(length: 1cm, {
    set-style(stroke: .42pt + ink, fill: tint)
    body
  })),
)

#let caxis(x, y, w: 0.9, h: 0.45, y-axis: true) = {
  line((x - w / 2, y), (x + w / 2, y),
    stroke: (paint: axiscol, dash: "dash-dotted", thickness: .38pt))
  if y-axis {
    line((x, y - h / 2), (x, y + h / 2),
      stroke: (paint: axiscol, dash: "dash-dotted", thickness: .38pt))
  }
}

#let cdot(x, y) = circle((x, y), radius: .022, fill: ink, stroke: none)

// quarter disk built from an explicit path: cetz's arc() places its sector
// inconsistently with the documented centre/angle convention
#let quarter(x, y, r) = {
  let n = 24
  let arc-pts = range(0, n + 1).map(i => {
    let a = i / n * 90deg
    (x + r * calc.cos(a), y + r * calc.sin(a))
  })
  line((x, y), ..arc-pts, close: true)
}

#let dimh(a, b, y, label, up: false, tx: auto) = {
  line((a, y), (b, y),
    stroke: (paint: soft, thickness: .3pt),
    mark: (start: "bar", end: "bar"))
  content((if tx == auto { (a + b) / 2 } else { tx },
      if up { y + .09 } else { y - .115 }),
    text(size: T, fill: soft)[#label])
}

#let dimv(x, a, b, label) = {
  line((x, a), (x, b),
    stroke: (paint: soft, thickness: .3pt),
    mark: (start: "bar", end: "bar"))
  content((x + .15, (a + b) / 2), text(size: T, fill: soft)[#label])
}

// ---------- card ----------
#let card(acc, name, figure, lines) = block(
  width: 100%,
  height: 100%,
  stroke: (top: 1.7pt + acc, rest: .3pt + rule),
  radius: 1.4pt,
  inset: (x: 3.2pt, top: 2.2pt, bottom: 1.2pt),
  fill: white,
  align(center + horizon, grid(
    columns: (2.15cm, 1fr),
    column-gutter: 3pt,
    align: (center + horizon, left + horizon),
    figure,
    block({
      set par(leading: 1.22em)
      text(size: 7.9pt, weight: "bold", fill: acc)[#name]
      for l in lines {
        linebreak(justify: false)
        text(size: 7.4pt)[#l]
      }
    }),
  )),
)

// ============================================================
//  FIGURES — group A (area moments)
// ============================================================
#let f-rect = fig(tA, {
  rect((0.30, 0.32), (1.56, 1.10))
  caxis(0.93, 0.71, w: 1.50)
  dimh(0.30, 1.56, 0.20, [$b$])
  dimv(1.66, 0.32, 1.10, [$h$])
})

#let f-hollow = fig(tA, {
  rect((0.28, 0.28), (1.60, 1.14))
  rect((0.54, 0.50), (1.34, 0.92), fill: white)
  caxis(0.94, 0.71, w: 1.52, h: 0.98)
  dimh(0.28, 1.60, 0.17, [$B$])
  dimh(0.54, 1.34, 0.40, [$b$], tx: 1.16)
})

#let f-para = fig(tA, {
  line((0.40, 0.30), (1.34, 0.30), (1.58, 1.10), (0.64, 1.10), close: true)
  caxis(0.99, 0.70, w: 1.05)
  line((0.36, 0.30), (1.38, 0.30), stroke: (paint: axiscol, dash: "dash-dotted", thickness: .38pt))
  dimh(0.40, 1.34, 0.18, [$b$])
  dimv(1.69, 0.30, 1.10, [$h$])
})

#let f-iso = fig(tA, {
  line((0.93, 1.14), (1.62, 0.26), (0.24, 0.26), close: true)
  caxis(0.93, 0.553, w: 0.78)
  line((0.20, 0.26), (1.66, 0.26), stroke: (paint: axiscol, dash: "dash-dotted", thickness: .38pt))
  dimh(0.24, 1.62, 0.14, [$b$])
  dimv(1.74, 0.26, 1.14, [$h$])
})

#let f-right = fig(tA, {
  line((0.30, 0.26), (1.52, 0.26), (0.30, 1.12), close: true)
  caxis(0.707, 0.547, w: 1.02)
  dimh(0.30, 1.52, 0.14, [$b$])
  dimv(1.64, 0.26, 1.12, [$h$])
})

#let f-trap = fig(tA, {
  line((0.60, 1.10), (1.30, 1.10), (1.64, 0.26), (0.26, 0.26), close: true)
  cdot(0.95, 0.634)
  line((0.36, 0.634), (1.54, 0.634), stroke: (paint: axiscol, dash: "dash-dotted", thickness: .38pt))
  dimh(0.60, 1.30, 1.19, [$a$], up: true)
  dimh(0.26, 1.64, 0.14, [$b$])
  dimv(1.76, 0.26, 1.10, [$h$])
})

#let f-circle = fig(tA, {
  circle((0.95, 0.68), radius: .46)
  caxis(0.95, 0.68, w: 1.06, h: 1.06)
  dimv(1.50, 0.68, 1.14, [$r$])
})

#let f-annulus = fig(tA, {
  circle((0.95, 0.68), radius: .47, fill: tA)
  circle((0.95, 0.68), radius: .25, fill: white)
  caxis(0.95, 0.68, w: 1.08, h: 1.08)
  dimv(1.52, 0.68, 1.15, [$R$])
})

#let f-semi = fig(tA, {
  arc((0.95, 0.24), start: 0deg, stop: 180deg, radius: .59, mode: "PIE")
  cdot(0.95, 0.24 + 4 * 0.59 / (3 * calc.pi))
  caxis(0.95, 0.24, w: 1.26, y-axis: false)
  dimv(1.62, 0.24, 0.83, [$r$])
})

#let f-quarter = fig(tA, {
  quarter(0.45, 0.26, 0.90)
  cdot(0.45 + 4 * 0.90 / (3 * calc.pi), 0.26 + 4 * 0.90 / (3 * calc.pi))
  line((0.35, 0.26), (1.44, 0.26),
    stroke: (paint: axiscol, dash: "dash-dotted", thickness: .38pt))
  line((0.45, 0.16), (0.45, 1.25),
    stroke: (paint: axiscol, dash: "dash-dotted", thickness: .38pt))
})

#let f-ellipse = fig(tA, {
  circle((0.95, 0.68), radius: (0.64, 0.38))
  caxis(0.95, 0.68, w: 1.38, h: 0.88)
  dimv(1.64, 0.68, 1.06, [$b$])
  dimh(0.31, 1.59, 0.20, [$a$])
})

#let f-tube = fig(tA, {
  circle((0.95, 0.68), radius: .46, fill: none, stroke: .95pt + ink)
  caxis(0.95, 0.68, w: 1.08, h: 1.08)
  dimv(1.53, 0.68, 1.14, [$R$])
  content((1.11, 0.30), text(size: T, fill: soft)[$t$])
})

// ============================================================
//  FIGURES — group B (mass moments)
// ============================================================
#let f-rod = fig(tB, {
  rect((0.22, 0.66), (1.62, 0.75), radius: .045)
  line((0.92, 0.46), (0.92, 0.95),
    stroke: (paint: axiscol, dash: "dash-dotted", thickness: .38pt))
  dimh(0.22, 1.62, 0.48, [$L$])
})

#let f-plate = fig(tB, {
  rect((0.36, 0.30), (1.44, 1.04))
  line((0.36, 1.04), (0.56, 1.16), (1.64, 1.16), (1.44, 1.04),
    stroke: .42pt + ink, fill: tB)
  line((1.44, 0.30), (1.64, 0.42), (1.64, 1.16), stroke: .42pt + ink, fill: none)
  cdot(0.90, 0.67)
  content((1.04, 0.80), text(size: T, fill: soft)[$z$])
  dimh(0.36, 1.44, 0.18, [$a$])
  dimv(1.76, 0.30, 1.04, [$b$])
})

#let f-diskring = fig(tB, {
  circle((0.55, 0.66), radius: .30)
  circle((1.34, 0.66), radius: .30, fill: none, stroke: .95pt + ink)
  caxis(0.55, 0.66, w: .74, h: .74)
})

#let f-sphere = fig(tB, {
  circle((0.95, 0.68), radius: .43)
  line((0.52, 0.68), (1.38, 0.68), stroke: (paint: ink, thickness: .3pt, dash: "dashed"))
  line((0.95, 0.25), (0.95, 1.11),
    stroke: (paint: axiscol, dash: "dash-dotted", thickness: .38pt))
  dimv(1.50, 0.68, 1.11, [$R$])
})

#let f-cyl = fig(tB, {
  line((0.58, 0.34), (0.58, 1.00), (1.28, 1.00), (1.28, 0.34),
    stroke: .42pt + ink, fill: none)
  circle((0.93, 1.00), radius: (0.35, 0.10), fill: tB)
  circle((0.93, 0.34), radius: (0.35, 0.10), fill: none)
  line((0.93, 0.16), (0.93, 1.12),
    stroke: (paint: axiscol, dash: "dash-dotted", thickness: .38pt))
  dimh(0.93, 1.28, 1.14, [$R$], up: true)
  dimv(1.48, 0.34, 1.00, [$L$])
})

#let f-cone = fig(tB, {
  line((0.93, 1.16), (1.50, 0.36), (0.36, 0.36), close: true)
  circle((0.93, 0.36), radius: (0.57, 0.13), fill: tB)
  line((0.93, 0.20), (0.93, 1.24),
    stroke: (paint: axiscol, dash: "dash-dotted", thickness: .38pt))
  line((1.50, 0.23), (1.50, 0.18), stroke: (paint: soft, thickness: .3pt))
  dimh(0.93, 1.50, 0.18, [$R$])
})

// ============================================================
//  HEADER
// ============================================================
#block(
  width: 100%,
  stroke: (bottom: .7pt + ink),
  inset: (bottom: 3pt),
  {
    grid(
      columns: (1fr, auto),
      align: (left + horizon, right + horizon),
      column-gutter: 8pt,
      stack(spacing: 3.5pt,
        text(size: 15.5pt, weight: "bold", tracking: -.01em)[Moments of Inertia],
        text(size: 6.2pt, fill: soft, tracking: .05em)[COMMON SECTIONS AND BODIES],
      ),
      text(size: 6.2pt, fill: soft)[
        #text(weight: "bold", fill: cA)[A] statics · second moment of area \
        #text(weight: "bold", fill: cB)[B] dynamics · second moment of mass
      ],
    )
    v(2.4pt)
    block(
      width: 100%,
      fill: rgb("#f2f4f7"),
      radius: 1.6pt,
      inset: (x: 6pt, y: 3pt),
      grid(
        columns: (1fr,) * 5,
        align: (center, center, center, center, center),
        $I_x = integral_A y^2 dif A$,
        $I_y = integral_A x^2 dif A$,
        $J_O = I_x + I_y$,
        $I = overline(I) + A d^2$,
        $k = sqrt(I \/ A)$,
      ),
    )
  },
)

#v(1.8mm)

// ---------- group wrapper ----------
#let group(acc, caption, rows, cards) = block(width: 100%, {
  set text(size: 6.6pt)
  block(
    width: 100%,
    inset: (left: 1pt, bottom: 2pt),
    text(fill: acc, weight: "bold")[#caption],
  )
  grid(
    columns: (1fr, 1fr, 1fr),
    rows: (23.6mm,) * rows,
    gutter: 2.5mm,
    ..cards,
  )
})

// ============================================================
//  DOCUMENT
// ============================================================
#group(cA, [*A — Area moments* #h(4pt) #text(weight: "regular", fill: soft)[$I = integral_A y^2 dif A$ · section property, mm⁴ · bar = centroidal axis, plain = axis shown]], 4, (
  card(cA, [Rectangle $b times h$], f-rect, (
    [$A = b h$],
    [$I_x = (b h^3) \/ 12$],
    [$I_y = (h b^3) \/ 12$],
    [$J_O = (b h (b^2 + h^2)) \/ 12$],
  )),
  card(cA, [Hollow rectangle], f-hollow, (
    [$A = B H - b h$],
    [$I_x = (B H^3 - b h^3) \/ 12$],
    [$I_y = (H B^3 - h b^3) \/ 12$],
  )),
  card(cA, [Parallelogram $b times h$], f-para, (
    [$A = b h$],
    [$overline(I)_x = (b h^3) \/ 12$],
    [$I_"base" = (b h^3) \/ 3$],
  )),
  card(cA, [Isosceles triangle], f-iso, (
    [$A = b h \/ 2$],
    [$I_"base" = (b h^3) \/ 12$],
    [$overline(I)_x = (b h^3) \/ 36$],
    [$overline(I)_y = (h b^3) \/ 48$],
  )),
  card(cA, [Right triangle], f-right, (
    [$A = b h \/ 2$],
    [$overline(I)_x = (b h^3) \/ 36$],
    [$overline(I)_y = (h b^3) \/ 36$],
    [$overline(I)_("xy") = -(b^2 h^2) \/ 72$],
  )),
  card(cA, [Trapezoid], f-trap, (
    [$A = ((a + b) h) \/ 2$],
    [$overline(I)_x = (h^3 (a^2 + 4 a b + b^2)) \/ (36 (a + b))$],
    [$overline(y) = (h (2a + b)) \/ (3(a+b))$  from base $b$],
  )),
  card(cA, [Circle $r$], f-circle, (
    [$A = pi r^2$],
    [$I_x = I_y = (pi r^4) \/ 4$],
    [$J_O = (pi r^4) \/ 2$],
    [$I_x = (pi d^4) \/ 64 quad (d = 2r)$],
  )),
  card(cA, [Annulus $R$, $r$], f-annulus, (
    [$A = pi (R^2 - r^2)$],
    [$I_x = I_y = (pi (R^4 - r^4)) \/ 4$],
    [$J_O = (pi (R^4 - r^4)) \/ 2$],
  )),
  card(cA, [Semicircle $r$], f-semi, (
    [$A = (pi r^2) \/ 2$],
    [$I_"base" = (pi r^4) \/ 8$],
    [$overline(I)_x approx 0.1098 r^4$],
    [$overline(y) = (4r) \/ (3pi)$],
  )),
  card(cA, [Quarter circle $r$], f-quarter, (
    [$A = (pi r^2) \/ 4$],
    [$I_"edge" = (pi r^4) \/ 16$],
    [$overline(I) approx 0.0549 r^4$],
    [$overline(x) = overline(y) = (4r) \/ (3pi)$],
  )),
  card(cA, [Ellipse $a$, $b$], f-ellipse, (
    [$A = pi a b$],
    [$I_x = (pi a b^3) \/ 4$],
    [$I_y = (pi a^3 b) \/ 4$],
  )),
  card(cA, [Thin-walled tube], f-tube, (
    [$A approx 2 pi R t$],
    [$I approx pi R^3 t$],
    [$J_O approx 2 pi R^3 t$],
    [$t << R$],
  )),
))

#v(1.8mm)

#group(cB, [*B — Mass moments* #h(4pt) #text(weight: "regular", fill: soft)[$I = integral r^2 dif m$ · rigid-body property, kg·m² · principal axis named on each line]], 2, (
  card(cB, [Thin rod, length $L$], f-rod, (
    [$overline(I) = (m L^2) \/ 12$],
    [$I_"end" = (m L^2) \/ 3$],
  )),
  card(cB, [Rectangular plate], f-plate, (
    [$I_z = (m (a^2 + b^2)) \/ 12$],
    [$I_"edge ∥ b" = (m a^2) \/ 3$],
  )),
  card(cB, [Disk / ring], f-diskring, (
    [disk $I_z = 1/2 m R^2$],
    [disk $I_"diam" = 1/4 m R^2$],
    [ring (thin) $I_z = m R^2$],
  )),
  card(cB, [Sphere], f-sphere, (
    [solid $I = 2/5 m R^2$],
    [thin shell $I = 2/3 m R^2$],
    [any diameter],
  )),
  card(cB, [Cylinder, length $L$], f-cyl, (
    [$I_"axis" = 1/2 m R^2$],
    [$I_"transv" = 1/4 m R^2 + (m L^2) \/ 12$],
    [thin shell $I_"axis" = m R^2$],
  )),
  card(cB, [Solid cone, height $h$], f-cone, (
    [$I_"axis" = 3/10 m R^2$],
    [$I_"transv" = 3/20 m R^2 + (3 m h^2) \/ 80$],
  )),
))

#v(1.8mm)

// ============================================================
//  FOOTER — composite example
// ============================================================
#block(
  width: 100%,
  fill: rgb("#f4f5f7"),
  stroke: (left: 2.2pt + ink),
  radius: 1.2pt,
  inset: (x: 6pt, y: 3pt),
  {
    set text(size: 6.9pt)
    grid(
      columns: (auto, 1fr, auto),
      column-gutter: 9pt,
      align: (left + horizon, left + horizon, right + horizon),
      text(weight: "bold")[Composite bodies #h(4pt) $I_x = sum_i (overline(I)_i + A_i d_i^2)$],
      [
        T-section, flange $100 times 20$ on web $20 times 80$ (#h(0.15em)total depth 100 mm):
        $A = 3600$ mm², $overline(y) = 67.8$ mm from the base, giving
        $I_x approx 3.14 times 10^6$ mm⁴ (about the base).
      ],
      text(fill: soft)[$d$ = centroid-to-axis distance  #h(8pt) $d = 0$ on a centroidal axis],
    )
  },
)
