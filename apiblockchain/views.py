from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .logic.accounts_bl import is_possible_create_account
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

            if is_possible_create_account(password):
                return Response({"status": status.HTTP_201_CREATED, "entity":{"address": password_hash}, "error": ""},\
                status=status.HTTP_201_CREATED)
            else:
                return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error": "Account already exist."},\
                status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error": "Campos ingresador de forma incorrecta"},\
            status=status.HTTP_400_BAD_REQUEST)