from django.conf.urls import url

from .rest_views import (
    BudgetList,
    TransactionUpdate,
    TransactionRecord,
    TransactionList,
)


urlpatterns = [
    url(r'^transaction/(?P<pk>\d+)/update/?$',
        TransactionUpdate.as_view(), name='transaction-update'),
    url(r'^transaction/record/?$',
        TransactionRecord.as_view(), name='transaction-record'),
    url(r'^transactions/?$',
        TransactionList.as_view(), name='transactions'),
    url(r'^budgets/?$', BudgetList.as_view(), name='budgets'),
]
