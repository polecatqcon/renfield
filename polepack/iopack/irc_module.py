#!/usr/bin/python
#
# Renfield 4th Gen IRC Module

# Python Imports
import ConfigParser
import sys
import time
import socket
import string
import Queue
import threading
import gc
import traceback

# Polecat Imports
from .. import globalz as g
from .. import mysql_module as mydb

# Configuration
config = ConfigParser.RawConfigParser()
config.read('_renfield.cfg')

host = config.get('DEFAULT', 'host')
port = int(config.get('DEFAULT', 'port'))
nickname = config.get('DEFAULT', 'nickname')
ident = config.get('DEFAULT', 'ident')
authpass = config.get('DEFAULT', 'authpass')
# End Configuration

# Variables
join_message = "I hunger..."

modID = "IRC"

channel = [
	"#renfield",
	"#qcon",
	"#quakecon",
	]

ircq = Queue.Queue()

now = time.time()

g.lastCheck = now
	
	
# Classes


# Functions
def ts():
	timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime(time.time()))
	return timestamp

	
def log(arg):
	print ts() + ' ' + str(arg)
	with open("logs/irclog.log", "a") as logfile:
		logfile.write(ts() + str(arg) + "\n")

		
def irc_connect():
	#global irc
	try:
		log("Initiating IRC socket connection...")
		g.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		g.irc.settimeout(130)
		g.irc.connect((host, port))
		irc_sendline('NICK '+nickname)
		irc_sendline('USER '+nickname+' '+nickname+' '+nickname+' :RenfieldAI')
		return True
		
	except:
		log(str(sys.exc_info()[0]))
		print '!!! Couldn\'t Connect to IRC Socket !!! ' + str(sys.exc_info()[0])
		irc_reset()
		return False


def irc_getdata():
	readbuffer = ""
	dothis = True
	while g.done == 0 and dothis:
		try:
			data =  str(g.irc.recv(4096))
			
		except:
			log("!!! FAILED TO RECEIVE DATA FROM SOCKET !!!")
			dothis = False
			irc_reset()		
			break
			
		if len(data) <= 0:
			log("!!! LOST CONNECTION - EMPTY SOCKET !!!")
			dothis = False
			irc_reset()
			
		readbuffer = readbuffer + data
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()
		
		for line in temp:
			line = string.rstrip(line)
			log(line)
			irc_parser(line)

			
def irc_sendline(line):
	g.irc.send(line + '\r\n')
	log("SENT-> " + line)
	
			
def irc_reset():
	g.irc.close()
	g.authed = False
	g.online = False
	
	
def irc_handler():
	print "IRC Handler initializing..."
	while g.isAlive:
		if g.online:
			irc_getdata()
			
		else:
			if irc_connect():
				g.online = True
			else:
				log("!!! Connection failed.  Waiting 10 seconds...")
				time.sleep(10)
			
	g.irc.close()
	
	return "Closed main IRC thread"


def respond(packet):
	ircq.put(packet)


def antifloodrate():
	ritenao = now
	lapse = ritenao - g.lastCheck
	g.lastCheck = ritenao
	
	g.quota += lapse * (g.rate / g.seconds)
	
	if g.quota > g.rate:
		g.quota = g.rate
		
	if g.quota > 1.0:
		g.quota -= 1.0
		print "true quota = " + str(g.quota)
		return True
	else:
		print "false quota = " + str(g.quota)
		return False


def chopper(strtext, strlimit):
	cnt = 0
	i = 0
	arr = []
	while cnt < len(strtext):
		arr.append(strtext[cnt:strlimit])
		cnt += strlimit
		i += 1
		
	return arr, i
		

def respondThread():
	print 'IRC Responding Thread Initialised...'
	while g.isAlive:
		try:
			incPack = ircq.get()
			x = 0
			txtblock, indices = chopper(incPack.get('response'), 400)
			while x < indices:
				responder(txtblock[x], incPack)
				time.sleep(1)
				x += 1
				
			ircq.task_done()
				
		except:
			#e = sys.exc_info()[0]
			e = traceback.format_exc()
			print '[IRC Responder Thread Error] ' + str(e)
	return


def responder(text, packet):
	try:
		if packet.exists('response') and packet.exists('chan'):
			irc_sendline("PRIVMSG " + packet.get('chan') + " :" + text)
			
	except:
		e = traceback.format_exc()
		print '!!! IRC ERROR !!! - ' + str(e)
	

def joincmd(c):
	print "IRC joining channel " + c
	irc_sendline('JOIN '+ c)


def irc_parser(line):
	global nickname
	
	word = string.split(line)
	
	if word[0] == "PING":
		irc_sendline("PONG " + word[1])
		
	if len(word) == 3:
		tline = line.lstrip(':')
		segment = tline.split(':')
		raw = segment[0].split()
		
		if len(raw) == 3:
			if raw[1] == "JOIN" and raw[0].find(nickname) != -1:
				log("Joined " + raw[2].strip() + " successfully.")
				irc_sendline("PRIVMSG " + raw[2].strip() + " :" + join_message)
			
	if len(word) >= 4:
		tline = line.lstrip(':')
		segment = tline.split(':', 1)
		raw = segment[0].split()
		
		if len(segment) > 1:
			msg = segment[1]
		
			if msg == "I recognize you.":
				g.authed = True
				
				for v in channel:
					joincmd(v)
			
		if len(raw) >= 2:
			if raw[1] == "433":
				nickname = nickname + '^'
				irc_sendline('NICK ' + nickname)
				
			if raw[1] == "MODE" and g.authed == False:
				irc_sendline('authserv AUTH '+ident+' '+authpass)
				botmask = raw[0].split('@')
				g.bothostmask = botmask[1]
				log("IRC sees my hostmask as " + g.bothostmask)
				
			if raw[1] == "PRIVMSG":
				person = raw[0].split("!")
				nick = person[0]
				hostmask = person[1]
				chan = raw[2]
				user = hostmask.split("@")
				userident = None
				usermask = None
				if len(user) > 1:
					userident = user[0]
					usermask = user[1]
					
				if chan != nickname:
					try:
						if mydb.doesexist("ident", userident):
							mydb.repush(chan, nick, userident, hostmask, msg)
						else:
							mydb.push(chan, nick, userident, hostmask, msg)
					except:
						e = traceback.format_exc()
						print('IRC DATABASE ERROR INFO-> '+str(e))
						
					packet = g.ActionPotential()
					
					packet.set('origin', modID)
					packet.set('msg', msg)
					packet.set('nick', nick)
					packet.set('chan', chan)
					packet.set('userident', userident)
					packet.set('usermask', usermask)
					packet.set('hostmask', hostmask)
					
					g.incoming.put(packet)

				
# Add response method
g.responseFunc.update({modID: respond})


#IRC Responding Thread
ircRThr = threading.Thread(target=respondThread, args=())
ircRThr.setDaemon(True)
ircRThr.start()
g.threadCount += 1


# IRC Thread
ircThr = threading.Thread(target=irc_handler, args=())
ircThr.setDaemon(True)
ircThr.start()
g.threadCount += 1


# EOF
	