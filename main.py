import hashlib
from typing import *
from transaction import Transaction
from block import Block


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