from django.db.models import Sum
from django.db.models import Q

from apps.budgets.models import Transaction, BudgetThroughModel


def get_savings_data(user, uncategorized_balance):
    """
    Returns a json serializable dataset that
    is used to display savings data.

    """
    data = [
        {
            'name': 'Uncategorized',
            'color': '#374952',
            'amount': uncategorized_balance
        }
    ]
    # get all of the through models that are associated with
    # savings budgets.
    for budget in user.budgets.filter(
            budget_type='savings').values_list('title', 'pk', 'icon_color'):
        # for each budget, add the transactions associated with it.
        total = BudgetThroughModel.objects.filter(
                budget=budget[1]).annotate(
                    amt=Sum('amount')).aggregate(Sum('amt'))
        # store as json text with 'name', 'color', and 'amount'.
        if total['amt__sum']:
            data.append({
                'name': budget[0],
                'color': budget[2],
                'amount': float(total['amt__sum'])
            })

    return data


def get_expenses_data(user):
    """
    Returns a json serializable dataset that
    is used to display spending data.

    """
    # find the total amount of debit transactions that have
    # not been allocated to a budget.
    uncategorized_balance = 0.0
    for transaction in Transaction.objects.filter(
            transaction_type='debit'):
        uncategorized_balance = float(transaction.amount)
        for i in transaction.budget_through_models.all():
            print(i.budget.title)
            uncategorized_balance -= float(i.amount)
    
    #for transaction in Transaction.objects.filter(transaction_type='debit'):
    #    if not transaction.budget_through_models.count():
    #        uncategorized_balance += transaction.amount

    data = [
        {
            'name': 'Uncategorized',
            'color': '#374952',
            'amount': uncategorized_balance
        }
    ]
    # get all of the through models that are associated with
    # expense & debt budgets.
    for budget in user.budgets.filter(
            Q(budget_type='expense') |
            Q(budget_type='debt')).values_list('title', 'pk', 'icon_color'):
        # for each budget, add the transactions associated with it.
        total = BudgetThroughModel.objects.filter(
                budget=budget[1]).annotate(
                    amt=Sum('amount')).aggregate(Sum('amt'))
        # store as json text with 'name', 'color', and 'amount'.
        if total['amt__sum']:
            data.append({
                'name': budget[0],
                'color': budget[2],
                'amount': float(total['amt__sum'])
            })

    print(data)
    return data
    
    
    uncategorized_amt = 0.0
    budget_names = [] 
    for transaction in Transaction.objects.filter(
            transaction_type='debit'):
        uncategorized_amt = float(transaction.amount)
        for i in transaction.budget_through_models.all():
            print(i.budget.title)
            uncategorized_amt -= float(i.amount)
        
    data = [] 
    for budget in user.budgets.filter(
            budget_type='expense').values_list('title','pk', 'icon_color'):
        total = BudgetThroughModel.objects.filter(
                budget=budget[1]).annotate(
                    amt=Sum('amount')).aggregate(Sum('amt'))
            
        if total['amt__sum']:
            data.append({
                'name': budget[0],
                'color': budget[2],
                'amount': float(total['amt__sum'])
            })
    if uncategorized_amt:
        data.append({
            'name': "Uncategorized",
            'color': "#ccc",
            'amount': float(uncategorized_amt)
        })

    return data

