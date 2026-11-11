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
	latexmk -c $(MAIN).tex
	latexmk -c bravais-desk.tex

distclean: clean
	rm -f $(MAIN).pdf bravais-desk.pdf

preview: all
	pdftoppm -png -r 72 -singlefile $(MAIN).pdf preview-poster
	pdftoppm -png -r 60 -singlefile bravais-desk.pdf preview-desk-1 -f 1 -l 1
	pdftoppm -png -r 60 -singlefile bravais-desk.pdf preview-desk-2 -f 2 -l 2

.PHONY: all poster desk clean distclean preview
