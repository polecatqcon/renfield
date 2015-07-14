#!/usr/bin/env python
#
# Polecat Grammar script

import ConfigParser
import MySQLdb as db

# Variables
config = ConfigParser.RawConfigParser()
config.read('_renfield.cfg')
dbhost = config.get('MYSQL', 'dbhost')
dbuser = config.get('MYSQL', 'dbuser')
dbpasswd = config.get('MYSQL', 'dbpasswd')
basedb = config.get('MYSQL', 'db')

# Functions
def AddWord(word):
	try:
		con = 1
		
	except db.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		
	finally:
		if con:
			con.close

def CheckFor(word):
	try:
		con = db.connect(host = dbhost, user = dbuser, passwd = dbpasswd, db = basedb)
		with con:
			cur = con.cursor(db.cursors.DictCursor)
			cur.execute("""SELECT %s FROM dictionary""", (word,))
			data = cur.fetchall()
			if data != None:
				return True
			else:
				#AddWord(word)
				return False

	except db.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])

	finally:
		if con:
			con.close