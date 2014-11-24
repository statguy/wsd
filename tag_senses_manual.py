#!/usr/bin/python

import sys
import wsd
import nltk
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.text import *
import csv

if len(sys.argv) != 5:
  print "Usage:", sys.argv[0], "corpus_index word sense1 sense2"
  exit(-1)
corpus_index = int(sys.argv[1])

focal_word = sys.argv[2]
senses = [sys.argv[3], sys.argv[4]]
#focal_word = "plant"
#senses = ["manufacturing","life"]
offset_margin = 10
word_sense_list = []
corpus = PlaintextCorpusReader('outcorpus/', '.*')

quit = False
for infile in sorted(corpus.fileids()[corpus_index:len(corpus.fileids())]):
  words = corpus.words(infile)
  text = Text(words)
  c = nltk.ConcordanceIndex(text.tokens)
  
  offsets = c.offsets(focal_word)
  for offset in offsets:
    print infile
    wsd.print_context(text, offset, offset_margin)
    #context_words = text.tokens[map(lambda x: x-5 if (x-offset_margin) > 0 else 0, [offset])[0]:offset+offset_margin]
    #print context_words
    
    i = 1
    for sense in senses:
      print str(i) + ":", sense
      i += 1
    print "s: skip"
    print "q: quit"
  
    key = ""
    while key != "s":
      key = raw_input("> ")
      if key.isdigit() and int(key) > 0 and int(key) <= len(senses):
        word_sense_list.append( (infile, offset, senses[int(key)-1]) )
        print infile, offset, senses[int(key)-1]
        break
      elif key == "q":
        quit = True
        break
    if quit == True:
      break
  if quit == True:
    break

print word_sense_list

outfile = "senses_" + focal_word + ".csv"
print "Saving to", outfile
with open(outfile, "w") as f:
  writer = csv.writer(f)
  writer.writerows(word_sense_list)
