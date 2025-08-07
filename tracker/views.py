from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm, BudgetForm
from django.contrib import messages
from .models import Transaction, Budget
from django.db.models import Sum
from datetime import date
from django.utils.timezone import now
from django.core.paginator import Paginator

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
    transactions = Transaction.objects.filter(user=user).order_by('-date')
    recent_transactions=transactions[:5]
    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income-total_expenses

    today = now().date()
    # current_month_start = today.replace(day=1)
    current_month_expenses = transactions.filter(type='expense', date__year=today.year, date__month=today.month).aggregate(Sum('amount'))['amount__sum'] or 0
    current_month_budget = Budget.objects.filter(user=user, month__month=today.month).first()
    budget_amount = current_month_budget.amount if current_month_budget else 0
    budget_difference = budget_amount-current_month_expenses

    return render (request, 'dashboard.html', {
        'total_income': total_income,
        'total_expenses' : total_expenses,
        'balance' : balance,
        'transactions': transactions,
        'recent_transactions': recent_transactions,
        'budget_amount': budget_amount,
        'current_month_expenses': current_month_expenses,
        'budget_difference': budget_difference,
        'current_month_budget':current_month_budget
        })

@login_required
def transaction_list(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-date')

    paginator = Paginator(transactions,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render (request, 'transaction_list.html', {
        'transactions': transactions,
        'page_obj': page_obj})


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

@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('dashboard')
    else:
        form = BudgetForm()
    return render(request, 'add_budget.html', {'form': form})


@login_required
def edit_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'edit_budget.html', {'form': form})