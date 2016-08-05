from django.forms import CharField

class TagField(CharField):
    
    def __init__(self, model, max_length=None, min_length=None, strip=True,
                 *args, **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        self.strip = strip
        self.model = model
        super(TagField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        tags = []
        for item in value.strip('|').split('|'):
            tag, was_created = self.model.objects.get_or_create(name=item)
            tags.append(tag)
        return tags

from django.forms import models
from django.forms.fields import ChoiceField
from apps.core.widgets import DataModelSelect

class ExtraAttributeChoiceIterator(models.ModelChoiceIterator):
    
    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label) + self.field.get_empty_data_labels()
        queryset = self.queryset.all()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        for obj in queryset:
            yield self.choice(obj)

    def choice(self, obj):
        return (self.field.prepare_value(obj),
                self.field.label_from_instance(obj),) +\
                self.field.get_data_attributes(obj)

class DataModelChoiceField(models.ModelChoiceField):
    
    iterator = ExtraAttributeChoiceIterator
    
    def __init__(self, queryset, data_attributes,
                 empty_label="---------", required=True, label=None,
                 initial=None, help_text='', to_field_name=None,
                 limit_choices_to=None, *args, **kwargs):

        widget = DataModelSelect

        super(DataModelChoiceField, self).__init__(
                queryset, empty_label="---------",
                required=True, widget=widget, label=None, initial=None,
                help_text='', to_field_name=None, limit_choices_to=None,
                *args, **kwargs)
        
        self.data_attributes = data_attributes
     
    def get_empty_data_labels(self):
        diff = 1 if len(self.data_attributes) > 1 else 0
        return ({},) * (len(self.data_attributes) - diff)
    
    def get_data_attributes(self, obj):
        d = {}
        for k,v in self.data_attributes.items():
            d[k] = getattr(obj, v)
        return (d,)

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return self.iterator(self)

    choices = property(_get_choices, ChoiceField._set_choices)

