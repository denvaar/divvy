from django.contrib import admin
from django import forms

from .models import Budget, Transaction, Tag


class TransactionForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        exclude = []

    def clean(self):
        cleaned_data = super(TransactionForm, self).clean()
        amount = cleaned_data.get('amount')
        transaction_type = cleaned_data.get('transaction_type')
        if (transaction_type == 'credit' and amount <= 0) or \
           (transaction_type == 'debit' and amount >= 0):
            raise forms.ValidationError(
                    "Invalid amount for transaction type.")


class TransactionAdmin(admin.ModelAdmin):
    form = TransactionForm


admin.site.register(Budget)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Tag)

