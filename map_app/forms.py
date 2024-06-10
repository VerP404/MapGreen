from django import forms
from .models import Object
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class ObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ['name', 'description', 'latitude', 'longitude', 'polygon', 'type_object', 'photos']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'polygon': forms.HiddenInput(),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'profession', 'workplace', 'position')
