from django.db.models import Count, Q
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
    objects = Object.objects.filter(is_published=True).values('name', 'description', 'latitude', 'longitude',
                                                              'type_object__color', 'type_object_id')
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
    user_projects = Object.objects.filter(user=request.user)
    project_stats = (
        user_projects
        .values('type_object__name')
        .annotate(total=Count('id'), published=Count('id', filter=Q(is_published=True)))
        .order_by('type_object__name')
    )
    return render(request, 'map_app/profile.html', {
        'user_projects': user_projects,
        'project_stats': project_stats,
    })


def project_list_view(request):
    categories = Category.objects.annotate(
        total_objects=Count('types__object', filter=Q(types__object__is_published=True))
    )

    category_types = {}
    for category in categories:
        category_types[category.id] = TypeObject.objects.filter(category=category).annotate(
            published_count=Count('object', filter=Q(object__is_published=True))
        )

    selected_category = request.GET.get('category')
    if selected_category:
        projects = Object.objects.filter(is_published=True, type_object__category__id=selected_category)
        category = Category.objects.get(id=selected_category)
    else:
        projects = Object.objects.filter(is_published=True)
        category = None

    return render(request, 'map_app/project_list.html', {
        'categories': categories,
        'projects': projects,
        'category': category,
        'category_types': category_types
    })
