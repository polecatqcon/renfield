#!/usr/bin/python
#
# Renfield 4th Gen A.I.

# Python Imports
import os
import ConfigParser
import Queue
import sys
import socket
import string
import time
import traceback
import threading


# Polecat Imports
from .. import globalz as g
from .. import mysql_module as mydb

import aipluginz

pluginzFound = []
for path, subdir, files in os.walk('./polepack/aipack/aipluginz'):
	for name in files:
		n = name.rsplit('.', 1)
		if n[1] == "py" and n[0] != "__init__":
			plugin = str(n[0])
			try:
				exec("from aipluginz import " + plugin)
				pluginzFound.append(plugin)
			except:
				e = traceback.format_exc()
				print 'Could not perform A.I. dependency Reload - ' + str(e)
				



# Variables
period = ["Hadean",
	"Archean",
	"Proterozoic",
	"Cambrian",
	"Ordovician",
	"Silurian",
	"Devonian",
	"Carboniferous",
	"Permian",
	"Triassic",
	"Jurassic",
	"Cretaceous",
	"Paleogene",
	"Neogene",
	"Quaternary"
	]

# VERSION
version = 4.119

gen = "4th"

stage = period[2]

cmdprefix = '?'

modID = "AI"

# End of Variables

# Functions
# Dynamic module reloading
def poleReload(plugin):
	good = True
	try:
		exec("from aipluginz import " + plugin)
		return True
		
	except:
		e = traceback.format_exc()
		print 'Could not perform A.I. dependency Reload - ' + str(e)
		return False



def parse_cmd(line):
	line = line.lstrip(cmdprefix)
	wordlist = line.split(' ') 
	return wordlist

def say(text):
	packet = g.ActionPotential()
						
	packet.set('origin', modID)
	packet.set('broadcast', True)
	packet.startTime = time.time()
	packet.set('response', str(text) + "\n")
	
	g.outgoing.put(packet)
	
def respond(packet):
	g.outgoing.put(packet)


def aihelp(packet):
	#packet.response = iternested(g.aicmds)
	result = ""
	prepipe = ""
	for k, x in g.aicmds.items():
		result += str(prepipe) + str(k) + " ~ " + str(x['desc']) + " [" + str(x['access']).upper() + "]"
		prepipe = '  |  '
	
	packet.set('response', result)
	respond(packet)

def filterz(packet):
	result = ""
	for k, v in g.dipnet:
		result += "\n" + str(k) + " ~ " + str(v)
	
	packet.set('response', result)
	respond(packet)
	

def getversion(packet):
	result = 'I am running version ' + str(version) + ' ' + str(gen) + ' gen ' + stage + ' stage.'
	packet.set('response', result)
	respond(packet)
	
	
def pluginz(packet):
	result = "Currently loaded plugins: "
	cycled = False
	for v in pluginzFound:
		if cycled:
			result += ", "
		result += str(v)
		cycled = True
	
	packet.set('response', result)
	respond(packet)
	
	
def iternested(d):
	result = ''
	for k, v in d.iteritems():
		if isinstance(v, dict):
			iternested(v)
		else:
			if k != "func":
				result += "{0} : {1}".format(k, v)
				
	return result
	

def didreload(x):
	if x == 1:
		text = "Renfield version " + str(version) + " has been loaded."
	else:
		text = "Failed to reload Renfield's new code!!!"
		
	say(text)
	
	# Perform if main code was reloaded successfully
	if x == 1:
		reload(aipluginz)
		
		plugtxt = " Pluginz reload status: "
		cycled = False
		try:
			for v in pluginzFound:
				if cycled:
					plugtxt += ", "
					
				if poleReload(v):
					plugtxt += "" + str(v) + " loaded"
				else:
					plugtxt += "" + str(v) + " FAILED"
				
				cycled = True
				
			say(plugtxt)
			
		except:
			e = traceback.format_exc()
			print 'Could not perform A.I. dependency Reload - ' + str(e)
			say("  Failed to reload dependencies for A.I. module!!! " + str(e) )
		

# Main Function
def handler(packet):
	master = False
	
	print "A.I. Logic handler executing for [" + packet.get('origin') + "] " + packet.get('msg')
	
		
	if packet.get('origin') == "KONSOLE":
		master = True
	
	if packet.get('origin') == "REMOTE":
		master = True
	
	try:
		msg = packet.get('msg')
		if msg.startswith(cmdprefix):
			word = parse_cmd(msg)
			cmd = word[0].lower()
			print "CMD-> " + cmd
			
			# Check if there is a command first
			if cmd == None or cmd == "":
				return
		
			# Admin commands
			if master:
				if cmd == "reload":
					packet.set('response', "Reloading A.I. Modules...")
					packet.set('broadcast', True)
					packet.set('dest', "ALL")
					respond(packet)
					g.doReload = True
					return
					
				if cmd == "quit":
					g.isAlive = False
					sys.exit(1)
					return
					
				if cmd == "broadcast":
					packet.set('response', " ".join(word[1:]))
					packet.set('broadcast', True)
					packet.set('dest', "ALL")
					respond(packet)
					return
					
			# Common commands
			if cmd == "aih":
				packet.set('response', str(g.aicmds))
				respond(packet)
				return
				
				
			# Dynamic command handling
			try:
				f = g.aicmds[cmd]["func"]
				print str(f)
				f(packet)
				return
				
			except KeyError as ke:
				print 'Trying alias list...'
				try:
					command = g.aicmdalias[cmd]["cmd"]
					print 'Command is ' + command
					f = g.aicmds[command]["func"]
					f(packet)
					return
					
				except Exception as ee:
					# No command found	
					e = traceback.format_exc()
					err = e.strip('\r')
					err = err.strip('\n')
					print str(e)
					packet.set('response', "Command '" + cmd + "' not found!  " + str(e))
					respond(packet)
					return
			
			
		# Plugin Filters get iterated
		try:
			for k, x in g.dipnet.items():
				print "-- Filtering with " + str(k)
				f = g.dipnet[k]["func"]
				f(packet)
				
		except Exception as e:
			e = traceback.format_exc()
			err = e.strip('\r')
			err = err.strip('\n')
			print str(e)
			packet.set('response', err)
			respond(packet)
			return
				
				
	except Exception as e:
		e = traceback.format_exc()
		err = e.strip('\r')
		err = err.strip('\n')
		print str(e)
		packet.set('response', err)
		respond(packet)

	# End of Logic

g.aicmds["help"] = {"desc": "Lists all known commands used by the A.I.", "func": aihelp, "access": "common"}
g.aicmds["version"] = {"desc": "Returns the current version of the code.", "func": getversion, "access": "common"}
g.aicmds["pluginz"] = {"desc": "Lists all plugins used by the A.I.", "func": pluginz, "access": "common"}
g.aicmds["filterz"] = {"desc": "Lists all plugins used by the A.I. that filter everything.", "func": filterz, "access": "common"}

g.aicmdalias["h"] = {"cmd": "help"}
g.aicmdalias["v"] = {"cmd": "version"}
	
# EOF
