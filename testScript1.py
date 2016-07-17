#!/usr/bin/python
import RPi.GPIO as GPIO
import datetime
import time
import ephem
import serial

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#init  pins for the relay, these will need to be labeled on the outlets for easy hookup
lightRelay = 2
GPIO.setup(lightRelay,GPIO.OUT)
GPIO.output(lightRelay,GPIO.HIGH)

pumpRelay = 3
GPIO.setup(pumpRelay,GPIO.OUT)
GPIO.output(pumpRelay,GPIO.HIGH)

fanRelay = 4
GPIO.setup(fanRelay,GPIO.OUT)
GPIO.output(fanRelay,GPIO.HIGH)

#LED Pins setup and initalization
red = 25
GPIO.setup(red, GPIO.OUT)
RED = GPIO.PWM(red, 100)
RED.start(0)

green = 24
GPIO.setup(green, GPIO.OUT)
GREEN = GPIO.PWM(green, 100)
GREEN.start(0)

blue = 23
GPIO.setup(blue, GPIO.OUT)
BLUE = GPIO.PWM(blue, 100)
BLUE.start(0)

arduino = serial.Serial('/dev/ttyS0', 9600)

#### TODO ##### Prompt user for desired grow city. Need to find API to covert city to GPS coords
growLocation = ephem.Observer()
growLocation.lat = '47.060045' 
growLocation.lon = '-122.9286967'
growLocation.elevation = 95

sun = ephem.Sun()
sunrise = growLocation.next_rising(sun)
sunset = growLocation.next_setting(sun)
sunriseNautical = growLocation.next_rising(sun)
sunsetNautical = growLocation.next_setting(sun)

#This number changes depending upon stage of growth generally between 70 and 40%
targetRoomHumidity = 70	
currentRoomHumidity = 0
#26-30 deg C generally.
targetRoomTemp = 28
currentRoomTemp = 0
#readings between 541 when fully sumberged and 1023 when dry, do not know what this value should be
targetSoilMoisture = 895
currentSoilMoisture = 0
#Photosynthisis of CO2 no longer occurs over 35 C
DANGERTEMP = 35.

#length to sleep between each poll
SleepTimeL = 2

task = "none"

def setColor(rgb = []):
	#convert 0-255 range to 0-100.
	rgb = [(x / 255.0)*100 for x in rgb]
	RED.ChangeDutyCycle(rgb[0])
	GREEN.ChangeDutyCycle(rgb[1])
	BLUE.ChangeDutyCycle(rgb[2])

def roomTemp():
	arduino.write('1'.encode())
	data = float(arduino.readline().strip())
	if data:
		currentRoomTemp = data
		print (currentRoomTemp)
	return

def roomHumid():
	arduino.write('2'.encode())
	data = float(arduino.readline().strip())
	if data:
		currentRoomHumidity = data
		print (currentRoomHumidity)
	return

def soilMoisture():
	arduino.write('3'.encode())
	data = int(arduino.readline().strip())
	if data:
		currentSoilMoisture = data
		if currentSoilMoisture > targetSoilMoisture:
			GPIO.output(pumpRelay, GPIO.LOW)
		elif currentSoilMoisture <= targetSoilMoisture:
			GPIO.output(pumpRelay, GPIO.HIGH)
		print (currentSoilMoisture)
	return

while True:
	roomTemp()
	roomHumid()
	soilMoisture()