from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from graphene_django.views import GraphQLView


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/accounts/login'), name='index'), 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^graphql', GraphQLView.as_view(graphiql=True)),
    url(r'^api/v1/accounts/',
        include('apps.accounts.urls',
        namespace="accounts")),
    url(r'^budgets/', include('apps.budgets.urls', namespace="budgets")),
    url(r'^rest/budgets/', include('apps.budgets.rest_urls',
        namespace="budgets-rest")),
    url(r'^api/v1/accounts/', include('apps.accounts.rest_urls',
        namespace="accounts-rest"))
]

