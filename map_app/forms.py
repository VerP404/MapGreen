from django import forms
from .models import Object


class ObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ['name', 'description', 'latitude', 'longitude', 'polygon', 'type_object', 'photos']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'polygon': forms.HiddenInput(),
        }