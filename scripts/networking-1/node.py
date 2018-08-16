# File: node.py
# Author: Nauman Mustafa
# Data: Aug 5, 2018
# Description: 
# 	This file shows as basic example of a network node. 

from socket import *
from threading import Thread, Lock
from time import time, sleep
import sys

class Node:

	def __init__(self, port, tracker_addr):
		self.sock = socket(type=SOCK_DGRAM)
		self.sock.bind(('0.0.0.0', port))
		self.sock.settimeout(1)
		self.tracker_addr = tracker_addr
		self.port = port
		self.working = True
		self.tw = Thread(target=self._worker,daemon=True)
		self.tw.start()


	def _worker(self):
		while self.working:
			self.sock.sendto(str(self.port).encode(), self.tracker_addr)
			try:
				data, addr = self.sock.recvfrom(200)
				if addr == self.tracker_addr:
					print(str(self.port)+': '+ data.decode())
			except:
				pass
			sleep(1)
		self.sock.close()

	def stop(self):
		self.working = False
		self.tw.join()

if __name__ == '__main__':
	n1 = Node(17935, (sys.argv[1], int(sys.argv[2])))
	for i in range(100000): sleep(100000)
