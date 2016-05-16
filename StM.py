from numpy import *
import math
import sys
from PIL import Image


def rule():
	print "Please follow the rule:"
	print "\t**********************************"
	print "\t*  python StM.py 105 5 .jpg      *" 
	print "\t**********************************"
	print "The message is random PN series."
	print "The third parameter is the number of picture"
	print "The fourth parameter is embedding rate of %"
	print "The fifth parameter is .png or .jpg"
	
def randomArray(size):
	ret = []
	for i in xrange(size):
		ret.append(random.choice([1, -1]))

	return ret

def gussion_random(size):
	ret = []
	s = size
	while s > 0:
		t = round(random.normal(0, 1.5))
		if abs(t) <= 5:
			s -= 1
			ret.append(t)

	return ret

def parity(x, k):
	m = pow(-1, k)
	c = int(x)/int(k)
	if c % 2: #2ik ~ (2i+1)k-1
		return -m
	else :
		return m #(2i-1)k ~ 2ik-1

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
	coverPixels = array(cover.convert('L'))
	coverWidth, coverHeight = cover.size
	imgSize = coverWidth * coverHeight  #total bytes
	message = randomArray(imgSize*int(rate)/100)

	random_1 = gussion_random(imgSize) #R
	random_2 = gussion_random(imgSize) #S

	tempPixel = []
	for i in range(imgSize):
		tempPixel.append(i)
	#round
	i = 0
	tsize = imgSize - 1
	message_index = 0
	while message_index < len(message):
		#random choise site
		choise = random.randint(0, tsize)
		h = tempPixel[choise]/coverHeight
		w = tempPixel[choise]%coverHeight

		k = abs(random_1[i] - random_2[i])
		x_R = coverPixels[h][w]+random_1[i]
		x_S = coverPixels[h][w]+random_2[i]

		if k == 0:
			temp_pixel = x_R

		else:
			if parity(x_R, k) == message[message_index]:
				temp_pixel = x_R
			elif parity(x_S, k) == message[message_index]:
				temp_pixel = x_S
			else : 
				print "Error!!!"
				print "cover:", coverPixels[h][w]
				print "R:", random_1[i]
				print "S:", random_2[i]
				print "k:", k
				print "p R:", parity(x_R, k)
				print "p S:", parity(x_S, k)
				sys.exit(0)
			message_index += 1

			#overflow
			if temp_pixel > 255:
				t = 255
				while parity(t, k) != parity(temp_pixel, k):
					t -= 1
				coverPixels[h][w] = t
			#underflow
			elif temp_pixel < 0:
				t = 0
				while parity(t, k) != parity(temp_pixel, k):
					t += 1
				coverPixels[h][w] = t
			else : 
				coverPixels[h][w] = temp_pixel
					
		temp = tempPixel[choise]
		tempPixel[choise] = tempPixel[tsize]
		tempPixel[tsize] = temp
		tsize -= 1
		i += 1

	#extract from stm 
	extractMessage = []
	messageCount = 0
	i = 0
	tsize = imgSize - 1
	while messageCount < len(message):
		h = tempPixel[tsize]/coverHeight
		w = tempPixel[tsize]%coverHeight
		k = abs(random_1[i] - random_2[i])

		if k != 0:
			extractMessage.append(parity(coverPixels[h][w], k))
			messageCount += 1

		i += 1
		tsize -= 1
		
	#check info
	if message != extractMessage:
		print "non hit!"
		sys.exit(0)

	#sample pair 
	analysiz(coverPixels, coverWidth, coverHeight)

	#save image
	result = Image.fromarray(coverPixels)
	result.save('stm/' + str(filename) + '_' + rate + f_format)
	

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
