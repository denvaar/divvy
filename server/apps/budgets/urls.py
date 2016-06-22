from django.conf.urls import url

from .views import TransactionAddView


urlpatterns = [
    url(r'^transaction/add/', TransactionAddView.as_view(),
        name='transaction-add'),
]
