from django.contrib import admin

from .models import Account, Header, Block

# Register your models here.
admin.site.register(Account)
admin.site.register(Header)
admin.site.register(Block)