#!/usr/bin/python
import sys

if len(sys.argv) != 2:
  print "Usage:", sys.argv[0], "file"
  exit(-1)

filename = sys.argv[1]
lines = [line.strip() for line in open(filename)]
list = ','.join('"' + str(x) + '"' for x in lines)
print list
