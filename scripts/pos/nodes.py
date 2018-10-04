# Wallet implementation Python
# Author: github.com/prakashpandey

import json

class Node(object):
	
	def __init__(self, address, coins):
		self.address = address
		self.coins = coins

	def __str__(self):
		node = {
			"address": self.address,
			"coins": self.coins
		}
		return json.dumps(node)

class Nodes(object):

	def __init__(self):
		self.nodes = []

	def add(self, node):
		self.nodes.append(node)
	
	def find(self, address):
		for node in self.nodes:
			if(node.address == address):
				return node
		return None			

	def __str__(self):
		nodes = []
		for n in self.nodes:
			nodes.append(str(n))
		return json.dumps(nodes)

if __name__ == "__main__":
	n = Node("sddd-ff", 100)
	nodes = Nodes()
	nodes.add(n)
	print(nodes)
