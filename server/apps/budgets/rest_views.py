from rest_framework import generics, status

from .serializers import TransactionSerializer
from .models import Transaction


class TransactionUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

