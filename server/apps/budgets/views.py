from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect

from .models import (
    Transaction,
    Budget,
)

from .forms import TransactionDetailForm, get_budget_form


class BudgetOverview(TemplateView):
    template_name = 'budgets/budgets.html'
    
    def get_context_data(self, **kwargs):
        context = super(BudgetOverview, self).get_context_data(**kwargs)
        context['budgets'] = Budget.objects.filter(user=self.request.user)
        return context

    def get_current_page(self):
        return 'budgets'
    


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


class TransactionListView(ListView):
    model = Transaction
    template_name = 'budgets/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(
                account__app_users=self.request.user).order_by('-created')


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


class TransactionDragDropView(TemplateView):
    template_name = 'budgets/drag_and_drop.html'

    def get_context_data(self, **kwargs):
        context = super(TransactionDragDropView, self).get_context_data(**kwargs)
        context['budgets'] = Budget.objects.filter(user=self.request.user)
        t = []
        transactions = Transaction.objects.filter(
                account__app_users=self.request.user).order_by('-created')
        for transaction in transactions:
            if not transaction.is_budgeted_for():
                t.append(transaction)
        context['transactions'] = t
        return context

