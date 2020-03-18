from apiblockchain.models import Account
from django.db.models import F

import hashlib

def is_possible_create_account(password):
    try:
        account = Account.objects.get(address=password)
        return False
    except Account.DoesNotExist:
        account = Account(balance = 0, address=password)
        account.save()
        return True

def validate_sign(sign, from_account):
    hash_sign = hashlib.sha256(sign.encode()).hexdigest()

    if(hash_sign == from_account):
        return True
    else:
        return False

def get_accounts(from_account, to_account):
    try:
        f_account = Account.objects.get(address=from_account)
        t_account = Account.objects.get(address=to_account)

        return f_account, t_account
    except Account.DoesNotExist:
        return None, None

def transfer(from_account, quantity, to_account):
    from_balance = from_account.balance

    if from_balance < quantity:
        return False

    from_account.balance = F('balance') - quantity
    to_account.balance = F('balance') + quantity
    from_account.save()
    to_account.save()
    return True

def create_mine_account(max_coins):
    try:
        miner_account = Account.objects.get(mine=True)
        return False, None
    except Account.DoesNotExist:
        password = "miner account"
        address = hashlib.sha256(password.encode()).hexdigest()
        account = Account(balance=max_coins, address=address, mine=True)
        account.save()
        return True, address

def get_mine_account():
    try:
        miner_account = Account.objects.get(mine=True)
        return miner_account
    except Account.DoesNotExist:
         return None