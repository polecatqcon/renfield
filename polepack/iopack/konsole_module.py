#!/usr/bin/python
#
# Renfield's Terminal Console by Polecat

# Python Imports
import cmd
import sys
import time
import threading
import Queue

# Polecat Importz
from .. import globalz as g


# Variables
modID = "KONSOLE"


# Functions
def test():
	print "AUTO FUNCTION WORKED"

# Console / Terminal Input
def konInput():
	print 'Konsole Thread Initialised...'
	while g.isAlive:
		timestamp = time.ctime(time.time())
		kbinput = raw_input(timestamp + ' -> ')
		
		packet = g.ActionPotential()
		
		packet.set('origin', modID)
		packet.set('dest', modID)
		packet.startTime = time.time()
		packet.set('msg', str(kbinput))
		
		g.incoming.put(packet)
	
	return
	
def respond(packet):
	print modID + " -> " + str(packet.get('response'))


# Add response function
g.responseFunc.update({modID: respond})


konsoleThr = threading.Thread(target=konInput, args=())
konsoleThr.setDaemon(True)
konsoleThr.start()
g.threadCount += 1

# EOF