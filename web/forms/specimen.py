from django.forms import ModelForm

from core.models import Specimen


class SpecimenForm(ModelForm):
    class Meta:
        model = Specimen
        fields = ['box', 'organism', 'happened_at', 'form', 'gender', 'notes', 'dna']
