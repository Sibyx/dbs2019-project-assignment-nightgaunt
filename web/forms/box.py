from django.forms import ModelForm

from core.models import Box


class BoxForm(ModelForm):
    class Meta:
        model = Box
        fields = ['title', 'description']
