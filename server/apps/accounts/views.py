import json

from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import TemplateView, View
from django.http import HttpResponseRedirect

from apps.budgets.models import Transaction, Budget, BudgetThroughModel
from apps.budgets.utils import get_expenses_data, get_savings_data

from .models import Account
from .forms import LoginForm, AccountDetailForm


class LoginFormView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get_success_url(self):
        next_param = self.request.GET.get('next', None)
        if next_param:
            return next_param
        return reverse('accounts:accounts-overview')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(self.request, user)
            return super(LoginFormView, self).form_valid(form)
        form.errors['__all__'] = form.error_class(['Invalid login'])
        return render(self.request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('accounts:login'))


class AccountsOverview(TemplateView):
    template_name = 'accounts/accounts.html'

    def get_context_data(self, **kwargs):
        context = super(AccountsOverview, self).get_context_data(**kwargs)
        context['total_balance'] = 0.0
        for account in self.request.user.accounts.all():
            context['total_balance'] += float(account.balance)
        uncategorized_amt = context['total_balance'] 
        budget_names = []  
        for transaction in Transaction.objects.filter(
                transaction_type='credit'):
            for i in transaction.budget_through_models.all():
                uncategorized_amt -= float(i.amount) 
        context['uncat_balance'] = float(uncategorized_amt)

        context['expenses_dataset'] = json.dumps(get_expenses_data(
                self.request.user)) 
        context['savings_dataset'] = json.dumps(get_savings_data(
                self.request.user, context['uncat_balance'])) 
        return context

    def get_current_page(self):
        return 'accounts'


class DashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'
   
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        transactions = Transaction.objects.filter(
            account__app_users=self.request.user).order_by('-created')
        context['transactions'] = transactions
        context['budgets'] = Budget.objects.filter(
            user=self.request.user)
        context['total_balance'] = 0.0
        for account in self.request.user.accounts.all():
            context['total_balance'] += float(account.balance)
       
        context['dataset'] = json.dumps(get_summary_data(self.request.user)) 
        return context


class AccountAddView(CreateView):
    template_name = 'accounts/account_add.html'
    model = Account
    form_class = AccountDetailForm
    success_message = "Account created."

    def post(self, *args, **kwargs):
        if 'cancel' in self.request.POST:
            return HttpResponseRedirect(reverse('accounts:accounts-overview'))
        return super(AccountAddView, self).post(*args, **kwargs)

    def get_success_url(self):
        return reverse('accounts:accounts-overview')

    def get_form_kwargs(self):
        kwargs = super(AccountAddView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

