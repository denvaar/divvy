from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import AppUser

from .serializers import TransactionSerializer, BudgetThroughModelSerializer
from .models import Transaction


def users_own_transactions(user_id):
    """Helper function to list all of given user's transactions"""

    user = get_object_or_404(AppUser, id=user_id)
    accounts = user.accounts.values_list('id', flat=True)
    return Transaction.objects.filter(account__id__in=accounts)


class TransactionUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get_queryset(self):
        return users_own_transactions(self.request.user.id)


class TransactionRecord(generics.CreateAPIView):
    serializer_class = BudgetThroughModelSerializer


class TransactionList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return users_own_transactions(self.request.user.id)
