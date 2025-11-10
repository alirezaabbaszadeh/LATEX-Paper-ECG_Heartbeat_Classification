.PHONY: bspc cbm all clean

BIB=references

all: bspc

# BSPC build
bspc:
	cd bspc && pdflatex -interaction=nonstopmode bspc_main.tex \n	&& bibtex bspc_main \n	&& pdflatex -interaction=nonstopmode bspc_main.tex \n	&& pdflatex -interaction=nonstopmode bspc_main.tex

# CBM build
cbm:
	cd cbm && pdflatex -interaction=nonstopmode cbm_main.tex \n	&& bibtex cbm_main \n	&& pdflatex -interaction=nonstopmode cbm_main.tex \n	&& pdflatex -interaction=nonstopmode cbm_main.tex

clean:
	find . -type f -regex '.*\\.(aux|log|out|bbl|blg|toc|synctex.gz)' -delete
