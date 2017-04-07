from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.db.models.signals import post_delete
from django.core.exceptions import ValidationError


d = {
    ('debit', 'savings'): 'subtract',
    ('debit', 'expense'): 'add',
    ('debit', 'debt'): 'add',
    ('credit', 'savings'): 'add',
    ('credit', 'expense'): 'subtract',
    ('credit', 'debt'): 'subtract'
}


class Budget(models.Model):
    BUDGET_TYPES = (
        ('expense', 'Expense'),
        ('savings', 'Savings'),
        ('debt', 'Debt'),
    )
    
    PERIOD_CHOICES = (
        ('yearly', 'Yearly'),
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
        ('daily', 'Daily'),
    )

    ICONS = (
        ('cube', 'Cube'),
        ('car', 'Car'),
        ('bicycle', 'Bicycle'),
        ('plane', 'Airplane'),
    )

    user = models.ForeignKey('accounts.AppUser', related_name='budgets')
    title = models.CharField(max_length=254)
    budget_type = models.CharField(choices=BUDGET_TYPES, max_length=254)
    # In the context of a savings budget, goal is the amount
    # that you are trying to reach. In the context of a
    # debt budget, it's the total amount you're trying to pay down.
    # In the context of an expense budget, it's the amount that
    # you don't want to exceede 
    goal = models.DecimalField(max_digits=14, decimal_places=2)
    goal_date = models.DateTimeField(default=timezone.now,
                                     blank=True, null=True) 
    # current amount in the budget.
    amount = models.DecimalField(max_digits=14, decimal_places=2,
                                 default=0.00)
    period = models.CharField(choices=PERIOD_CHOICES, max_length=254,
                              blank=True, null=True)
    # used in debt budget - the amount you pay per frequency
    payment_amount = models.DecimalField(max_digits=14, decimal_places=2,
                                         blank=True, null=True)
    created = models.DateTimeField(default=timezone.now) 
    icon_color = models.ForeignKey('budgets.Color')
    icon = models.ForeignKey('budgets.Icon')

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=254)
    
    def __str__(self):
        return self.name


class Transaction(models.Model):
    """Data model to represent a transaction"""

    TYPES = (
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    )
    
    ofx_id = models.CharField(max_length=254)
    name = models.CharField(max_length=254)
    description = models.CharField(max_length=254, blank=True, null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    transaction_type = models.CharField(choices=TYPES, max_length=254)
    created = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, blank=True)
    account = models.ForeignKey('accounts.Account', related_name='transactions')
    budgets = models.ManyToManyField('budgets.Budget', blank=True,
                                     through='budgets.BudgetThroughModel')
    ignore = models.BooleanField(default=False)

    def __str__(self):
        return "[ {2} ] {0}  {1}".format(self.name,
            self.description or '', self.amount)

    def clean(self):
        if not self.transaction_type in [i[0] for i in self.TYPES]:
            raise ValidationError(
                {'transaction_type': 'Invalid transaction type {}'.format(
                    self.transaction_type)})

    def save(self, *args, **kwargs):
        if self.transaction_type == 'debit':
            self.account.balance = self.account.balance - self.amount
        elif self.transaction_type == 'credit':
            self.account.balance = self.account.balance + self.amount
        self.account.save()
        super(Transaction, self).save(*args, **kwargs)

    def get_unbudgeted_amount(self):
        total = sum(
            [i.amount for i in self.budget_through_models.all()]
        )
        return abs(self.amount - total)

    def is_budgeted_for(self):
        if self.get_unbudgeted_amount() > 0:
            return False
        return True


def update_account(sender, instance, **kwargs):
    instance.account.balance = instance.account.balance - instance.amount
    instance.account.save()

post_delete.connect(update_account, sender=Transaction,
                    dispatch_uid='update_account')


class BudgetThroughModel(models.Model):
    """
    To allow portions of different transactions to go to
    different budgets.
    """
    budget = models.ForeignKey('budgets.Budget',
                               related_name='budget_through_models')
    transaction = models.ForeignKey('budgets.Transaction',
                                    related_name='budget_through_models')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    created = models.DateTimeField(default=timezone.now) 
    
    def __str__(self):
        return "{} from '{}' to '{}'".format(self.amount,
                                         self.transaction.name,
                                         self.budget.title)

    def clean(self):
        if self.amount > transaction.amount:
            raise ValidationError(
                {'amount': 'This transaction does not have that much.'})
    
    def save(self, *args, **kwargs):
        if d[(self.transaction.transaction_type,
              self.budget.budget_type)] == 'add':
            self.budget.amount += self.amount
        else:
            self.budget.amount -= self.amount
        self.budget.save()
        super(BudgetThroughModel, self).save(*args, **kwargs)

def update_budget(sender, instance, **kwargs):
    if d[(instance.transaction.transaction_type,
          instance.budget.budget_type)] == 'add':
        instance.budget.amount = instance.budget.amount - instance.amount
    else:
        instance.budget.amount = instance.budget.amount + instance.amount
    instance.budget.save()

post_delete.connect(update_budget, sender=BudgetThroughModel,
                    dispatch_uid='update_budget')
    

class Color(models.Model):
    name = models.CharField(max_length=254)
    value = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Icon(models.Model):
    name = models.CharField(max_length=254)
    value = models.CharField(max_length=254)

    def __str__(self):
        return self.name
        
    def as_icon(self):
        return mark_safe('<i class="fa fa-{}"></i>'.format(self.value))

