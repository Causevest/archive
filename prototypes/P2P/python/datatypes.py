"""
Author      : Sreeram
Version     : 0.0.1

Description : The idea is to avoid frequent changes to code base, just to change the static values
				like ip addresses, string constants etc.

TODO        : expose as a module after segregating the classes/functions
"""
from collections import namedtuple
import io
import json

NetworkNode = namedtuple('NetworkNode',['ipaddr','port','idletime'])
Peer = namedtuple('Peer',['expiry_time', 'limit'])

class NetworkInfo(object):
	def __init__(self,jsonfilepath: str,key: str):
		""" Load from json """
		jsonfile = open(jsonfilepath,'r')
		jsonobj = json.load(jsonfile)
		jsonnode = jsonobj[key]
		self.ipaddr = jsonnode['ipaddr']
		self.port = jsonnode['port']
		self.idletime = jsonnode['idletime']

	@property
	def ipaddr(self):
		return self.__ipaddr
	@ipaddr.setter
	def ipaddr(self,ipaddr):
		self.__ipaddr = str(ipaddr)

	@property
	def port(self):
		return self.__port
	@port.setter
	def port(self,port):
		self.__port = int(port)

	@property
	def idletime(self):
		return self.__idletime
	@idletime.setter
	def idletime(self,idletime):
		self.__idletime = int(idletime)

class PeerInf(object):
	def __init__(self,jsonfilepath: str):
		jsonfile = open(jsonfilepath,'r')
		jsonobj = json.load(jsonfile)
		jsonnode = jsonobj['peer']
		self.expiry_time = jsonnode['expiry_time']
		self.limit = jsonnode['limit']

	@property
	def expiry_time(self):
		return self.__expiry_time
	@expiry_time.setter
	def expiry_time(self,expiry_time):
		self.__expiry_time = float(expiry_time)

	@property
	def limit(self):
		return self.__limit
	@limit.setter
	def limit(self,limit):
		self.__limit = int(limit)
