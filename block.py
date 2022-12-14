import hashlib
from typing import *
from hashinglibrary import HashingLibrary
from transaction import Transaction

class Block:
    
    def __init__(self, transaction_list: List[Transaction], previous_hash: str) -> None:
        self.condition = 3
        self.transaction_list = transaction_list
        self.previous_hash = previous_hash
        self.nonce = 0
        self.merkle_root = self.get_merkle_root([tx.get_tx_hash() for tx in self.transaction_list])
        self.block_hash = self.get_block_hash()

    
    def get_merkle_root(self, depth_list: List) -> str:
        if(len(depth_list) % 2 != 0):
            depth_list.append(depth_list[-1])

        rec_depth_list = []
        for i in range(0, len(depth_list), 2):
            rec_depth_list.append(
                HashingLibrary.doubleSHA256(
                    str(depth_list[i + 0]).encode() + 
                    str(depth_list[i + 1]).encode()
                )
            )
            
        if(len(rec_depth_list) != 1):
            return self.get_merkle_root(rec_depth_list)
        return depth_list[0]

    
    def get_block_hash(self):
        hash_calc = HashingLibrary.doubleSHA256(
            str(self.previous_hash).encode() + 
            str(self.nonce).encode() + 
            str(self.merkle_root).encode()
        )

        while(not self.hash_condition(hash_calc, self.condition)):
            self.nonce += 1
            hash_calc = HashingLibrary.doubleSHA256(
                str(self.previous_hash).encode() + 
                str(self.nonce).encode() + 
                str(self.merkle_root).encode()
            )
        
        return hash_calc


    def hash_condition(self, hash: str, units: int) -> bool:
        return hash[0:units] == ("0" * units)

    
    def output_block_data(self) -> None:
        print('\033[93m' + '='*93 + '\033[0m')
        print('\033[92m' + '[Prev] Block Hash:       ' + '\033[0m' + str(self.previous_hash))
        print('\033[92m' + '[Curr] Block Nonce:       ' + '\033[0m' + str(self.nonce))
        print('\033[92m' + '[Curr] Block Merkle Root: ' + '\033[0m' + str(self.merkle_root))
        print('\033[92m' + '[Curr] Block Hash:        ' + '\033[0m' + str(self.block_hash))
        print('\033[91m' + '='*93 + '\033[0m')



