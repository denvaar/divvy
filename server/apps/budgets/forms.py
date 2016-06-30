from django import forms

from .models import Transaction, Budget, ExpenseBudget


class TransactionDetailForm(forms.ModelForm):

    class Meta:
        model = Transaction
        exclude = []

    def clean(self):
        cleaned_data = super(TransactionDetailForm, self).clean()
        amount = cleaned_data.get('amount')
        transaction_type = cleaned_data.get('transaction_type')
        if (transaction_type == 'credit' and amount <= 0) or \
           (transaction_type == 'debit' and amount >= 0): 
            raise forms.ValidationError(
                    "Invalid amount for transaction type."
                    " Use negative amount for debits and "
                    "positive amount for credits.")


class BudgetDetailForm(forms.ModelForm):
    
    class Meta:
        model = ExpenseBudget
        exclude = []

