# Bravais lattice reference sheet
#
#   make          build both sheets
#   make poster   A3 portrait wall sheet
#   make desk     A3 landscape desk copy
#   make clean    remove intermediate files

MAIN = bravais-lattices

all: $(MAIN).pdf bravais-desk.pdf

poster: $(MAIN).pdf

cells.tex: gen_cells.py
	python3 gen_cells.py poster

cells-desk.tex: gen_cells.py
	python3 gen_cells.py desk

$(MAIN).pdf: $(MAIN).tex cells.tex
	latexmk -pdf -interaction=nonstopmode $(MAIN).tex

bravais-desk.pdf: bravais-desk.tex $(MAIN).tex cells-desk.tex
	latexmk -pdf -interaction=nonstopmode bravais-desk.tex

desk: bravais-desk.pdf

clean:
	latexmk -C $(MAIN).tex
	latexmk -C bravais-desk.tex

.PHONY: all poster desk clean
