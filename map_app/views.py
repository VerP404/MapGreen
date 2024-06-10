from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from allauth.account.views import SignupView, LoginView
from .models import Category, Object, TypeObject
from .forms import ObjectForm, CustomUserCreationForm
from allauth.account.forms import LoginForm, SignupForm


def index(request):
    objects = Object.objects.filter(is_published=True).values('name', 'description', 'latitude', 'longitude', 'type_object__color', 'type_object_id')
    types = TypeObject.objects.all()
    categories = Category.objects.prefetch_related('types').all()
    login_form = LoginForm()
    signup_form = SignupForm()
    form = CustomUserCreationForm()
    return render(request, 'map_app/index.html', {
        'objects': list(objects),
        'types': types,
        'categories': categories,
        'login_form': login_form,
        'signup_form': signup_form,
        'form': form
    })


def register(request):
    if request.method == 'POST' and request.is_ajax():
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CustomUserCreationForm()
    return render(request, 'map_app/registration/register.html', {'form': form})


@csrf_exempt
@login_required
def add_object(request):
    if request.method == 'POST':
        form = ObjectForm(request.POST, request.FILES)
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.user = request.user
            if 'latitude' in request.POST and request.POST['latitude']:
                new_object.latitude = request.POST['latitude']
                new_object.longitude = request.POST['longitude']
            if 'polygon' in request.POST and request.POST['polygon']:
                new_object.polygon = request.POST['polygon']
            new_object.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'invalid method'}, status=405)


@login_required
def profile_view(request):
    return render(request, 'map_app/profile.html')