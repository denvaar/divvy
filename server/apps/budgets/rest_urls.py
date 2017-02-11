from django.conf.urls import url

from .rest_views import TransactionUpdate, TransactionRecord, TransactionList


urlpatterns = [
    
    url(r'^transaction/update/(?P<pk>\d+)/?$',
        TransactionUpdate.as_view(), name='transaction-update'),
    url(r'^transaction/record/?$',
        TransactionRecord.as_view(), name='transaction-record'),
    
    url(r'^transactions/?$',
        TransactionList.as_view(), name='transactions'),

]
