#!/usr/bin/python
#
# Polecat MySQL Functions

# Python Imports
import MySQLdb as db
import ConfigParser

# Variables
config = ConfigParser.RawConfigParser()
config.read('_renfield.cfg')
dbhost = config.get('MYSQL', 'dbhost')
dbuser = config.get('MYSQL', 'dbuser')
dbpasswd = config.get('MYSQL', 'dbpasswd')
basedb = config.get('MYSQL', 'db')

# ------- MySQL Functions ----------------
def push(chan, nick, ident, hostmask, lastwords):
	try:
		con = db.connect(host = dbhost, user = dbuser, passwd = dbpasswd, db = basedb)
		with con:
			cur = con.cursor()
			cur.execute("""INSERT INTO hosts (chan, nick, ident, hostmask, lastwords) VALUES ( %s, %s, %s, %s, %s)""", (chan, nick, ident, hostmask, lastwords))
			con.commit

	except db.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		con.rollback

	finally:
		if con:
			con.close

def repush(chan, nick, ident, hostmask, lastwords):
	try:
		con = db.connect(host = dbhost, user = dbuser, passwd = dbpasswd, db = basedb)
		with con:
			cur = con.cursor()
			cur.execute("""UPDATE hosts SET chan = %s, nick = %s, hostmask = %s, lastwords = %s WHERE ident = %s""", (chan, nick, hostmask, lastwords, ident))
			con.commit

	except db.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		con.rollback

	finally:
		if con:
			con.close

def pull(pf, pv):
	try:
		con = db.connect(host = dbhost, user = dbuser, passwd = dbpasswd, db = basedb)
		with con:
			cur = con.cursor(db.cursors.DictCursor)
			cur.execute("""SELECT * FROM hosts WHERE """+str(pf)+""" = %s ORDER BY lasttime DESC""", (pv,))
			data = cur.fetchall()
			if data != None:
				for row in data:
					return row
			else:
				return False

	except db.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])

	finally:
		if con:
			con.close
			
def doesexist(col,val):
	try:
		con = db.connect(host = dbhost, user = dbuser, passwd = dbpasswd, db = basedb)
		with con:
			cur = con.cursor()
			cur.execute("""SELECT COUNT(1) FROM hosts WHERE """+str(col)+""" = %s""", (val,))
			#cur.execute(query)
			
			if cur.fetchone()[0]:
				return True
			else:
				return False
		
	except db.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])

	finally:
		if con:
			con.close
			
def setloc(ident, location):
	try:
		con = db.connect(host = dbhost, user = dbuser, passwd = dbpasswd, db = basedb)
		with con:
			cur = con.cursor()
			cur.execute("""UPDATE hosts SET location = %s WHERE ident = %s""", (location, ident))
			con.commit

	except db.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		con.rollback

	finally:
		if con:
			con.close
			
def setCountdown(ident, cdName, cdUnix):
	try:
		con = db.connect(host = dbhost, user = dbuser, passwd = dbpasswd, db = basedb)
		with con:
			cur = con.cursor()
			cur.execute("""UPDATE hosts SET countdown = %s, countdown_name = %s WHERE ident = %s""", (cdUnix, cdName, ident))
			con.commit

	except db.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		con.rollback

	finally:
		if con:
			con.close
			
# END MySQL Functions --------------------------------