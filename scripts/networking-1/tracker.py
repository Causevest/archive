# File: tracker.py
# Author: Nauman Mustafa
# Data: Aug 5, 2018
# Description: 
# 	This file shows as basic example of a DNS seed. 

from socket import *
from threading import Thread, Lock
from time import time, sleep

def check_int(s:str):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

class Tracker:
	
	def __init__(self, port, peer_expiry_time):
		self.sock = socket(type=SOCK_DGRAM)
		self.sock.bind(('0.0.0.0', port))
		self.sock.settimeout(1)
		self.expiry = peer_expiry_time
		self.working = True
		self.lock = Lock()
		self.peers = {}
		self.t1 = Thread(target=self._worker)
		self.t2 = Thread(target=self._expiry_loop)
		self.t1.setDaemon(True)
		self.t2.setDaemon(True)
		self.t1.start()
		self.t2.start()

	def _expiry_loop(self):
		while self.working:
			for ap in self.peers:
				st = self.peers[ap]
				if time()-st < self.expiry:
					continue
				self.lock.acquire()
				del self.peers[ap]
				self.lock.release()
				break
			sleep(1)

	def _worker(self):
		while self.working:
			try:
				port, addr = self.sock.recvfrom(5)
				if not check_int(port):
					continue
				port = int(port)
				plist = list(self.peers)
				ptext = ''
				for pa,pp in plist[:10]:
					ptext += str(pa) + ':' + str(port) + ','
				self.sock.sendto(ptext, (addr, port))
				self.lock.acquire()
				self.peers[(addr, port)] = time()
				self.lock.release()
			except:
				pass
		self.sock.close()

	def stop(self):
		self.working = False
		self.t1.join()
		self.t2.join()

	