#!/usr/bin/python
#
# Renfield 4th Gen A.I. - Core

# Python Imorts
import threading

# Polecat Imports
from polepack import globalz as g
from polepack import core


# MAIN
if __name__ == '__main__':
	mainThr = threading.Thread(target=core.main, args=())
	mainThr.setDaemon(True)
	mainThr.start()
	while g.isAlive:
		pass
			
	print 'Renfield is dead.'
	

# End