from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin

from .models import Transaction
from .forms import TransactionDetailForm


class TransactionAddView(SuccessMessageMixin, CreateView):
    template_name = 'budgets/transaction_add.html'
    model = Transaction
    form_class = TransactionDetailForm
    success_message = "Transaction recorded."

    def get_success_url(self):
        return reverse('budgets:transaction-add')
 
