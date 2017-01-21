import graphene
from graphene_django import DjangoObjectType

from apps.accounts.models import (
    AppUser as AppUserModel,
    Account as AccountModel,
)


class Account(DjangoObjectType):
    class Meta:
        model = AccountModel
        description = AccountModel.__doc__
        interfaces = (graphene.relay.Node,)

    @classmethod
    def get_node(cls, id, context, info):
        print ('here')
        return AccountModel.objects.get(id=1)


class AppUser(DjangoObjectType):
    class Meta:
        model = AppUserModel
        description = AppUserModel.__doc__


class AccountQuery(graphene.AbstractType):
    accounts = graphene.List(Account, description='All bank accounts')
    account = graphene.relay.Node.Field(Account, description='A single account')
    reverse = graphene.String(word=graphene.String())

    def resolve_reverse(self, args, context, info):
        return args.get('word')[::-1]

    users = graphene.List(AppUser, description='All users on the platform')

    def resolve_accounts(self, args, context, info):
        return AccountModel.objects.all()

    def resolve_account(self, args, context, info):
        print('what')

    def resolve_users(self, args, context, info):
        return AppUserModel.objects.all()
