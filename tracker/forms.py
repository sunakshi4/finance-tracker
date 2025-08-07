from django import forms
from .models import Transaction, Budget
from datetime import date


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'type', 'amount', 'description','date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['month', 'amount']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['month'].initial = date.today().replace(day=1)