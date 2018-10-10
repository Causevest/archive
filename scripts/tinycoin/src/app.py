# Application main file

import os
import json
import requests
import datetime as date
from flask import Flask
from flask import request
from flask_cors import CORS
import requests

from utils import *
from transaction import Transaction
from genesis import create_genesis_block
from block import Block, Data, get_block_obj

from pathlib import Path

node = Flask(__name__)
CORS(node)

# Create a blockchain and initialize it with a genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# A completely random address of the owner of this node
miner_address = None

# Version 1.7 changes
# Just in case
default_ip = "0.0.0.0" # Works in all cases whether from docker or command window etc.
default_port = 5000
default_miner = "default_miner_address"

# Transactions that this node is doing
nodes_transactions = []
nwtxnid = 1

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
    if not address:
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
    if peers:
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
    if peers:
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
    this_node = os.getenv("HOST", default_ip) + ":" + os.getenv("PORT", default_port)
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
        transaction_received['amount'],
        transaction_received['timestamp'],
        transaction_received['txnid'],
        transaction_received['signature']
    )
    
    # print transaction logs
    print("New Transaction")
    print(f"From: { transaction_received['from'] }")
    print(f"To: { transaction_received['to'] }")
    print(f"Amount: { transaction_received['amount'] }")
    print(f"timestamp: { transaction_received['timestamp'] }")
    print(f"TxnId: { transaction_received['txnid'] }\n")
    
    if transaction.is_valid():
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
    longest_chain = find_longest_sub_list(other_chains)
    global blockchain
    if len(longest_chain) > len(blockchain):
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
    
    global nwtxnid;
    last_block = get_block_obj(blockchain[len(blockchain) - 1])
    last_proof = json.loads(last_block.data)['proof_of_work']

    # Find proof of work for the current block being mined
    proof = proof_of_work(last_proof)

    # Ones the miner found out the proof of work
    # the network rewards the miner by adding a transaction
    nodes_transactions.append(Transaction("network", 
        miner_address, 
        1,
        get_string_datetime(date.datetime.now()),
        str(nwtxnid),
        "Under Research ...").to_json())
    nwtxnid += 1

    # Create a block
    new_block_data = Data(proof, nodes_transactions).create()
    new_block_index = last_block.index + 1
    last_block_hash = last_block.hash
    new_block_timestamp = get_string_datetime(date.datetime.now())

    # Empty the current transaction as it is already processed
    nodes_transactions[:] = []
    # Creating new block
    mined_block = Block(new_block_index, new_block_timestamp, new_block_data, last_block_hash)
    blockchain.append(mined_block.to_json())
    # Broadcast to the world that we have mined
    return mined_block.to_json() + "\n"


@node.route("/version", methods=['GET'])
def version():
    currdir = os.path.dirname(__file__)
    versonFile = os.path.join(currdir, '../VERSION')
    version = "default"
    file = Path(versonFile)
    if not file.exists():
        print("'%s' doesn't exists." % versonFile)
        return version

    with file.open("r") as fd:
        for line in fd:
            line.strip()
            if len(line) == 0:
                continue
            version = line
            break
    return version


if __name__ == "__main__":
    print("Tinycoin server started ...!\n")
    miner_address = os.getenv("MINER_ADDRESS", default_miner)
    if not miner_address:
        print("Can not start application as valid miner address is not found")
        # exit the system with error
        exit(1)
    peers = os.getenv("PEERS", None)
    if peers:
        peer_nodes.update(peers.split(","))
    host = os.getenv("HOST", default_ip)
    port = int(os.getenv("PORT", default_port))
    print("Using the following info to run the Tinycoin server ...")
    print("\t Host:", host)
    print("\t Port:", port)
    print("\tMiner:", miner_address)
    node.run(host = str(host), port = int(port))
