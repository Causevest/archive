"""
This is an implementation of Merkel Tree Hash algorithm
"""
import hashlib


class MerkelTreeHash(object):

    def __init__(self):
        pass

    #
    #   Find a merkel tree hash of all the file hashes  passed to this function
    #
    def find_merkel_hash(self, file_hashes):

        blocks = []

        if not file_hashes:
            raise ValueError(
                "Missing required file hashes for computing merkel tree hash")

        # sorted file hashes

        for m in sorted(file_hashes):
            blocks.append(m)

        list_len = len(blocks)

        # Adjust the block of hashes until we have even number
        # of items in the blocks, this entails appending to the end of the
        # block the last entry

        while list_len % 2 != 0:
            blocks.extend(blocks[-1:])
            list_len = len(blocks)

        # group the items in twos
        secondary = []
        for k in [blocks[x:x+2] for x in range(0, len(blocks), 2)]:
            print(k)

            # k is a list with only two items.
            # concatenate them  and create a new hash from them

            hasher = hashlib.sha256()
            hasher.update(k[0].encode('utf-8') + k[1].encode('utf-8'))
            secondary.append(hasher.hexdigest())

        # a single item in the list marks the end of the iteration
        # and we can return the last hash as the merkel root

        if len(secondary) == 1:
            # return only first 64 characters
            return secondary[0][0:64]
        else:
            return self.find_merkel_hash(secondary)

# test with random 13 hashes

if __name__ == '__main__':

    import uuid

    file_hashes = []

    for i in range(0, 13):
        file_hashes.append(str(uuid.uuid4().hex))

    print("Finding the merkel tree hash of {0} random hashes".format(len(file_hashes)))

    cls = MerkelTreeHash()
    mk = cls.find_merkel_hash(file_hashes)

    print("The Merkel tree hash of the hashes below is: {0}".format(mk))
    print("-------------------")
    print(file_hashes)









