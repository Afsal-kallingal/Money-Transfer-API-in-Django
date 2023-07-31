from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User,Wallet,Transactions

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'phone_number']

class UserLoginSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['phone_number', 'password']


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wallet
        fields='__all__'
        depth=1


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transactions
        fields='__all__'
        depth=1
  