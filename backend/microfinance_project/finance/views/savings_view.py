from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Savings, Transaction
from decimal import Decimal
from ..serializers import SavingsSerializer
from ..services.services import create_transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Saving ViewSet
class SavingView(APIView):
    def get(self, request, user_id=None):
        """
        Fetch savings for a specific user if `user_id` is provided.
        Otherwise, fetch all savings records.
        """
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
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

    def patch(self, request):
        """
        Update the amount saved for a specific user. Supports both deposit and withdrawal.
        """
        try:
            # Fetch savings record for the user
            print(request.data)
            savings = Savings.objects.get(group_id= request.data.get('group_id'))

            # Validate the input amount
            amount_str = request.data.get('amount')
            print("Amount Value:", amount_str)
            print("Amount Type:", type(amount_str))
            if not amount_str:
                return Response({'error': 'Amount is required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Convert amount to Decimal
                amount = Decimal(amount_str.strip())
                print("Converted Amount:", amount)
                print("Amount Type:", type(amount))
            except (ValueError, TypeError) as e:
                print("Decimal Conversion Error:", str(e))
                return Response({'error': 'Invalid input. Amount must be a number.'}, status=status.HTTP_400_BAD_REQUEST)


            if amount <= 0:
                return Response({'error': 'Invalid amount. Must be a positive number.'}, status=status.HTTP_400_BAD_REQUEST)

            # Handle transaction type
            transaction_type = request.data.get('transaction_type')
            print("Savings Amount Type:", type(savings.amount))
            if transaction_type == 'deposit':
                savings.amount += amount
            elif transaction_type == 'withdrawal':
                if amount > savings.amount:
                    return Response({'error': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)
                savings.amount -= amount
            else:
                return Response({'error': 'Invalid transaction type.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update transactions
            group_id = request.data.get('group_id')
            user_id = request.data.get('user_id')
            create_transaction(user_id, amount, transaction_type, group_id)

            savings.save()

            # Serialize and return the updated savings record
            serializer = SavingsSerializer(savings)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Savings.DoesNotExist:
            return Response({'error': 'Savings record not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:  # Catch all exceptions
            print("Unexpected Error:", str(e))  # Debug log
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


