VENV_DIR = ./venv
VENV_SENTINEL = $(VENV_DIR)/.venv-done

PYTHON = $(VENV_DIR)/bin/python

BUILD_DIR = ./build
AUXDIR = ./aux
TIKZ_DIR = $(BUILD_DIR)/tikz

ALL_PY = $(wildcard *.py)
ALL_TIKZ_PY = $(wildcard *.tikz.py)
ALL_TIKZ = $(ALL_TIKZ_PY:.tikz.py=.tikz)
ALL_PGF_PY = $(wildcard *.pgf.py)
ALL_PGF = $(ALL_PGF_PY:.pgf.py=.pgf)

all: $(BUILD_DIR)/main.pdf

venv: $(VENV_SENTINEL)

$(TIKZ_DIR):
	mkdir -p $(TIKZ_DIR)

$(VENV_SENTINEL): requirements.txt
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	$(PYTHON) -m pip install -Ur requirements.txt
	touch $(VENV_SENTINEL)

$(BUILD_DIR)/main.pdf: main.tex $(ALL_TIKZ) $(ALL_PGF) $(ALL_PY) $(VENV_SENTINEL) | $(TIKZ_DIR)
	latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode" -shell-escape -halt-on-error -use-make -interaction=nonstopmode -synctex=1 -file-line-error -jobname=main -outdir=$(BUILD_DIR) -auxdir=$(AUXDIR) main.tex

%.tikz: %.tikz.py venv
	$(PYTHON) $< 1> $@ 2>&2 || (rm -f $@ && false)

%.pgf: %.pgf.py venv
	$(PYTHON) $<

clean:
	-latexmk -c
	-rm -rf $(BUILD_DIR)
	-rm -rf $(AUXDIR)
	-rm -f $(ALL_TIKZ)
	-rm -f $(ALL_PGF)

clean-venv:
	-rm -rf $(VENV_DIR)
	-rm -f $(VENV_SENTINEL)
	-rm -rf __pycache__

.PHONY: clean clean-venv venv all