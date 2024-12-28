import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

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




