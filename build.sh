#!/bin/bash
python3 to_latex.py > laulut.tex && \
pdflatex laulukirja.tex && \
pdflatex laulukirja.tex && \
pdflatex laulukirja.tex