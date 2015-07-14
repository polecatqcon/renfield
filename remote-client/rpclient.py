#!/usr/bin/python
#
# Remote Presence Client code by Polecat

# Python Imports
import socket
import select
import string
import sys
import time
from Tkinter import *
import threading


# Variables
doThis = True

displayText = "Initializing..."

# Functions


# Classes
class RemotePresence:
	
	def __init__(self, master):
		self.master = master
		self.inc = 0
		
		# Display window
		self.frame1 = Frame(self.master)
		self.frame1.pack(side=TOP, expand=1, fill=BOTH)
		
		self.scr = Scrollbar(self.frame1)
		self.scr.pack(side=RIGHT, fill=Y)
		
		self.textLog = Text(self.frame1, bg="#404040", fg="green")
		self.textLog.pack(side=LEFT, expand=1, fill=BOTH)
		self.textLog.insert(END, "Connecting to Renfield...\n")
		self.textLog.config(state=DISABLED)
		
		self.scr.config(command=self.textLog.yview)
		self.textLog.config(yscrollcommand=self.scr.set)
		
		# Entry Line
		self.entryline = Entry(self.master, bg="#606060", fg="cyan", insertbackground="cyan")
		self.entryline.pack(side=BOTTOM, fill=X)
		self.entryline.bind("<Return>", self.enter)
		self.entryline.focus()
		
		self.master.after(1000, self.cycle)
		
	def addline(self,msg):
		self.textLog.config(state=NORMAL)
		self.textLog.insert(END, msg + "\n")
		self.textLog.yview(END)
		self.textLog.config(state=DISABLED)
	
	def cycle(self):
		self.inc += 1
		self.addline(str(self.inc))
	
		self.master.after(1000, self.cycle)
		
	def enter(self, event):
		self.addline("You -> " + self.entryline.get())
		self.entryline.delete(0, END)
		

# MAIN
if __name__ == "__main__":
	# GUI
	root = Tk()
	root.wm_iconbitmap(r'renfield.ico')
	root.title("Renfield Remote Presence")
	root.minsize(720, 480)
	root.maxsize(1280, 720)
	
	app = RemotePresence(root)
	
	#root.after(1000, cycle)
	
	root.mainloop()
	
	print "EXITED Remote Presence client"



# EOF
