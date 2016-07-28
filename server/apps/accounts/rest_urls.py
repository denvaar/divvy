from django.conf.urls import url

from .rest_views import AccountCreate

urlpatterns = [
    url(r'^account/create/?$',
        AccountCreate.as_view(), name='account-create'),
]

