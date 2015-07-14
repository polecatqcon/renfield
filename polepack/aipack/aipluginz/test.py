#!/usr/bin/python
#
# Test

import string


from ... import globalz as g

def test(packet):
	print 'Performing Test'
	packet.set('response', "Command Format: g.aicmds[\"test\"] = {\"desc\": \"Performs simple command test.MEOW\", \"func\": test, \"access\": \"common\"}")
	return packet

# Append to module list
g.aimods.append('test')

# Append to cmd array
g.aicmds["test"] = {"desc": "Performs simple command test.", "func": test, "access": "common"}