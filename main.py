import hashlib
from typing import *
from block import *
import random


def main():

    senders = ["Alice", "Bob", "Charlie", "Dave", "Eve"]
    recipients = ["Alice", "Bob", "Charlie", "Dave", "Eve"]

    transaction_list = []
    while True:
        for i in range(random.randint(1, 20)):
            transaction_list.append(
                Transaction(
                    sender=senders[random.randint(0, len(senders) - 1)],
                    recipient=recipients[random.randint(0, len(recipients) - 1)],
                    amount=round(random.uniform(0, 1000), 2)
                )
            )

        block = Block(transaction_list=transaction_list)
        transaction_list = []


if __name__ == "__main__":
    main()