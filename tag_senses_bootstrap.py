#!/usr/bin/python
import sys
import wsd
import nltk
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.text import *

if len(sys.argv) != 4:
  print "Usage:", sys.argv[0], "word sense1 sense2"
  exit(-1)

focal_word = sys.argv[1]
senses = [sys.argv[2], sys.argv[3]]
#focal_word = "plant"
#senses = ["manufacturing","life"]
corpus = PlaintextCorpusReader('outcorpus/', '.*')
collocations = [ wsd.BigramLeft(senses, 0), wsd.BigramRight(senses, 1), wsd.BigramScope(senses, 2, [2, 10]) ]
decision_list = wsd.DecisionList()
decision_list.load("senses_bootstrap_" + focal_word + ".csv")    

i = 0
for infile in sorted(corpus.fileids()):
  print i, "/", len(corpus.fileids())
  i += 1
  
  words = corpus.words(infile)
  text = Text(words)
  c = nltk.ConcordanceIndex(text.tokens)
  offsets = c.offsets(focal_word)
  
  for offset in offsets:
    for collocation in collocations:
      tokens = collocation.get_collocation(text, offset)
      if tokens == None: continue
      sense = decision_list.get_sense(tokens, collocation.index)
      if sense == None: continue
      collocation.add_collocation(text, offset, sense)
      collocation.update_decision_list(decision_list)
      #decision_list.add_sense(sense, tokens, collocation.index, score)
      print sense

decision_list.save("senses_bootstrap_" + focal_word + ".csv")

