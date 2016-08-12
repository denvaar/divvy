from django.contrib import admin
from django import forms

from fancy_feast.forms.fields import TagField

from .models import (
    Budget, 
    Transaction,
    Tag,
    BudgetThroughModel,
    Color
)


class TransactionForm(forms.ModelForm):

    tags = TagField(model=Tag, field='name')

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
    
    def save(self, commit):
        obj = super(TransactionForm, self).save(commit=False)
        obj.save()
        [obj.tags.add(t) for t in self.cleaned_data.get('tags')]
        self.save_m2m()
        return obj

class TransactionAdmin(admin.ModelAdmin):
    form = TransactionForm


admin.site.register(Budget)
admin.site.register(BudgetThroughModel)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Tag)
admin.site.register(Color)

