from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Savings, Transaction
from decimal import Decimal
from ..serializers import UserSerializer, SavingsSerializer, TransactionSerializer

# Saving ViewSet
class SavingView(APIView):
    def get(self, request, user_id=None):
        """
        Fetch savings for a specific user if `user_id` is provided.
        Otherwise, fetch all savings records.
        """
        if user_id:
            try:
                # Fetch savings records for a specific user
                savings = Savings.objects.filter(user_id=user_id)
                if not savings.exists():
                    return Response({'error': 'Savings not found for the user.'}, status=status.HTTP_404_NOT_FOUND)

                serializer = SavingsSerializer(savings, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)  # Use `.data` to get JSON serializable data
            except ValueError:
                return Response({'error': 'Invalid id. Id must be a number.'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch all savings records
        savings = Savings.objects.all()
        serializer = SavingsSerializer(savings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new savings record.
        """
        serializer = SavingsSerializer(data=request.data)
        if serializer.is_valid():
            # Update transactions
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, user_id=None):
        """
        Update the amount saved for a specific user.
        """
        try:
            # Fetch savings record for the user
            savings = Savings.objects.get(user_id=user_id)

            # Validate the input amount
            amount = request.data.get('amount_saved')
            if not amount or float(amount) <= 0:
                return Response({'error': 'Invalid amount. Must be a positive number.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the savings amount
            savings.amount_saved += Decimal(amount)
            savings.save()
            
            # Serialize and return the updated savings record
            serializer = SavingsSerializer(savings)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Savings.DoesNotExist:
            return Response({'error': 'Savings record not found.'}, status=status.HTTP_404_NOT_FOUND)

        except ValueError:
            return Response({'error': 'Invalid input. Amount must be a number.'}, status=status.HTTP_400_BAD_REQUEST)