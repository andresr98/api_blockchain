from django.db import models

# Create your models here.
class Account(models.Model):
    balance = models.FloatField(blank = True, default = 0.0)
    address = models.CharField(blank = True, max_length = 255)
    mine = models.BooleanField(default = False)

class Header(models.Model):
    nonce = models.IntegerField(blank = True, default = 0)
    prev_hash = models.CharField(blank = True, max_length = 255)
    merkle_root = models.CharField(blank = True, max_length = 255)
    high = models.IntegerField(default = 0, null = True)
    own_hash = models.CharField(primary_key = True, max_length = 255)
    difficult = models.PositiveIntegerField(default = 2, null = True) 

class Block(models.Model):
    own_hash = models.CharField(primary_key = True, max_length = 255)
    header = models.OneToOneField(Header, on_delete=models.SET_NULL, null = True, blank = True)

class Transaction(models.Model):
    from_account = models.CharField(blank = True, max_length = 255)
    quantity = models.FloatField(blank = True, default = 0)
    to_account = models.CharField(blank = True, max_length = 255)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null = True, blank = True)