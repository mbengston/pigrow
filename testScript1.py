#!/usr/bin/python
import RPi.GPIO as GPIO
from pymongo import MongoClient
import ephem
import serial
import datetime
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#init  pins for the relay, these will need to be labeled on the outlets for easy hookup
lightRelay = 9
GPIO.setup(lightRelay,GPIO.OUT)
GPIO.output(lightRelay,GPIO.HIGH)

pumpRelay = 10
GPIO.setup(pumpRelay,GPIO.OUT)
GPIO.output(pumpRelay,GPIO.HIGH)

fanRelay = 22
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

daylight = 0

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

client = MongoClient('mongodb://localhost:27017/')
db = client['local']
collection = db['local']
startlog = db.startup_log
startlog.find_one()

#define some CRUD
def dbInsert(recTime,roomT,roomH,soilM,lights):
	db.sensorpolls.insert_one(
		{
			"time": recTime,
			"roomtemperature": roomT,
			"roomhumidity": roomH,
			"soilmoisure": soilM,
			"lights": lights
		}	
	)	

def pinControl(arg, state):
	if state == 1:
		GPIO.output(arg, GPIO.LOW)
	elif state == 0:
		GPIO.output(arg, GPIO.HIGH)
	return

def setColor(rgb = []):
	#convert 0-255 range to 0-100.
	rgb = [(x / 255.0)*100 for x in rgb]
	RED.ChangeDutyCycle(rgb[0])
	GREEN.ChangeDutyCycle(rgb[1])
	BLUE.ChangeDutyCycle(rgb[2])

def lightPoll():
	if growLocation.previous_rising(ephem.Sun()) <= growLocation.date <= growLocation.next_setting(ephem.Sun()):
		pinControl(lightRelay, 1)
		daylight=1
		print("Day")
	elif growLocation.previous_setting(ephem.Sun()) <= growLocation.date <= growLocation.next_rising(ephem.Sun()):
		pinControl(lightRelay,0)
		daylight=0
		print("Night")
	return daylight

def roomTemp():
	arduino.write('1'.encode())
	data = float(arduino.readline().strip())
	if data:
		currentRoomTemp = data
		if currentRoomTemp > targetRoomTemp:
			pinControl(fanRelay, 1)
		elif currentRoomTemp < targetRoomTemp:
			pinControl(fanRelay, 0)
		print ("Room temperature: " + str(currentRoomTemp))
	return currentRoomTemp

def roomHumid():
	arduino.write('2'.encode())
	data = float(arduino.readline().strip())
	if data:
		currentRoomHumidity = data
		if currentRoomHumidity > targetRoomHumidity:
			pinControl(fanRelay, 1)
		elif currentRoomHumidity < targetRoomHumidity:
			pinControl(fanRelay, 0)
			print ("Room humidity: " + str(currentRoomHumidity))
	return currentRoomHumidity

def soilMoisture():
	arduino.write('3'.encode())
	data = int(arduino.readline().strip())
	if data:
		currentSoilMoisture = data
		if currentSoilMoisture > targetSoilMoisture:
			pinControl(pumpRelay, 1)
			setColor([255,0,0])
		elif currentSoilMoisture <= targetSoilMoisture:
			setColor([0,255,0])
			pinControl(pumpRelay, 0)
			print ("Soil moisture: " + str(currentSoilMoisture))
	return currentSoilMoisture

while True:
	dbInsert(growLocation.date, roomTemp(), roomHumid(),soilMoisture(),lightPoll())