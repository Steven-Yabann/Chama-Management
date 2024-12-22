from rest_framework import serializers
from .models import User, Savings, Transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# User serializer
class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 
            'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'user_type', 
            'groups', 'user_permissions', 'password1'
        )

    def validate(self, attrs):
        # Validates the password if needed
        password = attrs.get('password')
        if not password:
            raise serializers.ValidationError("Password is required.")
        validate_password(password)  # Assuming you have a custom validation function
        return attrs

    def create(self, validated_data):
        # Create user with required fields
        user = User.objects.create(
            username=validated_data['email'],
            user_type=validated_data['user_type'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=True, 
            is_staff=False,
        )

        # Set password (hashed) for the user
        user.set_password(validated_data['password'])
        user.save()

        return user

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