from allauth.account.forms import SignupForm
from django import forms
from .models import Object, CustomUser, Category, TypeObject
from django.contrib.auth.forms import UserCreationForm


class ObjectForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, label='Категория')
    type_object = forms.ModelChoiceField(queryset=TypeObject.objects.none(), required=True, label='Тип объекта')

    class Meta:
        model = Object
        fields = ['name', 'description', 'latitude', 'longitude', 'polygon', 'category', 'type_object', 'photos']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'polygon': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['type_object'].queryset = TypeObject.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeObject.DoesNotExist):
                self.fields['type_object'].queryset = TypeObject.objects.none()
        elif self.instance.pk:
            self.fields['type_object'].queryset = self.instance.category.typeobject_set.order_by('name')

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'profession', 'workplace', 'position')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
            'phone': 'Телефон',
            'profession': 'Профессия',
            'workplace': 'Место работы',
            'position': 'Должность',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    phone = forms.CharField(max_length=15, label='Телефон', required=False)
    profession = forms.CharField(max_length=50, label='Профессия', required=False)
    workplace = forms.CharField(max_length=100, label='Место работы', required=False)
    position = forms.CharField(max_length=50, label='Должность', required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.profession = self.cleaned_data['profession']
        user.workplace = self.cleaned_data['workplace']
        user.position = self.cleaned_data['position']
        user.save()
        return user


ICON_CHOICES = [
    ('ri-file-list-line', 'ri-file-list-line'),
    ('ri-drop-line', 'ri-drop-line'),
    ('ri-user-line', 'ri-user-line'),
    ('ri-star-line', 'ri-star-line'),
    ('ri-heart-line', 'ri-heart-line'),
    ('ri-map-pin-line', 'ri-map-pin-line'),
    ('ri-compass-line', 'ri-compass-line'),
    ('ri-sun-line', 'ri-sun-line'),
    ('ri-moon-line', 'ri-moon-line'),
    ('ri-cloud-line', 'ri-cloud-line'),
    ('ri-rainbow-line', 'ri-rainbow-line'),
    ('ri-snowy-line', 'ri-snowy-line'),
    ('ri-thunderstorm-line', 'ri-thunderstorm-line'),
    ('ri-wind-line', 'ri-wind-line'),
    ('ri-water-drop-line', 'ri-water-drop-line'),
    ('ri-earth-line', 'ri-earth-line'),
    ('ri-fire-line', 'ri-fire-line'),
    ('ri-seedling-line', 'ri-seedling-line'),
    ('ri-tree-line', 'ri-tree-line'),
    ('ri-palm-tree-line', 'ri-palm-tree-line'),
]

class CategoryForm(forms.ModelForm):
    icon = forms.ChoiceField(choices=ICON_CHOICES, widget=forms.Select(attrs={'onchange': 'updateIconPreview()'}))

    class Meta:
        model = Category
        fields = '__all__'

    class Media:
        js = ('admin/js/icon_preview.js',)
