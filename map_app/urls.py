from django.urls import path
from .views import  add_object, index, profile_view, register

urlpatterns = [
    path('', index, name='index'),
    path('add_object/', add_object, name='add_object'),
    path('profile/', profile_view, name='profile'),
    path('register/', register, name='register'),
]
