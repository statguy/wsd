#!/usr/bin/python
import sys
import csv
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.text import *
import wsd

if len(sys.argv) != 4:
  print "Usage:", sys.argv[0], "word sense1 sense2"
  exit(-1)

corpus = PlaintextCorpusReader('outcorpus/', '.*')
focal_word = sys.argv[1]
senses = [sys.argv[2], sys.argv[3]]
#senses = ["manufacturing","life"]
collocations = [ wsd.BigramLeft(senses, 0), wsd.BigramRight(senses, 1), wsd.BigramScope(senses, 2, [2, 10]) ]

with open("senses_" + focal_word + ".csv") as senses_file:
  reader = csv.reader(senses_file)
  for row in reader:
    infile, offset, sense = row
    offset = int(offset)
    words = corpus.words(infile)
    text = Text(words)
    
    for collocation in collocations:
      collocation.add_collocation(text, offset, sense)


#print collocations[0].frequencies.items()[0][1].items()[0][1]

decision_list = wsd.DecisionList()
print collocations[0].frequencies
print collocations[0].update_decision_list(decision_list)
print decision_list.decision_items
print ""
print collocations[1].frequencies
print collocations[1].update_decision_list(decision_list)
print decision_list.decision_items
print ""
print collocations[2].frequencies
print collocations[2].update_decision_list(decision_list)
print decision_list.decision_items
decision_list.save("senses_bootstrap_" + focal_word + ".csv")
