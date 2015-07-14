#!/usr/bin/python
#
# Renfield Weather Script by Polecat

# Python Imports
import re
import urllib2
import xml.etree.ElementTree as et
import json
import traceback
import ast
import pprint

# Polecat Importz
from ... import globalz as g
from ... import mysql_module as mydb

# Variables
modID = __name__

# Functions
def getWeather(qloc):
	print 'Looking up weather for '+qloc
	weatherurl = 'http://api.wunderground.com/auto/wui/geo/WXCurrentObXML/index.xml?query='+qloc
	try:
		f = urllib2.urlopen(weatherurl,None,20)
		wxml = et.parse(f)
		f.close()
		root = wxml.getroot()
		location = root[4][0].text
		observed = root[7].text
		weather = root[13].text
		temp = root[14].text
		humidity = root[17].text
		wind = root[18].text
		pressure = root[23].text
		dewpoint = root[26].text
		heat_index = root[29].text
		wind_chill = root[32].text
		vis_mi = root[35].text
		vis_km = root[36].text
		observeloc = root[5][1].text
	
		if location != ', ':
			result = 'Current weather for '+location+' ('+observeloc+') : '
			if weather is not None:
				result = result + weather
			if temp is not None:
				result = result + ' - ' + temp
			if dewpoint is not None:
				result = result + ', dewpoint ' + dewpoint
			if heat_index is not None and heat_index != "NA":
				result = result + ', heat index ' + heat_index
			if wind_chill is not None and wind_chill != "NA":
				result = result + ', wind chill ' + wind_chill
			if humidity is not None:
				result = result + ' - ' + humidity
			if pressure is not None:
				result = result + ' - ' + pressure
			if wind is not None:
				result = result + ' - ' + wind
			if vis_mi is not None:
				result = result + ' - visibility ' + vis_mi + ' miles'
			if vis_km is not None:
				result = result + '(' + vis_km + ' km)'
			if observed is not None:
				result = result + ' - ' + observed
		else:
			result = 'Could not find weather data for '+qloc.replace('%20', ' ')+'.'
			
	except Exception as ee:
		e = traceback.format_exc()
		print ' ERROR INFO-> '+str(ee)
		err = e.strip('\r')
		err = err.strip('\n')
		error = str(err).strip()
		#error = error.strip('\n')
		result = 'There was a problem looking up '+qloc+'.  ('+error+')'
	
	return result
		


def getWeather2(location, packet):
	url = 'http://api.openweathermap.org/data/2.5/weather?q='+str(location)+'&units=imperial'
	
	try:
		data = json.load(urllib2.urlopen(url))
		pprint.pprint(data)
		
		loc = data['name']
		desc = data['weather'][0]['description']
		temp = data['main'][0]['temp']
		
		result = "Weather for " + loc + ": " + desc + ", " + temp + "F"
		
	except:
		e = traceback.format_exc()
		#print(' ERROR INFO-> '+str(e))
		error = str(e).strip()
		#error = error.strip('\n')
		result = 'There was a problem looking up '+str(location)+'.  ('+error+')'
	
	return result
	

def setweather(packet):
	msg = packet.get('msg')
	smsg = msg.split(' ', 1)
	loc = smsg[1]
	mydb.setloc(packet.get('userident'), loc)
	response = "Weather plugin location for " + str(packet.get('nick')) + " set to " + str(loc)
	packet.set('response', response)
	g.outgoing.put(packet)


def weather_parse(packet):
	msg = packet.get('msg')
	word = msg.split(' ')
	qloc = '%20'.join(word[1:])
	chkqloc = qloc.strip(' ')
	chkqloc = chkqloc.strip('%20')
	if chkqloc == "":
		cdata = mydb.pull('ident', packet.get('userident'))
		if cdata['location'] != "Unknown_Location":
			qloc = str(cdata['location'])
		else:
			qloc = False
		
	if qloc:
		response = getWeather(qloc)
	else:
		response = 'No location given and no default location found in records.  Use ?setweather <location> or ?setw <location> for your default.'
		
	packet.set('response', response)
	g.outgoing.put(packet)
	
	
	
# Append to module list
g.aimods.append(modID)
g.aipluginz[modID] = {"desc": "OpenWeatherMap plugin"}

# Append to cmd array
g.aicmds["weather"] = {"desc": "Reports the weather.", "func": weather_parse, "access": "common"}
g.aicmds["setweather"] = {"desc": "Sets your location for the weather plugin.", "func": setweather, "access": "common"}

g.aicmdalias["w"] = {"cmd": "weather"}
g.aicmdalias["setw"] = {"cmd": "setweather"}
	
g.aipluginz[modID] = {"desc": "OpenWeatherMap plugin"}


# EOF