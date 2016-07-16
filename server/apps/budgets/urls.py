from django.conf.urls import url

from .views import (
    TransactionAddView,
    BudgetSelectView,
    BudgetAddView,
    TransactionDragDropView
)


urlpatterns = [
    url(r'^transaction/add/?$', TransactionAddView.as_view(),
        name='transaction-add'),
    url(r'^budget/select/?$', BudgetSelectView.as_view(),
        name='budget-select'),
    url(r'^budget/(?P<pk>\d+)/add/?$', TransactionAddView.as_view(),
        name='transaction-add'),
    url(r'^budget/(?P<type>savings|expense|debt)/add/?$',
        BudgetAddView.as_view(), name='budget-add'),
    url(r'^budget/assign-transactions/?$',
        TransactionDragDropView.as_view(), name='budget-drop'),
]
