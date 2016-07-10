from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.forms.widgets import TextInput


class TagInput(TextInput):
    template_name = '_widgets/_tag_input.html'

    def render(self, name, value, attrs=None):
        attrs['placeholder'] = 'Add tags'
        if 'class' in attrs:
            attrs['class'] += ' tag-input'
        else:
            attrs['class'] = 'tag-input '
        context = {
            'input': super(TagInput, self).render(name, value, attrs),
            'id': attrs['id'],
        }
        return mark_safe(render_to_string(self.template_name, context))

    def value_from_datadict(self, data, files, name):
        print(data.get(name))
        return super(TagInput, self).value_from_datadict(data, files, name)

