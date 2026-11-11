# Cheatsheets

One-page reference sheets. Each sheet lives in its own folder with its source
and a compiled PDF next to it.

| Sheet | Covers | Build |
| --- | --- | --- |
| [bravais-lattices](bravais-lattices/) | The 5 two-dimensional and 14 three-dimensional Bravais lattices, with cells drawn from their own lattice parameters | `cd bravais-lattices && make` |
| [moments-of-inertia](moments-of-inertia/) | Second moment of area and mass moment of inertia for common sections and bodies | `cd moments-of-inertia && typst compile moi-cheatsheet.typ` |

Both build to a single A4 landscape page.

## Layout

```
.
├── bravais-lattices/     LaTeX + TikZ, Makefile-driven
└── moments-of-inertia/   Typst + CeTZ
```

## Requirements

- **bravais-lattices** — a TeX Live installation (`pdflatex`, `latexmk`) and
  Python 3 for `gen_cells.py`
- **moments-of-inertia** — Typst 0.15 or newer; CeTZ 0.5.2 is fetched from
  Typst Universe on first build
