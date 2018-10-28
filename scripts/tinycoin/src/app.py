# Application main file

import os
import json
import requests
import datetime as date
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import requests

from utils import *
from transaction import Transaction
from miner import Miner

from genesis import create_genesis_block
from block import Block, Data, get_block_obj
from flask_ngrok import run_with_ngrok

from pathlib import Path

node = Flask(__name__)
CORS(node)
run_with_ngrok(node)
my_peer = ''

# Create a blockchain and initialize it with a genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Version 1.7 changes
# Just in case
default_ip = "0.0.0.0" # Works in all cases whether from docker or command window etc.
default_port = "5000"
default_miner = "default_miner_address"
# A completely random address of the owner of this node
owner = Miner(default_miner)


# Transactions that this node is doing
nodes_transactions = []
nwtxnid = int(1)

# Link of peer nodes
peer_nodes = set()
# If we are mining or not
mining = True 
miningfees = int(1)

# Mock the rest request
mock = False

# global messages
success = "success"
failed = "failed"
resultStatus = "result"
resultText ="text"
resultData = "data"
resultFrom = "from"

@node.route("/get_miner_address", methods=['GET'])
def get_miner_address():
    """
        Returns miner address
    """
    global success;
    global owner;
    
    result = {
        resultStatus: success,
        resultText: "Successfully fetched miner address",
        resultData: owner.address,
        resultFrom: owner.to_json()
    };
    return jsonify(result)


@node.route("/update_miner_address", methods=['POST'])
def update_miner_address():
    """
        Update miner address
    """
    address = request.get_json()['miner_address'];
    result = {};
    
    global success;
    global failed;
    global owner;
    
    if not address:
        result[resultStatus] = failed
        result[resultData] = ''
        result[resultText] = "Can not update miner_address as valid miner address is not found"
    else:
        owner.address = address
        result[resultData] = owner.address
        result[resultStatus] = success
        result[resultText] = "Successfully updated miner address"
        
    result[resultFrom] = owner.to_json();
    return jsonify(result)

@node.route("/peers", methods=['GET'])
def peer():
    """
        Returns peers of this node
    """
    global success;
    global owner;    
    result = {
        resultStatus: success,
        resultText: "Returned peer list",
        resultData: json.dumps(list(peer_nodes)),
        resultFrom: owner.to_json()
    }
    return jsonify(result)


@node.route("/add_peers", methods=['POST'])
def add_peers():
    """
        Override the existing peers list with new `given peers` list
    """
    global success;
    global failed;
    global owner;
    
    result = {
        resultData: '',
        resultFrom: owner.to_json()
    }
    peers = json.loads(request.data)
    if peers:
        # clear the peer list
        peer_nodes.clear()
        peer_nodes.update(peers)
        result[resultStatus] =success
        result[resultText] = "Peer list updated. Peer/peers replaced with new peer/peers."
    else:
        result[resultStatus] = failed
        result[resultText] = "Failed while adding peer/peers. Error[empty peer list received]"
    return jsonify(result)


@node.route("/append_peers", methods=['POST'])
def append_peers():
    """
        Append peers to this node
    """
    global success;
    global failed;
    global owner;
    
    result = {
        resultData: '',
        resultFrom: owner.to_json()
    }
    peers = json.loads(request.data)
    if peers:
        peer_nodes.update(peers)
        result[resultStatus] = success
        result[resultText] = "Peer list updated. Peer/peers is/are appended."
    else:
        result[resultStatus] = failed
        result[resultText] = "Failed while appending peer/peers. Error[empty peer list received]"

    return jsonify(result)


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

    global success;
    global owner;
    result = {
        resultStatus: success,
        resultText: "Returned updated peer list",
        resultData: json.dumps(list(peer_nodes)),
        resultFrom: owner.to_json()
    }

    return jsonify(result)


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
    
    global success;
    global failed;
    global owner;

    amt = int(transaction_received['amount']);
    result = {
        resultData: ''
    }
    if transaction.is_valid():
        nodes_transactions.append(transaction.to_json())
        result[resultStatus] = success
        result[resultText] = "Transaction submission successful."
        owner.spent += amt;
        owner.balance -= amt;
    else:
        result[resultStatus] = failed
        result[resultText] = "Invalid transaction"
    result[resultFrom] = owner.to_json()
    
    return jsonify(result)

@node.route("/blocks", methods=['GET'])
def get_blocks():
    global success;
    global owner;

    result = {
        resultStatus: success,
        resultText: "Returned blocks",
        resultData: json.dumps(blockchain),
        resultFrom: owner.to_json()
    }
    return json.dumps(result)


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

    global success;
    global owner;
    
    result ={
        resultStatus: success,
        resultText: "Consensus successfully done",
        resultData: '',
        resultFrom: owner.to_json()
    }
    return jsonify(result)


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
    global success;
    global failed;
    global owner;
    result = { }
    result[resultFrom] = owner.to_json()
    
    # Return if no transaction is available to mine
    
    if not nodes_transactions:
        result[resultStatus] = failed
        result[resultText] = "Transaction is empty, noting to mine."
        result[resultData] = ''
        return jsonify(result)
    
    global nwtxnid, miningfees;
    last_block = get_block_obj(blockchain[len(blockchain) - 1])
    last_proof = json.loads(last_block.data)['proof_of_work']

    # Find proof of work for the current block being mined
    proof = proof_of_work(last_proof)

    # Ones the miner found out the proof of work
    # the network rewards the miner by adding a transaction
    nodes_transactions.append(Transaction("network", 
        owner.address, 
        miningfees,
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
    owner.earned += miningfees
    owner.balance += miningfees

    result[resultStatus] = success,
    result[resultText] = "Returned mined block",
    result[resultData] = mined_block.to_json(),

    return jsonify(result)


@node.route("/version", methods=['GET'])
def version():
    currdir = os.path.dirname(__file__)
    versonFile = os.path.join(currdir, '../VERSION')
    version = "default"
    file = Path(versonFile)

    global success;
    global failed;
    global owner;
    
    result = { }

    if not file.exists():
        text = "'%s' doesn't exists." % versonFile
        print(text)
        result = {
            resultStatus: failed,
            resultText: text,
            resultData: verson,
            resultFrom: owner.to_json()
        }
        return jsonify(result)

    # WARNING: Returning the first non-empty line from VERSION, in full. No parsing whatsoever
    with file.open("r") as fd:
        for line in fd:
            line.strip()
            if len(line) == 0:
                continue
            version = line
            break

    result = {
        resultStatus: success,
        resultText: 'Returned the fetched Tinycoin version',
        resultData: version,
        resultFrom: owner.to_json()
    }

    return jsonify(result)


@node.route('/auto_peer')
def auto_peer():
    peer_server = 'tcs.serveo.net'
    resp = requests.get('http://' + peer_server + '/peers/' + my_peer)
    peer_nodes.update(json.loads(resp.text))


if __name__ == "__main__":
    print("Tinycoin server started ...!\n")
    owner.address = os.getenv("MINER_ADDRESS", default_miner)
    if not owner.address:
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
    print("\tMiner:", owner.address)
    
    node.run(host = str(host), port = int(port))
