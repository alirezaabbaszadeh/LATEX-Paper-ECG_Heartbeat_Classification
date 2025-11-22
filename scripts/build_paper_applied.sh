#!/usr/bin/env bash
set -euo pipefail

# Build the applied sciences paper without requiring a preinstalled TeX Live.
# A portable TinyTeX distribution is bootstrapped into .cache/tinytex on first use.

SCRIPT_DIR=$(cd -- "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)
PAPER_DIR="$REPO_ROOT/paper-applied/src"
OUTPUT_DIR="$PAPER_DIR/output"
CACHE_DIR="$REPO_ROOT/.cache/tinytex"
TINY_ROOT="$CACHE_DIR/.TinyTeX"
HOME_TINY="$HOME/.TinyTeX"

mkdir -p "$OUTPUT_DIR"

find_tex_binary() {
  find "$CACHE_DIR" "$TINY_ROOT" "$HOME_TINY" -maxdepth 3 -type f -name "$1" 2>/dev/null | head -n 1
}

PDFLATEX_CMD=${PDFLATEX_CMD:-}
LATEXMK_CMD=${LATEXMK_CMD:-}
BIBTEX_CMD=${BIBTEX_CMD:-}
TLMGR_CMD=${TLMGR_CMD:-}

if [ -z "$PDFLATEX_CMD" ] && command -v pdflatex >/dev/null 2>&1; then
  PDFLATEX_CMD=$(command -v pdflatex)
fi

if [ -z "$PDFLATEX_CMD" ]; then
  PDFLATEX_CMD=$(find_tex_binary pdflatex || true)
fi

if [ -z "$PDFLATEX_CMD" ]; then
  echo "Installing portable TinyTeX into $CACHE_DIR ..."
  mkdir -p "$CACHE_DIR"
  tmp_tar=$(mktemp)
  curl -fsSL https://github.com/rstudio/tinytex-releases/releases/download/daily/TinyTeX-1.tar.gz -o "$tmp_tar"
  tar -xzf "$tmp_tar" -C "$CACHE_DIR"
  rm "$tmp_tar"
  PDFLATEX_CMD=$(find_tex_binary pdflatex)
fi

TLMGR_CMD=${TLMGR_CMD:-$(find_tex_binary tlmgr || true)}
LATEXMK_CMD=${LATEXMK_CMD:-$(find_tex_binary latexmk || true)}
BIBTEX_CMD=${BIBTEX_CMD:-$(find_tex_binary bibtex || true)}

if [ -z "$TLMGR_CMD" ] && [ -x "$HOME_TINY/bin/x86_64-linux/tlmgr" ]; then
  TLMGR_CMD="$HOME_TINY/bin/x86_64-linux/tlmgr"
fi

if [ -n "$TLMGR_CMD" ]; then
  echo "Using tlmgr at: $TLMGR_CMD (installing core LaTeX packages)"
  TLMGR_FLAGS="--verify-repo=none"
  "$TLMGR_CMD" $TLMGR_FLAGS option repository http://mirrors.ctan.org/systems/texlive/tlnet >/dev/null || true
  CORE_PKGS="latexmk fancyhdr grfext graphics lastpage tabto-ltx colortbl pbox ragged2e tocloft marginnote marginfix enotez xstring translations soul microtype natbib siunitx booktabs enumitem xcolor float hyperref lineno setspace etoolbox titlesec multirow caption subfig pgf amsfonts amsmath epstopdf-pkg footmisc was frankenstein koma-script"
  "$TLMGR_CMD" $TLMGR_FLAGS install $CORE_PKGS >/dev/null || true
  LATEXMK_CMD=${LATEXMK_CMD:-$(find_tex_binary latexmk || true)}
  BIBTEX_CMD=${BIBTEX_CMD:-$(find_tex_binary bibtex || true)}
fi

if [ -z "$BIBTEX_CMD" ]; then
  BIBTEX_CMD=$(command -v bibtex || true)
fi

if [ -z "$PDFLATEX_CMD" ]; then
  echo "Error: pdflatex not found and TinyTeX installation failed." >&2
  exit 1
fi

echo "Using pdflatex at: $PDFLATEX_CMD"
cd "$PAPER_DIR"

if [ -n "$LATEXMK_CMD" ]; then
  echo "Running latexmk..."
  "$LATEXMK_CMD" -shell-escape -pdf -interaction=nonstopmode -halt-on-error -outdir="$OUTPUT_DIR" main.tex
else
  echo "Running manual pdflatex/bibtex sequence..."
  "$PDFLATEX_CMD" -interaction=nonstopmode -halt-on-error -shell-escape -output-directory "$OUTPUT_DIR" main.tex
  if [ -n "$BIBTEX_CMD" ]; then
    (cd "$OUTPUT_DIR" && "$BIBTEX_CMD" main || true)
  fi
  "$PDFLATEX_CMD" -interaction=nonstopmode -halt-on-error -shell-escape -output-directory "$OUTPUT_DIR" main.tex
  "$PDFLATEX_CMD" -interaction=nonstopmode -halt-on-error -shell-escape -output-directory "$OUTPUT_DIR" main.tex
fi

echo "Build complete: $OUTPUT_DIR/main.pdf"
