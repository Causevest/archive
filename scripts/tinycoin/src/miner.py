import json

class Miner(object):
    """
        Miner class to hold miner address, coins spent, earned and balance
    """
    def __init__(self, address):
        self._address = address.strip()
        self._earned = int(0)
        self._spent = int(0)
        self._balance = int(10) # Have some coins to spend :)

    def to_json(self):
        miner = {
            "address": self.address,
            "balance": self.balance,
            "earned": self.earned,
            "spent": self.spent
        }
        return json.dumps(miner)

    @property
    def address(self):
        return self._address
    @address.setter
    def address(self, value):
        self._address = value.strip()

    @property
    def earned(self):
        return self._earned
    @earned.setter
    def earned(self, value):
        self._earned = int(value)

    @property
    def spent(self):
        return self._spent
    @spent.setter
    def spent(self, value):
        self._spent = int(value)

    @property
    def balance(self):
        return self._balance
    @balance.setter
    def balance(self, value):
        self._balance = int(value)
