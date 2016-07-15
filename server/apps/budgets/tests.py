from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase, override_settings, Client
from django.core.exceptions import ValidationError

from apps.accounts.models import Account
from .forms import TransactionDetailForm


class BudgetsTests(TestCase):
    fixtures = ['budgets_test.json']

    @override_settings(AUTH_USER_MODEL=settings.AUTH_USER_MODEL)
    def setUp(self):
        self.client = Client()

    @override_settings(AUTH_USER_MODEL=settings.AUTH_USER_MODEL)
    def test_add_transaction_with_fake_transaction_type(self):
        data = {
            'name': 'Test',
            'amount': 90.99,
            'transaction_type': 'nachos', # fake trans. type
            'account': Account.objects.first().pk,
            'tags': ''
        }
        form = TransactionDetailForm(data=data)
        self.assertFalse(form.is_valid())
