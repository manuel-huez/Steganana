# Steganana.py

import os, time
from PIL import Image

class Steganana:

	def __init__(self, file):
		print('Steganana instance launched')
		self.file = file
		try:
			self.image = Image.open(file)
			self.image.load()
		except:
			print('Unable to load the image')
			exit(2)

	def encode(self, text, output):
		print('Encoding...')

		if(output == None):
			output = 'output.png'

		binaryString = self.getBinaryString(text)

		for y in range(0, self.image.size[1]):
			for x in range(0, self.image.size[0]):
				r = self.image.getpixel((x, y))[0]
				g = self.image.getpixel((x, y))[1]
				b = self.image.getpixel((x, y))[2]
				a = self.image.getpixel((x, y))[3]
				i = 0
				while i < 3 and len(binaryString) > 0:
					if(i == 0):
						r = self.manageOddEven(r, binaryString[0])
					elif(i == 1):
						g = self.manageOddEven(r, binaryString[0])
					elif(i == 2):
						b = self.manageOddEven(r, binaryString[0])
					binaryString = binaryString[1:]
					i += 1
				self.image.putpixel((x, y), (r, g, b, a))

		self.image.save(output)
		print "Saved!"

	def decode(self):
		print('Decoding...')

		decoded = ''
		curChar = ''

		for y in range(0, self.image.size[1]):
			for x in range(0, self.image.size[0]):
				curColor = self.image.getpixel((x, y))
				curChar += str(int(curColor[0] % 2 == 1))
				curChar += str(int(curColor[1] % 2 == 1))
				curChar += str(int(curColor[2] % 2 == 1))

				if(curChar[:8] == '00000000'):
					return decoded
				if(len(curChar) >= 8):
					decoded += self.bin2char(curChar[:8])
					curChar = curChar[8:]

		return decoded

	def test(self):
		print('Showing up the pixels')
		for y in range(0, 10):
			for x in range(0, 10):
				print self.image.getpixel((x, y))

	def getBinaryString(self, text):
		binaryString    = ''
		curTextPosition = 0

		while(curTextPosition < len(text)):
			curChar          = text[curTextPosition]
			curTextPosition += 1

			binaryString += self.char2bin(curChar)

		print binaryString

		return binaryString + '00000000'

	def formatBin(self, i, clen):
		i = i.replace('0b', '')

		while len(i) < clen:
			i = '0' + i
		return i

	def char2bin(self, i):
		return self.formatBin(bin(ord(i)), 8)

	def bin2char(self, i):
		return chr(int(i, base=2))

	def makeOdd(self, number):
		return number | 1

	def makeEven(self, number):
		return number & ~1

	def manageOddEven(self, number, base):
		if(base == '0'):
			return self.makeEven(number)
		else:
			return self.makeOdd(number)
