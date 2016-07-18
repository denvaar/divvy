from django import template
from django.utils import timezone
from datetime import timedelta, datetime

register = template.Library()

@register.filter()
def as_currency(value):
    return '${:2,.2f}'.format(value)

@register.filter()
def abso(value):
    return abs(float(value))

@register.filter()
def time_diff(value):
    return (value - timezone.now()).days

# TODO: move to budgets templatetags
@register.filter()
def change_size(value, sz):
    split_value = value.split(" ")
    quote_char = split_value[2][-1]
    classes = split_value[2][:-1]
    classes += " {}{}".format(sz, quote_char)
    split_value[2] = classes
    return " ".join(split_value)
    
