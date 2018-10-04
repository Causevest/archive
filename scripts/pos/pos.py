# POS implementation Python
# Author: github.com/prakashpandey

from blockchain import Block 
from nodes import Node
import json
from random import randint
import utils


class Lottery(object):

	def __init__(self, node, block):
		self.node = node
		self.block = block
	
	def __str__(self):
		return "lottery"

class Lotteries(object):

	def __init__(self):
		self.lotteries = []
	
	def add(self, lottery):
		self.lotteries.append(lottery)
	
	def __str__(self):
		return "lotteries"

class POS(object):
	
	def __init__(self, nodes, blockchain):
		self.nodes = nodes
		self.blockchain = blockchain
		self.candidate_blocks = []
		# index of genesis is 0 
		self.index = 1
		self.prev_block = self.blockchain.blockchain[0]
		

	
	def __str__(self):
		return json.dumps(self.wallets)
	
	def generate_block(self):
		print("__INIT__[Generating blocks]")
		# randomly select a node
		node = self.nodes.nodes[utils.rand_number_between(0, len(self.nodes.nodes) - 1)]
		block = Block(index = self.index, prev_hash = self.prev_block.hash, validator = node.address)
		self.index += 1
		self.candidate_blocks.append(block)

	def select_node(self):
		print("selecting block from candidate blocks....")
		# select one block from candidate blocks
		lotteries = Lotteries()
		for block in self.candidate_blocks:
			address = block.validator
			node = self.nodes.find(address = block.validator)
			# add block to lottery time the coin invested
			for i in range(0, node.coins):
				lottery = Lottery(node = node, block = block)
				lotteries.add(lottery)
		lottery_won = lotteries.lotteries[utils.rand_number_between(0, len(lotteries.lotteries) - 1)]
		node_won = lottery_won.node
		# increase the coins of this node 
		node_won.coins += 10
		block_won = lottery_won.block
		# add this block to blockchain
		self.blockchain.add_block(block_won)
		self.prev_block = block_won
		print("[Adding block to blockchain] \n[{}]".format(str(block_won)))
		# clear candidate blocks list
		del self.candidate_blocks[:]



			
