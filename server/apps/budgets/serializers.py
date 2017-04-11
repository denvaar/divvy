from rest_framework import serializers

from .models import Transaction, Budget, BudgetThroughModel


class BudgetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Budget
        fields = ('id', 'user', 'title', 'budget_type',
                  'goal', 'amount',)


class TransactionSerializer(serializers.ModelSerializer):
    transaction_type = serializers.CharField(
        source='get_transaction_type_display')
    
    class Meta:
        model = Transaction
        exclude = []


class BudgetThroughModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BudgetThroughModel
        fields = ('amount', 'budget', 'transaction')

    def validate(self, attrs):
        if attrs['amount'] > attrs['transaction'].amount:
            raise serializers.ValidationError(
                {'amount': 'This transaction does not have that much.'})
        return attrs
 
