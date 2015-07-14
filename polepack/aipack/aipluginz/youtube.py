#!/usr/bin/python
#
# Renfield's Youtube module

# Python Imports
import requests
from bs4 import BeautifulSoup
import traceback

# Polecat Imports
from ... import globalz as g

modID = __name__

def ytube(packet):
	try:
		msg = packet.get('msg')
	
		if msg.find('youtube.com/watch?') != -1 or msg.find('youtu.be') != -1:
			print "Found a youtube video."
			wrds = msg.split(' ')
			response = ''
			for wrd in wrds:
				if wrd.find('youtube.com/watch?') != -1:
					try:
						hresponse = requests.get(wrd)
						soup = BeautifulSoup(hresponse.text)
						duration = soup.find('meta', attrs={'itemprop': 'duration', 'content': True})
						response = response+'YouTube title: '+soup.title.text.rsplit(' - ', 1)[0] + " | Duration: " + duration['content'].lstrip('PT')
						response = response.encode('utf-8').decode('ascii', 'ignore')
					except:
						response = response+'Error on video query for '+wrd
					
				if wrd.find('youtu.be/') != -1:
					try:
						hresponse = requests.get(wrd)
						hresponse.text = hresponse.text.encode('utf-8').decode('ascii', 'ignore')
						soup = BeautifulSoup(hresponse.text)
						duration = soup.find('meta', attrs={'itemprop': 'duration', 'content': True})
						response = response+'YouTube title: '+soup.title.text.rsplit(' - ', 1)[0] + " | Duration: " + duration['content'].lstrip('PT')
						response = response.encode('utf-8').decode('ascii', 'ignore')
					except:
						response = response+'Error on video query for '+wrd
					
			if response != '':
				packet.set('response', response)
				g.outgoing.put(packet)
				
	except:
		e = traceback.format_exc()
		err = e.strip('\r')
		err = err.strip('\n')
		print str(e)
		response = str(e)
		packet.set('response', response)
		g.outgoing.put(packet)



# Append Filter
g.dipnet[modID] = {"func": ytube, "desc": "Looks for Youtube links and retrieves simple info"}

g.aipluginz[modID] = {"desc": "Youtube plugin"}



# EOF