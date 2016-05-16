import numpy
import random
import sys
import math
from PIL import Image


def rule():
	print "Please follow the rule:"
	print "\t**********************************"
	print "\t*  python LSB.py Lena_Gray.tiff  *" 
	print "\t**********************************"
	print "The message is random PN series."
	print "The third parameter is embedding rate of %"
	print "If you want to execute more times, please add times at fourth parameter."

def analysiz(coverPixels, coverWidth, coverHeight):

	X = 0
	Y = 0
	Z = 0
	W = 0
	V = 0

	for h in xrange(coverHeight):
		for w in xrange(coverWidth):
			if w % 2 : continue

			f = coverPixels[h][w]
			b = coverPixels[h][w+1]

			if f < b:
				if b % 2 :
					Y += 1
					if ((b-f) == 1) : W += 1
					else : V += 1
				else : X += 1

			elif f > b:
				if b % 2 : X += 1
				else :
					Y += 1 
					if ((f-b) == 1) : W += 1
					else : V += 1

			else : Z += 1

	doublea = W + Z
	b = 2*X - (X + Y + Z)
	c = Y - X
	Discriminant = b*b - 2*doublea*c
	#print X, " ", Y

	if Discriminant < 0:
		Discriminant = 0
		print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	else:
		rate1 = (-b + math.sqrt(Discriminant)) / doublea
		rate2 = (-b - math.sqrt(Discriminant)) / doublea
		if max(rate1, rate2) >= 1:
			answer = max(0, min(rate1, rate2))
		else: 
			answer = max(0, max(rate1, rate2))
		print answer
	
if len(sys.argv) < 4: 
	rule()
	sys.exit(0) 

elif len(sys.argv) == 4:
	if(sys.argv[1].isdigit()):
		i = 1
		t = int(sys.argv[1])
		while i < t + 1:
			filename = 't/' + str(i) + '_' + sys.argv[2] + sys.argv[3]
			#filename = 'sample/' + str(i) + sys.argv[3]
			cover = Image.open(filename)
			coverPixels = numpy.array(cover.convert('L'))
			coverWidth, coverHeight = cover.size
			analysiz(coverPixels, coverWidth, coverHeight)
			i += 1

	else:
		rule()
		sys.exit(0)
else:
	rule()
	sys.exit(0)
