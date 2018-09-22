# A Stand-alone implementation of proof-of-stake
# An implementation from
#   https://medium.com/@mycoralhealth/code-your-own-proof-of-stake-blockchain-in-go-610cd99aa658

from time import time, sleep
from collections import namedtuple
from random import randrange as rand, seed, shuffle


MAX_RANDOM = 1000000000


Block = namedtuple('Block', (
	'Timestamp',
	'Seed',
	'Validator',
))


class BlockChain:
	
	def __init__(self):
		print('Proof-of-stake Simulator')
		self.block_chain = []
		self.validators = {}
		print('Generating Genesis Block...')
		self.block_chain.append(Block(
				Timestamp=time(),
				Seed=rand(MAX_RANDOM),
				Validator=0))
		print('\t', self.block_chain[0])
	
	def round(self):
		seed(time())
		print('Starting investment round...')
		self.validators.clear()
		count = 0
		while count == 0:
			count = rand(20)  # up to 50 random validators for the sake of simulation
		print(F'{count} Validators Investing...')
		for i in range(count):
			val_id = rand(MAX_RANDOM)
			tokens = rand(1000)
			self.validators[val_id] = tokens  # validators stake up to 1000 tokens
			print('\t', F'Validator "{val_id}" invested "{tokens}" tokens')
		print('Investment Locked...')
		print('Determining Lucky Validator...')
		seed(self.block_chain[-1].Seed)
		cdf = [0]
		for k in self.validators:
			v = self.validators[k]
			cdf.append(cdf[-1] + v)
		choice = rand(cdf[-1])
		print('\t\tCDF:', cdf)
		print('\t\tChoice Point:', choice)
		val_id = None
		v = 0
		for k in self.validators:
			v += self.validators[k]
			if v > choice:
				val_id = k
				break
		print(F'Validator {val_id} selected! (invested {self.validators[k]} tokens!!)')
		self.block_chain.append(Block(
				Timestamp=time(),
				Seed=rand(MAX_RANDOM),
				Validator=val_id))
		print('New Block Appended:')
		print('\t', self.block_chain[-1])


if __name__ == '__main__':
	chain = BlockChain()
	while True:
		chain.round()
		print('Waiting for next round...')
		sleep(5)
