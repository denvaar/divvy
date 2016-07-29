from rest_framework import generics

from .serializers import AccountSerializer
from .models import AppUser


class AccountCreate(generics.CreateAPIView):
    serializer_class = AccountSerializer

    #def perform_create(self, serializer):
    #    obj = serializer.save()
    #    self.request.user.accounts.add(obj)
            
        
