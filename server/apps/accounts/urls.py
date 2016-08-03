from django.conf.urls import url

from .views import (
    LoginFormView,
    LogoutView,
    AccountsOverview,
    DashboardView,
    AccountAddView,
)


urlpatterns = [
    url(r'^login/?$', LoginFormView.as_view(), name='login'),
    url(r'^logout/?$', LogoutView.as_view(), name='logout'),
    url(r'^dashboard/?$', DashboardView.as_view(), name='dashboard'),
    url(r'^overview/?$', AccountsOverview.as_view(), name='accounts-overview'),
    url(r'^account/add/?$', AccountAddView.as_view(), name='account-add')
]
