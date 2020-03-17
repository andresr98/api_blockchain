from apiblockchain.models import Account

def is_possible_create_account(password):

    account = Account.objects.values('id').get(address=password)
    
    if not account:
        account = Account(balance = 0, address=password)
        account.save()
        return True
    else:
        return False