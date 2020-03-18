from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.Accounts.as_view(), name='Register account'),
    path('transfer', views.Transfers.as_view(), name='Transfers'),
    path('blockchain', views.Blockchains.as_view(), name='blockchain'),
    path('blockchain/<slug:hash>', views.Transactions.as_view(), name="block-contain"),
]