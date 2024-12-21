from rest_framework import serializers
from .models import CustomUser, Savings, Transaction

# CustomUser serializer
class UserSerializer( serializers.ModelSerializer):
    password_alt = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
    class Meta:
        model = CustomUser
        fields = ( "id", "username", "password", )

# Savings serializer
class SavingsSerializer( serializers.ModelSerializer):
    class Meta:
        model = Savings
        fields = '__all__'

# Transaction serializer
class TransactionSerializer( serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'