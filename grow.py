#!/usr/bin/python
import datetime

# keyfile = open('owmapi', 'r')
# OWM_api=keyfile.readline().rstrip()
# owm = pyowm.OWM(OWM_api)

now = datetime.datetime.now()

#Grow will require the follow;
# name - title of this grow which will be unique in DB
# location - location to try and match weather patterns
# strain - strain for the database
# planted - the date the grow started, calculations are based mostly
# on the start date of the grow.
# started - clone or seed, this changes the moisture levels and likely
# invluences the nutrient mixes
class Grow(object ):
	def __init__( self, name, location, strain, planted, starter ):
		self.name = name
		self.location = location
		self.strain = strain
		self.planted = planted
		self.starter = starter
		self.estVeg = planted + datetime.timedelta( 14 )
		self.estHarvest = planted + datetime.timedelta( 77 )

# Return estimated datys to Veg growth based on date planted
	def daysToVeg( self ):
		days = self.estVeg - now
		return days

# Return days to harvest based on date planted
	def daysToHarvest( self ):
		days = self.estHarvest - now
		return days

# Return days since planted.
	def daySincePlant( self ):
		days = now - self.planted
		return days

# Returns current nutrient mix based on date planted
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

# Returns current target humidity level using date planted.
# Requires specification of clone of seed
	def targetHumidity( self ):
		# If starting from a clone use these humidity values
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
		# If we're starting from seedling these moisture values
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