from apiblockchain.models import Transaction
import hashlib

transactions = []
max_transactions = 3

def can_insert_transaction():
    if len(transactions) >= max_transactions:

        for transaction in transactions:
            print("P.K1 " + str(transaction.from_account) + " P.K 2" + str(transaction.to_account))
        return False
    return True

def insert_transaction(from_account, quantity, to_account):
    transaction = Transaction(from_account=from_account, quantity=quantity,to_account=to_account, block =None)
    transactions.append(transaction)

