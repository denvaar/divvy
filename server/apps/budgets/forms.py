from django import forms

from .models import Transaction


class TransactionDetailForm(forms.ModelForm):

    class Meta:
        model = Transaction
        exclude = []

