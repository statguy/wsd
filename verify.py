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
corpus_ids = corpus.fileids()
random.shuffle(corpus_ids)

num_words = 1
num_words_max = 100
tagged = 0
ambiguous = 0
unknown = 0

for infile in corpus_ids:
  if num_words > num_words_max: break

  words = corpus.words(infile)
  text = Text(words)
  c = nltk.ConcordanceIndex(text.tokens)
  offsets = c.offsets(focal_word)
  
  if len(offsets) > 0:
    offset = random.choice(offsets)
    print num_words, "/", num_words_max
    num_words += 1
    score_max = 0
    senses_max = None
    ambiguous_max = False
    
    for collocation in collocations:
      tokens = collocation.get_collocation(text, offset)
      if tokens == None: continue
      senses_score = decision_list.get_senses_score(tokens, collocation.index)
      if senses_score == None: continue
      #print senses_score
      
      if score_max < senses_score[1]:
        score_max = senses_score[1]
        senses_max = senses_score[0]
        ambiguous_max = senses_score[2]
    
    if senses_max == None:
      unknown += 1
    else:
      if ambiguous_max == True:
        ambiguous += 1
      else:
        tagged += 1

    print senses_max, score_max, "ambiguous = ", ambiguous_max
    wsd.print_context(text, offset)

  if len(offsets) > 0:
    print "--------------------------------------------------------"

print "Tagged =", tagged, "ambiguous =", ambiguous, "unknown =", unknown
