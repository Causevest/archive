import json
import random
import string

class Miner(object):
    """
        Miner class to hold miner address, coins spent, earned and balance
    """
    addr_size = 31
    base58 = ''
    def __init__(self, ipaddr):
        self.genBase58()
        self._ipaddr = ipaddr
        self._address = self.genAddr(ipaddr)
        self._earned = int(0)
        self._spent = int(0)
        self._balance = int(10) # Have some coins to spend :)
        self._alladdr = [self.address] # All miner addresses used by this owner

    def genBase58(self):
        if len(Miner.base58) != 58:
            Miner.base58 = ''
            Miner.base58 = string.ascii_letters+string.digits
            Miner.base58.replace('0','')
            Miner.base58.replace('O','')
            Miner.base58.replace('l','')
            Miner.base58.replace('I','')

    def genAddr(self, ipaddr):
        """
            TODO: Generate using ipaddr, public/private key comination
        """
        return '1'+''.join(random.choices(Miner.base58,k=Miner.addr_size))

    def to_json(self):
        miner = {
            "address": self.address,
            "balance": self.balance,
            "earned": self.earned,
            "spent": self.spent
        }
        return json.dumps(miner)

    @property
    def ipaddr(self):
        return self._ipaddr
    @ipaddr.setter
    def ipaddr(self, value):
        self._ipaddr = value.strip()

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

    @property
    def alladdr(self):
        return self._alladdr
    @alladdr.setter
    def alladdr(self,value):
        if value.strip() not in self.alladdr:
            self._alladdr.append(value.strip())
