from numpy import *

def parity(x, k):
	m = pow(-1, k)
	print "m:", m
	c = x/k
	if c % 2: #2ik ~ (2i+1)k
		return -m
	else :
		return m #(2i-1)k ~ 2ik

c = 32
R = -1
S = 3


print parity(c+R, abs(R-S))
print parity(c+S, abs(R-S))
