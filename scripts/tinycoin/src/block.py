# Block class

import hashlib as hasher
import json

class Data(object):
    """
        Data structure of a 'data' in a block
    """

    def __init__(self, proof_of_work, transactions=[]):
         self.transactions = transactions
         self.proof_of_work = proof_of_work
    
    def add_transaction(self, transaction):
        """
            Add a transaction 
        """
        self.transactions.append(transaction)

    def create(self):
        """
            Returns block data
        """
        data = {
            "proof_of_work": self.proof_of_work,
            "transactions": list(self.transactions)
        }
        return json.dumps(data)
    

class Block(object):
    
    def __init__(self, index, timestamp, data, last_block_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.last_block_hash = last_block_hash
        self.hash = self.hash_block()

    def message(self):
        return str(str(self.index)
                    + str(self.timestamp)
                    + str(self.data)
                    + str(self.last_block_hash)
                ).encode("utf-8")

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(self.message())
        return sha.hexdigest()
    
    def to_json(self):
        b = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.hash
        }
        return str(json.dumps(b))


def get_block_obj(block):
    """
        block(str): represent the block data in string format
        return the Block() object
    """
    b = json.loads(block)
    index = b['index']
    timestamp = b['timestamp']
    data = b['data']
    hash = b['hash'] 
    return Block(index, timestamp, data, hash)

if __name__ == "__main__":
    b = Block(1, "2018-10-2025", "this is a data", "2233cdd-44dffd-33443dd-ddd332w")
    print(b.to_json() + "\n")
    
    
    