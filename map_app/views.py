import os

from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from allauth.account.views import SignupView, LoginView
from .models import Category, Object, TypeObject, Photo
from .forms import ObjectForm, CustomUserCreationForm, CustomSignupForm, PhotoFormSet
from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth import login as auth_login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
import logging


def index(request):
    objects = Object.objects.filter(is_published=True).values('name', 'description', 'latitude', 'longitude',
                                                              'type_object__color', 'type_object_id')
    types = TypeObject.objects.all()
    categories = Category.objects.prefetch_related('types').all()
    form = CustomUserCreationForm()
    return render(request, 'map_app/index.html', {
        'objects': list(objects),
        'types': types,
        'categories': categories,
        'form': form
    })


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'email': user.email})
            else:
                return redirect('index')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CustomUserCreationForm()
    return render(request, 'map_app/registration/register.html', {'form': form})


# Настройка логгера
logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user(), backend='django.contrib.auth.backends.ModelBackend')
        response_data = {'success': True, 'redirect_url': '/'}
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            logger.debug(f"Response data (valid form): {response_data}")
            return JsonResponse(response_data)
        return super().form_valid(form)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        response_data = {'success': False, 'errors': errors}
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            logger.debug(f"Response data (invalid form): {response_data}")
            return JsonResponse(response_data)
        return super().form_invalid(form)


@csrf_exempt
@login_required
def add_object(request):
    if request.method == 'POST':
        form = ObjectForm(request.POST)
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.user = request.user
            if 'latitude' in request.POST and request.POST['latitude']:
                new_object.latitude = request.POST['latitude']
                new_object.longitude = request.POST['longitude']
            new_object.save()

            main_photo_index = int(request.POST.get('main_photo_index', 0))
            photos = request.FILES.getlist('photos')

            for index, photo in enumerate(photos):
                photo_instance = Photo.objects.create(
                    object=new_object,
                    image=photo,
                    is_main=(index == main_photo_index)
                )
                # Rename the file
                project_folder = os.path.join(settings.MEDIA_ROOT, f'projects/{new_object.id}')
                os.makedirs(project_folder, exist_ok=True)
                new_filename = f'{index + 1}.{photo_instance.image.name.split(".")[-1]}'
                new_path = os.path.join(project_folder, new_filename)
                os.rename(photo_instance.image.path, new_path)
                photo_instance.image.name = f'projects/{new_object.id}/{new_filename}'
                photo_instance.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = ObjectForm()
    return render(request, 'map_app/modal/objects/add_object.html',
                  {'form': form, 'categories': Category.objects.all()})


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

    selected_category_id = request.GET.get('category')
    view_mode = request.GET.get('view_mode', 'grid')
    if selected_category_id:
        projects = Object.objects.filter(is_published=True, type_object__category__id=selected_category_id)
        category = Category.objects.get(id=selected_category_id)
    else:
        projects = Object.objects.filter(is_published=True)
        category = None

    # Fetch the main photo for each project
    for project in projects:
        project.main_photo = project.photos.filter(is_main=True).first()

    login_form = LoginForm()
    signup_form = SignupForm()
    form = CustomUserCreationForm()

    return render(request, 'map_app/project_list.html', {
        'categories': categories,
        'projects': projects,
        'category': category,
        'category_types': category_types,
        'view_mode': view_mode,
        'login_form': login_form,
        'signup_form': signup_form,
        'form': form
    })


def category_list(request):
    categories = Category.objects.prefetch_related('types').all()
    return render(request, 'map_app/includes/sidebar.html', {'categories': categories})


def get_type_objects_by_category(request, category_id):
    type_objects = TypeObject.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse({'type_objects': list(type_objects)})


def get_published_objects(request):
    category_id = request.GET.get('category')
    type_id = request.GET.get('type')

    filters = {'is_published': True}

    if category_id:
        filters['type_object__category_id'] = category_id

    if type_id:
        filters['type_object_id'] = type_id

    objects = Object.objects.filter(**filters).values('id', 'name', 'description', 'latitude', 'longitude',
                                                      'type_object__color')
    return JsonResponse({'objects': list(objects)})


def about_us(request):
    return render(request, 'map_app/about_us.html')


def object_modal(request, object_id):
    obj = get_object_or_404(Object, pk=object_id)
    photos = Photo.objects.filter(object=obj)
    user_projects_count = Object.objects.filter(user=obj.user).count()
    user_registration_date = obj.user.date_joined
    category = obj.type_object.category

    return render(request, 'map_app/modal/objects/object_modal.html', {
        'object': obj,
        'photos': photos,
        'user_projects_count': user_projects_count,
        'user_registration_date': user_registration_date,
        'category': category,
    })
