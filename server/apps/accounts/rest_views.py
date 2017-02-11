from django.contrib.auth import authenticate
from django.http import Http404

from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import AppUser, Account
from apps.accounts.serializers import (
    AccountSerializer,
    UserSerializer,
    AppUserSerializer,
)


class SessionCreate(APIView):
    """Create a new session for an authenticated user."""

    def post(self, request, format=None):
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response({
                'errors': ['Missing username or password']
            }, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username.lower(), password=password)
        if user is not None:
            if user.is_active:
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({
                'errors': ['User is not active']
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({'errors': ['Incorrect password']},
                        status=status.HTTP_400_BAD_REQUEST)


class UserRetrieve(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AppUserSerializer

    def get_object(self):
        if self.request.user.is_active:
            return self.request.user
        raise Http404('Invalid user')


class AppUserCreate(generics.CreateAPIView):
    model = AppUser
    serializer_class = AppUserSerializer


class AccountCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    model = Account
    serializer_class = AccountSerializer
