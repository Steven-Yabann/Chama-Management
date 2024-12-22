from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token


class LogoutView(APIView):  
    def post(self, request):
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
