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
import Queue


# Variables
doThis = True

displayText = "Initializing..."

# Functions


# Classes
class RemotePresence:
	
	def __init__(self, master):
		self.prefix = {}
		self.konectid = False

		# Display window
		self.master = master
		
		# Toolbar
		#self.frame0 = Frame(self.master, bg="#101010")
		#self.frame0.pack(side=TOP, fill=X)
		
		#self.conbut = Button(self.frame0, text="Connect", bg="#408040", activebackground="#80BB80", fg="yellow", command=self.konnect)
		#self.conbut.pack(side=LEFT)
		
		# main window
		self.frame1 = Frame(self.master)
		self.frame1.pack(side=TOP, expand=1, fill=BOTH)
		
		self.scr = Scrollbar(self.frame1, bg="#606060", troughcolor="#404040")
		self.scr.pack(side=RIGHT, fill=Y)
		
		self.textLog = Text(self.frame1, bg="#202020", fg="green")
		self.textLog.pack(side=LEFT, expand=1, fill=BOTH)
		
		self.textLog.tag_add("server", END)
		self.textLog.tag_config("server", foreground="green")
		self.prefix["server"] = "Renfield -> "
		
		self.textLog.tag_add("client", END)
		self.textLog.tag_config("client", foreground="cyan")
		self.prefix["client"] = "-> "
		
		self.textLog.tag_add("alert", END)
		self.textLog.tag_config("alert", foreground="orange")
		self.prefix["alert"] = "ALERT -> "
		
		self.textLog.config(state=DISABLED)
		
		self.scr.config(command=self.textLog.yview)
		self.textLog.config(yscrollcommand=self.scr.set)
		
		# Entry Line
		self.entryline = Entry(self.master, bg="#404040", fg="cyan", insertbackground="cyan")
		self.entryline.pack(side=BOTTOM, fill=X)
		self.entryline.bind("<Return>", self.enter)
		self.entryline.focus()
		
		# GUI created, begin Networking
		self.netverk()
		
	
	def ts(self):
		timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime(time.time()))
		return timestamp
	
	def addline(self, ktag, msg):
		self.textLog.config(state=NORMAL)
		self.textLog.insert(END, self.ts() + self.prefix[ktag] + msg + "\n", ktag)
		self.textLog.yview(END)
		self.textLog.config(state=DISABLED)
		
	def enter(self, event):
		if self.konectid:
			self.cs.send(self.entryline.get())
			
		self.addline("client", "o.0 -> " + self.entryline.get())
		self.entryline.delete(0, END)
	
			
	def parsedata(self, pdata):
		self.addline("server", pdata)
		
	
	def netverk(self):
		self.addline("alert", "Initiating the Netverk function...")
		thr = threading.Thread(target=self.recvdata, args=())
		thr.setDaemon(True)
		thr.start()
	
	def konnect(self):
		self.host = "192.168.14.140"
		self.port = 14714
		self.cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		try:
			self.addline("alert", 'Connecting to Renfield @ ' + str(self.host) + ':' + str(self.port))
			self.cs.connect((self.host, self.port))
		
		except:
			self.addline("alert", 'Connection FAILED!!!')
			time.sleep(5)
			return False
		
		self.addline("alert", 'Connection Successful')
		return True
		
	def recvdata(self):
		while 1:
			if self.konectid:
				data = self.cs.recv(4096)
				if not data:
					self.addline("alert", 'Loss of connection.')
					self.cs.close()
					self.konectid = False
					
				else:
					self.addline("server", data)
			else:
				self.konectid = self.konnect()
			

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
