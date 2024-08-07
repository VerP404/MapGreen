# urls.py
from django.urls import path
from .views import add_object, index, profile_view, register, project_list_view, CustomLoginView, category_list, \
    get_type_objects_by_category, get_published_objects, about_us, object_modal, check_auth
from allauth.account.views import LoginView, LogoutView

urlpatterns = [
    path('', index, name='index'),
    path('add_object/', add_object, name='add_object'),
    path('profile/', profile_view, name='profile'),
    path('register/', register, name='register'),
    path('projects/', project_list_view, name='project_list'),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    path('categories/', category_list, name='category_list'),
    path('api/type_objects/<int:category_id>/', get_type_objects_by_category, name='get_type_objects_by_category'),
    path('api/objects/', get_published_objects, name='get_published_objects'),
    path('about_us/', about_us, name='about_us'),
    path('object/<int:object_id>/modal/', object_modal, name='object_modal'),
    path('api/check_auth/', check_auth, name='check_auth'),
]
