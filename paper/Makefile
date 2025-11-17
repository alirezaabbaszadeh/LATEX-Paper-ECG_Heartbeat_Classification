.PHONY: bspc cbm all clean

BIB=references

all: bspc

# BSPC build
bspc:
	cd bspc && pdflatex -interaction=nonstopmode bspc_main.tex \
	&& bibtex bspc_main \
	&& pdflatex -interaction=nonstopmode bspc_main.tex \
	&& pdflatex -interaction=nonstopmode bspc_main.tex

# CBM build
cbm:
	cd cbm && pdflatex -interaction=nonstopmode cbm_main.tex \
	&& bibtex cbm_main \
	&& pdflatex -interaction=nonstopmode cbm_main.tex \
	&& pdflatex -interaction=nonstopmode cbm_main.tex

clean:
	find . -type f -regex '.*\\.(aux|log|out|bbl|blg|toc|synctex.gz)' -delete
