from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .models import Header
from .logic.accounts_bl import *
from .logic.transactions_bl import *
from .logic.headers_bl import *
from .logic.blocks_bl import *
import hashlib

# Create your views here.
def index(request):
    return HttpResponse("Hello from the API URLS")

#This view just let a user to create an Account
class Accounts(APIView):
    def post(self, request):
        try:
            data = request.data
            password = data['password']
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            if is_possible_create_account(password_hash):
                return Response({"status": status.HTTP_201_CREATED, "entity":{"address": password_hash}, "error": ""},\
                status=status.HTTP_201_CREATED)
            else:
                return Response({"status": status.HTTP_406_NOT_ACCEPTABLE, "entity":"", "error": "Account already exist."},\
                status=status.HTTP_406_NOT_ACCEPTABLE)
        except KeyError:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error": "Campos ingresador de forma incorrecta"},\
            status=status.HTTP_400_BAD_REQUEST)

#This view manage all the process to insert a transaction in a block
class Transfers(APIView):
    def post(self, request):
        try:
            data = request.data
            from_account = data['from_account']
            quantity = data['quantity']
            to_account = data['to_account']
            sign = data['sign']

            if not can_insert_transaction():
                return Response({"status": status.HTTP_202_ACCEPTED, "entity":"", "error": "Maximum transactions per block reached. Please mine a new block."},\
                status=status.HTTP_202_ACCEPTED)

            if not validate_sign(sign, from_account):
                return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error": "Sign does not match from account. Please verify"},\
                status=status.HTTP_400_BAD_REQUEST)

            f_account, t_account = get_accounts(from_account, to_account)

            if f_account is None or t_account is None:
                return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error": "From Account or To Account does not exists."},\
                status=status.HTTP_400_BAD_REQUEST)

            if not transfer(f_account, quantity, t_account):
                return Response({"status": status.HTTP_202_ACCEPTED, "entity":"", "error": "From Account does not have sufficient balance"},\
                status=status.HTTP_202_ACCEPTED)
            
            insert_transaction(from_account, quantity, to_account)
            return Response({"status": status.HTTP_201_CREATED, "entity":"Transaction complete", "error": ""},\
                status=status.HTTP_201_CREATED)

        except KeyError:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error": "Campos ingresador de forma incorrecta"},\
            status=status.HTTP_400_BAD_REQUEST)

#This view will insert the genesis block and define how many coins could be on the entire blockchain
class Configurations(APIView):
    def post(self, request):
        try:
            data = request.data
            max_coins = data['max_coins']
            max_tx = data['max_tx']

            #If a mine account exist, return an error
            result, mine_address = create_mine_account(max_coins)
            if not result:
                return Response({"status": status.HTTP_202_ACCEPTED, "entity":"", "error": "Configuration has alredy been done"},\
                status=status.HTTP_202_ACCEPTED)
            else:
                #Insert the primitive transaction and mine the genesis block
                insert_transaction(mine_address, max_coins, mine_address)
                result = mine_genesis_block(mine_address, max_coins)

                if result:
                    return Response({"status": status.HTTP_201_CREATED, "entity":"Configuration and genesis block created", "error": ""},\
                    status=status.HTTP_201_CREATED)
                    
                return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "entity":"", "error": "Configuration has finished with an error"},\
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error": "Campos ingresador de forma incorrecta"},\
            status=status.HTTP_400_BAD_REQUEST)

#This view will return all block headers order by their height
class Blockchains(APIView):
    def get(self, request):
        headers = Header.objects.values('nonce', 'prev_hash', 'merkle_root', 'high', 'own_hash', 'difficult').order_by('high')

        return Response({"status": status.HTTP_200_OK, "entity": headers, "error": ""},\
                status=status.HTTP_200_OK)

#This view will return all the transaction inside a block.
class Transactions(APIView):
    def get(self, request, hash):
        try:
            transactions = get_transactions_in_block(hash)
            return Response({"status": status.HTTP_200_OK, "entity":transactions, "error": ""},\
                status=status.HTTP_200_OK)
        except KeyError:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error": "Campos ingresador de forma incorrecta"},\
            status=status.HTTP_400_BAD_REQUEST)

class Mines(APIView):
    def post(self, request):
        try:
            data = request.data
            difficult = data['difficult']
            account_address = data['account']

            miner_account = get_mine_account()
            if miner_account == None:
                return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error": "There is no a mine account. Can not mine a block"},\
                status=status.HTTP_400_BAD_REQUEST)

            account = get_account(account_address)
            if account == None:
                return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error": "The address inserted do not exists"},\
                status=status.HTTP_400_BAD_REQUEST)

            transfer(miner_account, 25, account)
            insert_transaction(miner_account.address, 25, account_address)
            result = to_mine(difficult)

            if result: 
                return Response({"status": status.HTTP_201_CREATED, "entity":"Block mined succesfully", "error": ""},\
                status=status.HTTP_201_CREATED)

            return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "entity":"", "error": "Can not insert block, header or transactions"},\
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except KeyError:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error": "Campos ingresador de forma incorrecta"},\
            status=status.HTTP_400_BAD_REQUEST)