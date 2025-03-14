from django.db import models

# Create your models here.
from django.db import models
from collections import defaultdict, deque
from datetime import datetime

# In-memory data structures
farmer_balances = {}  # HashMap for balance storage
farmer_transactions = defaultdict(deque)  # Stack (deque) for transactions


class Farmer(models.Model):
    farmer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)

    def get_balance(self):
        return farmer_balances.get(self.farmer_id, 0)


class Transaction(models.Model):
    TRANSACTION_TYPE = (('deposit', 'Deposit'), ('withdraw', 'Withdraw'))

    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.transaction_type == 'withdraw' and farmer_balances.get(self.farmer.farmer_id, 0) < self.amount:
            raise ValueError("Insufficient Balance")

        # Update balance
        if self.transaction_type == 'deposit':
            farmer_balances[self.farmer.farmer_id] = farmer_balances.get(self.farmer.farmer_id, 0) + self.amount
        else:
            farmer_balances[self.farmer.farmer_id] -= self.amount

        # Store transaction in stack (deque)
        farmer_transactions[self.farmer.farmer_id].appendleft({
            'amount': self.amount, 'type': self.transaction_type, 'timestamp': datetime.now()
        })
        super().save(*args, **kwargs)

    @staticmethod
    def get_recent_transactions(farmer_id, N=5):
        return list(farmer_transactions[farmer_id])[:N]
