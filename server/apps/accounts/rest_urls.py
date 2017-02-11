import jwt
from django.conf.urls import url

from rest_framework_jwt.views import verify_jwt_token

from apps.accounts.rest_views import (
    SessionCreate,
    UserRetrieve,
    AppUserCreate,
    AccountCreate,
)


urlpatterns = [
    url(r'verify-jwt-token/?$', verify_jwt_token, name='verify-jwt'),
    url(r'sessions/?$', SessionCreate.as_view(), name='login'),
    url(r'^users/retrieve/?$', UserRetrieve.as_view(), name='user-retrieve'),
    url(r'^users/create/?$', AppUserCreate.as_view(), name='user-create'),
    url(r'^account-create/?$', AccountCreate.as_view(), name='account-create'),
]
