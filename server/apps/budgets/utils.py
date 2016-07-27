from django.db.models import Sum

from apps.budgets.models import Transaction, BudgetThroughModel

def get_savings_data(user):
    """
    Returns a json serializable dataset that
    is used to display savings data.

    """
    uncategorized_amt = 0.0
    budget_names = [] 
    for transaction in Transaction.objects.filter(
            transaction_type='credit'):
        uncategorized_amt = float(transaction.amount)
        for i in transaction.budget_through_models.all():
            uncategorized_amt -= float(i.amount)
        
    data = [] 
    for budget in user.budgets.filter(
            budget_type='savings').values_list('title','pk','icon_color'):
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

def get_summary_data(user):
    """
    Returns a json serializable dataset that
    is used to display spending data.

    """
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

