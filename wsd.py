import abc
import math
import operator
import csv
from collections import defaultdict

class DecisionList(object):
  def __init__(self):
    self.decision_items = defaultdict(float)
  
  def add_sense(self, sense, collocation, collocation_object_index, score):
    key = ",".join([sense, collocation, str(collocation_object_index)])
    self.decision_items[key] = score # Overwrite if the key already exists
  
  def save(self, outfile):
    x = sorted(self.decision_items.items(), key=operator.itemgetter(1), reverse=True)
    y = []
    for key, value in x:
      y.append( key.split(",") + [str(value)] )
    with open(outfile, "w") as f:
      writer = csv.writer(f)
      writer.writerows(y)
      
  def load(self, infile):
    with open(infile) as senses_file:
      reader = csv.reader(senses_file)
      for row in reader:
        sense, collocation, collocation_object_index, score = row
        self.add_sense(sense, collocation, collocation_object_index, float(score))
        
  def get_sense(self, tokens, collocation_object_index):
    sense = None
    score_max = 0
    
    for token in tokens:
      kv = { k:v for k,v in self.decision_items.iteritems() if k.endswith(",".join(["", token, str(collocation_object_index)])) }
      if len(kv) == 0 or len(kv) > 1: continue # No sense found or ambiguous sense
      key, score = kv.items()[0]
      if score > score_max:
        score_max = score
        sense,_,_ = key.split(",")
      #print kv.items()[0]
    #print "-----"
    return sense
    
  def get_senses_score(self, tokens, collocation_object_index):
    score_max = 0
    senses_max = None
    
    for token in tokens:
      #kv = { k:v for k,v in self.decision_items.iteritems() if ",".join(["", token, ""]) in k }
      kv = { k:v for k,v in self.decision_items.iteritems() if k.endswith(",".join(["", token, str(collocation_object_index)])) }
      if len(kv) == 0: return None # No sense assigned
      keys, scores = kv.keys(), kv.values()
      senses = [x.split(",")[0] for x in keys]
      if scores[0] > score_max:
        score_max = scores[0]
        senses_max = senses
    
    return [ senses_max, score_max ]
    

class Collocation(object):
  __metaclass__ = abc.ABCMeta
  
  def __init__(self, senses, index):
    self.frequencies = defaultdict(defaultdict)
    self.index = index
    for sense in senses:
      self.frequencies[sense] = defaultdict(int)
  
  @abc.abstractmethod
  def get_collocation(self, text, offset):
    pass
  
  def add_collocation(self, text, offset, sense):
    tokens = self.get_collocation(text, offset)
    if tokens == None: return
    for token in tokens:
      self.frequencies[sense][token] += 1
  
  def update_decision_list(self, decision_list):
    sense_a = self.frequencies.items()[0][0]
    sense_b = self.frequencies.items()[1][0]
    
    for collocation_a, frequency_a in self.frequencies.items()[0][1].items():
      frequency_b = next((frequency_b for collocation_b, frequency_b in self.frequencies.items()[1][1].items() if collocation_a == collocation_b), 1e-1)
      frequency_a = float(frequency_a)
      frequency_b = float(frequency_b)
      total = frequency_a + frequency_b
      logl = abs(math.log((frequency_a/total) / (frequency_b/total)))
      decision_list.add_sense(sense_a, collocation_a, self.index, logl)

    for collocation_b, frequency_b in self.frequencies.items()[1][1].items():
      frequency_a = next((frequency_a for collocation_a, frequency_a in self.frequencies.items()[0][1].items() if collocation_a == collocation_b), 1e-1)
      frequency_a = float(frequency_a)
      frequency_b = float(frequency_b)
      total = frequency_a + frequency_b
      logl = abs(math.log((frequency_a/total) / (frequency_b/total)))
      decision_list.add_sense(sense_b, collocation_b, self.index, logl)

class BigramLeft(Collocation):
  def get_collocation(self, text, offset):
    if offset == 0:
      return None
    return [text.tokens[offset-1]]

class BigramRight(Collocation):
  def get_collocation(self, text, offset):
    if offset >= len(text.tokens) - 1:
      return None
    return [text.tokens[offset+1]]

class BigramScope(Collocation):
  def __init__(self, senses, index, scope):
    super(self.__class__, self).__init__(senses, index)
    self.scope = scope
    
  def get_collocation(self, text, offset):
    scope_left = [max(offset - self.scope[1], 0), offset - self.scope[0]]
    if offset - scope_left[0] < self.scope[0]: scope_left = [-1, -1]
    scope_right = [offset + self.scope[0], min(offset + self.scope[1], len(text.tokens) - 1)]
    if scope_right[1] - offset < self.scope[1]: scope_right = [-1, -1]
    
    tokens = []
    for i in range(scope_left[0], scope_left[1] + 1) + range(scope_right[0], scope_right[1] + 1):
      tokens += [text.tokens[i]]  
    tokens = list(set(tokens)) # Remove duplicates
    return tokens


def print_context(text, offset, offset_margin=20):
  print text.tokens[map(lambda x: x-5 if (x-offset_margin) > 0 else 0, [offset])[0]:offset+offset_margin]
  
