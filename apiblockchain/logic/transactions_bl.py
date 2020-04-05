from apiblockchain.models import Transaction
import hashlib

transactions = []
max_transactions = 5

def can_insert_transaction():
    if len(transactions) >= max_transactions:
        return False
    return True

def insert_transaction(from_account, quantity, to_account):
    transaction = Transaction(from_account=from_account, quantity=quantity,to_account=to_account, block =None)
    transactions.append(transaction)

def get_transactions_in_block(hash):
    txs = Transaction.objects.values('from_account', 'quantity', 'to_account').filter(block=hash)
    return txs

def get_current_transactions():
    return transactions

def get_hash_current_transactions():
    hash_txs = []

    for transaction in transactions:
        string_tx = "P.K1 " + str(transaction.from_account) + " P.K 2" + str(transaction.to_account)
        hash_tx = hashlib.sha256(string_tx.encode()).hexdigest()
        hash_txs.append(hash_tx)
    return hash_txs

def reset_transactions():
    self.transactions = []

def save_current_transactions(block):
    print(transactions)
    for transaction in transactions:
        try:
            transaction.block = block
            transaction.save()
        except Exception:
            return False
    reset_transactions()
    return True
        