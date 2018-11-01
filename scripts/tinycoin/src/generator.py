# This class generate new blocks into blockchain

import datetime as date


class BlockGenerator(object):

    def __init__(self, last_block):
        self.index = last_block.index + 1
        self.timestamp = date.datetime.now()
        self.data = "I am block %d" % self.index
        self.last_block_hash = last_block.hash
    
    def next(self):
            
        return Block(self.index, self.timestamp, self.data, self.last_block_hash)