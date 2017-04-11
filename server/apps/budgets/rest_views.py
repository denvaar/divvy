from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import AppUser

from .serializers import (
    TransactionSerializer, 
    BudgetSerializer,
    BudgetThroughModelSerializer
)
from .models import Transaction, Budget


def users_own_budgets(user_id):
    """Helper function to list all of given user's budgets"""

    user = get_object_or_404(AppUser, id=user_id)
    return Budget.objects.filter(user=user)

def users_own_transactions(user_id):
    """Helper function to list all of given user's transactions"""

    user = get_object_or_404(AppUser, id=user_id)
    accounts = user.accounts.values_list('id', flat=True)
    return Transaction.objects.filter(account__id__in=accounts)


class BudgetList(generics.ListAPIView):
    serializer_class = BudgetSerializer
    
    def get_queryset(self):
        return users_own_budgets(self.request.user.id)


class TransactionUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get_queryset(self):
        return users_own_transactions(self.request.user.id)


class TransactionRecord(generics.CreateAPIView):
    serializer_class = BudgetThroughModelSerializer

    def perform_create(self, serializer):
        obj = serializer.save()
        transaction_obj = obj.transaction
        if transaction_obj.amount == obj.amount:
            transaction_obj.categorized = True
            transaction_obj.save()


class TransactionList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return users_own_transactions(self.request.user.id)
