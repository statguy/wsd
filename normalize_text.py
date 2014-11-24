#!/usr/bin/python
import sys
from os import listdir
from os.path import isfile, join
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import *
from nltk.stem.porter import *

if len(sys.argv) != 3:
  print "Usage:", sys.argv[0], "in_dir out_dir"
  exit(-1)

in_dir = sys.argv[1]
out_dir = sys.argv[2]
filenames = [join(in_dir, f) for f in listdir(in_dir) if isfile(join(in_dir, f))]

is_text = False
text = ""
corpus_index = 1
tokenizer = RegexpTokenizer(r'\w+')
stemmer = PorterStemmer()

def extract_text(line):
  global is_text, text, corpus_index, tokenizer, stemmer
  if line.startswith("<TEXT>"):
    is_text = True
  elif line.startswith("</TEXT>"):
    tokens = tokenizer.tokenize(text)
    
    #stop = set(stopwords.words("english"))
    #words = [w for w in tokens if w not in stop]
    
    #words_stemmed = []
    #for word in words:
    #  words_stemmed.append(stemmer.stem(word))

    #final_text = ' '.join(words_stemmed)
    final_text = ' '.join(tokens)
    #print final_text # FOR debugging
    
    if len(final_text) > 0:
      out_file = open(join(out_dir, "corpus" + str(corpus_index)), "w")
      out_file.write(final_text)
      out_file.close()
      
    is_text = False
    text = ""
    corpus_index += 1
  elif is_text == True:
    text = text + line.strip().lower() + " "
  return None

for filename in sorted(filenames):
  print filename
  [extract_text(line) for line in open(filename)]
#filename = filenames[0]
#[extract_text(line) for line in open(filename)]
