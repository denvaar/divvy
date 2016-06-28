from datetime import date

from django import forms
from django.forms.forms import BoundField, BaseForm
from django.forms.utils import ErrorList
from django.template import Library, TemplateSyntaxError
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = Library()

VERTICAL_TEMPLATE = 'forms/forms.html'
TEMPLATE_ERRORS = 'forms/non_field_errors.html'

def render_non_field_errors(errors):
    if not errors:
        return ''
    context = {'errors': errors}
    return render_to_string(TEMPLATE_ERRORS, context=context)


def render_field(bound_field, show_label, template):
    disabled = "false"
    widget = bound_field.field.widget
    parse_date = False
    if isinstance(widget, forms.RadioSelect):
        input_type = 'radio'
    elif isinstance(widget, (forms.DateInput, forms.DateTimeInput)):
        input_type = 'date'
        if isinstance(bound_field.value(), date):
            parse_date = True
        if bound_field.field.widget.attrs.get('disabled', None):
            disabled = "true"
    elif isinstance(widget, forms.Select):
        input_type = 'select'
    elif isinstance(widget, forms.Textarea):
        input_type = 'textarea'
    elif isinstance(widget, forms.CheckboxInput):
        input_type = 'checkbox'
    elif issubclass(type(widget), forms.MultiWidget):
        input_type = 'multi_widget'
    else:
        input_type = 'input'
    context = {'bound_field': bound_field, 'input_type': input_type,
               'show_label': show_label, 'disabled': disabled,
               'parse_date': parse_date}
    return render_to_string(template, context=context)

def as_form(obj, show_label, template):
    if isinstance(obj, BoundField):
        return render_field(obj, show_label, template)
    elif isinstance(obj, ErrorList):
        return render_non_field_errors(obj)
    elif isinstance(obj, BaseForm):
        non_field_errors = render_non_field_errors(obj.non_field_errors())
        fields = (render_field(field, show_label, template) for field in obj)
        form = ''.join(fields)
        return mark_safe(non_field_errors + form)
    else:
        raise TemplateSyntaxError('Filter accepts form, field and non fields '
                                  'errors.')


@register.filter
def as_vertical_form(obj, show_label=True):
    return as_form(obj=obj, show_label=show_label,
                   template=VERTICAL_TEMPLATE)

@register.simple_tag
def render_widget(obj, **attrs):
    return obj.as_widget(attrs=attrs)
