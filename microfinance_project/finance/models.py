from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    # Add additional fields if needed
    user_type_choices = [
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]

    user_type = models.CharField(max_length=10, choices=user_type_choices, default='member')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True, blank=True)

    def __str__(self):
        return self.username

# Savings model
class Savings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="savings", default='member')
    amount_saved = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_saved = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.amount_saved}'

# Transaction model
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions", default='member')
    transaction_type_choices = [
        ('deposit', 'Deposit'),
    ]
    transaction_type = models.CharField(max_length=10, choices=transaction_type_choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now=True)

    def __str__(self):
        return f'{self.transaction_type} - {self.amount} - {self.user.username}'
