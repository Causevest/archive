# Block datastructure 
# Author: github.com/prakashpandey 

import hashlib as hasher
from datetime import datetime as date
import json

class Block(object):

	def __init__(self, index, prev_hash, validator):	
		self.index = index
		self.timestamp = str(date.now())
		self.hash = None
		self.prev_hash = prev_hash
		self.validator = validator

	def hash_message(self):
		message = str(self.index) + self.timestamp + self.prev_hash + self.validator
		return message
	
	def __str__(self):
		message = {
				"index": str(self.index), 
				"timestamp": self.timestamp, 
				"hash": self.hash, 
				"prev_hash": self.prev_hash, 
				"validator": self.validator
		}	
		return json.dumps(message)

	def calculate_hash(self):
		message = self.hash_message()
		sha = hasher.sha256()
		sha.update(message.encode("utf-8"))
		self.hash = sha.hexdigest()

class Blockchain(object):
	
	def __init__(self):
		self.blockchain = []
	
	def add_block(self, block):
		self.blockchain.append(block)
	
	
	def __str__(self):
		blockchain_str = []
		for block in self.blockchain:
			blockchain_str.append(str(block))
		return json.dumps(blockchain_str)
	


   


