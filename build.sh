#!/bin/bash
python3 to_latex.py ordering.csv songs/ > laulut.tex && \
pdflatex laulukirja.tex && \
pdflatex laulukirja.tex && \
pdflatex laulukirja.tex
