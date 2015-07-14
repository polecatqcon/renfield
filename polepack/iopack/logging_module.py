#!/usr/bin/python
#
# Renfield 4th Gen Logging Module

# Python Imports
import string
import time

# Polecat Imports


# Variables
lfile = 'mainlog.log'

# Classes


# Functions
def ts():
	timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime(time.time()))
	return timestamp

def log(arg):
	print ts() + ' ' + str(arg)
	with open("logs/"+lfile, "a") as logfile:
		logfile.write(ts() + str(arg) + "\n")