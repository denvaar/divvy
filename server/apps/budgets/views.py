from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect

from .models import (
    Transaction,
    Budget,
    ExpenseBudget,
    SavingsBudget,
    DebtBudget
)

from .forms import TransactionDetailForm, dynamic_form_factory


class TransactionAddView(SuccessMessageMixin, CreateView):
    template_name = 'budgets/transaction_add.html'
    model = Transaction
    form_class = TransactionDetailForm
    success_message = "Transaction recorded."

    def post(self, *args, **kwargs):
        if 'cancel' in self.request.POST:
            return HttpResponseRedirect(reverse('accounts:dashboard'))
        return super(TransactionAddView, self).post(*args, **kwargs)
    
    def get_success_url(self):
        return reverse('budgets:transaction-add')
 
    def get_context_data(self, **kwargs):
        context = super(TransactionAddView, self).get_context_data(**kwargs)
        return context


class BudgetAddView(SuccessMessageMixin, CreateView):
    template_name = 'budgets/budget_add.html'
    model = ExpenseBudget
    success_message = "Budget created."
    
    def get_form_class(self):
        groups = (
            ('savings', SavingsBudget),
            ('expense', ExpenseBudget),
            ('debt', DebtBudget)
        )
        return dynamic_form_factory(base_model=Budget,
                                    groups=groups,
                                    label='What type of budget do you want?')

    def get_context_data(self, **kwargs):
        context = super(BudgetAddView, self).get_context_data(**kwargs)
        context['group'] = 'expense'
        return context

    def post(self, *args, **kwargs):
        if 'cancel' in self.request.POST:
            return HttpResponseRedirect(reverse('accounts:dashboard'))
        return super(BudgetAddView, self).post(*args, **kwargs)

    def get_success_url(self):
        return reverse('accounts:dashboard')

