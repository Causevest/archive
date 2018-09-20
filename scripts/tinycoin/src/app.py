# Application main file

import datetime as date
import genesis
import block
from block import Block, Data
from generator import BlockGenerator
from transaction import Transaction
from flask import Flask
from flask import request
import requests

import json
import utils
import os

node = Flask(__name__)

# Create a blockchain and initialize it with a genesis block
blockchain = [genesis.create_genesis_block()]
previous_block = blockchain[0]

# A completely random address of the owner of this node
miner_address = None

# Transactions that this node is doing
nodes_transactions = []

# Link of peer nodes
peer_nodes = set()
# If we are mining or not
mining = True 

# Mock the rest request
mock = False

@node.route("/get_miner_address", methods=['GET'])
def get_miner_address():
    """
        Returns miner address
    """
    return miner_address

@node.route("/update_miner_address", methods=['POST'])
def update_miner_address():
    """
        Update miner address
    """
    address = request.get_json()['miner_address']
    if(not address):
        return "Can not update miner_address as valid miner address is not found"
    else:
        global miner_address
        miner_address = address
        return "Successfully updated miner address"

@node.route("/peers", methods=['GET'])
def peer():
    """
        Returns peers of this node
    """
    return json.dumps(list(peer_nodes)) 

@node.route("/add_peers", methods=['POST'])
def add_peers():
    """
        Override the existing peers list with new `given peers` list
    """
    peers = json.loads(request.data)
    if(peers):
        # clear the peer list
        peer_nodes.clear()
        peer_nodes.update(peers)
        return "Peer list updated"
    else:
        return "Failed while adding peer/peers. Error[empty peer list received]"

@node.route("/append_peers", methods=['POST'])
def append_peers():
    """
        Append peers to this node
    """
    peers = json.loads(request.data)
    if(peers):
        peer_nodes.update(peers)
        return "Peer list updated"
    else:
        return "Failed while adding peer/peers. Error[empty peer list received]"

@node.route("/connect_to_peers_of_peers", methods=['GET'])
def connect_to_peers_of_peers():
    """
        Find all nodes connected to the peers of this node
    """
    peers = []
    for peer in peer_nodes:
        try:
            response = requests.get(peer + "/peers").content
            peers_of_peer = json.loads(response)
            peers.extend(peers_of_peer)
        except Exception as e:
            print(f"__ERROR__ while trying to find peers of a peer. { str(e) }")
    # remove the self node
    this_node = os.getenv("HOST", "127.0.0.1") + ":" + os.getenv("PORT", 5000)
    while this_node in peers:
        peers.remove(this_node)
    # update the current peers list
    peer_nodes.update(peers)
    return json.dumps(list(peer_nodes))

@node.route("/transaction", methods=['POST'])
def transaction():
    transaction_received = request.get_json()
    print(f"transaction_received: { transaction_received }")
    transaction = Transaction(
        transaction_received['from'], 
        transaction_received['to'], 
        transaction_received['amount']
    )
    
    # print transaction logs
    print("New Transaction")
    print(f"From: { transaction_received['from'] }")
    print(f"From: { transaction_received['to'] }")
    print(f"Amount: { transaction_received['amount'] }\n")
    
    if(transaction.is_valid()):
        nodes_transactions.append(transaction.to_json())
        return "Transaction submission successful\n"
    else:
        return "Invalid transaction\n"

@node.route("/blocks", methods=['GET'])
def get_blocks():
    return json.dumps(blockchain)

def find_new_chains():
    other_chains = []
    for node_url in peer_nodes:
        chain = None
        if mock:
            # mock call
            chain = get_blocks()
        else:
            # real call
            try:
                chain = json.loads(requests.get(node_url + "/blocks").content)
            except Exception as e:
                print(f"__ERROR__ while trying to find new seeds. { e.__str__() }")
        other_chains.append(chain)
    return other_chains

@node.route("/consensus", methods=['GET'])
def consensus():
    """
        A simple consensus algorithm
        considering the longest chain as the most trusted chain
    """

    # Get other chains from peers 
    other_chains = find_new_chains()
    
    # Find the longest chain in other chain
    longest_chain = utils.find_longest_sub_list(other_chains)
    global blockchain
    if(len(longest_chain) > len(blockchain)):
        blockchain = longest_chain
    
    return "Consensus successfully done"

def proof_of_work(last_proof):
    """
        This is a simple , sudo, not production ready proof of work
    """
    incrementor = last_proof + 1
    while not (incrementor % 31 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    # Broadcast this number as proof that we have successfully performed proof of work
    return incrementor

@node.route("/mine", methods=['GET'])
def mine():
    # Return if no transaction is available to mine
    if not nodes_transactions:
        return "Transaction is empty, noting to mine."
    
    last_block = block.get_block_obj(blockchain[len(blockchain) - 1])
    last_proof = json.loads(last_block.data)['proof_of_work']

    # Find proof of work for the current block being mined
    proof = proof_of_work(last_proof)

    # Ones the miner found out the proof of work
    # the network rewards the miner by adding a transaction
    nodes_transactions.append(Transaction("network", miner_address, 1).to_json())

    # Create a block
    new_block_data = Data(proof, nodes_transactions).create()
    new_block_index = last_block.index + 1
    last_block_hash = last_block.hash
    new_block_timestamp = utils.get_string_datetime(date.datetime.now())

    # Empty the current transaction as it is already processed
    nodes_transactions[:] = []
    # Creating new block
    mined_block = Block(new_block_index, new_block_timestamp, new_block_data, last_block_hash)
    blockchain.append(mined_block.to_json())
    # Broadcast to the world that we have mined
    return mined_block.to_json() + "\n"
    
if __name__ == "__main__":
    print("Tinycoin server started ...!\n")
    miner_address = os.getenv("MINER_ADDRESS", None)
    if(not miner_address):
        print("Can not start application as valid miner address is not found")
        # exit the system with error
        exit(1)
    peers = os.getenv("PEERS", None)
    if(peers):
        peer_nodes.update(peers.split(","))
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 5000))
    node.run(host = host, port = port)