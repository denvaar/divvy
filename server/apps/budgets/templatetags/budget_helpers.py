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
    split_value = value.split(" ")
    quote_char = split_value[2][-1]
    classes = split_value[2][:-1]
    classes += " {}{}".format(sz, quote_char)
    split_value[2] = classes
    return " ".join(split_value)
    
