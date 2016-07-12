from django.db import models
from django.utils import timezone
from django.db.models.signals import post_delete


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

    def __str__(self):
        return self.title


class Transaction(models.Model):
    
    TYPES = (
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    )

    name = models.CharField(max_length=254)
    description = models.CharField(max_length=254, blank=True, null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    transaction_type = models.CharField(choices=TYPES, max_length=254)
    created = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField('Tag', blank=True)
    account = models.ForeignKey('accounts.Account', related_name='transactions')
    budget = models.ForeignKey('budgets.Budget', blank=True, null=True,
                               related_name='transactions')

    def __str__(self):
        return "[ {2} ] {0}  {1}".format(self.name,
            self.description, self.amount)

    def save(self, *args, **kwargs):
        self.account.balance = self.account.balance + self.amount
        self.account.save()
        super(Transaction, self).save(*args, **kwargs)


def update_account(sender, instance, **kwargs):
    instance.account.balance = instance.account.balance - instance.amount
    instance.account.save()

post_delete.connect(update_account, sender=Transaction,
                    dispatch_uid='update_account')


class Tag(models.Model):
    name = models.CharField(max_length=254)
    
    def __str__(self):
        return self.name

