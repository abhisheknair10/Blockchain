import hashlib
from typing import *


class HashingLibrary:
    
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
        return HashingLibrary.doubleSHA256(
            str(self.sender).encode() + 
            str(self.recipient).encode() + 
            str(self.amount).encode()
        )     



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




def main():

    tx1 = Transaction(
        "c36ba8fa451512b07fba65fa12b12f37ee508ac9564195bec3ed97ad5e3f3225", 
        "35dcc88de4c81a9edf183e1ae365b7bd9715db4697719c3b660c2924790fe47c",
        3.5
    )

    tx2 = Transaction(
        "4e3c8d90862f30d384259b61920a66529887a476c4e713929bc46a0b865f2713", 
        "4d8225d4599f1af070b1079e865b2df8b1bbf919902028bd1d80fd94c78273c0",
        10.4
    )

    tx3 = Transaction(
        "39a3e05d53e6e3dc595630dc0894cf97f367eb5af8a9433131568f77a1239afe", 
        "49e419a45e5fe1635c0dde6c541f4cf99b393bf7158c8c90cad86329b6ab3adf",
        0.3
    )

    transaction_list = [tx1, tx2, tx3]

    block = Block(
        transaction_list, 
        "0000000000000000000000000000000000000000000000000000000000000000"
    )

    block.output_block_data()
    


if __name__ == "__main__":
    main()