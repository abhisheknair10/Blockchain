import hashlib
from typing import *
from hashinglibrary import HashingLibrary

class Transaction:

    def __init__(self, sender: str, recipient: str, amount: float) -> None:
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.tx_hash = self.get_tx_hash()

    
    def get_tx_hash(self) -> str:
        return HashingLibrary.doubleSHA256(
            str(self.sender).encode() + 
            str(self.recipient).encode() + 
            str(self.amount).encode()
        )   