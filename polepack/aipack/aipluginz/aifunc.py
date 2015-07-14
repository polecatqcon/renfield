#!/usr/bin/python
#
# Common Functions by Polecat


# Python Imports
import re
import time


# Polecat Imports
from ... import globalz as g


# Variables
modID = 'AIFUNC'


# Functions
def ts():
	timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime(time.time()))
	return timestamp
	
	
def detag(data):
    p = re.compile(r'<[^<]*?>')
    return p.sub('', data)

	
def timeelapsed(sec):
	sec = ceil(sec)


def is_number(text):
		try:
			float(text)
			return True
		except ValueError:
			return False

			
def elapsedformat(x):
	answer = ''
	seconds = int(x % 60)
	minutes = int(x / 60 % 60)
	hours = int(x / 3600 % 24)
	days = int(x / 86400)
	if days > 0 :
		answer += str(days)
		answer += ' day' if days == 1 else ' days'
		
	if hours > 0 :
		answer += ', ' if days > 0 else ''
		answer += str(hours)
		answer += ' hour' if hours == 1 else ' hours'
		
	if minutes > 0 :
		answer += ', ' if days > 0 or hours > 0 else ''
		answer += str(minutes)
		answer += ' minute' if minutes == 1 else ' minutes'
		
	if seconds > 0 :
		answer += ', ' if days > 0 or hours > 0 or minutes > 0 else ''
		answer += str(seconds)
		answer += ' second' if seconds == 1 else ' seconds'
	
	return answer

	
def reply(packet):
	msg = packet.get('msg')
	packet.set('response', msg[1:].upper())
	g.outgoing.put(packet)

	
	
g.aimods.append('aifunc')
g.aicmds["reply"] = {"desc": "Echoes your message in capitals.", "func": reply, "access": "common"}


# EOF
