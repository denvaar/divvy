from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('apps.accounts.urls', namespace="accounts")),
    url(r'^budgets/', include('apps.budgets.urls', namespace="budgets")),
    url(r'^rest/budgets/', include('apps.budgets.rest_urls',
        namespace="budgets-rest"))
]

