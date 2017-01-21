import graphene

from apps.budgets.schema import TransactionQuery
from apps.accounts.schema import AccountQuery


class Query(TransactionQuery, AccountQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
