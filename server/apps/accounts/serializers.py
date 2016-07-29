from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        exclude = ['balance']

    def validate(self, data):
        user = self.context['request'].user
        existing = user.accounts.filter(name=data['name'])
        total = user.accounts.count()
        if total > 9:
            raise serializers.ValidationError(
                    "Sorry, you may only have 10 accounts at a time.")
        if existing.count():
            raise serializers.ValidationError(
                    "You've already created an account with this name.")
        return data

    def create(self, validated_data):
        obj = super(AccountSerializer, self).create(validated_data)
        self.context['request'].user.accounts.add(obj)
        return obj
