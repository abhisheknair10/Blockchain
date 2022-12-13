import hashlib
from typing import *


class Transaction:

    def __init__(self, send, rec, amt) -> None:
        self.sender = send
        self.recipient = rec
        self.amount = amt
        self.tx_hash = self.get_tx_hash()

    
    def get_tx_hash(self) -> str:
        return hashlib.sha256(
            str(self.sender).encode() + 
            str(self.recipient).encode() + 
            str(self.amount).encode()
        ).hexdigest()


class Block:
    
    def __init__(self, transaction_list: List[Transaction], previous_hash: str) -> None:
        self.transaction_list = transaction_list
        self.previous_hash = previous_hash
        self.merkle_root = self.merkle_root(transaction_list)
        self.nonce = 0
        


def main():

    tx1 = Transaction("Alice", "Bob", 10)
    tx2 = Transaction("Bob", "Charlie", 5)
    tx3 = Transaction("Charlie", "Alice", 2)
    
    l = [tx1, tx2, tx3]
    print(l[0].tx_hash())
    print(l[1].tx_hash())
    print(l[2].tx_hash())


if __name__ == "__main__":
    main()