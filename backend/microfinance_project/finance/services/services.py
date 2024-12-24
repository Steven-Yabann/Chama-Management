from decimal import Decimal
from ..models import Savings, Transaction, User

def deposit_to_savings(user_id, amount):
    try:
        savings = Savings.objects.get(user_id=user_id)
        savings.amount_saved += Decimal(amount)
        savings.save()
        return savings
    except Savings.DoesNotExist:
        raise ValueError("Savings record not found for this user.")

def create_transaction(user_id, amount, transaction_type, group_id):
    # Fetch the User instance based on the user_id
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValueError("User does not exist")
    
    # Convert amount to Decimal if necessary
    amount_decimal = Decimal(amount)
    print(f'user is {user} , amount is {amount_decimal} and transaction type is {transaction_type}')
    
    # Create the transaction object
    return Transaction.objects.create(
        user=user, amount=amount_decimal, transaction_type=transaction_type, group_id=group_id
    )
