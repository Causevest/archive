# NXT style POS implementation in python
# Author: github.com/prakashpandey 

from blockchain import Block, Blockchain 

# validator address
validator = "ass22-552d-255dss"
# prev block
prev_block = None
# blockchain
blockchain = Blockchain()

def generate_genesis_block():
    b = Block(index = 0, prev_hash = "", validator = validator)    
    b.calculate_hash()    	
    blockchain.add_block(b)

def print_blockchain():
    print(str(blockchain))

if __name__ == "__main__":
    print("NXT style POS implementation in python")
    generate_genesis_block()
    print_blockchain()
