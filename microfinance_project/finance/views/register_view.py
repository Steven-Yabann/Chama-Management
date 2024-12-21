from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from ..serializers import UserSerializer  # Ensure correct import

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            print(token.key)
            return Response({'token': token.key, 'username': user.username}, status=status.HTTP_201_CREATED)
        return Response({"error": "Failed Registration"}, status=status.HTTP_400_BAD_REQUEST)
