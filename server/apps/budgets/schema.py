import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from apps.budgets.models import (
    Transaction as TransactionModel,
    Tag as TagModel,
)


class Transaction(DjangoObjectType):
    class Meta:
        model = TransactionModel
        description = TransactionModel.__doc__


class Tag(DjangoObjectType):
    class Meta:
        model = TagModel
        description = TagModel.__doc__


class TransactionQuery(graphene.AbstractType):
    transactions = graphene.List(Transaction, description='All transactions')
    tags = graphene.List(Tag, description='All tags')

    def resolve_transactions(self, args, context, info):
        return TransactionModel.objects.all()
    
    def resolve_tags(self, args, context, info):
        return TagModel.objects.all()
