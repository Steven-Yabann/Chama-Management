import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from dateutil.relativedelta import relativedelta

# Custom User model
class User(AbstractUser):
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

# Chama group Model
class ChamaGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=  100)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_groups')
    group_code = models.CharField(max_length=10, unique=True, editable=False)
    group_members = models.ManyToManyField(User, through='GroupMember', related_name='chama_groups')

    def save(self, *args, **kwargs):
        # Auto-generate group_code if not set
        if not self.group_code:
            self.group_code = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
       
# Chama group member model
class GroupMember(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    group = models.ForeignKey(ChamaGroup, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} in {self.group.name}"

# Savings model
class Savings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="savings")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    group = models.ForeignKey(ChamaGroup, on_delete=models.CASCADE, related_name='savings')
    saved_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.amount_saved}'

# Transaction model
class Transaction(models.Model):
    transaction_type_choices = [
        ('deposit', 'Deposit'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    group = models.ForeignKey(ChamaGroup, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=transaction_type_choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now=True)

    def __str__(self):
        return f'{self.transaction_type} - {self.amount} - {self.user.username}'


# Loan model
class Loan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    group = models.ForeignKey('ChamaGroup', on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)  # Default 1% interest
    term_in_months = models.PositiveIntegerField()  # Loan term in months
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_monthly_payment(self):
        """
        Calculates the monthly payment using the amortization formula.
        """
        principal = Decimal(self.amount)
        rate = Decimal(self.interest_rate) / (100 * 12)
        months = self.term_in_months

        if rate > 0:
            monthly_payment = principal * rate * (1 + rate)**months / ((1 + rate)**months - 1)
        else:
            monthly_payment = principal / months

        return round(monthly_payment, 2)

    def __str__(self):
        return f"Loan {self.id} - {self.user.username}"

