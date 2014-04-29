from basedevice import BaseDevice as BD
from basedevice import View
import json
import time
import RPi.GPIO as GPIO

class Mod(BD):
	def __init__(self, index, type, name, connectionString):
		BD.__init__(self, index, type, name, connectionString)
		self.views.append(View('EMW200R_remote', 'Remote'))
		self.on = "1111"
		self.off = "1110"
		self.one = "0111"
		self.two = "1011"
		self.three = "1101"
		# self.four = "1110"
		self.pone = "10001110"
		self.pzero = "10001000"
		self.GPIOPin = 11

	def viewcommand(self, command, data):
		if command == 'remoteon':
			return self.transmit('On')
		elif command == 'remoteoff':
			return self.transmit('Off')

	def transmit(self, command):
		print self.conStr
		csDict = dict(entry.split('=') for entry in self.conStr.split(';'))
		set = csDict['set']
		socket = csDict['socket']
		
		# Build up the sequence to send
		seq = ""
		if set == "A":
			seq += self.getsequence(self.one)
		elif set == "B":
			seq += self.getsequence(self.two)
		elif set == "C":
			seq += self.getsequence(self.three)
		elif set == "D":
			seq += self.getsequence(self.four)
			
		if socket == "1":
			seq += self.getsequence(self.one)
		elif socket == "2":
			seq += self.getsequence(self.two)
		elif socket == "3":
			seq += self.getsequence(self.three)
			
		if command == "On":
			seq += self.getsequence(self.on)
		elif command == "Off":
			seq += self.getsequence(self.off)
		
		GPIO.setmode(GPIO.BOARD)
		#GPIO.setwarnings(False)
		GPIO.setup(self.GPIOPin, GPIO.OUT)

		# Repeat 10 times to make sure the sequence goes through
		for repeat in range(10):
			for c in seq:
				if c == "1":
					GPIO.output(self.GPIOPin, GPIO.HIGH)
				else:
					GPIO.output(self.GPIOPin, GPIO.LOW)
				time.sleep(0.0002)
			
			# End sequences
			GPIO.output(self.GPIOPin, GPIO.HIGH)
			time.sleep(0.0002)
			GPIO.output(self.GPIOPin, GPIO.LOW)
			time.sleep(0.00964)
		GPIO.cleanup()

	def getsequence(self, s):
		seq = ""
		for c in s:
			if c == "1":
				seq += self.pone
			else:
				seq += self.pzero
		return seq