import numpy
import random
import sys
import math
from PIL import Image


def rule():
	print "Please follow the rule:"
	print "\t**********************************"
	print "\t*  python LSB.py 105 5 .jpg      *" 
	print "\t**********************************"
	print "The message is random PN series."
	print "The third parameter is the number of picture"
	print "The fourth parameter is embedding rate of %"
	print "The fifth parameter is .png or .jpg"
	
def randomArray(size):
	ret = []
	for i in xrange(size):
		ret.append(random.choice([1, 0]))

	return ret

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

def hidemessage(filename, rate, f_format):
	fname = "sample/" + str(filename) + f_format
	cover = Image.open(fname)
	coverPixels = numpy.array(cover.convert('L'))
	coverWidth, coverHeight = cover.size
	imgSize = coverWidth * coverHeight  #total bytes
	message = randomArray(imgSize*int(rate)/100)

	#print message

	#for random choice
	tempPixel = []
	for i in range(imgSize):
		tempPixel.append(i)

	#LSB
	tsize = imgSize - 1
	messageCount = 0
	while messageCount < len(message):
		choise = random.randint(0, tsize)
		h = tempPixel[choise]/coverHeight
		w = tempPixel[choise]%coverHeight
		coverPixels[h][w] = coverPixels[h][w] & 0xfe | message[messageCount]
		temp = tempPixel[choise]
		tempPixel[choise] = tempPixel[tsize]
		tempPixel[tsize] = temp
		tsize -= 1
		messageCount += 1

	#extract from lsb
	extractMessage = []
	messageCount = 0
	tsize = imgSize - 1
	while messageCount < len(message):
		h = tempPixel[tsize]/coverHeight
		w = tempPixel[tsize]%coverHeight
		extractMessage.append(coverPixels[h][w] & 1)
		tsize -= 1
		messageCount += 1
		
	#check info
	if message != extractMessage:
		print "non hit!"
		sys.exit(0)
	
	#sample pair 
	analysiz(coverPixels, coverWidth, coverHeight)

	#save image
	result = Image.fromarray(coverPixels)
	result.save('t/' + str(filename) + '_' + rate + f_format)
		
if len(sys.argv) < 4: 
	rule()
	sys.exit(0) 

elif len(sys.argv) == 4:
	if(sys.argv[1].isdigit()):
		i = 1
		s = 0
		t = int(sys.argv[1])
		while i < t + 1:
			hidemessage(i, sys.argv[2], sys.argv[3])
			i += 1

	else:
		rule()
		sys.exit(0)
else:
	rule()
	sys.exit(0)
	
