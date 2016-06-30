from django.conf.urls import url

from .views import TransactionAddView, BudgetAddView


urlpatterns = [
    url(r'^transaction/add/', TransactionAddView.as_view(),
        name='transaction-add'),
    url(r'^budget/add/', BudgetAddView.as_view(),
        name='budget-add'),
]
