#!/bin/sh

INCORPUS=corpus
OUTCORPUS=outcorpus
WORD=plant
SENSES=manufacturing life

./normalize_text.py "$INCORPUS" "$OUTCORPUS"
./tag_sense_manual.py "$OUTCORPUS" "$WORD" "$SENSES"
./find_collocations.py "$WORD" "$SENSES"
./tag_senses_bootstrap.py "$WORD" "$SENSES"
./verify.py "$WORD" "$SENSES"
