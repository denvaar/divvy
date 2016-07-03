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


def dynamic_form_factory(base_model, groups,
                         label, excluded_fields=[]):
    """
        ``base_model`` is a model that contains fields
        that are common to each group.
        ``groups`` is a tuple mapping to additional
        models.
        ``excluded_fields`` is a list of fields to exclude
        from the form.
    """
    TYPES = (
        ('', '----'),
        ('savings', 'Savings'),
        ('expense', 'Expense'),
        ('debt', 'Debt payment'),
    )

    # Grab extra fields to include
    extra_fields = {}
    for model_mapping in groups:
        extra_fields[model_mapping[0]] = []
        for field in model_mapping[1]._meta.fields:
            if field not in base_model._meta.fields:
                if field.formfield():
                    extra_fields[model_mapping[0]].append(
                        (field.verbose_name, field.formfield()))
    for k,v in extra_fields.items():
        print(k,v)

    class _Form(forms.ModelForm):
        
        # The field which determines which group to display.
        group_select = forms.ChoiceField(choices=TYPES,
            label=label, required=True,
            widget=forms.Select(
                attrs={'onChange': 'getFormGroup()'}))

        class Meta:
            model = base_model
            exclude = excluded_fields

        def __init__(self, *args, **kwargs):
            super(_Form, self).__init__(*args, **kwargs)
            # Now add the extra form fields from the groups.
            for group, fields in extra_fields.items():
                for _field in fields:
                    self.fields[_field[0]] = _field[1]
                    self.fields[_field[0]].widget.attrs['data-groupid'] = \
                            'group_{}'.format(group)
                        #widget=field.widget(
                        #attrs={'data-groupid': 'group_{}'.format('')}))

    return _Form

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
    
