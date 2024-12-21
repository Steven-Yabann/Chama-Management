from decimal import Decimal
from ..models import Savings, Transaction

def deposit_to_savings(user_id, amount):
    try:
        savings = Savings.objects.get(user_id=user_id)
        savings.amount_saved += Decimal(amount)
        savings.save()
        return savings
    except Savings.DoesNotExist:
        raise ValueError("Savings record not found for this user.")

def create_transaction(user_id, amount, transaction_type):
    return Transaction.objects.create(
        user_id=user_id, amount=amount, transaction_type=transaction_type
    )
