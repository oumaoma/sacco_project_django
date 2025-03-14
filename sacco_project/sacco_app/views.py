from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .models import Farmer, Transaction
import time
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Deposit Money
class DepositView(View):
    def post(self, request, farmer_id, amount):
        farmer = Farmer.objects.get(pk=farmer_id)
        transaction = Transaction(farmer=farmer, amount=amount, transaction_type='deposit')
        transaction.save()
        return JsonResponse({'message': 'Deposit successful', 'balance': farmer.get_balance()})

# Withdraw Money
class WithdrawView(View):
    def post(self, request, farmer_id, amount):
        farmer = Farmer.objects.get(pk=farmer_id)
        transaction = Transaction(farmer=farmer, amount=amount, transaction_type='withdraw')
        transaction.save()
        return JsonResponse({'message': 'Withdrawal successful', 'balance': farmer.get_balance()})

# Retrieve Account Statement
class StatementView(View):
    def get(self, request, farmer_id, N=5):
        transactions = Transaction.get_recent_transactions(farmer_id, N)
        return JsonResponse({'transactions': transactions})

# Dashboard GUI
def dashboard(request):
    farmers = Farmer.objects.all()
    return render(request, 'sacco_app/dashboard.html', {'farmers': farmers})

# Authentication Views
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'sacco_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
