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

def get_budget_form(budget_model):
    
    TYPES = (
        ('savings', 'Savings'),
        ('expense', 'Expense'),
        ('debt', 'Debt payment'),
    )

    class BudgetForm(forms.ModelForm):
        
        budget_type = forms.ChoiceField(choices=TYPES,
                        label='What will this budget be used for?',
                        widget=forms.Select(
                            attrs={'onChange': 'getFormType()'}))
        
        class Meta:
            model = budget_model
            exclude = []

        def __init__(self, *args, **kwargs):
            super(BudgetForm, self).__init__(*args, **kwargs)
            print(self.fields)

    return BudgetForm
    
