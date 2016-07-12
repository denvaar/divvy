from copy import copy
import uuid

from django import forms

from apps.core.widgets import TagInput
from apps.core.fields import TagField

from .models import (
    Transaction,
    Budget,
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
    
    _fields = {
        'savings': [],
        'expense': [],
        'debt': []
    }
    
    class BudgetForm(forms.ModelForm):

        class Meta:
            model = Budget
            exclude = ['user', 'budget_type']

        def __init__(self, *args, **kwargs):
            self.user = kwargs.pop('user', None)
            super(BudgetForm, self).__init__(*args, **kwargs)

        def save(self):
            obj = super(BudgetForm, self).save(commit=False)
            obj.user = self.user
            obj.budget_type = budget_type
            obj.save()
            self.save_m2m()
            return obj

    return BudgetForm

