# NXT style POS implementation in python
# Author: github.com/prakashpandey 

from blockchain import Block, Blockchain 
from nodes import Nodes, Node
from pos import POS
import time

# wallets
nodes = Nodes()
# blockchain
blockchain = Blockchain()

def generate_genesis_block():
    b = Block(index = 0, prev_hash = "", validator = nodes.nodes[0].address)    
    b.calculate_hash()    	
    blockchain.add_block(b)

def print_blockchain():
    print("Blockchain: \n{}\n".format(str(blockchain)))

if __name__ == "__main__":
    print("NXT style POS implementation in python.\n")
    
    # wallet-1
    n = Node("node-1", 100)
    nodes.add(n)
    # wallet-2
    n = Node("node-2", 10)
    nodes.add(n)
    print("nodes in the system: \n{}\n".format(str(nodes)))
    generate_genesis_block()
    print_blockchain()
    pos = POS(nodes = nodes, blockchain = blockchain)
    iteration = 0
    print("-------------------------------------------------------------------------------------------------------------\n")
    print("-------------------------------------------------------------------------------------------------------------\n")
    while(True):
        print("[Iteration {}]".format(iteration))
        pos.generate_block()
        pos.select_node()
        time.sleep(4)
        iteration += 1
        print("-------------------------------------------------------------------------------------------------------------\n")
	
        

    
