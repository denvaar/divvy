from django import template

register = template.Library()

@register.filter()
def as_percentage(budget):
    p = (float(budget.amount) / float(budget.goal)) * 100.0
    if p > 100:
        return 100
    return p

@register.filter()
def change_size(value, sz):
    l = value.split("\">")
    return l[0] + " {}\">".format(sz) + l[1]
    
