from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    return HttpResponse("Hello from the API URLS")