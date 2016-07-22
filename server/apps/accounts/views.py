import json

from apps.budgets.models import BudgetThroughModel
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import TemplateView, View
from django.contrib.messages.views import SuccessMessageMixin

from apps.budgets.models import Transaction
from apps.budgets.models import Budget
from apps.accounts.models import Account

from .forms import LoginForm, AccountDetailForm


class LoginFormView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get_success_url(self):
        next_param = self.request.GET.get('next', None)
        if next_param:
            return next_param
        return reverse_lazy('accounts:dashboard')

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


class DashboardView(SuccessMessageMixin, TemplateView):
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
        
        data = []
        for budget in self.request.user.budgets.values_list('title','pk'):
            total = BudgetThroughModel.objects.filter(
                    budget=budget[1]).annotate(amt=Sum('amount')).aggregate(Sum('amt'))
            if total['amt__sum']:
                data.append({
                    'name': budget[0],
                    'amount': float(total['amt__sum'])
                })
        data.append({
            'name': "Uncategorized",
            'amount': abs(context['total_balance'] - sum([i['amount'] for i in data]))
        })
        context['dataset'] = json.dumps(data)
        return context

class AccountAddView(SuccessMessageMixin, CreateView):
    template_name = 'accounts/account_add.html'
    model = Account
    form_class = AccountDetailForm
    success_message = "Account created."

    def post(self, *args, **kwargs):
        if 'cancel' in self.request.POST:
            return HttpResponseRedirect(reverse('accounts:dashboard'))
        return super(AccountAddView, self).post(*args, **kwargs)

    def get_success_url(self):
        return reverse('accounts:dashboard')

    def get_form_kwargs(self):
        kwargs = super(AccountAddView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

