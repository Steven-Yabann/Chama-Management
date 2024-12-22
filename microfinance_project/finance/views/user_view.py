from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import User, Savings, Transaction
from ..serializers import UserSerializer, SavingsSerializer, TransactionSerializer

class UserView(APIView):
    def get(self, request, id=None):
        """
        Fetch a single user if `id` is provided.
        Otherwise, fetch all users.
        """
        if id:
            try:
                # Fetch a single user
                user = User.objects.get(id=id)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response({'error': 'Invalid id. Id must be a number.'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch all users
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            user_type = serializer.validated_data.get("user_type")
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)










