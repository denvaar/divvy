import json
from datetime import timedelta, datetime
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError

from ofxclient.ofxclient import OFXClient
from ofxclient.ofxparser import OFXParser

from apps.accounts.models import Account
from apps.budgets.models import Transaction


class Command(BaseCommand):
    help = 'Update transactions for accounts'

    def add_arguments(self, parser):
        parser.add_argument('n_days', nargs='+', type=int)

        parser.add_argument(
            '--account',
            action='store',
            dest='account',
            default=None,
            type=int,
            help='The account (Django model) id to fetch transactions for'
        )

    def handle(self, *args, **options):
        days_ago = datetime.now() - timedelta(days=options['n_days'][0])
        parser = OFXParser()
        if options['account']:
            accounts = Account.objects.filter(id=options['account'])
            if not accounts.exists():
                self.stdout.write(self.style.ERROR(
                    'Account id {} not found ¯\_(ツ)_/¯'.format(
                        options['account'])))

        else:
            accounts = Account.objects.all()
        for account in accounts:
            self.stdout.write('Updating {}... '.format(account.name), ending='')
            try:
                client = OFXClient(fi=account.fi,
                                   userid=account.userid,
                                   userpass=account.userpass,
                                   acctid=account.acctid)
                transaction_data = parser.as_json(
                    client.get_transactions(days_ago),
                    pretty=True
                )
                transaction_objects = []
                for data in json.loads(transaction_data):
                    transaction_objects.append(
                        Transaction(ofx_id=data['id'],
                                    name=data['name'],
                                    amount=abs(Decimal(data['transactionAmount'])),
                                    transaction_type=(
                                        data['transactionType'].lower()),
                                    created=data['datePosted'],
                                    account=account)
                    )
                Transaction.objects.bulk_create(transaction_objects)
            except (KeyError, Exception) as e:
                self.stdout.write(self.style.ERROR('failed!  ☹  ❌  '))
                self.stdout.write(self.style.ERROR(e))
            else: 
                self.stdout.write(self.style.SUCCESS('success! 🙂  ✅  '))
