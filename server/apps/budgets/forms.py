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
        fields = [
            'name',
            'amount',
            'transaction_type',
            'created',
            'description',
            'account',
            'budget',
            'tags']

    def clean(self):
        cleaned_data = super(TransactionDetailForm, self).clean()

    def save(self):
        obj = super(TransactionDetailForm, self).save(commit=False)
        obj.save()
        [obj.tags.add(t) for t in self.cleaned_data.get('tags')]
        self.save_m2m()
        return obj 


def get_budget_form(budget_type, user):
    
    _fields = {
        'savings': ['title','goal','goal_date','amount'],
        'expense': ['title','goal','goal_date','period'],
        'debt': ['title','goal','payment_amount','goal_date','period'],
    }
    _fields[budget_type].extend(['icon','icon_color'])
    
    _labels = {
        'savings': ['Label','Goal amount','Goal date','Current amount saved'],
        'expense': ['Label','Expense amount','Due date','Period'],
        'debt': ['Label','Total amount owed','Payment amount','Payment due date','Payment interval'],
    }
    
    class BudgetForm(forms.ModelForm):

        class Meta:
            model = Budget
            fields = _fields[budget_type]

        def __init__(self, *args, **kwargs):
            super(BudgetForm, self).__init__(*args, **kwargs)
            for field in zip(_fields[budget_type], _labels[budget_type]):
                self.fields[field[0]].label = field[1]
                

        def save(self):
            obj = super(BudgetForm, self).save(commit=False)
            obj.user = user
            obj.budget_type = budget_type
            obj.save()
            self.save_m2m()
            return obj

    return BudgetForm

