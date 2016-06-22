from django.conf.urls import url

from .views import (
    LoginFormView,
    LogoutView,
    DashboardView,
)


urlpatterns = [
    url(r'^login/?$', LoginFormView.as_view(), name='login'),
    url(r'^logout/?$', LogoutView.as_view(), name='logout'),
    url(r'^dashboard/?$', DashboardView.as_view(), name='dashboard')
]
