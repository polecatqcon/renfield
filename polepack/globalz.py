#!/usr/bin/python
#
# Renfield 4th Gen Globalz Variables


# Python Imports
import Queue


# Polecat Importz
from actionpotential import *


# Internal
#ActionPotential = actionpotential.ActionPotential()

# Globalz
incoming = Queue.Queue()

outgoing = Queue.Queue()

isAlive = True

online = False

done = False

authed = False

doReload = False

didReload = False

threadList = []

threadCount = 0

# Command Array
cmds = []

# Filter Array
dipnet = {}

# Response Function Array
responseFunc = {}

# A.I. module list
aimods = []
aipluginz = {}


# A.I. command functions
aicmds = {}
aicmdalias = {}



# IRC Section
rate = 3.0
seconds = 4.0
quota = rate
lastCheck = 0.0

# EOF