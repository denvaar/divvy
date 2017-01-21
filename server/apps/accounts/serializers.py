from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import Account


class UserSerializer(serializers.ModelSerializer):
    jwt = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'jwt', 'first_name', 'last_name',)

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.set_password(self.initial_data.get('password'))
        instance.save()
        return instance

    def validate(self, data):
        if not self.instance and not self.initial_data.get('password'):
            raise serializers.ValidationError(
                {'password': ['Password is required']})
        return data

    def get_jwt(self, obj):
        payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        encode_handler = api_settings.JWT_ENCODE_HANDLER
        try:
            payload = payload_handler(obj)
            token = encode_handler(payload)
        except:
            token = ''
        return token


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
