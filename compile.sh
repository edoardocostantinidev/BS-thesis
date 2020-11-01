#!/bin/sh
#
# Esempio di uso della class phddiauniroma3
# (C) 2006, Franco Milicchio
#

# PDF, immagini in PDF
LATEX=pdflatex

# PS, immagini in EPS
#LATEX=latex

BIBTEX=bibtex
MAKEINDEX=makeindex

$LATEX main
$BIBTEX main
$LATEX main
$MAKEINDEX main
$LATEX main
$LATEX main
