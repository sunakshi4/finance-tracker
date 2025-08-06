from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'type', 'amount', 'description','date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }