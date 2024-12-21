from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Savings, Transaction
from ..serializers import UserSerializer, SavingsSerializer, TransactionSerializer
from ..services.transactions_services import deposit_to_savings, create_transaction

# Transaction ViewSet
class TransactionView(APIView):
    def get(self, request, user_id=None):
        """
        Retrieve transactions for a specific user if `user_id` is provided.
        Otherwise, return all transactions.
        """
        if user_id:
            try:
                # Fetch transactions for the given user ID
                transactions = Transaction.objects.filter(user_id=user_id)
                if not transactions.exists():
                    return Response(
                        {'error': 'No transactions found for the given user.'},
                        status=status.HTTP_404_NOT_FOUND
                    )

                serializer = TransactionSerializer(transactions, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except ValueError:
                return Response(
                    {'error': 'Invalid user ID. It must be a number.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Fetch all transactions
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction_type = serializer.validated_data.get("transaction_type")
            amount = serializer.validated_data.get("amount")
            user_id = serializer.validated_data.get("user_id")

            if transaction_type == "deposit":
                try:
                    # Use the service to handle deposit and savings update
                    savings = deposit_to_savings(user_id, amount)
                    create_transaction(user_id, amount, "deposit")
                except ValueError as e:
                    return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)