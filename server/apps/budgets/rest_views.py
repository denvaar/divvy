from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import AppUser

from .serializers import TransactionSerializer, BudgetThroughModelSerializer
from .models import Transaction


class TransactionUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class TransactionRecord(generics.CreateAPIView):
    serializer_class = BudgetThroughModelSerializer


class TransactionList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        user = get_object_or_404(AppUser, id=self.request.user.id)
        accounts = user.accounts.values_list('id', flat=True)
        return Transaction.objects.filter(account__id__in=accounts)
