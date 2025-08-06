from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from django.contrib import messages
from .models import Transaction
from django.db.models import Sum

def register(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
            form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)
    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income-total_expenses
    return render (request, 'dashboard.html', {
        'total_income': total_income,
        'total_expenses' : total_expenses,
        'balance' : balance,
        'transactions': transactions})

@login_required
def transaction_list(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-date')
    return render (request, 'transaction_list.html', {
        'transactions': transactions})


@login_required
def add_transaction(request):
    if request.method=='POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'transaction added successfully')
            return redirect('dashboard')
    else:
            form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})

@login_required
def delete_transaction(request, pk):
    user = request.user
    transaction = get_object_or_404(Transaction,pk=pk,user=user)
    if request.method == "POST":
        transaction.delete()
        messages.success(request, 'Transaction deleted')
        return redirect('transaction_list')
    return render (request, 'delete_transaction.html', {'transaction': transaction})

@login_required
def edit_transaction(request, pk):
    user = request.user
    transaction = get_object_or_404(Transaction,pk=pk,user=user)
    if request.method=='POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'transaction updates successfully')
            return redirect('transaction_list')
    else:
            form = TransactionForm(instance=transaction)
    return render(request, 'edit_transaction.html', {'form': form})
