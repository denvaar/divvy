from django.conf.urls import url

from .views import (
    TransactionAddView,
    TransactionListView,
    BudgetSelectView,
    BudgetAddView,
    TransactionDragDropView,

    BudgetOverview,
)


urlpatterns = [
    
    url(r'^overview/?$', BudgetOverview.as_view(),
        name='budget-overview'),
    url(r'^transaction/?$', TransactionListView.as_view(),
        name='transaction-overview'),
    
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
