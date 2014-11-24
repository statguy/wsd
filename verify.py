#!/usr/bin/python

import sys
import wsd
import random
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.text import *
import nltk

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

corpus_random = [corpus.fileids()[ random.randint(0, len(corpus.fileids())) ] for p in range(0, 100)]
i = 0
for infile in sorted(corpus_random):
  print i, "/", len(corpus_random)
  i += 1
  
  words = corpus.words(infile)
  text = Text(words)
  c = nltk.ConcordanceIndex(text.tokens)
  offsets = c.offsets(focal_word)
  
  for offset in offsets:
    score_max = 0
    senses_max = None
    
    for collocation in collocations:
      tokens = collocation.get_collocation(text, offset)
      if tokens == None: continue
      senses_score = decision_list.get_senses_score(tokens, collocation.index)
      if senses_score == None: continue
      #print senses_score
      
      if score_max < senses_score[1]:
        score_max = senses_score[1]
        senses_max = senses_score[0]
    
    print senses_max, score_max
    if senses_max != None:
      wsd.print_context(text, offset)
