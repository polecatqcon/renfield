#!/usr/bin/python
#
# Template for Python scripts

import re
import urllib2
import json
import traceback

# Variables
user = "polecat"
pword = "chevy350"
appid = "adaf9ef8b1658493bb1e1b5e4e5a09b7"

# Functions

def getWeather(location):
	url = 'http://api.openweathermap.org/data/2.5/weather?q='+str(location)+'&units=imperial'
	
	try:
		req = urllib2.Request(url)
		opener = urllib2.build_opener()
		f = opener.open(req)
		data = json.loads(f.read())
		return data[2]['main']
		
	except:
		e = traceback.format_exc()
		print(' ERROR INFO-> '+str(e))
		error = str(e).strip()
		#error = error.strip('\n')
		result = 'There was a problem looking up '+str(location)+'.  ('+error+')'
	
	return result

# End