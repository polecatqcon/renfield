#!/usr/bin/python
#
# Action Potiental Class for Renfield API I/O

# Python Imports
import string
import time


class ActionPotential(object):
	# This is basically a I/O data wrapper for the Renfield API
	
	# Initializes default state
	def __init__(self):
		self.startTime = time.time()
		self.data = {}
		
	
	# Stores a Key/Value pair
	def set(self, key, value):
		try:
			self.data[key] = value
			return True
		except:
			return False
			
	
	# Checks if a key exists
	def exists(self, key):
		try:
			if key in self.data:
				return True
			else:
				return False
		except:
			return False
	
	
	# Retrieves a Key/Value pair
	def get(self, key):
		try:
			result = self.data[key]
			return result
		except:
			return "'" + str(key) + "' is NOT set."
	
	
	# Returns time elapsed since instance creation
	def age(self):
		executionTime = time.time() - self.startTime
		return executionTime
		
	
	# Diagnostic function
	def show(self):
		result = "Name: " + str(self.get('name')) + "{ \n"
		for k, v in self.data.iteritems():
			result += "    " + str(k) + " => " + str(v) + "\n"
		result += "}"		
		
		return result


# EOF