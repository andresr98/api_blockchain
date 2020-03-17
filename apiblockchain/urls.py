from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.Accounts.as_view(), name="Register account"),
    path('transfer', views.Transfers.as_view(), name="Transfers")
]