#!/usr/bin/python
import datetime

now = datetime.datetime.now()

class Grow(object ):
	def __init__( self, name, location, strain, planted, starter ):
		self.name = name
		self.location = location
		self.strain = strain
		self.planted = planted
		self.starter = starter
		self.estVeg = planted + datetime.timedelta( 14 )
		self.estHarvest = planted + datetime.timedelta( 77 )
	def daysToVeg( self ):
		days = self.estVeg - now
		return days
	def daysToHarvest( self ):
		days = self.estHarvest - now
		return days
	def daySincePlant( self ):
		days = now - self.planted
		return days
	def nutrientLoad( self ):
		mix=[]
		if now < self.estVeg:
			mix.append( 2.5 )
			mix.append( 2.5 )
			mix.append( 2.5 )
		else:
			mix.append( 0 )
			mix.append( 0 )
			mix.append( 0 )
		return mix
	def targetHumidity( self ):
		if self.starter == "clone":
			if now < self.planted + datetime.timedelta( 14 ):
				self.targetHumidity = 0.70
			elif now < self.planted + datetime.timedelta( 21 ):
				self.targetHumidity = 0.65
			elif now < self.planted + datetime.timedelta( 28 ):
				self.targetHumidity = 0.60
			elif now < self.planted + datetime.timedelta( 35 ):
				self.targetHumidity = 0.55
			elif now < self.planted + datetime.timedelta( 49 ):
				self.targetHumidity = 0.50
			elif now < self.planted + datetime.timedelta( 63 ):
				self.targetHumidity = 0.45
			else:
				self.targetHumidity = 0.40
		else:
			if now < self.planted + datetime.timedelta( 14 ):
				self.targetHumidity = 0.60
			elif now < self.planted + datetime.timedelta( 21 ):
				self.targetHumidity = 0.55
			elif now < self.planted + datetime.timedelta( 42 ):
				self.targetHumidity = 0.50
			elif now < self.planted + datetime.timedelta( 56 ):
				self.targetHumidity = 0.45
			else:
				self.targetHumidity = 0.40
		return self.targetHumidity

# This is going to change, for right now it is sufficient
	def targetTemperature( self ):
		# Growth
		if now < self.planted + datetime.timedelta( 14 ):
			self.tempMin = 20 #Celcius
			self.tempMax = 28
			self.tempDiff = 5
		# Veg
		elif now < self.planted + datetime.timedelta( 63 ):
			self.tempMin = 20
			self.tempMin = 28
			self.tempDiff = 10
		# Flowering
		else:
			self.tempMin = 23
			self.tempMax = 28
			self.tempDiff = 5