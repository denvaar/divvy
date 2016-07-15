from django.conf.urls import url

from .rest_views import TransactionUpdate


urlpatterns = [
    
    url(r'^transaction/update/(?P<pk>\d+)/?$',
        TransactionUpdate.as_view(), name='transaction-update'),

]
