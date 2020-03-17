from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .logic.accounts_bl import *
import hashlib

# Create your views here.
def index(request):
    return HttpResponse("Hello from the API URLS")

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

class Transfers(APIView):
    def post(self, request):
        try:
            data = request.data
            from_account = data['from_account']
            quantity = data['quantity']
            to_account = data['to_account']
            sign = data['sign']

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

            return Response({"status": status.HTTP_201_CREATED, "entity":"Transaction complete", "error": ""},\
                status=status.HTTP_201_CREATED)

        except KeyError:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error": "Campos ingresador de forma incorrecta"},\
            status=status.HTTP_400_BAD_REQUEST)