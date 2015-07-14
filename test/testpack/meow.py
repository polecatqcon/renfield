#!/usr/bin/python
#
# test module

import time

def ts():
	x = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime(time.time()))
	
	#x = 'Polecat'
	return x


