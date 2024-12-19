from django.db import models

# Create your models here.
# userModel
class User(models.Model):
    user_choices = [
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    user_type = models.CharField(max_length=10, choices=user_choices, default='Member')

    def __str__(self):
        return self.username
    
# Savings model
class Savings(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_saved = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_saved = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.amountSaved}'
    
# Transaction model
class Transaction(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type_choice = [
        ('deposit', 'Deposit'),
    ]
    transaction_type = models.CharField(max_length=10, choices=transaction_type_choice)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now=True)


    def __str__(self):
        return f'{self.transaction_type} - {self.amount} - {self.user.username}'