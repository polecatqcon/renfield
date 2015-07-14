#!/usr/bin/python
#
# Renfield 4th Gen A.I. - Core

# Python Imorts
import cmd
import sys
import time
import string
import Queue
import threading
import traceback
import gc
gc.collect()

# Polecat Imports
import globalz as g

from iopack import konsole_module
from iopack import remote_module
from iopack import irc_module
#from iopack import web_module

from aipack import ai_module


# Variables



# Functions
def dispatcher(packet):
	if not packet.exists('response'):
		packet.set('response',  packet.get('msg'))
	
	if not packet.exists('dest'):
		packet.set('dest', packet.get('origin'))
	
	print "Response arg --> " + str(packet.get('response'))
	
	if packet.exists('broadcast') and packet.get('broadcast'):
		try:
			print "Attempting to broadcast packet to all clients..."
			for k in g.responseFunc:
				g.responseFunc[k](packet)
			
		except:
			e = traceback.format_exc()
			print('RESPONSE ERROR INFO-> '+str(e))
			
	else:
		try:
			g.responseFunc[packet.get('dest')](packet)
			
		except:
			e = traceback.format_exc()
			print('RESPONSE ERROR INFO-> '+str(e))


# This thread checks for all input in the queue and sends it through the AI function
def incomingThread():
	print 'Parsing Thread Initialised...'
	while g.isAlive:
		try:
			incPacket = g.incoming.get()
			ai_module.handler(incPacket)
			g.incoming.task_done()
		except:
			#e = sys.exc_info()[0]
			e = traceback.format_exc()
			print '[Parsing Thread Error] ' + str(e)
	return

# This thread checks for any responses from any module and sends it through the response function
def outgoingThread():
	print 'Response Thread Initialized...'
	while g.isAlive:
		try:
			outPacket = g.outgoing.get()
			dispatcher(outPacket)
			g.outgoing.task_done()
		except:
			#e = sys.exc_info()[0]
			e = traceback.format_exc()
			print '[Response Thread Error] ' + str(e)
	return
	
# This thread checks for the reload command
def reloader():
	while g.isAlive:
		try:
			if g.doReload:
				print "CORE-> Recieved Reload command"
				reload(ai_module)
				gc.collect()
				g.doReload = False
				g.didReload = True
			
			if g.didReload:
				g.didReload = False
				ai_module.didreload(1)
		except:
			g.doReload = False
			g.didReload = False
			ai_module.didreload(0)
			e = traceback.format_exc()
			print 'Could not perform Code Reload - ' + str(e)

# Main thread that initiates the sub threads
def main():
	# Incoming data thread
	incThr = threading.Thread(target=incomingThread, args=())
	incThr.setDaemon(True)
	incThr.start()
	g.threadCount += 1
	
	# Outgoing data thread
	outThr = threading.Thread(target=outgoingThread, args=())
	outThr.setDaemon(True)
	outThr.start()
	g.threadCount += 1
	
	# Script reloader
	reloaderThr = threading.Thread(target=reloader, args=())
	reloaderThr.setDaemon(True)
	reloaderThr.start()
	g.threadCount += 1

# MAIN
if __name__ == '__main__':
	main()
	while g.isAlive:
		pass
			
	print 'Main thread is finished'
	

# End