#!/usr/bin/python
#
# Renfield Remote Presence script by Polecat

# Python Imports
import socket
import select
import Queue
import time
import sys
import traceback
import threading

# Polecat Imports
from .. import globalz as g


# Variables
connArr = []
	
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = "192.168.14.140"
port = 14714

modID = "REMOTE"


# Functions
def respond(packet):
	if packet.exists('broadcast') and packet.get('broadcast'):
		try:
			for z in connArr:
				if z != ss:
					z.send(str(packet.get('response')))
		except:
			print "Remote Presence Respond function failed on '" + str(packet.get('response')) + "'"
		
	else:
		try:
			packet.get('conn').send(packet.get('response'))
		except:
			print "Remote Presence Respond function failed on '" + str(packet.get('response')) + "'"

# Server Function
def server():
	print "Remote Presence Thread Initialised..."
	
	ss.bind((host, port))
	
	ss.listen(10)
	
	connArr.append(ss)
	
	print "Remote Presence server listening @ "+ str(host) + ':' + str(port)
	
	while g.isAlive:
		rpIn, rpOut, rpErr = select.select(connArr, [], [])
		
		for x in rpIn:
			# New Client connection
			if x == ss:
				clientConn, clientAddr = ss.accept()
				
				connArr.append(clientConn)
				
				print "Detected new Remote Presence @ " + str(clientAddr)
				
				npacket = g.ActionPotential()
				
				npacket.set('origin', modID)
				npacket.set('dest', modID)
				npacket.startTime = time.time()
				npacket.set('response', "Hello, My name is Renfield.  I see you @ " + str(clientAddr))
				npacket.set('conn', clientConn)
				
				g.outgoing.put(npacket)
			
			# Incoming msg
			else:
				try:
					data = x.recv(4096)
					
					if data:
						print "[" + str(clientAddr) + "] " + data
						
						packet = g.ActionPotential()
						
						packet.set('origin', modID)
						packet.startTime = time.time()
						packet.set('msg', data)
						packet.set('conn', x)
						
						g.incoming.put(packet)
						
				except:
					print "Lost connection to client @ " + str(clientAddr)
					
					packet = g.ActionPotential()
					
					packet.set('origin', modID)
					packet.startTime = time.time()
					packet.set('msg', "Lost connection to " + str(clientAddr))
					
					g.incoming.put(packet)
							
							
					x.close()
					connArr.remove(x)
					
					continue
		
	s.close()

	
# Add response method
g.responseFunc.update({modID: respond})


# Remote Presence Thread
rpThr = threading.Thread(target=server, args=())
rpThr.setDaemon(True)
rpThr.start()
g.threadCount += 1

	
# EOF