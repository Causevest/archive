# This is a special file containing a genesis block

import datetime as date
from block import Block, Data
from transaction import Transaction
import utils

def create_genesis_block():
    # Manually crate a block with index zero
    # and arbitary previous hash
    print("Creating and initializing blockchain at %s \n" %
          str(utils.get_string_datetime(date.datetime.now())))
    transactions = []
    # 9 is the random sudo proof of work
    data = Data(9, transactions).create()
    # "0" is the sudo hash of previous work
    return Block(0, utils.get_string_datetime(date.datetime.now()), data, "0").to_json()