import hashlib
from typing import *
from copy import deepcopy
import os
import json
import glob


class PrintGreen:
    def __init__(self, green: str, white: str) -> None:
        print(" " * 100, end='\r')
        print('\033[92m' + green + '\033[0m' + white)


class PrintOrange:
    def __init__(self, orange: str, white: str) -> None:
        print('\033[93m' + orange + '\033[0m' + white, end='\r')


class HashingLib:
    
    def doubleSHA256(arg: bytes) -> str:
        return hashlib.sha256(
            hashlib.sha256(
                arg
            ).hexdigest().encode()
        ).hexdigest()


class Transaction:

    def __init__(self, sender: str, recipient: str, amount: float) -> None:
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.tx_hash = self.get_tx_hash()

    
    def get_tx_hash(self) -> str:
        return HashingLib.doubleSHA256(
            str(self.sender).encode() + 
            str(self.recipient).encode() + 
            str(self.amount).encode()
        )
    
    def get_tx_details(self) -> str:
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'tx_hash': self.tx_hash
        }
    

class Block:

    def __init__(self, transaction_list: List[Transaction]) -> None:

        PrintOrange(orange="Mining Block...", white="")

        self.leading_zeros = 5
        self.previous_hash = self.get_previous_hash()
        self.transaction_list = transaction_list
        self.merkle_tree = self.build_merkle_tree()
        self.merkle_root = self.get_merkle_root()
        self.block_hash = None
        self.nonce = 0
        self.block_num = None
        self.compute_block_hash()
        self.save_block()

        PrintGreen(green=f"Block {self.block_num} Mined", white="")
        PrintGreen(green=f"Block Hash: ", white=f"{self.block_hash}")
        PrintGreen(green=f"Nonce: ", white=f"{self.nonce}")
    
    def get_previous_hash(self) -> str:
        if not os.path.isfile('blockchain/Block0.json'):
            return "0" * 64

        file_count = len(glob.glob1('blockchain/',"*.json"))

        with open(f'blockchain/Block{file_count-1}.json', 'r') as f:
            block_data = json.load(f)

        return block_data['block_hash']

    def build_merkle_tree(self) -> List[str]:
        self.merkle_tree = []
        self.merkle_tree.append([tx.tx_hash for tx in self.transaction_list])

        if len(self.merkle_tree[0]) == 0:
            return None

        if len(self.merkle_tree[0]) == 1:
            return self.merkle_tree[0]

        current_level = self.merkle_tree[0]
        while len(current_level) > 1:
            next_level = []
            duplicate = False
            
            if len(current_level) % 2 == 1:
                duplicate = True
                current_level.append(current_level[-1])

            for i in range(0, len(current_level), 2):
                next_level.append(
                    HashingLib.doubleSHA256(
                        current_level[i].encode() + current_level[i+1].encode()
                    )
                )

            if duplicate:
                current_level.pop()

            self.merkle_tree.append(next_level)
            current_level = deepcopy(next_level)

        return self.merkle_tree

    def get_merkle_root(self) -> str:
        return self.merkle_tree[-1][0]

    def compute_block_hash(self):
        Mine = Miner(self, leading_zeros=self.leading_zeros)
        block_hash = Mine.mine()
    
    def save_block(self):
        if not os.path.isfile('blockchain/Block0.json'):
            self.block_num = 0
            with open('blockchain/Block0.json', 'w') as f:
                f.write(json.dumps({
                    'previous_hash': self.previous_hash,
                    'transaction_list': [tx.get_tx_details() for tx in self.transaction_list],
                    'merkle_tree': self.merkle_tree,
                    'merkle_root': self.merkle_root,
                    'block_hash': self.block_hash,
                    'nonce': self.nonce
                }, indent=4))

        else:
            file_count = len(glob.glob1('blockchain/',"*.json"))
            self.block_num = file_count
            with open(f'blockchain/Block{file_count}.json', 'w') as f:
                f.write(json.dumps({
                    'previous_hash': self.previous_hash,
                    'transaction_list': [tx.get_tx_details() for tx in self.transaction_list],
                    'merkle_tree': self.merkle_tree,
                    'merkle_root': self.merkle_root,
                    'block_hash': self.block_hash,
                    'nonce': self.nonce
                }, indent=4))


class Miner:

    def __init__(self, block: Block, leading_zeros: int) -> None:
        self.block = block
        self.leading_zeros = leading_zeros

    def mine(self) -> str:
        while True:
            inter_hash = HashingLib.doubleSHA256(
                str(self.block.previous_hash).encode() +
                str(self.block.merkle_root).encode() +
                str(self.block.nonce).encode()
            )

            if inter_hash[:self.leading_zeros] == "0" * self.leading_zeros:
                self.block.block_hash = inter_hash
                break

            self.block.nonce += 1

        return self.block.block_hash


class Verify:
    
    def verify_transaction(block_num: int, transaction: Transaction) -> bool:
        with open(f'blockchain/Block{block_num}.json', 'r') as f:
            block_data = json.load(f)

        for tx in block_data['transaction_list']:
            if tx['tx_hash'] == transaction.tx_hash:
                merkle_root = block_data['merkle_root']
                merkle_tree = block_data['merkle_tree']
                current_level = merkle_tree[0]
                for i in range(1, len(merkle_tree)):
                    next_level = []
                    double = False
                    if len(current_level) % 2 == 1:
                        double = True
                        current_level.append(current_level[-1])

                    for j in range(0, len(current_level), 2):
                        next_level.append(
                            HashingLib.doubleSHA256(
                                current_level[j].encode() + current_level[j+1].encode()
                            )
                        )   

                    if double:
                        current_level.pop()

                    current_level = deepcopy(next_level)

                if current_level[0] == merkle_root:
                    return True

        return False