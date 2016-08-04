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
class ExtraAttributeChoiceIterator(models.ModelChoiceIterator):
    def choice(self, obj):
        return (self.field.prepare_value(obj),
                self.field.label_from_instance(obj), obj.value or "#fff")


class DataAttribChoiceField(models.ModelChoiceField):
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return ExtraAttributeChoiceIterator(self)
    choices = property(_get_choices, ChoiceField._set_choices)

