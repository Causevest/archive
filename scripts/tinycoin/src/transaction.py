# Transaction contains the data structure of transaction in a blockchain
import json

class Transaction(object):
    """
        Data structure of a transaction in a blockchain

        E.g:
        {
            "from": "71238uqirbfh894-random-public-key-a-alkjdflakjfewn204ij",
            "to": "93j4ivnqiopvh43-random-public-key-b-qjrgvnoeirbnferinfo",
            "amount": 3
        }
    """
    def __init__(self, _from_, to, amount):
        self._from_ = _from_.strip()
        self.to = to.strip()
        self.amount = amount
        if(isinstance(amount, int)):
            self.amount = amount
        else:
             self.amount = 0
    
    def to_json(self):
        transaction = {
            "from": self._from_,
            "to": self.to,
            "amount": self.amount
        }
        return json.dumps(transaction)
    
    def is_valid(self):
        """
            Add rules to validate a transaction(Accept/Reject)
        """
        if(not self._from_ or not self.to):
            return False
        if(self.amount < 1):
            return False
        return True



   