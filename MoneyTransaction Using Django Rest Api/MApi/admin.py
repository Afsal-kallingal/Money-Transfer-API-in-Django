from django.contrib import admin
from MApi.models import User,Wallet,Transactions

admin.site.register(User)
admin.site.register( Wallet)
admin.site.register(Transactions)