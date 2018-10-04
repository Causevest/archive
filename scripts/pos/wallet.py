# Wallet implementation Python
# Author: github.com/prakashpandey

import json

class Wallet(object):
	
	def __init__(self, address, coins):
		self.address = address
		self.coins = coins

	def __str__(self):
		wallet = {
			"address": self.address,
			"coins": self.coins
		}
		return json.dumps(wallet)

class Wallets(object):

	def __init__(self):
		self.wallets = []

	def add(self, wallet):
		self.wallets.append(wallet)

	def __str__(self):
		wallets = []
		for w in self.wallets:
			wallets.append(str(w))
		return json.dumps(wallets)

if __name__ == "__main__":
	w = Wallet("sddd-ff", 100)
	wallets = Wallets()
	wallets.add(w)
	print(wallets)
