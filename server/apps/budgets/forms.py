from django import forms

from .models import (
    Transaction,
    Budget,
    ExpenseBudget,
    SavingsBudget,
    DebtBudget
)


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


def get_budget_form(base_model):
    
    TYPES = (
        ('', '----'),
        ('savings', 'Savings'),
        ('expense', 'Expense'),
        ('debt', 'Debt payment'),
    )

    PERIODS = (
        ('yearly', 'Yearly'),
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
        ('daily', 'Daily'),
    )

    MODELS = {
        'savings': SavingsBudget,
        'expense': ExpenseBudget,
        'debt': DebtBudget
    }

    class BudgetForm(forms.ModelForm):
        
        limit = forms.DecimalField(widget=forms.NumberInput(
                    attrs={'data-groupid': 'group_expense'}))
        period = forms.ChoiceField(choices=PERIODS,
                    widget=forms.Select(
                        attrs={'data-groupid': 'group_expense'}))

        budget_type = forms.ChoiceField(choices=TYPES,
                        label='What will this budget be used for?',
                        required=True,
                        widget=forms.Select(
                            attrs={'onChange': 'getFormGroup()'}))
        
        class Meta:
            model = base_model
            exclude = []

        def __init__(self, *args, **kwargs):
            super(BudgetForm, self).__init__(*args, **kwargs)

        def save(self):
            data = self.cleaned_data
            _model = MODELS[data['budget_type']]
            data.pop('budget_type')
            _model.objects.create(**data)

    return BudgetForm
    
