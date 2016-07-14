from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect

from .models import (
    Transaction,
    Budget,
)

from .forms import TransactionDetailForm, get_budget_form


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


class BudgetSelectView(TemplateView):
    template_name = 'budgets/budget_select.html'
    
    def get_context_data(self, **kwargs):
        context = super(BudgetSelectView, self).get_context_data(**kwargs)
        return context


class BudgetAddView(CreateView):
    template_name = 'budgets/budget_add.html'

    def get_form_class(self):
        budget_type = self.kwargs.get('type', None)
        return get_budget_form(budget_type, self.request.user)

    def get_success_url(self):
        return reverse('accounts:dashboard')

