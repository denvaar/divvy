from django import forms

from .models import Account


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class AccountDetailForm(forms.ModelForm):

    class Meta:
        model = Account
        exclude = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AccountDetailForm, self).__init__(*args, **kwargs)

    def save(self):
        obj = super(AccountDetailForm, self).save()
        self.user.accounts.add(obj)
        return obj
        
