from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Loan
from ..serializers import LoanSerializer
from decimal import Decimal

class LoanView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get all loans for the authenticated user.
        """
        loans = Loan.objects.filter(user=request.user)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Borrow a loan.
        """
        data = request.data
        print(data)
        data['user'] = request.user.id
        serializer = LoanSerializer(data=data)
        if serializer.is_valid():
            loan = serializer.save(balance=data['amount'])
            return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanRepaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, loan_id):
        """
        Make a payment towards a loan.
        """
        try:
            loan = Loan.objects.get(id=loan_id, user=request.user)

            amount_paid = Decimal(request.data.get('amount'))
            if amount_paid <= 0:
                return Response({'error': 'Payment amount must be positive.'}, status=status.HTTP_400_BAD_REQUEST)

            if amount_paid > loan.balance:
                return Response({'error': 'Payment exceeds loan balance.'}, status=status.HTTP_400_BAD_REQUEST)

            loan.balance -= amount_paid
            loan.save()

            return Response({'message': 'Payment successful.', 'balance': loan.balance}, status=status.HTTP_200_OK)
        except Loan.DoesNotExist:
            return Response({'error': 'Loan not found.'}, status=status.HTTP_404_NOT_FOUND)
