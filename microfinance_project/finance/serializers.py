from rest_framework import serializers
from .models import User, Savings, Transaction

# user serializer
class UserSerializer( serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# Savings serializer
class SavingsSerializer( serializers.ModelSerializer):
    class Meta:
        model = Savings
        fields = '__all__'

# user serializer
class TransactionSerializer( serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'