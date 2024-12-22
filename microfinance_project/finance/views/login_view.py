from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

class LoginView(APIView):
    def post(self, request):
        login_username = request.data.get('username')
        login_password = request.data.get('password')
        user = authenticate(username = login_username, password = login_password)
        
        if user is not None:
            return Response({"message": "Login successful", "username": user.username}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)