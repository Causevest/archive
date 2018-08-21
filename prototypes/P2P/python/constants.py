"""
Author      : Sreeram
Version     : 0.0.1

Description : The idea is to avoid frequent changes to code base, just to change the static values
				like ip addresses, string constants etc.

TODO        : expose as a module after segregating the classes/functions
"""

import sys
from datatypes import *

# An example to read network addresses from configuration json file(s)
class TrackerInfo(NetworkInfo):
	def __init__(self,filename='.\\constants.json'): # Current directory!
		try:
			super().__init__(filename,'tracker')
		except:
			print("WARNING!!! Loading defaults")
			super().__init__(NetworkNode(ipaddr='127.0.0.1',
				port=18000,
				idletime=600000))

class LocalNodeInfo(NetworkInfo):
	def __init__(self,filename='.\\constants.json'): # Current directory!
		try:
			super().__init__(filename,'localnode')
		except:
			print("WARNING!!! Loading defaults")
			super().__init__(NetworkNode(ipaddr='127.0.0.1',
				port=19000,
				idletime=600000))

class PeerInfo(PeerInf):
	def __init__(self,filename='.\\constants.json'): # Current directory!
		try:
			super().__init__(filename)
		except:
			print("WARNING!!! Loading defaults")
			super().__init__(Peer(expiry_time=99,limit=10))

# Example test case
if __name__ == "__main__":
	i = TrackerInfo('.\\constants.json')
	print("Tracker Information")
	print(i.ipaddr)
	print(i.port)
	print(i.idletime)
	print()

	print("Local Node Information")
	i = LocalNodeInfo('.\\constants.json')
	print(i.ipaddr)
	print(i.port)
	print(i.idletime)
	print()

	print("Peer Information")
	i = PeerInfo('.\\constants.json')
	print(i.expiry_time)
	print(i.limit)
	print()
