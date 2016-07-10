from copy import copy
import uuid

from django import forms

from apps.core.widgets import TagInput
from apps.core.fields import TagField

from .models import (
    Transaction,
    Budget,
    ExpenseBudget,
    SavingsBudget,
    DebtBudget,
    Tag
)


class TransactionDetailForm(forms.ModelForm):
        
    tags = TagField(Tag, widget=TagInput(
            attrs={
                'class':'tag-input'
            }))


    class Meta:
        model = Transaction
        exclude = ['tags']

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

    def save(self):
        obj = super(TransactionDetailForm, self).save(commit=False)
        print(self.cleaned_data)
        obj.save()
        [obj.tags.add(t) for t in self.cleaned_data.get('tags')]
        self.save_m2m()
        return obj 


def get_budget_form(budget_type):
    
    budgets = {
        'savings': SavingsBudget,
        'expense': ExpenseBudget,
        'debt': DebtBudget
    }

    class BudgetForm(forms.ModelForm):

        class Meta:
            model = budgets[budget_type]
            exclude = []

    return BudgetForm

