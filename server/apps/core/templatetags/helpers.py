from django import template

register = template.Library()

@register.filter()
def as_currency(value):
    return '${:20,.2f}'.format(value)

@register.filter()
def abso(value):
    return abs(float(value))

