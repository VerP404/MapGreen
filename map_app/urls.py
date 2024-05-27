from django.urls import path
from .views import CustomSignupView, CustomLoginView, add_object, index, profile_view

urlpatterns = [
    path('', index, name='index'),
    path('add_object/', add_object, name='add_object'),
    path('signup/', CustomSignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', profile_view, name='profile'),
]
