from rest_framework import generics, status

from .serializers import TransactionSerializer, BudgetThroughModelSerializer
from .models import Transaction


class TransactionUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class TransactionRecord(generics.CreateAPIView):
    serializer_class = BudgetThroughModelSerializer

