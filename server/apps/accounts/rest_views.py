from rest_framework import generics
from rest_framework.serializers import ValidationError

from .serializers import AccountSerializer
from .models import AppUser


class AccountCreate(generics.CreateAPIView):
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        name = serializer.data['name']
        existing = self.request.user.accounts.filter(name=name)
        if existing.count():
            raise ValidationError("You already have an account with this name.")
        obj = serializer.save()
        self.request.user.accounts.add(obj)
            
        
