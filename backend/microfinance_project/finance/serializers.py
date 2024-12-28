from rest_framework import serializers
from .models import User, Savings, Transaction, GroupMember, ChamaGroup
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
            username=validated_data['username'],
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


class ChamaGroupSerializer(serializers.ModelSerializer):
    group_members = serializers.StringRelatedField(many=True, read_only=True)
    admin = UserSerializer()
    class Meta:
        model = ChamaGroup
        fields = ('id', 'name', 'description', 'admin', 'group_code', 'group_members')
        read_only_fields = ['group_code']


class GroupMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = GroupMember
        fields = ('id', 'user', 'group', 'joined_at')


class SavingsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Savings
        fields = ('id', 'amount', 'saved_at', 'group', 'user')


class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Transaction
        fields = ('id', 'transaction_type', 'amount', 'date', 'group', 'user')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
    
        # custom classes
        token['id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['user_type'] = user.user_type

        return token