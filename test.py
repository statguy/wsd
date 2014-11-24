#!/usr/bin/python

scope = [2,10]
offset = 20
lentext = 30

scope = [1,1]

scope_left = [max(offset - scope[1], 0), offset - scope[0]]
print scope_left
if offset - scope_left[0] < scope[0]: scope_left = [0, 0]
print scope_left
print "---"

scope_right = [offset + scope[0], min(offset + scope[1], lentext - 1)]
print scope_right
if scope_right[1] - offset < scope[0]: scope_right = [0, 0]
print scope_right

print "---"
print range(scope_left[0], scope_left[1] + 1) + range(scope_right[0], scope_right[1] + 1)

#for i in [scope_left, scope_right]:
#  self.add_tokens(text.tokens[i], sense)
