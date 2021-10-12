import hashlib
import merkle_root
import validation
import time
start_time = time.time()

class ChainLinkBlock:
    def __init__(self, previous_block_hash, txlist):
        self.previous_block_hash = previous_block_hash
        self.txlist = txlist
        self.nonce = 0

        self.txsingle_hash = merkle_root.findMerkleRoot(txlist)

        while(True):
            self.block_data = previous_block_hash + "\n" + self.txsingle_hash + "\n" + str(self.nonce)
            self.block_hash = merkle_root.double_sha256(self.block_data)
            if(validation.leading_zeros(self.block_hash)):
                break
            self.nonce += 1


new_block = ChainLinkBlock("0000", ["1", "2"])

print()
print('\033[95m' + "Hash Found: " + '\033[92m' + new_block.block_hash + '\033[0m')
print('\033[95m' + "Nonce: " + '\033[96m' + str(new_block.nonce) + '\033[0m')
print('\033[95m' + "New Block Found after: " + '\033[93m' + "%.5s seconds" % (time.time() - start_time) + '\033[0m')
print()