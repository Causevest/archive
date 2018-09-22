# A Stand-alone implementation of proof-of-stake
# An implementation from https://blockgeeks.com/guides/ethereum-casper/
# Terms: 
#	Validators: Miners of PoS
#	

stakes = dict()

class Validator:
	
	def __init__(self, max_coins):
		 self.max_coins = max_coins

	# Puts coins on stack and starts validating transections
	def stake(self, n_coins):
		if n_coins < self.max_coins:
			return
		stakes[self] = n_coins
		self.max_coins -= n_coins 
		

	

