import hashlib
import merkle_root
import validation
import time
import json
start_time = time.time()

class Block:
    def __init__(self, previous_block_hash, txlist):
        self.previous_block_hash = previous_block_hash
        self.txlist = txlist
        self.nonce = 0

        print('\n'.join(txlist))
        self.block_data_raw = previous_block_hash + '\n' + merkle_root.findMerkleRoot(str('\n'.join(txlist))) + '\n'

        while(True):
            self.block_data = self.block_data_raw + str(self.nonce)
            self.block_hash = merkle_root.double_sha256(self.block_data)
            if(validation.leading_zeros(self.block_hash)):
                print(self.block_data)
                break
            self.nonce += 1

def main():
    x = "{'subcat' : 'manu', 'org' : 'Apple', 'prod' : 'iPhone', 'prno' : '13 Pro', 'proid' : 'A12I90N2GN953', 'dnt' : '6:22:50 12-10-2021', 'loc' : 'China'}"
    x = str(json.dumps(x))

    y = "{ 'subcat' : 'distr', 'org' : 'Apple', 'prod' : 'iPhone', 'prno' : '12 Pro', 'proid' : 'A12IQFN2GX9UP', 'dnt' : '6:24:03 12-10-2021', 'loc' : 'CN', 'dest' : 'USA'}"

    y = str(json.dumps(y))
    print(type(y))

    new_block = Block(
        "bcca8a3082f6f7aa527c4a04ea1058e69a1096e7c53060271ac9d25fd0e98438", 
        [x, y]
    )

    print()
    print('\033[95m' + "Hash Found: " + '\033[92m' + new_block.block_hash + '\033[0m')
    print('\033[95m' + "Nonce: " + '\033[96m' + str(new_block.nonce) + '\033[0m')
    print('\033[95m' + "New Block Found after: " + '\033[93m' + "%.5s seconds" % (time.time() - start_time) + '\033[0m')
    print()


if __name__ == "__main__":
    main()
