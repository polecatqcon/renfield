#!/usr/bin/python
#
# I/O Tester for Renfield


# Python Imports
import Queue
import time


# Polecat Importz
from .. import actionpotential as ap


# Variables
testpack = Queue.Queue()
testpack2 = Queue.Queue()

# Functions
def testpacket(x):
	print "Populating..."
	for i in range(0, x):
		packet = ap.ActionPotential()
		packet.set("name", "tp" + str(i))
		packet.meow = i
		testpack.put(packet)
		

def report():
	print "Reporting..."
	while not testpack.empty():
		p = testpack.get()
		name = str(p.get('nam'))
		
		print name+ " -> " + str(p.age())
			
		testpack.task_done()
		
		testpack2.put(p)
		
		
def dumpit():
	print "Final..."
	while not testpack2.empty():
		pp = testpack2.get()
		
		print pp.show()
			
		testpack2.task_done()
		
		
# MAIN
if __name__ == "__main__":
	print " Time: " + str(time.time())
	testpacket(3)
	report()
	dumpit()
	
print "Script Terminated"